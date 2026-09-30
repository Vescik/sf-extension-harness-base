#!/usr/bin/env node
// Cross-platform launcher for the Salesforce review MCP from sf-extension-harness.
// Resolve a Python runtime with both direct dependencies and validate local review
// configuration before starting the server. The server proves live org identity
// before exposing its seven read tools.

import { spawn, spawnSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = resolve(SCRIPT_DIR, "..");
const CONFIG_PATH = resolve(REPO_ROOT, "config", "harness.local.json");
const REVIEW_SERVER = resolve(SCRIPT_DIR, "salesforce_review_server.py");
const PROBE_TIMEOUT_MS = 15_000;

function fail(message) {
  process.stderr.write(`Salesforce MCP startup blocked: ${message}\n`);
  process.exit(2);
}

function parseArgs(argv) {
  const parsed = {};
  for (let index = 0; index < argv.length; index += 2) {
    const key = argv[index];
    const value = argv[index + 1];
    if (!key?.startsWith("--") || value === undefined) {
      fail("expected --mode review --org <alias>");
    }
    parsed[key.slice(2)] = value;
  }
  return parsed;
}

const { mode, org } = parseArgs(process.argv.slice(2));
// This launcher exposes the structured review facade only. Developer writes deliberately use
// direct sf/sfdx commands, so no write-mode MCP process is launched from here.
if (mode !== "review") {
  fail(`unsupported mode '${mode ?? ""}'; this MCP launcher supports review mode only`);
}
// Use the same bounded read-only workflow for every authenticated org.
// The Python server still proves the live host and Organization Id before serving tools.
if (!org) {
  fail("the org alias is missing");
}

let config;
if (!existsSync(CONFIG_PATH)) {
  fail(
    "config/harness.local.json is missing; create the ignored local policy from " +
      "config/harness.example.json before starting Salesforce MCP",
  );
}
try {
  config = JSON.parse(readFileSync(CONFIG_PATH, "utf8"));
} catch (error) {
  fail(`cannot read valid ${CONFIG_PATH}: ${error.message}`);
}

const matches = config?.salesforce?.orgs?.filter((candidate) => candidate?.alias === org) ?? [];
if (matches.length > 1) fail("duplicate configured alias");
const entry = matches[0];
const environment = entry ? String(entry.environment) : null;
if (entry && !new Set(["dev", "uat", "stage", "prod", "development", "production"]).has(environment)) {
  fail(`alias '${org}' requires an explicit dev/uat/stage/prod environment (legacy qa has no automatic mapping)`);
}
if (config?.salesforce?.review?.enabled !== true) {
  fail("Salesforce org review is disabled in local configuration");
}

process.stderr.write("Salesforce MCP startup: resolving the Python runtime\n");

// Probe both direct dependencies before selecting an interpreter.
function interpreterCandidates() {
  const candidates = [];
  if (process.env.SALESFORCE_MCP_PYTHON) candidates.push([process.env.SALESFORCE_MCP_PYTHON]);
  candidates.push(
    [join(REPO_ROOT, ".venv", "bin", "python")],
    [join(REPO_ROOT, ".venv", "Scripts", "python.exe")],
    ["py", "-3"],
    ["python3"],
    ["python"],
  );
  return candidates;
}

let python = null;
for (const candidate of interpreterCandidates()) {
  const probe = spawnSync(candidate[0], [...candidate.slice(1), "-c", "import requests, jsonschema"], {
    timeout: PROBE_TIMEOUT_MS,
    stdio: "ignore",
  });
  if (!probe.error && probe.status === 0) {
    python = candidate;
    break;
  }
}
if (!python) {
  fail(
    "no Python interpreter with the 'requests' and 'jsonschema' dependencies was found (tried " +
      "SALESFORCE_MCP_PYTHON, the repo .venv, py -3, python3, python); run: " +
      "python -m pip install --require-hashes -r requirements-mcp.lock",
  );
}

process.stderr.write(
  "Salesforce MCP startup: launching the review facade; CLI authorization and live org validation run before tool discovery\n",
);

const child = spawn(python[0], [...python.slice(1), REVIEW_SERVER, "--org", org], {
  cwd: REPO_ROOT,
  // PYTHONUTF8 forces UTF-8 std streams on Windows, where the default encoding is a
  // legacy code page and the MCP spec mandates UTF-8 frames.
  env: { ...process.env, PYTHONUTF8: "1" },
  stdio: "inherit",
  shell: false,
});

child.on("error", (error) => fail(`failed to start the Python review facade: ${error.message}`));
child.on("exit", (code, signal) => {
  if (signal) process.kill(process.pid, signal);
  else process.exit(code ?? 1);
});
