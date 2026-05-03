## Summary

Describe the change and why it matters for Codex Desktop, MCP runtime behavior, diagnostics, or privacy-safe release workflow.

## Checklist

- [ ] I did not include API keys, tokens, account IDs, private paths, local gateway routes, or production queue details.
- [ ] I updated bilingual docs when changing public-facing behavior.
- [ ] I ran `python -m pytest`.
- [ ] I ran `codex-shared-mcp-audit .`.
- [ ] I ran `powershell -ExecutionPolicy Bypass -File scripts/check-no-secrets.ps1`.

## Notes

Add screenshots, sanitized diagnostic snippets, or benchmark results here if relevant.
