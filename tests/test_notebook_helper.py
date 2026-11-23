import io
import json
import unittest
from unittest.mock import patch

from coursekit import make_ask


class NotebookHelperTests(unittest.TestCase):
    def test_gemini_and_deepseek_serialize_their_actual_live_requests(self):
        expected = {
            "deepseek": ("https://api.deepseek.com/v1/chat/completions", "DEEPSEEK_API_KEY"),
            "gemini": ("https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", "GEMINI_API_KEY"),
        }
        payload = {"choices": [{"finish_reason": "stop", "message": {"content": '{"decision":"retry"}'}}]}
        for provider, (endpoint, key_name) in expected.items():
            with self.subTest(provider=provider), patch("coursekit.notebook.secret", return_value="TEST_ONLY") as read_key, \
                    patch("coursekit.runtime.urllib.request.build_opener") as opener:
                opener.return_value.open.return_value = io.BytesIO(json.dumps(payload).encode())
                ask = make_ask(provider=provider)
                self.assertEqual(ask("Inspect idempotency"), '{"decision":"retry"}')
                request = opener.return_value.open.call_args.args[0]
                body = json.loads(request.data)
                self.assertEqual(request.full_url, endpoint)
                self.assertEqual(request.get_header("Authorization"), "Bearer TEST_ONLY")
                self.assertEqual(body["messages"][-1]["content"], "Inspect idempotency")
                self.assertEqual(body["max_tokens"], 256)
                self.assertNotIn("fixture", request.data.decode())
                self.assertNotIn("TEST_ONLY", request.data.decode())
                if provider == "deepseek":
                    self.assertEqual(body["model"], "deepseek-flash")
                    self.assertEqual(body["thinking"], {"type": "disabled"})
                    self.assertNotIn("reasoning_effort", body)
                else:
                    self.assertEqual(body["model"], "gemini-3.5-flash")
                    self.assertEqual(body["reasoning_effort"], "minimal")
                    self.assertNotIn("thinking", body)
                read_key.assert_called_once_with(key_name)

    def test_uses_secret_and_model_override(self):
        with patch("coursekit.notebook.secret", return_value="TEST_ONLY"), patch("coursekit.notebook.Client") as factory:
            factory.return_value.ask.return_value = "Actual response"
            ask = make_ask(model="chosen-model", secret_name="MY_SECRET")
            self.assertEqual(ask("Say hello"), "Actual response")
            self.assertEqual(factory.call_args.kwargs["model"], "chosen-model")


    def test_providers_fill_in_their_own_settings(self):
        expected = {"freeinference": ("https://freeinference.org/v1", "FREEINFERENCE_API_KEY", None),
                    "deepseek": ("https://api.deepseek.com/v1", "DEEPSEEK_API_KEY", {"thinking": {"type": "disabled"}}),
                    "gemini": ("https://generativelanguage.googleapis.com/v1beta/openai", "GEMINI_API_KEY",
                               {"reasoning_effort": "minimal"})}
        for provider, (url, key_name, extra) in expected.items():
            with self.subTest(provider=provider), patch("coursekit.notebook.secret", return_value="TEST_ONLY") as read_key, \
                    patch("coursekit.notebook.Client") as factory:
                make_ask(provider=provider)
                read_key.assert_called_once_with(key_name)
                self.assertEqual(factory.call_args.kwargs["base_url"], url)
                self.assertEqual(factory.call_args.kwargs["extra_body"], extra)

    def test_overrides_win_and_unknown_providers_are_refused(self):
        with patch("coursekit.notebook.secret", return_value="TEST_ONLY") as read_key, patch("coursekit.notebook.Client") as factory:
            make_ask(provider="gemini", model="another-model", extra_body={}, max_tokens=768)
            read_key.assert_called_once_with("GEMINI_API_KEY")
            self.assertEqual(factory.call_args.kwargs["model"], "another-model")
            self.assertEqual(factory.call_args.kwargs["extra_body"], {})
            self.assertEqual(factory.call_args.kwargs["max_tokens"], 768)
        with self.assertRaisesRegex(ValueError, "Unknown provider"):
            make_ask(provider="nobody")

if __name__ == "__main__":
    unittest.main()
