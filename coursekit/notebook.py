"""One small learner-facing function; transport details live in runtime.py."""
from .runtime import Client, secret

# Each provider speaks the Chat Completions format. "family" names the default model's family.
# Model ids change over time; check the provider's model list before teaching.
PROVIDERS = {
    "freeinference": dict(base_url="https://freeinference.org/v1", model="qwen3.6-35b",
                          secret_name="FREEINFERENCE_API_KEY", family="Qwen"),
    # Both reason before answering by default; the hidden reasoning would use up the small output budget.
    "deepseek": dict(base_url="https://api.deepseek.com/v1", model="deepseek-flash",
                     secret_name="DEEPSEEK_API_KEY", family="DeepSeek", extra_body={"thinking": {"type": "disabled"}}),
    "gemini": dict(base_url="https://generativelanguage.googleapis.com/v1beta/openai", model="gemini-3.5-flash",
                   secret_name="GEMINI_API_KEY", family="Gemini", extra_body={"reasoning_effort": "minimal"}),
}


def make_ask(mode="practice", *, provider="freeinference", base_url=None, model=None, secret_name=None,
             token_field="max_tokens", extra_body=None):
    """Create ask(prompt, example=...). Practice returns the explicit example.

    A provider fills in the base URL, model, secret name, and any provider-specific settings;
    each of them can still be overridden, for example to use another model or a university gateway.
    """
    if provider not in PROVIDERS:
        raise ValueError(f"Unknown provider {provider!r}; choose one of {sorted(PROVIDERS)}")
    preset = PROVIDERS[provider]
    secret_name = secret_name or preset["secret_name"]
    client = Client(mode=mode, model=model or preset["model"], family=preset["family"] if not model else "",
                    base_url=base_url or preset["base_url"],
                    api_key=secret(secret_name) if mode == "live" else "",
                    token_field=token_field, max_calls=12, max_tokens=256,
                    extra_body=preset.get("extra_body") if extra_body is None else extra_body)

    def ask(prompt, *, example=""):
        return client.ask(prompt, practice=example)

    return ask
