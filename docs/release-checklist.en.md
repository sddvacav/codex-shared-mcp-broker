# Release Checklist

Before publishing:

- [ ] No real API keys, OAuth tokens, route tokens, account IDs, billing details, or private production paths.
- [ ] `python -m pytest` passes.
- [ ] `codex-shared-mcp-audit .` returns `audit-ok`.
- [ ] `scripts/check-no-secrets.ps1` returns `secret-scan-ok`.
- [ ] README links work.
- [ ] English and Chinese docs are both present.
- [ ] SVG diagrams render on GitHub.
- [ ] Image2 bitmap assets, if generated, are committed only under `assets/` and contain no private text.
- [ ] GitHub repository description does not claim "first MCP gateway".

Suggested repository description:

```text
Windows-oriented Codex Desktop shared MCP broker setup, bilingual docs, diagrams, and validation tools for high-effort multi-window workloads.
```

