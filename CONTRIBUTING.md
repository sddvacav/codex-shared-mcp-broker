# Contributing

Contributions are welcome when they keep the repository focused:

- Codex Desktop shared MCP configuration;
- Windows preflight checks;
- broker lifecycle validation;
- documentation and diagrams;
- sanitized examples.

Please do not submit private machine configs, tokens, local account state, billing details, or production queue configuration.

Before opening a pull request:

```powershell
python -m pip install -e ".[test]"
python -m pytest
codex-shared-mcp-audit .
```

