# Short Demo Script

Public stage: `0.06`

Goal: record a 60-90 second demo that shows the repository as a practical agent-runtime toolkit, not just documentation.

## Demo Title

Keep xhigh reasoning. Fix local MCP fan-out.

## Storyboard

| Time | Scene | Narration | Visual |
| --- | --- | --- | --- |
| 0-10s | Problem | "When multiple Codex Desktop windows use MCP tools, the slow part may be local tool fan-out." | Show the cover image and the one-line problem. |
| 10-25s | Pattern | "Instead of letting every window spawn its own stdio tool tree, route MCP through shared local HTTP endpoints." | Show architecture diagram. |
| 25-40s | Diagnose | "The diagnostic command reports config policy, live MCP transport shape, and broker reachability without printing private paths." | Run `codex-shared-mcp-diagnose --output codex-runtime-report.md`. |
| 40-55s | Benchmark | "The synthetic benchmark explains the process ownership change: 80 units direct stdio, 9 units through the broker." | Show benchmark SVG. |
| 55-70s | Privacy | "Before publishing, the privacy guard checks for tokens, private paths, local gateway names, and runtime traces." | Run `agent-runtime-privacy-guard .`. |
| 70-90s | Close | "The scope is narrow: Windows, Codex Desktop, MCP process fan-out, and release-safe validation." | Show release page and repo link. |

## Commands To Record

```powershell
python -m pip install -e ".[test]"
python -m pytest
codex-shared-mcp-audit .
codex-shared-mcp-diagnose --output codex-runtime-report.md
codex-shared-mcp-benchmark --windows 10 --servers 8 --output benchmark.md
agent-runtime-privacy-guard .
```

## Recording Rules

- Do not show private terminals, account names, API keys, local paths, or live routing.
- Use the sanitized example config when showing files.
- Keep the benchmark synthetic.
- Do not claim unlimited concurrency.
- Do not claim this is the first MCP gateway.

## Final Line

Codex Shared MCP Broker is a practical release-safe pattern for local MCP-heavy agent runtime workstations.
