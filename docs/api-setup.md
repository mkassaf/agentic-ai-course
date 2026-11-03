# Model API setup

Each notebook can use **practice** responses or a **live** model. Practice mode uses explicit scripted fixtures and sends no model API requests. Live mode sends the example’s actual prompts to a configurable OpenAI-compatible Chat Completions service.

The initial configuration uses **FreeInference**, but the teaching adapter is provider-neutral.

## Initial Colab setup

1. Open the notebook and run its practice example.
2. Open Colab’s **Secrets** panel, create `FREEINFERENCE_API_KEY`, and grant the notebook access. Never paste the key into a code cell.
3. Set the run mode to `"live"` in the configuration cell.
4. Run one small request and inspect its response and trace.

```python
MODE = "live"
BASE_URL = "https://freeinference.org/v1"
MODEL = "qwen3.6-35b"
SECRET_NAME = "FREEINFERENCE_API_KEY"
```

`SECRET_NAME` is the name of the saved secret, not the credential itself. If no Colab secret is available, the helper uses a hidden input prompt. Current model access and quotas depend on the service and account; check the [FreeInference documentation](https://doc.freeinference.org/) before class.

## Use another compatible service

Change `BASE_URL`, `MODEL`, and `SECRET_NAME` to the chosen service. Use a base URL including its API prefix, such as `/v1`, but **without** `/chat/completions`; the client appends that path.

The adapter sends a `model`, a `messages` array, and an output-token bound to `POST <base_url>/chat/completions`. If a provider requires `max_completion_tokens` instead of the default `max_tokens`, add `token_field="max_completion_tokens"` to the `Client(...)` setup. This is the [Chat Completions request format](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create), not a claim that every model service implements it identically.

Services with deployment-specific URLs, native Gemini/Messages APIs, SSO-only authentication, or custom headers may require a transport change. Practice examples remain available while that change is made. Use the endpoint and approved models supplied by your institution when required.

## Calls, errors, and limits

The example client uses HTTPS, a timeout, bounded calls/output, and no silent retry or credential switching. It keeps usage unknown when the provider does not report it. FreeInference requests are non-streaming; provider-specific settings remain separate from the general interface. A cold-start placeholder should be treated as a request to wait and retry manually, not as a useful answer.

| Symptom | Check |
| --- | --- |
| 401/403 | Key validity, secret permission, and model access |
| 404 | API prefix, base URL, and model identifier |
| 400 | Supported parameters, token field, and message roles |
| 429 | Current quota and rate limits; reduce concurrency |
| Empty or truncated answer | Response content and output-token budget |
| Invalid JSON or unsupported citation | Model output and validation; do not bypass the check |

The MCP, A2A, and LangGraph examples install their respective packages in setup cells. Package download needs internet access. The small protocol examples do not require a live model key.

Automated verification runs practice and local protocol examples with no paid model calls. Test live-provider compatibility separately with a small request before teaching. See [Google’s Colab FAQ](https://research.google.com/colaboratory/faq.html) for notebook/runtime details.
