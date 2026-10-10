"""
Web security for every request (see docs/security.md).

What this file does:
    SECURITY_HEADERS   headers added to every response: Content-Security-Policy
                       (the page may only load its own files, plus the Open-Meteo
                       weather API), no MIME sniffing, no referrer, no framing.
    LIMITS             how many requests one visitor (and everyone together) may
                       send per minute to /api/assistant/* and /api/sensor/*.
    MAX_BODY_BYTES     the largest request body we accept (our biggest is the
                       chat question with its short history, about 15 KB).
    SecurityMiddleware wraps the whole app and applies all of the above.

Rate limits are in memory, like the assistant's (they reset when the server restarts).
"""

from __future__ import annotations

import json
import threading
import time
from collections import deque

# The page's own files, plus the browser's direct weather download (frontend/weather.js).
# 'unsafe-inline' for styles only: GSAP and our SVG markup set style attributes. Scripts
# never run inline, so injected <script> or onerror="..." code is blocked by the browser.
CONTENT_SECURITY_POLICY = "; ".join([
    "default-src 'self'",
    "script-src 'self'",
    "style-src 'self' 'unsafe-inline'",
    "img-src 'self' data:",
    "font-src 'self'",
    "connect-src 'self' https://api.open-meteo.com",
    "object-src 'none'",
    "base-uri 'none'",
    "form-action 'self'",
    "frame-ancestors 'none'",
])

SECURITY_HEADERS = {
    "content-security-policy": CONTENT_SECURITY_POLICY,
    "x-content-type-options": "nosniff",
    "referrer-policy": "no-referrer",
    "x-frame-options": "DENY",
    "permissions-policy": "camera=(), microphone=(), geolocation=()",
    "cross-origin-opener-policy": "same-origin",
}
# FastAPI's /docs and /redoc pages load their scripts from a CDN, so they skip the page's CSP.
CSP_EXEMPT = ("/docs", "/redoc")

MAX_BODY_BYTES = 32 * 1024

# (method, path start): (per visitor per minute, everyone together per minute).
# A real sensor sends one reading every 5 s (12 a minute). The dashboard opens one
# sensor stream per pond and reconnects on its own if the connection drops.
LIMITS = {
    ("POST", "/api/sensor/"): (30, 600),
    ("GET", "/api/sensor/"): (60, 1200),
    ("POST", "/api/assistant/"): (30, 600),
}

TOO_MANY = {"en": "Too many requests. Please wait a minute and try again.",
            "kn": "ತುಂಬಾ ವಿನಂತಿಗಳು. ದಯವಿಟ್ಟು ಒಂದು ನಿಮಿಷ ಕಾಯಿರಿ ಮತ್ತು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ."}
TOO_BIG = {"en": "The request is too large.", "kn": "ವಿನಂತಿ ತುಂಬಾ ದೊಡ್ಡದಾಗಿದೆ."}


def client_address(forwarded_for: str, client_host: str | None) -> str:
    """Who is asking. Render puts the visitor's address first in X-Forwarded-For.
    It can be faked, which is why every limit also has a total for everyone."""
    return forwarded_for.split(",")[0].strip() or client_host or "unknown"


class RequestLimiter:
    """Requests per minute, for each visitor and for everyone together, per rule in LIMITS."""

    def __init__(self, limits: dict = LIMITS, clock=time.monotonic) -> None:
        self.limits, self.clock = limits, clock
        self._lock = threading.Lock()
        self._visitors: dict[tuple, deque] = {}
        self._everyone: dict[tuple, deque] = {rule: deque() for rule in limits}

    def rule_for(self, method: str, path: str) -> tuple | None:
        return next(((m, p) for m, p in self.limits if m == method and path.startswith(p)), None)

    def allow(self, rule: tuple, visitor: str) -> bool:
        per_visitor, total = self.limits[rule]
        now = self.clock()
        with self._lock:
            mine = self._visitors.setdefault((rule, visitor), deque())
            everyone = self._everyone[rule]
            for times in (mine, everyone):
                while times and now - times[0] >= 60:
                    times.popleft()
            if len(mine) >= per_visitor or len(everyone) >= total:
                return False
            mine.append(now)
            everyone.append(now)
            if len(self._visitors) > 10000:          # forget idle visitors so memory stays small
                self._visitors = {k: v for k, v in self._visitors.items() if v}
            return True

    def clear(self) -> None:
        """Forget all counts (what a server restart does; used by the tests)."""
        with self._lock:
            self._visitors.clear()
            for times in self._everyone.values():
                times.clear()


class SecurityMiddleware:
    """Rate limits, body size limit and security headers, around the whole app (plain ASGI,
    so it also works for the Server-Sent Events streams)."""

    def __init__(self, app, limiter: RequestLimiter | None = None) -> None:
        self.app = app
        self.limiter = limiter or RequestLimiter()

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        path, method = scope["path"], scope["method"]
        headers = {k.decode("latin-1"): v.decode("latin-1") for k, v in scope["headers"]}
        extra = dict(SECURITY_HEADERS)
        if path.startswith(CSP_EXEMPT):
            extra.pop("content-security-policy")

        async def send_with_headers(message):
            if message["type"] == "http.response.start":
                present = {k.lower() for k, _ in message.get("headers", [])}
                message["headers"] = list(message.get("headers", [])) + [
                    (k.encode(), v.encode()) for k, v in extra.items() if k.encode() not in present]
            await send(message)

        rule = self.limiter.rule_for(method, path)
        visitor = client_address(headers.get("x-forwarded-for", ""), scope["client"][0] if scope.get("client") else None)
        if rule and not self.limiter.allow(rule, visitor):
            return await _reply(send_with_headers, 429, {"error": "too_many_requests", "message": TOO_MANY},
                                [(b"retry-after", b"60")])

        if method in ("POST", "PUT", "PATCH"):
            # Read the whole (small) body first, so an oversized one is refused before any parsing.
            declared = headers.get("content-length", "")
            if declared.isdigit() and int(declared) > MAX_BODY_BYTES:
                return await _reply(send_with_headers, 413, {"error": "too_large", "message": TOO_BIG})
            body, more = b"", True
            while more:
                message = await receive()
                if message["type"] == "http.disconnect":
                    return
                body += message.get("body", b"")
                more = message.get("more_body", False)
                if len(body) > MAX_BODY_BYTES:
                    return await _reply(send_with_headers, 413, {"error": "too_large", "message": TOO_BIG})
            sent = False

            async def replay():
                nonlocal sent
                if not sent:
                    sent = True
                    return {"type": "http.request", "body": body, "more_body": False}
                return await receive()
            return await self.app(scope, replay, send_with_headers)

        return await self.app(scope, receive, send_with_headers)


async def _reply(send, status: int, content: dict, headers: list | None = None) -> None:
    body = json.dumps(content, ensure_ascii=False).encode("utf-8")
    await send({"type": "http.response.start", "status": status,
                "headers": [(b"content-type", b"application/json; charset=utf-8"),
                            (b"content-length", str(len(body)).encode()), *(headers or [])]})
    await send({"type": "http.response.body", "body": body})
