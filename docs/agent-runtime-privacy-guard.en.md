# Agent Runtime Privacy Guard

Public stage: `0.05`

The Agent Runtime Privacy Guard is a release-safety layer for AI-agent repositories.

It complements platform secret scanning. It is not a replacement for GitHub Secret Scanning, push protection, Gitleaks, GitGuardian, or enterprise data loss prevention. The narrower scope is agent-runtime leakage:

- local agent home directories;
- private Windows user paths;
- local gateway names;
- machine-name shaped identifiers;
- generated session traces;
- common API key and token assignment shapes;
- risky secret-bearing file names.

## Run

```powershell
agent-runtime-privacy-guard .
```

Equivalent project-scoped command:

```powershell
codex-shared-mcp-privacy-guard .
```

Write a report:

```powershell
agent-runtime-privacy-guard . --output privacy-report.md
```

JSON output:

```powershell
agent-runtime-privacy-guard . --format json
```

## Output Policy

The report prints:

- rule id;
- severity;
- category;
- file path relative to the scanned repository;
- line number;
- short message.

The report does not print matched secret values or private path contents.

## What It Catches

The default rules cover:

- OpenAI-style API key shapes;
- GitHub token shapes;
- generic key, token, bearer, and password assignments;
- private local gateway references;
- private Codex runtime directory markers;
- Windows user profile paths;
- non-example private drive paths;
- machine-name shaped identifiers;
- risky file names such as environment or credentials files.

## How It Fits With GitHub

GitHub Secret Scanning and push protection should still be enabled when available. This guard adds a local pre-release check focused on AI-agent runtime artifacts that generic secret scanners may not classify as credentials.

Current references checked:

- GitHub Secret Scanning detection scope: <https://docs.github.com/en/code-security/reference/secret-security/secret-scanning-detection-scope>
- GitHub Secret Protection: <https://github.com/security/advanced-security/secret-protection>
- OWASP Secrets Management Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html>

## Boundary

This tool is intentionally conservative. Treat findings as a release blocker until reviewed. If a rule is too strict for a public template, use a targeted allowlist rather than disabling privacy checks globally.
