"""Offline integration of the packaged Node launcher and its Python dependency closure."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_salesforce_review as fixture


@unittest.skipUnless(shutil.which("node"), "Node.js is required for launcher integration")
class PackagedLauncher(fixture.FacadeHarness):
    def setUp(self) -> None:
        super().setUp()
        self.package = self.tmp_path / "package"
        # An isolated package catches accidental imports from the full source harness.
        files = [
            "scripts/start_salesforce_mcp.mjs",
            "scripts/salesforce_review_server.py",
            "scripts/salesforce_review_client.py",
            "scripts/schema_format.py",
            "scripts/salesforce_operation_policy.py",
            "scripts/verify_salesforce_org.py",
            "config/salesforce-review-policy.json",
            "schemas/salesforce-review-policy.schema.json",
            "schemas/salesforce-org-review-evidence.schema.json",
        ]
        for name in files:
            destination = self.package / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(fixture.ROOT / name, destination)
        self.local_config = self.package / "config" / "harness.local.json"
        shutil.copy2(self.config_path, self.local_config)

    def launch(self, messages: list[dict]) -> subprocess.CompletedProcess:
        env = self.server_env()
        # Exercise normal packaged config paths. Only CLI and REST transports are fake.
        env.pop("SF_HARNESS_CONFIG_PATH", None)
        env.pop("SF_HARNESS_REVIEW_POLICY_PATH", None)
        env["SALESFORCE_MCP_PYTHON"] = sys.executable
        env["PYTHONPATH"] = ""
        return subprocess.run(
            [
                shutil.which("node"),
                str(self.package / "scripts" / "start_salesforce_mcp.mjs"),
                "--mode", "review", "--org", fixture.ALIAS,
            ],
            cwd=self.tmp_path,
            env=env,
            input="".join(json.dumps(message) + "\n" for message in messages),
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

    def assert_no_contact(self, result: subprocess.CompletedProcess) -> None:
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertNotIn("resolving the Python runtime", result.stderr)
        self.assertEqual((self.tmp_path / "cli-calls.log").read_text(encoding="utf-8"), "")
        self.assertEqual(fixture.MockSalesforce.requests_seen, [])

    def test_packaged_launcher_serves_identity_through_fake_transports(self) -> None:
        result = self.launch([
            self.initialize_message(),
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            self.call(3, "review_org_identity"),
        ])
        self.assertEqual(result.returncode, 0, result.stderr)
        responses = [json.loads(line) for line in result.stdout.splitlines()]
        initialized = next(response for response in responses if response["id"] == 1)
        self.assertEqual(initialized["result"]["serverInfo"]["version"], "3.0.0")
        tools = next(response for response in responses if response["id"] == 2)["result"]["tools"]
        self.assertEqual(len(tools), 7)
        self.assertTrue(all(tool["annotations"]["readOnlyHint"] for tool in tools))
        envelope = self.envelope_of(responses, 3)
        fixture.validate_salesforce_review_envelope(self.package, envelope)
        self.assertEqual(envelope["status"], "VERIFIED")
        self.assertEqual(envelope["target"]["organizationId"], fixture.ORG_ID_18[:15])
        self.assertEqual(self.cli_calls(["version"]), 1)
        self.assertTrue(fixture.MockSalesforce.requests_seen)
        self.assertNotIn("token-1", result.stdout + result.stderr)

    def test_missing_local_config_stops_before_python_cli_or_rest(self) -> None:
        self.local_config.unlink()
        result = self.launch([self.initialize_message()])
        self.assert_no_contact(result)
        self.assertIn("config/harness.local.json is missing", result.stderr)

    def test_disabled_review_stops_before_python_cli_or_rest(self) -> None:
        config = json.loads(self.local_config.read_text(encoding="utf-8"))
        config["salesforce"]["review"]["enabled"] = False
        self.local_config.write_text(json.dumps(config), encoding="utf-8")
        result = self.launch([self.initialize_message()])
        self.assert_no_contact(result)
        self.assertIn("review is disabled", result.stderr)


if __name__ == "__main__":
    unittest.main()
