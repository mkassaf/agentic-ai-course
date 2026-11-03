"""Small, provider-configurable teaching client. Standard library only."""
import getpass
import json
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

# Shared by every Client in this notebook/process, including parallel workflows.
_NETWORK_SLOTS = threading.BoundedSemaphore(2)


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # Never forward a university credential to another host.


class Client:
    """Practice responses are explicit fixtures, not an LLM or model simulation."""
    def __init__(self, mode="practice", model="", family="", base_url="", api_key="",
                 max_calls=24, max_tokens=512, timeout=45, token_field="max_tokens", extra_body=None):
        if extra_body is not None and (not isinstance(extra_body, dict) or
                set(extra_body) & {"model", "messages", "max_tokens", "max_completion_tokens", "stream"}):
            raise ValueError("extra_body must be a dict and cannot override the request contract or budgets")
        if mode not in {"practice", "live"}:
            raise ValueError("mode must be practice or live")
        if token_field not in {"max_tokens", "max_completion_tokens"}:
            raise ValueError("Ask the university which output-token field it supports")
        if max_calls < 1 or max_tokens < 1 or timeout <= 0:
            raise ValueError("Call, output, and timeout bounds must be positive")
        if mode == "live":
            url = urllib.parse.urlsplit(base_url)
            if url.scheme != "https" or not url.netloc or url.username or url.password or url.query or url.fragment:
                raise ValueError("Use the university HTTPS API base URL, without credentials/query/fragment")
            if not model.strip() or not family.strip() or not api_key.strip():
                raise ValueError("Live mode requires a model, verified model family, and secret key")
        self.mode, self.model, self.family = mode, model, family
        self.base_url, self._api_key = base_url.rstrip("/"), api_key
        self.max_calls, self.max_tokens, self.timeout = max_calls, max_tokens, timeout
        self.token_field, self.trace = token_field, []
        self.extra_body = dict(extra_body or {})
        self._freeinference = urllib.parse.urlsplit(self.base_url).hostname == "freeinference.org"
        self._attempts, self._lock = 0, threading.Lock()

    def ask(self, prompt, *, system="You are a concise teaching assistant.", practice=""):
        if not isinstance(prompt, str) or len(prompt) + len(system) > 28000:
            raise ValueError("Prompt must be text and total prompt length <= 28,000 characters")
        with self._lock:
            if self._attempts >= self.max_calls:
                raise RuntimeError("Call budget reached; inspect the trace before increasing it")
            self._attempts += 1
            call_id = self._attempts
        started = time.perf_counter()
        row = dict(call=call_id, mode=self.mode, model=self.model or "scripted-fixture",
                   family=self.family or "practice", input_tokens=None, output_tokens=None,
                   cost=None, status="ok")
        try:
            if self.mode == "practice":
                content = practice
            else:
                messages = [{"role": "system", "content": system}, {"role": "user", "content": prompt}]
                body = {"model": self.model, "messages": messages, self.token_field: self.max_tokens}
                body.update(self.extra_body)
                if self._freeinference:
                    body.update({"stream": False, "thinking": {"type": "disabled"}})
                req = urllib.request.Request(self.base_url + "/chat/completions",
                    data=json.dumps(body).encode(), method="POST",
                    headers={"Authorization": "Bearer " + self._api_key, "Content-Type": "application/json"})
                try:
                    with _NETWORK_SLOTS:
                        with urllib.request.build_opener(_NoRedirect).open(req, timeout=self.timeout) as response:
                            payload = json.load(response)
                except urllib.error.HTTPError as exc:
                    if exc.code == 429:
                        raise RuntimeError("Gateway HTTP 429: rate/quota limit. Ask the TA about quota; no retry or key rotation made.") from None
                    raise RuntimeError(f"Gateway HTTP {exc.code}; check university access/configuration. No retry made.") from None
                except (urllib.error.URLError, TimeoutError, OSError, ValueError):
                    raise RuntimeError("Gateway/network/JSON error; inspect university configuration. No retry made.") from None
                try:
                    choice = payload["choices"][0]
                    if choice.get("finish_reason") == "length":
                        raise RuntimeError("Output truncated; inspect token budget before retrying")
                    content = choice["message"]["content"]
                    if not isinstance(content, str):
                        raise ValueError("Missing text response")
                    usage = payload.get("usage") or {}
                    row["input_tokens"] = usage.get("prompt_tokens")
                    row["output_tokens"] = usage.get("completion_tokens")
                    if self._freeinference and "model is starting up" in content.lower():
                        raise RuntimeError("FreeInference model is starting up. Wait about 120 seconds, then retry manually; this attempt used the call budget.")
                except (KeyError, IndexError, TypeError, ValueError, AttributeError):
                    raise RuntimeError("Gateway response has no usable text; schema/capability check needed") from None
            return content
        except Exception:
            row["status"] = "error"
            raise
        finally:
            row["latency_s"] = round(time.perf_counter() - started, 4)
            with self._lock:
                self.trace.append(row)


def secret(name="FREEINFERENCE_API_KEY"):
    """Read a Colab secret, then fall back to a hidden local prompt. Never print it."""
    try:
        from google.colab import userdata
        key = userdata.get(name)
        if key:
            return key
    except Exception:
        pass
    return getpass.getpass(f"{name} (hidden): ")


def parse_object(text):
    value = json.loads(text)
    if not isinstance(value, dict):
        raise ValueError("Expected one JSON object")
    return value


def summarize_trace(clients):
    rows = [row for client in clients for row in client.trace]
    return dict(calls=len(rows), failed_calls=sum(r["status"] != "ok" for r in rows),
                input_tokens=sum(r["input_tokens"] for r in rows) if rows and all(isinstance(r["input_tokens"], int) for r in rows) else None,
                output_tokens=sum(r["output_tokens"] for r in rows) if rows and all(isinstance(r["output_tokens"], int) for r in rows) else None,
                summed_call_latency_s=round(sum(r["latency_s"] for r in rows), 4), cost=None)
