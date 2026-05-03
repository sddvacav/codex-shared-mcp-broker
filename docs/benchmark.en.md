# Synthetic Benchmark

This repository includes a synthetic benchmark for explaining MCP process fan-out.

It is intentionally not a live machine benchmark. It does not inspect process lists, private paths, account IDs, tokens, or local routing state.

## Run

```powershell
codex-shared-mcp-benchmark --windows 10 --servers 8 --output benchmark.md
```

JSON output is also available:

```powershell
codex-shared-mcp-benchmark --windows 10 --servers 8 --format json
```

## Default Result

The default scenario is 10 Codex windows and 8 MCP servers per window.

| Scenario | Process trees | Backend process units | Broker process units | Total process units |
| --- | ---: | ---: | ---: | ---: |
| Direct stdio | 80 | 80 | 0 | 80 |
| Shared broker | 8 | 8 | 1 | 9 |

Synthetic reduction: 71 process units, or 88.75%.

![Synthetic benchmark](../assets/svg/benchmark.en.svg)

## How To Interpret

The benchmark models local runtime fan-out. It does not claim model speedup, model intelligence improvement, or unlimited concurrency.

The point is narrower: if each window starts its own local MCP backend tree, the workstation can pay duplicated local runtime cost. A shared local HTTP broker changes the process ownership pattern.
