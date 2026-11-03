"""Transport-boundary tests: these never contact a provider."""
import io
import json
import unittest
import urllib.error
from unittest.mock import patch

from coursekit.runtime import Client, parse_object, summarize_trace


def client(**overrides):
    options = dict(mode="live", model="university-model", family="verified-family",
                   base_url="https://gateway.university.example/v1",
                   api_key="UNITTEST_ONLY_KEY", max_calls=3)
    options.update(overrides)
    return Client(**options)


class ClientTests(unittest.TestCase):
    def test_practice_runs_offline_and_reports_unknown_usage(self):
        model = Client(max_calls=1)
        with patch("coursekit.runtime.urllib.request.build_opener") as opener:
            self.assertEqual(model.ask("hello", practice="explicit fixture"), "explicit fixture")
        opener.assert_not_called()
        trace = summarize_trace([model])
        self.assertEqual(trace["calls"], 1)
        self.assertIsNone(trace["input_tokens"])
        self.assertIsNone(trace["cost"])
        with self.assertRaisesRegex(RuntimeError, "budget"):
            model.ask("second request")

    def test_compatible_request_uses_real_prompt_and_records_provider_usage(self):
        payload = {"choices": [{"finish_reason": "stop", "message": {"content": "actual answer"}}],
                   "usage": {"prompt_tokens": 11, "completion_tokens": 7}}
        model = client(token_field="max_completion_tokens", max_tokens=123)
        with patch("coursekit.runtime.urllib.request.build_opener") as opener:
            opener.return_value.open.return_value = io.BytesIO(json.dumps(payload).encode())
            self.assertEqual(model.ask("real prompt", system="real system", practice="fixture ignored"), "actual answer")
            request = opener.return_value.open.call_args.args[0]
            sent = json.loads(request.data)
            self.assertEqual(request.full_url, "https://gateway.university.example/v1/chat/completions")
            self.assertEqual(sent["messages"][-1]["content"], "real prompt")
            self.assertEqual(sent["max_completion_tokens"], 123)
            self.assertNotIn("fixture ignored", request.data.decode())
        self.assertEqual(model.trace[0]["input_tokens"], 11)
        self.assertEqual(model.trace[0]["output_tokens"], 7)
        self.assertNotIn("UNITTEST_ONLY_KEY", json.dumps(model.trace))
        self.assertNotIn("real prompt", json.dumps(model.trace))

    def test_gateway_error_is_redacted_and_consumes_budget(self):
        model = client(max_calls=1)
        failure = urllib.error.HTTPError("https://example.invalid/", 401,
                                         "sensitive response text", {}, None)
        with patch("coursekit.runtime.urllib.request.build_opener") as opener:
            opener.return_value.open.side_effect = failure
            with self.assertRaises(RuntimeError) as caught:
                model.ask("private prompt")
            self.assertIn("401", str(caught.exception))
            self.assertNotIn("sensitive", str(caught.exception))
            with self.assertRaisesRegex(RuntimeError, "budget"):
                model.ask("again")
            self.assertEqual(opener.return_value.open.call_count, 1)
        self.assertEqual(model.trace[0]["status"], "error")

    def test_truncation_and_invalid_responses_do_not_silently_pass(self):
        for payload in (
            {"choices": [{"finish_reason": "length", "message": {"content": "partial"}}]},
            {"choices": []},
            {"choices": [{"message": {"content": None}}]},
            {"choices": [None]},
        ):
            with self.subTest(payload=payload):
                model = client()
                with patch("coursekit.runtime.urllib.request.build_opener") as opener:
                    opener.return_value.open.return_value = io.BytesIO(json.dumps(payload).encode())
                    with self.assertRaises(RuntimeError):
                        model.ask("question")
                self.assertEqual(model.trace[0]["status"], "error")

    def test_live_configuration_requires_https_and_verified_metadata(self):
        for change in (
            {"base_url": "http://gateway.university.example/v1"},
            {"base_url": "https://user:password@gateway.university.example"},
            {"base_url": "https://gateway.university.example/?key=secret"},
            {"family": ""}, {"model": ""}, {"api_key": ""},
        ):
            with self.subTest(change=change), self.assertRaises(ValueError):
                client(**change)

    def test_json_contract_rejects_nonobjects_and_broken_json(self):
        self.assertEqual(parse_object('{"decision":"review"}')["decision"], "review")
        for value in ("[]", "null", "not json", '{"decision":'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_object(value)


if __name__ == "__main__":
    unittest.main()
