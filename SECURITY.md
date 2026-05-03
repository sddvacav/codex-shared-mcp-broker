# Security Policy

This repository is designed to be public and sanitized.

Do not commit:

- API keys;
- OAuth tokens;
- bearer tokens;
- billing or quota data;
- private routing configuration;
- production queue state;
- real account identifiers;
- local machine credentials.

If you find a secret in the repository, revoke it first, then open a private security report if available or contact the maintainer through GitHub.

Run before publishing:

```powershell
python -m pytest
codex-shared-mcp-audit .
powershell -ExecutionPolicy Bypass -File scripts/check-no-secrets.ps1
```

