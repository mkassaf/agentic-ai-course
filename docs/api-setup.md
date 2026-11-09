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

Gemini and DeepSeek models reason before they answer by default, and the hidden reasoning counts against the 256-token output budget, so a long reply comes back truncated. The presets turn reasoning off. Model ids and these switches change over time: in our tests, `gemini-3.8-flash` kept reasoning even at `"low"`, and `gemini-2.5-flash` had been retired. Check each provider's model list before teaching, and if you choose another model, pass its own setting, for example `make_ask(mode="live", provider="gemini", model="gemini-3.5-flash-lite", extra_body={})`.

Lab 06's council needs at least three model families in live mode, so its architects use all three providers: Qwen on FreeInference, DeepSeek, and Gemini. Save all three keys in Colab Secrets.

## Reasoning demo (Lab 01): a plain model vs a reasoning model

Lab 01's Step 5 is an optional live demonstration of **reasoning models** and **tokens**, using the "how many R's in strawberry" task. It **does not** go through `make_ask`: it makes a direct request to OpenRouter so it can read the model's `reasoning` field (which `make_ask` drops) and so it can call a reasoning model with thinking *enabled* (the `make_ask` presets turn reasoning off).

To run it live:

1. Add a Colab Secret named **`OPENROUTER_API_KEY`** and grant the notebook access. Never paste the key into a cell.
2. Set `MODE = "live"` in the setup cell. The step runs only when the key is present **and** `MODE` is `"live"`; otherwise it prints scripted answers (2 / 3 / 3), so the automated practice run stays offline.
3. The step calls three setups on [OpenRouter](https://openrouter.ai/models):
   - `openai/gpt-3.5-turbo-0613` with a simple prompt — typically misses the count (`2`).
   - the same old model with a chain-of-thought prompt — typically counts `3`.
   - `qwen/qwen3-235b-a22b-thinking-2507` (a reasoning model) with the simple prompt — counts `3`: it writes the count in a `reasoning` field before answering in `content`.

The reasoning model's inner writing is charged as **output tokens** (`completion_tokens_details.reasoning_tokens`), so give it a generous `max_tokens` (the step uses 900) or it runs out *mid-reasoning* and never emits the final answer. Model ids change over time; verify both ids serve on your key before class.

## Decision-model lab (17): TypeSafe JEV

Lab 17's live step asks TypeSafe's System One model **JEV** to score each architecture option on a criterion, using the `Score` primitive, and then runs the same weighted matrix in plain code. It **does not** go through `make_ask`: TypeSafe serves a System One endpoint (`POST /v1/systemone`) with typed question primitives, not OpenAI-format chat completions, so the lab installs the TypeSafe SDK directly and keeps the arithmetic independent of the model.

To run the live step:

1. Install the SDK (the notebook setup does this): `pip install "typesafe-sdk==0.7.2"`.
2. Add a Colab Secret named **`TYPESAFE_API_KEY`** and grant the notebook access.
3. The lab reads the key from the environment (the SDK does this automatically). The default base URL is `https://api.typesafe.ai` and the default model is `jev-latest`.

```python
from typesafe_sdk import Score, TypeSafeClient
with TypeSafeClient() as client:          # reads TYPESAFE_API_KEY from the environment
    resp = client.system_one(state=..., questions={...})
print(resp.scores["modular monolith:Cost"].score)   # a position in the rubric
```

**JEV over OpenRouter.** The TypeSafe JEV models are also reachable through [OpenRouter](https://openrouter.ai/models/typesafe) with a standard OpenRouter API key. `typesafe/jev-1.13` (alias for `typesafe/jev-1.13-<date>`) and `typesafe/jev-1.14` work, but **only through OpenRouter's decisions endpoint** (`POST /api/alpha/decisions`, not `/chat/completions`): JEV is a decisions model. The request mirrors TypeSafe's System One shape — a `state` plus `questions` keyed by id, each with a `type` of `score`, `choice`, `noul`, or `box`:

```bash
curl https://openrouter.ai/api/alpha/decisions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -d '{
    "model": "typesafe/jev-1.13",
    "state": {"option": "Microservices", "criterion": "Operations", "context": "..."},
    "questions": {
      "score_ops": {
        "type": "score",
        "instructions": "Score how well this option satisfies the criterion. Higher is better.",
        "criteria": ["1: clearly worst", "2", "3: average", "4", "5: clearly best"]
      }
    }
  }'
```

A successful call returns `answers.<id>.score` (a position on the rubric), per-level `probabilities`, and `confidence`. OpenRouter resolves `typesafe/jev-1.13` to a pinned dated snapshot. Note: `typesafe/jev-router` on OpenRouter routes to a non-TypeSafe model, so it is not a real JEV route — do not point students at it. The native `typesafe_sdk` route (above) is the simpler, primary path and is what the lab uses.

Without a `TYPESAFE_API_KEY`, Lab 17 falls back to scripted scores and the matrix arithmetic still runs, so the live step is optional.

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
