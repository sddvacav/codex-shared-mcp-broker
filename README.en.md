# Codex Shared MCP Broker

[![CI](https://github.com/sddvacav/codex-shared-mcp-broker/actions/workflows/ci.yml/badge.svg)](https://github.com/sddvacav/codex-shared-mcp-broker/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/sddvacav/codex-shared-mcp-broker)](https://github.com/sddvacav/codex-shared-mcp-broker/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

![Image2 cover](assets/image2/cover.png)

Codex Shared MCP Broker is a reproducible Windows setup for running multiple Codex Desktop windows with shared MCP tooling.

**Tagline:** stop local MCP process fan-out before it turns your AI coding workstation into the bottleneck.

It documents the configuration pattern, example broker registry, validation checks, diagrams, and release hygiene needed to avoid local MCP process fan-out.

## Why Star This

- You run multiple Codex Desktop windows and later windows get slower.
- You use MCP servers and suspect local `npx` / `uvx` / Python subprocess fan-out.
- You want to keep `xhigh` reasoning instead of downgrading model quality for speed.
- You need a sanitized, reproducible pattern for sharing MCP tools through local HTTP endpoints.
- You care about agent runtime privacy and release hygiene.

## Problem

In a multi-window Codex Desktop workflow, a single window can be fast, while the second, third, or fourth window becomes slow. A common local cause is not the model itself. It is local tool fan-out:

- each window starts its own MCP stdio subprocesses;
- Node, Python, `npx`, `uvx`, Git, fetch, filesystem, memory, and similar tools accumulate;
- local CPU and memory pressure grow faster than the number of visible windows;
- long scientific/research tasks stall before the model can do useful work.

## Design

The core pattern is:

1. Keep Codex reasoning quality high: `model_reasoning_effort = "xhigh"`.
2. Keep the desired policy target: `model_context_window = 400000`.
3. Put MCP backends behind one local HTTP broker.
4. Point Codex MCP entries at URLs such as `http://127.0.0.1:38808/servers/git/mcp`.
5. Verify that Codex no longer lists direct `npx`, `uvx`, `python`, or `powershell` MCP commands.

![Architecture](assets/svg/architecture.en.svg)

## What This Repository Contains

- bilingual README files;
- bilingual architecture notes;
- GitHub landscape and differentiation notes;
- sanitized Codex config examples;
- sanitized MCP backend registry example;
- PowerShell preflight checks;
- Python repository audit CLI;
- privacy-safe runtime diagnostics and synthetic benchmark commands;
- CI workflow for tests and public artifact audit;
- SVG diagrams for architecture, workflow, impact, and product overview;
- Image2 prompts and generated bitmap assets;
- GitHub launch roadmap and post drafts.

## Image2 Design Assets

![Image2 product overview](assets/image2/product-overview.png)

The generated bitmap assets are committed under [assets/image2](assets/image2). The source prompts are committed under [assets/image2-prompts](assets/image2-prompts), and the full design process is documented in [docs/design-process.en.md](docs/design-process.en.md).

## What This Repository Does Not Include

This is intentionally not a dump of a private machine configuration.

It does not include:

- API keys;
- OAuth tokens;
- billing or quota settings;
- private routing configuration;
- local account state;
- production queues;
- private absolute paths except harmless example placeholders.

## Example Codex Policy

```toml
model = "gpt-5.5"
model_reasoning_effort = "xhigh"
model_context_window = 400000
model_auto_compact_token_limit = 360000
service_tier = "fast"

[agents]
max_threads = 96
max_depth = 8

[mcp_servers.git]
url = "http://127.0.0.1:38808/servers/git/mcp"
```

Full example: [examples/codex-config.toml](examples/codex-config.toml).

## Validation

Install and run the checks:

```powershell
python -m pip install -e ".[test]"
python -m pytest
codex-shared-mcp-audit .
```

Generate a privacy-safe runtime diagnostic report:

```powershell
codex-shared-mcp-diagnose --output codex-runtime-report.md
```

The diagnostic report summarizes:

- Codex policy values such as `xhigh`, `400000`, and `360000`;
- whether MCP entries use shared local HTTP URLs;
- whether live `codex mcp list` output still exposes stdio-style tool commands;
- whether the broker port is reachable;
- red/yellow/green status and next actions.

It does not print private absolute paths, account IDs, tokens, or local routing details.

Generate a synthetic fan-out benchmark:

```powershell
codex-shared-mcp-benchmark --windows 10 --servers 8 --output benchmark.md
```

Default result: direct stdio has 80 synthetic process units, shared broker has 9, a synthetic reduction of 88.75%.

![Synthetic benchmark](assets/svg/benchmark.en.svg)

Demo storyboard:

![Demo storyboard](assets/svg/demo-storyboard.en.svg)

Run the agent runtime privacy guard:

```powershell
agent-runtime-privacy-guard .
```

It checks public-release artifacts for common secret shapes and private local agent runtime details without printing matched secret values.

On a configured machine, run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/preflight.ps1
```

Expected public repository result:

```text
audit-ok
```

## Runtime Workflow

![Runtime workflow](assets/svg/workflow.en.svg)

## Impact

![Impact](assets/svg/impact.en.svg)

The intended outcome is not "infinite concurrency". Hardware, model service limits, and runtime scheduling still matter. The intended outcome is to remove a preventable local bottleneck: duplicated MCP process trees per Codex window.

## Context Window Note

A local config can document and request a `400000` context policy, but Codex Desktop may report a smaller live `model_context_window` when `xhigh` reasoning is active. In observed runs, `xhigh` can reserve a large reasoning budget and expose a smaller effective live window. This repository keeps `xhigh` because the target workload is complex research, and it optimizes the local MCP/process layer instead of reducing reasoning effort.

## Related Projects

This project is not the first MCP proxy or gateway. See [docs/github-landscape.en.md](docs/github-landscape.en.md).

The differentiating scope here is narrower:

> Windows + Codex Desktop + multi-window MCP process fan-out + shared local HTTP broker + reproducible validation.

## GitHub Growth Plan

The public roadmap is in [docs/github-heat-roadmap.en.md](docs/github-heat-roadmap.en.md). The short version:

1. Make this repository the flagship case study for Codex Desktop + MCP process fan-out.
2. Extract reusable runtime privacy checks into a second tool.
3. Add cross-client examples for other MCP-heavy agent desktops.
4. Publish the launch post in [docs/launch-post.en.md](docs/launch-post.en.md).

Additional launch assets:

- [ROADMAP.md](ROADMAP.md)
- [PUBLIC_STAGE.md](PUBLIC_STAGE.md)
- [docs/agent-runtime-privacy-guard.en.md](docs/agent-runtime-privacy-guard.en.md)
- [docs/benchmark.en.md](docs/benchmark.en.md)
- [docs/cross-client-runtime-notes.en.md](docs/cross-client-runtime-notes.en.md)
- [docs/demo-script.en.md](docs/demo-script.en.md)
- [docs/release-asset-pack.en.md](docs/release-asset-pack.en.md)
- [docs/design-flow-v0.06.en.md](docs/design-flow-v0.06.en.md)
- [docs/current-source-check.en.md](docs/current-source-check.en.md)
- [docs/demo-benchmark-plan.en.md](docs/demo-benchmark-plan.en.md)

## License

MIT.
