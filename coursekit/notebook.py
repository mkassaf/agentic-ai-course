"""One small learner-facing function; transport details live in runtime.py."""
from .runtime import Client, secret


def make_ask(mode="practice", *, base_url="https://freeinference.org/v1",
             model="qwen3.6-35b", secret_name="FREEINFERENCE_API_KEY",
             token_field="max_tokens"):
    """Create ask(prompt, example=...). Practice returns the explicit example."""
    client = Client(mode=mode, model=model, base_url=base_url,
                    api_key=secret(secret_name) if mode == "live" else "",
                    token_field=token_field, max_calls=12, max_tokens=256)

    def ask(prompt, *, example=""):
        return client.ask(prompt, practice=example)

    return ask
