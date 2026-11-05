import unittest
from unittest.mock import patch

from coursekit import make_ask


class NotebookHelperTests(unittest.TestCase):
    def test_practice_requires_neither_secret_nor_network(self):
        with patch("coursekit.notebook.secret") as read_key, patch("coursekit.runtime.urllib.request.build_opener") as network:
            ask = make_ask()
            self.assertEqual(ask("Say hello", example="Hello!"), "Hello!")
        read_key.assert_not_called()
        network.assert_not_called()

    def test_live_uses_secret_and_ignores_scripted_answer(self):
        with patch("coursekit.notebook.secret", return_value="TEST_ONLY"), patch("coursekit.notebook.Client") as factory:
            factory.return_value.ask.return_value = "Actual response"
            ask = make_ask(mode="live", model="chosen-model", secret_name="MY_SECRET")
            self.assertEqual(ask("Say hello", example="Fixture"), "Actual response")
            self.assertEqual(factory.call_args.kwargs["mode"], "live")
            self.assertEqual(factory.call_args.kwargs["model"], "chosen-model")


    def test_providers_fill_in_their_own_settings(self):
        expected = {"freeinference": ("https://freeinference.org/v1", "FREEINFERENCE_API_KEY", None),
                    "deepseek": ("https://api.deepseek.com/v1", "DEEPSEEK_API_KEY", {"thinking": {"type": "disabled"}}),
                    "gemini": ("https://generativelanguage.googleapis.com/v1beta/openai", "GEMINI_API_KEY",
                               {"reasoning_effort": "minimal"})}
        for provider, (url, key_name, extra) in expected.items():
            with self.subTest(provider=provider), patch("coursekit.notebook.secret", return_value="TEST_ONLY") as read_key, \
                    patch("coursekit.notebook.Client") as factory:
                make_ask(mode="live", provider=provider)
                read_key.assert_called_once_with(key_name)
                self.assertEqual(factory.call_args.kwargs["base_url"], url)
                self.assertEqual(factory.call_args.kwargs["extra_body"], extra)

    def test_overrides_win_and_unknown_providers_are_refused(self):
        with patch("coursekit.notebook.secret", return_value="TEST_ONLY") as read_key, patch("coursekit.notebook.Client") as factory:
            make_ask(mode="live", provider="gemini", model="another-model", extra_body={})
            read_key.assert_called_once_with("GEMINI_API_KEY")
            self.assertEqual(factory.call_args.kwargs["model"], "another-model")
            self.assertEqual(factory.call_args.kwargs["extra_body"], {})
        with self.assertRaisesRegex(ValueError, "Unknown provider"):
            make_ask(provider="nobody")

if __name__ == "__main__":
    unittest.main()
