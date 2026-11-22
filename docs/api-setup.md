# Model API setup

Model-based notebooks can use **practice** responses or a **live** model. Practice mode returns the explicit `example` text without a model request. Live mode sends the prompt to the selected service. The MCP lab and deterministic A2A adapter need no model key.

The initial configuration uses **FreeInference**, but the teaching adapter is provider-neutral.

## Initial Colab setup

1. Open the notebook, run its single setup cell, then run the practice example.
2. Open Colab’s **Secrets** panel, create `FREEINFERENCE_API_KEY`, and grant the notebook access. Never paste the key into a code cell.
3. Set `MODE = "live"` in the setup cell.
4. Run the small example and read its answer.

```python
MODE = "live"
PROVIDER = "freeinference"  # or "gemini" or "deepseek"
ask = make_ask(mode=MODE, provider=PROVIDER)
```

The defaults are FreeInference (`https://freeinference.org/v1`), model `qwen3.6-35b`, and secret name `FREEINFERENCE_API_KEY`; see *Providers and the council* below for Gemini and DeepSeek. If no Colab secret is available, the helper uses a hidden input prompt. Check current access and quotas in the [FreeInference documentation](https://doc.freeinference.org/).

## Use another compatible service

Pass the chosen service settings to the same helper:

```python
ask = make_ask(mode="live", base_url="https://gateway.example/v1",
               model="your-model", secret_name="YOUR_SECRET_NAME")
```

Use a base URL including its API prefix, such as `/v1`, without `/chat/completions`. The example URL above is a placeholder.

The helper uses the [Chat Completions request format](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create). If a provider requires `max_completion_tokens`, add `token_field="max_completion_tokens"` to `make_ask(...)`.

Services with deployment-specific URLs, native Gemini/Messages APIs, SSO-only authentication, or custom headers may require a transport change. Practice examples remain available while that change is made. Use the endpoint and approved models supplied by your institution when required.

## Providers and the council

`make_ask` knows three providers. Each one fills in its base URL, default model, and Colab Secret name:

| Provider | Default model (family) | Colab Secret | Notes |
| --- | --- | --- | --- |
| `freeinference` | `qwen3.6-35b` (Qwen) | `FREEINFERENCE_API_KEY` | The default. The free tier takes one request at a time. |
| `gemini` | `gemini-3.5-flash` (Gemini) | `GEMINI_API_KEY` | Uses Google's OpenAI-compatible endpoint, with `reasoning_effort: "minimal"`. |
| `deepseek` | `deepseek-flash` (DeepSeek) | `DEEPSEEK_API_KEY` | Sends `thinking: disabled`. |

```python
ask = make_ask(mode="live", provider="gemini")
ask = make_ask(mode="live", provider="deepseek", model="deepseek-v4-pro")  # another model from the same provider
```

The presets configure a small output budget and provider-specific reasoning settings. Model identifiers and accepted settings can change; verify current availability with student-equivalent access before teaching, and override the model and `extra_body` when your institution supplies different settings.

Lab 06's council needs at least three model families in live mode, so its architects use all three providers: Qwen on FreeInference, DeepSeek, and Gemini. Save all three keys in Colab Secrets.

## Checkable reasoning and tokens (Lab 01)

The final step compares a short prompt with explicit eventId deduplication instructions using the same course provider. It makes the answer checkable against Python, rather than claiming to observe private model reasoning or guaranteeing one model fails a familiar word puzzle. Token budgets and reasoning-model behavior are explained without a separate account.

## Optional TypeSafe scores (Lab 17)

The default matrix uses explicit illustrative scores with `MODE="practice"`. The optional live step uses the pinned TypeSafe SDK and the System One endpoint, not Chat Completions. Add `TYPESAFE_API_KEY` to Colab Secrets and change that lab's own mode to `live`. `coursekit.secret` reads the Colab secret or falls back to hidden local input. No request is made simply because a key exists in the environment.

The live state describes task-queue versus event-log choices and eight option–criterion questions. TypeSafe returns typed scores; Python owns weighting and eligibility. Confidence describes the returned distribution, not a guarantee of good architecture. See the [Score](https://docs.typesafe.ai/primitives/score) and [Python SDK](https://docs.typesafe.ai/sdk/python) references. FreeInference keys cannot authenticate TypeSafe.

## Optional: LangSmith traces (Lab 07)

Lab 07 can send a trace of each council run to [LangSmith](https://smith.langchain.com/). Create a free account and an API key, save it in Colab Secrets as `LANGSMITH_API_KEY`, and set `LANGSMITH_TRACING="true"` before the first step, as the lab shows. Without the key, nothing is sent, and the lab runs on its logs alone. A trace contains the case and every agent's reply, so do not trace private data to a shared project.

## Calls, errors, and limits

The example client uses HTTPS, a timeout, bounded calls/output, and no silent retry or credential switching. It keeps usage unknown when the provider does not report it. FreeInference requests are non-streaming; provider-specific settings remain separate from the general interface. A cold-start placeholder should be treated as a request to wait and retry manually, not as a useful answer.

| Symptom | Check |
| --- | --- |
| 401/403 | Key validity, secret permission, and model access |
| 404 | API prefix, base URL, and model identifier |
| 400 | Supported parameters, token field, and message roles |
| 429 | Current quota and rate limits; FreeInference's free tier allows one request at a time |
| Empty or truncated answer | Response content and output-token budget |
| Invalid JSON or unsupported citation | Model output and validation; do not bypass the check |

The setup cell installs the shared course package from a pinned public GitHub revision. Protocol and framework labs also install their relevant SDK. This needs internet access; the small MCP/A2A examples themselves do not require a model key. Runtime and server setup code is in the package rather than embedded in each notebook.

Automated verification runs practice and local protocol examples with no paid model calls. Test live-provider compatibility separately with a small request before teaching. See [Google’s Colab FAQ](https://research.google.com/colaboratory/faq.html) for notebook/runtime details.


## Lecture-aligned examples

Labs 00–17 now revisit the supplied microservices and DDD decks; see the [slide map](slide-map.md). The A2A lab (13) uses a deterministic local payment adapter, so it no longer needs a model key. Lab 17 uses its own explicit `MODE="practice"` switch and requires a **TypeSafe** key only for optional live scoring. FreeInference credentials cannot be used as TypeSafe credentials. Lab 01's token/checkable-reasoning example uses the course provider; no extra OpenRouter account is required.
