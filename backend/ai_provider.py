"""
Talks to the AI service for the "Ask AquaNexus" assistant. Backend only:
the page never sees the provider or the key.

Everything comes from environment variables (on Render: the service's
Environment tab; never in the code, the page or git):

    ASSISTANT_PROVIDER   gemini (recommended), groq, openrouter, or custom
    ASSISTANT_API_KEY    the secret key from that provider
    ASSISTANT_MODEL      optional; each provider has a default below
    ASSISTANT_BASE_URL   only for "custom": any OpenAI-compatible API address

All these providers accept the same "OpenAI-compatible" chat request, so one
small class talks to all of them, and switching provider is just changing
the variables. No key set = no provider = the assistant uses its ready answers.

Uses only Python's standard library (urllib), so no extra packages on Render.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

PRESETS = {
    # provider: (OpenAI-compatible base URL, default model). Check the model names on each
    # provider's site; they change. Gemini's free limits per model: aistudio.google.com/rate-limit
    "gemini": ("https://generativelanguage.googleapis.com/v1beta/openai", "gemini-3.5-flash-lite"),
    "groq": ("https://api.groq.com/openai/v1", "openai/gpt-oss-20b"),
    "openrouter": ("https://openrouter.ai/api/v1", ""),   # free models change often: set ASSISTANT_MODEL
}
TIMEOUT_SECONDS = 20
MAX_REPLY_TOKENS = 400


class ProviderError(Exception):
    """The AI service could not answer (no internet, wrong key, quota used up, bad reply)."""


@dataclass
class OpenAICompatible:
    name: str
    base_url: str
    api_key: str
    model: str

    def complete(self, system: str, messages: list[dict], opener=urlopen) -> str:
        """One chat reply. `messages` = [{"role": "user" | "assistant", "content": ...}]."""
        body = {"model": self.model, "temperature": 0.2, "max_tokens": MAX_REPLY_TOKENS,
                "messages": [{"role": "system", "content": system}, *messages]}
        request = Request(f"{self.base_url.rstrip('/')}/chat/completions", method="POST",
                          data=json.dumps(body).encode("utf-8"),
                          headers={"Content-Type": "application/json",
                                   "Authorization": f"Bearer {self.api_key}"})
        try:
            with opener(request, timeout=TIMEOUT_SECONDS) as response:
                reply = json.loads(response.read())
            return reply["choices"][0]["message"]["content"] or ""
        except HTTPError as error:          # 401 wrong key, 429 quota, 5xx provider trouble
            raise ProviderError(f"{self.name} answered HTTP {error.code}") from None
        except (URLError, TimeoutError, OSError) as error:
            raise ProviderError(f"{self.name} unreachable: {error}") from None
        except (KeyError, IndexError, TypeError, ValueError):
            raise ProviderError(f"{self.name} sent a reply we could not read") from None


def provider_from_env(env=os.environ) -> OpenAICompatible | None:
    """The configured provider, or None if no key (or no usable provider) is set."""
    key = env.get("ASSISTANT_API_KEY", "").strip()
    name = env.get("ASSISTANT_PROVIDER", "gemini").strip().lower() or "gemini"
    if not key:
        return None
    if name == "custom":
        base_url, model = env.get("ASSISTANT_BASE_URL", "").strip(), env.get("ASSISTANT_MODEL", "").strip()
        if not base_url or not model:
            return None
    elif name in PRESETS:
        base_url, model = PRESETS[name]
        model = env.get("ASSISTANT_MODEL", "").strip() or model
        if not model:
            return None
    else:
        return None
    return OpenAICompatible(name, base_url, key, model)
