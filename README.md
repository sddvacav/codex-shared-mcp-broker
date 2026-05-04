# Codex Shared MCP Broker

[![CI](https://github.com/sddvacav/codex-shared-mcp-broker/actions/workflows/ci.yml/badge.svg)](https://github.com/sddvacav/codex-shared-mcp-broker/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/sddvacav/codex-shared-mcp-broker)](https://github.com/sddvacav/codex-shared-mcp-broker/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

English: [README.en.md](README.en.md)  
中文：[README.zh.md](README.zh.md)

![Image2 cover](assets/image2/cover.png)

Codex Shared MCP Broker is a Windows-oriented open-source package for documenting, validating, and reproducing a shared MCP setup for Codex Desktop. It targets the failure mode where multiple Codex windows each spawn their own heavy MCP stdio process tree, causing later windows to become slow even when the first window is fast.

This repository keeps the high-quality setting intact: `model_reasoning_effort = "xhigh"`. The optimization is not to reduce reasoning quality. The optimization is to move MCP backends behind one shared local HTTP broker and validate that Codex windows connect through HTTP MCP URLs.

Runtime diagnostics:

```powershell
codex-shared-mcp-diagnose --output codex-runtime-report.md
```

Synthetic benchmark:

```powershell
codex-shared-mcp-benchmark --windows 10 --servers 8 --output benchmark.md
```

Agent runtime privacy guard:

```powershell
agent-runtime-privacy-guard .
```

![Architecture](assets/svg/architecture.en.svg)

## Quick Start

```powershell
python -m pip install -e ".[test]"
python -m pytest
codex-shared-mcp-audit .
```

See:

- [English README](README.en.md)
- [中文说明](README.zh.md)
- [English architecture notes](docs/architecture.en.md)
- [中文架构说明](docs/architecture.zh.md)
- [Synthetic benchmark](docs/benchmark.en.md)
- [合成 Benchmark](docs/benchmark.zh.md)
- [GitHub landscape](docs/github-landscape.en.md)
- [GitHub 相关项目对比](docs/github-landscape.zh.md)
- [Design process](docs/design-process.en.md)
- [设计流程](docs/design-process.zh.md)
- [Roadmap](ROADMAP.md)
- [Public stage numbering](PUBLIC_STAGE.md)
- [Agent Runtime Privacy Guard](docs/agent-runtime-privacy-guard.en.md)
- [Agent Runtime Privacy Guard 中文说明](docs/agent-runtime-privacy-guard.zh.md)
- [Current source check](docs/current-source-check.en.md)
- [当前来源核对](docs/current-source-check.zh.md)
- [Cross-client runtime notes](docs/cross-client-runtime-notes.en.md)
- [跨客户端 runtime 说明](docs/cross-client-runtime-notes.zh.md)
- [Demo and benchmark plan](docs/demo-benchmark-plan.en.md)
- [演示和 Benchmark 方案](docs/demo-benchmark-plan.zh.md)
- [GitHub heat roadmap](docs/github-heat-roadmap.en.md)
- [GitHub 热度路线图](docs/github-heat-roadmap.zh.md)
- [Launch post draft](docs/launch-post.en.md)
- [发布帖草稿](docs/launch-post.zh.md)
