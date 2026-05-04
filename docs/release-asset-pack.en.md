# Release Asset Pack

Public stage: `0.06`

This pack contains copy blocks for launching the project after the `diagnose + benchmark + privacy guard` flow is available.

## One-Line Pitch

Keep xhigh reasoning. Fix local MCP process fan-out. Publish agent-runtime evidence safely.

## Short Description

Codex Shared MCP Broker is a Windows-oriented toolkit for Codex Desktop users running MCP-heavy multi-window workflows. It documents the shared local HTTP broker pattern and includes runtime diagnostics, synthetic benchmarks, and an agent-runtime privacy guard.

## GitHub Release Blurb

This release adds a complete launch asset pack and short demo script. The project now has a clear public story: diagnose the local MCP runtime, explain the process fan-out reduction with a synthetic benchmark, and verify privacy before publishing artifacts.

## X / Twitter Thread

1. I opened multiple Codex Desktop windows and found the bottleneck was not only model latency.
2. The local runtime was multiplying MCP stdio tool process trees.
3. Codex Shared MCP Broker documents a shared local HTTP MCP pattern for Windows.
4. It keeps `xhigh` reasoning. The optimization is the local tool layer.
5. v0.2 added runtime diagnostics.
6. v0.3 added a synthetic benchmark: 10 windows × 8 MCP servers, 80 direct stdio units vs 9 shared broker units.
7. v0.5 added an agent-runtime privacy guard for release safety.
8. Repo: https://github.com/sddvacav/codex-shared-mcp-broker

## Hacker News / Show HN

Title:

Show HN: A Windows Codex Desktop MCP fan-out diagnostic and broker pattern

Post:

I built a small open-source toolkit for a specific local AI workstation problem: when multiple Codex Desktop windows use MCP tools, later windows can slow down because local stdio tool servers are duplicated per window.

The repository documents a shared local HTTP MCP broker pattern and includes:

- runtime diagnostics;
- synthetic fan-out benchmark;
- agent-runtime privacy guard;
- bilingual docs;
- release-safe examples.

It does not claim to be the first MCP gateway or to provide unlimited concurrency. The scope is narrower: Codex Desktop on Windows, MCP process fan-out, and safe public evidence.

Repo: https://github.com/sddvacav/codex-shared-mcp-broker

## Reddit

Title:

Tooling pattern for Codex Desktop + MCP process fan-out on Windows

Body:

I published a small repo around a local runtime issue: multiple Codex Desktop windows with MCP tools can duplicate stdio tool servers and make later windows slow. The repo keeps reasoning effort high and focuses on the local tool/process layer.

It includes diagnostic reports, a synthetic benchmark, and a privacy guard for public release artifacts.

Repo: https://github.com/sddvacav/codex-shared-mcp-broker

## Visual Assets

Use:

- `assets/image2/cover.png`
- `assets/image2/product-overview.png`
- `assets/svg/architecture.en.svg`
- `assets/svg/benchmark.en.svg`
- `assets/svg/workflow.en.svg`

## Safety Checklist

- Run `agent-runtime-privacy-guard .`.
- Use synthetic benchmark data only.
- Do not show private terminal paths.
- Do not publish local gateway routing.
- Do not claim universal client support.
