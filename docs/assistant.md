# "Ask AquaNexus": farmer assistant chat

A chat card on the dashboard. Farmers ask in English or Kannada about their readings, safe levels, tonight's
weather or fish diseases. It is always labelled **"AI assistant: can make mistakes" / "AI ಸಹಾಯಕ: ತಪ್ಪುಗಳಾಗಬಹುದು"**.

| | |
|---|---|
| Page | `frontend/assistant.js` (chat card, suggested questions, speaker button per reply) |
| Server | `backend/assistant.py` (content, ready answers, safety, rate limit), `backend/ai_provider.py` (the AI call), `backend/safety.py` (banned words, shared with the disease guide) |
| API | `POST /api/assistant/ask`, `POST /api/assistant/suggestions` |
| Tests | `tests/test_assistant.py`. The AI is always faked; `tests/conftest.py` removes any real key, so no test can call a real AI |

## Safety rules

1. **Only our own content.** The AI gets a block of text built by the server from:
   - the current readings, graded again on the server: simulated pond, test kit, live sensor, each with its label;
   - the Safe / Warning / Danger levels from `config/thresholds.toml`;
   - the action checklist (`backend/actions.py`, documented in `docs/actions.md`);
   - the Fish disease guide (`backend/diseases.py`);
   - tonight's crash risk (`backend/weather.py`).

   It is told to use nothing else. If the answer isn't there it must reply `UNKNOWN`, which the server turns into
   **"I don't know, please ask your fisheries officer."**
2. **No chemicals, medicines, doses or diagnosis.**
   - Questions asking for a medicine, chemical or dose are refused *before* reaching the AI.
   - Every AI reply is checked against `backend/safety.py`: the same banned-word list as the disease guide (English
     and Kannada chemical and medicine names), amounts like "20 kg per acre", and diagnosis sentences like "your
     fish have EUS".
   - A reply that fails the check is **replaced** with a safe answer that points to the Fish disease guide.
3. **Disease or treatment → "Please confirm with your fisheries officer / KVK."** This is added by the server
   whenever the question or the reply is about disease or treatment.
4. **Simulated data stays labelled.** Simulated readings come with "These are simulated readings from the demo pond,
   not a real pond" in the content. Every reply shows tags for the data it used: **Simulated data**, Test kit or
   Live sensor.
5. **Labelled as AI.** Each reply says *AI answer*, *Ready answer from the app* or *Safety answer from the app*.

**Limits, honestly.** Checks on words and patterns catch the common cases, not every possible wording. The
AI can still be wrong *inside* our content, for example by mixing up two numbers. That is why the card says
"can make mistakes". Kannada replies are written by the AI and are **not** in the native-speaker review
(`docs/kannada-review.md`); only the app's fixed texts are.

## When the AI can't answer: ready answers

The page always shows **suggested questions** whose answers the server builds from the same content, without any AI:

| Question | Built from |
|---|---|
| Is my pond safe right now? | current readings and their risk |
| What should I do now? | the action checklist for the worst reading |
| Is there a risk of an oxygen crash tonight? | tonight's weather risk |
| What are the safe levels for oxygen, pH, temperature and ammonia? | `config/thresholds.toml` |
| Which diseases are more likely with my readings? | the disease guide's links to readings |
| My fish look sick. What should I do? | the guide's "what to do" steps |
| How can I prevent fish diseases? | the guide's prevention steps |

If there is no key, no internet, a provider error or the rate limit is reached, a typed question gets a message
saying so, and the farmer can tap a suggested question. Tapping one never calls the AI, so the demo always works.

## Rate limit

Kept in memory (cleared when the free server sleeps). Only real AI calls count:

- each visitor: **4 questions a minute, 20 an hour**;
- everyone together: **300 a day** (change with the `ASSISTANT_DAILY_LIMIT` environment variable).

A visitor is recognised by the first address in `X-Forwarded-For` (set by Render). That can be faked, which is why
the daily total exists: even someone faking many visitors cannot use more than 300 calls a day.
Questions are at most 500 characters, and at most 4 earlier turns are sent.

## Provider: research and recommendation (checked 10 October 2026)

| Provider | Free tier | Notes |
|---|---|---|
| **Google Gemini API** (AI Studio) | Yes, no card. Limits are per project and per model, shown in AI Studio; Google no longer prints the numbers in its docs [1]. Third-party guides give very different numbers for Flash (about 20 to 1,500 requests a day), and Flash-Lite models get more [4]. | OpenAI-compatible endpoint [2]. Strong at Indian languages. **Free-tier prompts may be read by human reviewers and used to improve Google's products; don't send personal information. Users must be 18 or older** [3]. |
| **Groq** | Yes. Its docs list e.g. `openai/gpt-oss-20b` at 30 requests a minute, 1,000 a day, 8,000 tokens a minute [5]. | OpenAI-compatible [6]. Very fast. 8,000 tokens a minute is tight for our content block (~3,000–5,000 tokens a question in Kannada). |
| **OpenRouter** | `:free` models, about 50 requests a day without credit; the list of free models changes often [4]. | OpenAI-compatible. Set `ASSISTANT_MODEL` to a current free model. |
| Cerebras, Mistral | Free tiers recently changed or ended; not counted on [4]. | |

**Recommendation: Gemini with `gemini-3.5-flash-lite`.** It's free with no card, handles Kannada well, and our
grounded answers don't need a big model. Check its daily limit for your project at aistudio.google.com/rate-limit
before the demo. If it is too low, switch to Groq by changing two environment variables (no code change).

Sources:
1. Google, *Gemini API rate limits*, last updated 2026-10-09. https://ai.google.dev/gemini-api/docs/rate-limits
2. Google, *OpenAI compatibility*, last updated 2026-09-02. https://ai.google.dev/gemini-api/docs/openai
3. Google, *Gemini API Additional Terms of Service*, last updated 2026-04-28. https://ai.google.dev/gemini-api/terms
4. OpenRouter, *Free LLM API in 2026: 13 options ranked and compared* (third-party comparison). https://openrouter.ai/blog/tutorials/free-llm-apis-compared/
5. Groq, *Rate limits*. https://console.groq.com/docs/rate-limits
6. Groq, *OpenAI compatibility*. https://console.groq.com/docs/openai

## Settings (environment variables, never in code or git)

| Variable | Value |
|---|---|
| `ASSISTANT_PROVIDER` | `gemini` (default), `groq`, `openrouter` or `custom` |
| `ASSISTANT_API_KEY` | the secret key from that provider. **Not set = ready answers only** |
| `ASSISTANT_MODEL` | optional for gemini (`gemini-3.5-flash-lite`) and groq (`openai/gpt-oss-20b`); required for openrouter and custom |
| `ASSISTANT_BASE_URL` | only for `custom`: any OpenAI-compatible address ending in `/v1` |
| `ASSISTANT_DAILY_LIMIT` | optional, default `300` |

To add another provider, add a line to `PRESETS` in `backend/ai_provider.py`, or use `custom`.

Try it on your laptop (PowerShell):

```powershell
$env:ASSISTANT_PROVIDER = "gemini"
$env:ASSISTANT_API_KEY = "<your key>"
uvicorn backend.main:app --reload
```

Never paste the key into a file in this project. Close the PowerShell window when you're done.
