# Model API setup

Model-based notebooks can use **practice** responses or a **live** model. Practice mode returns the explicit `example` text without a model request. Live mode sends the prompt to the selected service. The MCP lab needs no model key. In the A2A lab, the reviewer agent never calls a model; only the proposer does.

The initial configuration uses **FreeInference**, but the teaching adapter is provider-neutral.

## Initial Colab setup

1. Open the notebook, run its single setup cell, then run the practice example.
2. Open Colab’s **Secrets** panel, create `FREEINFERENCE_API_KEY`, and grant the notebook access. Never paste the key into a code cell.
3. Set `MODE = "live"` in the setup cell.
4. Run the small example and read its answer.

```python
MODE = "live"
ask = make_ask(mode=MODE)
```

The defaults are `https://freeinference.org/v1`, model `qwen3.6-35b`, and secret name `FREEINFERENCE_API_KEY`. If no Colab secret is available, the helper uses a hidden input prompt. Check current access and quotas in the [FreeInference documentation](https://doc.freeinference.org/).

## Use another compatible service

Pass the chosen service settings to the same helper:

```python
ask = make_ask(mode="live", base_url="https://gateway.example/v1",
               model="your-model", secret_name="YOUR_SECRET_NAME")
```

Use a base URL including its API prefix, such as `/v1`, without `/chat/completions`. The example URL above is a placeholder.

The helper uses the [Chat Completions request format](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create). If a provider requires `max_completion_tokens`, add `token_field="max_completion_tokens"` to `make_ask(...)`.

Services with deployment-specific URLs, native Gemini/Messages APIs, SSO-only authentication, or custom headers may require a transport change. Practice examples remain available while that change is made. Use the endpoint and approved models supplied by your institution when required.

## Three model families for the council

Lab 09's council needs at least three model families in live mode. FreeInference serves the Qwen family. Point the other two architects at a second compatible service by replacing the placeholders in the lab's `live` settings:

```python
GATEWAY = dict(base_url="https://your-gateway.example/v1", secret_name="GATEWAY_API_KEY")
live = {"Pragmatist": dict(model="qwen3.6-35b"),
        "Guardian": dict(GATEWAY, model="your-llama-model"), "Innovator": dict(GATEWAY, model="your-mistral-model")}
```

Save the second key in Colab Secrets under the chosen secret name. The lab refuses to run live while the placeholders remain.

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
