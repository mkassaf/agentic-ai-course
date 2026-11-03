# API setup: FreeInference first, configurable providers

The notebooks have two modes. **Practice** uses visible scripted fixtures with no network requests. **Live** sends the example's actual prompts using the OpenAI-compatible Chat Completions request format. The initial provider is **FreeInference**, with **`qwen3.6-35b`**. Endpoint, model, family, secret name and token parameter remain configurable, so a university gateway or another compatible provider can be substituted. Providers with a different protocol need an adapter.

## Initial configuration

```python
MODE = "practice"  # change to "live" when ready to make API requests
BASE_URL = "https://freeinference.org/v1"
MODEL = "qwen3.6-35b"
FAMILY = "Qwen"
SECRET_NAME = "FREEINFERENCE_API_KEY"
TOKEN_FIELD = "max_tokens"
```

The provider's [quickstart](https://doc.freeinference.org/quickstart) documents the base URL and model ID. The [model catalogue](https://doc.freeinference.org/models) describes `qwen3.6-35b` as a non-thinking model; the authenticated `/v1/models` result is the source of truth for account access. Availability and quota can change. Students use the key supplied by the teaching team; these labs do not require them to create accounts.

## Information the teaching team must supply

| Setting | Required information |
| --- | --- |
| API base URL | An approved HTTPS URL including its API prefix, e.g. `https://gateway.university.example/v1`. The client appends `/chat/completions`. |
| Model | The exact deployment/model ID accepted by the gateway. |
| Model family | The underlying family verified by the university, not an invented role label. |
| API key | A teaching-team-provided credential stored as a Colab secret, initially `FREEINFERENCE_API_KEY`. |
| Output-token field | `max_tokens` or `max_completion_tokens`, according to gateway documentation. |
| Quota and policy | Approved models, per-student budget, rate limits, and data-use rules. |

The `.example` URL above is deliberately non-operational. Do not paste it into a live class configuration. If the university uses Azure's deployment-specific URL and `api-key` authentication, Google Gemini's native API, Claude's native Messages API, SSO-only authentication, or custom headers, the supplied adapter needs a provider-specific change. The course can still run in practice mode while that change is made.

## In Colab

1. Open the notebook and run the practice example once.
2. In the key/Secrets panel, add a secret named `FREEINFERENCE_API_KEY` and grant that notebook access. Alternatively, the helper prompts with hidden input. `SECRET_NAME` can be changed for another provider.
3. Change `MODE` to `"live"`. Keep the FreeInference defaults or set the endpoint, model ID, family, and token field supplied by the TA. Leave key values out of code cells.
4. Run one small request and inspect its trace. If a JSON/schema check fails, inspect the response and improve the contract or bounded repair step; do not bypass validation to make the demo pass.

Lab 06 and Lab 07 require three distinct verified model families for a real council. Configure each council member's model metadata; the same gateway/key can serve several models if the university supports it. The offline council tests protocol mechanics only.

## What the client does

The teaching adapter sends a `model`, a `messages` array containing system/user text, and one output-token bound to `POST <base_url>/chat/completions`. It extracts the returned text and usage fields where supplied. This minimal schema is grounded in the [official Chat Completions reference](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create).

The client uses HTTPS, a request timeout, a per-client call bound, a shared maximum of two simultaneous requests, and no automatic retries. It records call metadata, elapsed time, success/failure, and supplied token counts. Token counts and monetary cost remain unknown when they are not measured; practice speed and zero API use must not be presented as live-model performance. Summed request durations are not parallel wall-clock latency.

The FreeInference transport uses non-streaming responses and detects a known cold-start placeholder before treating it as an answer. If the model is starting, wait as directed and retry deliberately; the client does not sleep, rotate keys, or hide additional requests. Provider-specific request options stay separate from the generic API contract. The provider states that prompts and responses are logged for research, so use the synthetic course scenarios or other approved public data. See the [provider's service statement](https://freeinference.org/).

Tool use in this course is an intentionally small JSON action protocol interpreted by Python. It is not a native provider function-calling implementation. The host validates and allowlists tools, supplies observations, and decides when execution stops. Prompt instructions alone do not enforce the boundary.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| HTTP 401/403 | Credential validity, model entitlements, and secret access. |
| HTTP 404 | Base URL, required API prefix, and deployment/model ID. |
| HTTP 400 | Gateway-specific token field, supported roles, and model parameters. |
| HTTP 429 | Quota or rate limit; reduce concurrency and follow the university retry guidance. |
| Truncated output | Output budget; inspect before paying for another request. |
| Invalid JSON or citation | Treat it as model behavior to handle, not an adapter transport success. |
| Network/SSO problem in Colab | Check whether the university permits Colab access to that endpoint. |

Live execution cannot be certified without the university's endpoint and student-equivalent access. The repository's automated tests use scripted fixtures and mocked HTTP responses; they never make paid API calls.
