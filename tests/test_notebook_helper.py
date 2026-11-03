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


if __name__ == "__main__":
    unittest.main()
