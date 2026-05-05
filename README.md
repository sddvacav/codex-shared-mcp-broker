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

High-concurrency broker sharding:

```powershell
codex-shared-mcp-shards --config D:/codex_cli_launcher/homes/slot1 --config D:/codex_cli_launcher/homes/slot3 --ports 38808,38809 --from-ports 38808
```

Synthetic benchmark:

```powershell
codex-shared-mcp-benchmark --windows 10 --servers 8 --output benchmark.md
```

Agent runtime privacy guard:

```powershell
agent-runtime-privacy-guard .
```

Remotion demo video:

```powershell
npm install
npm run video:render
```

Static landing page:

```text
site/index.html
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
- [Short demo script](docs/demo-script.en.md)
- [短演示脚本](docs/demo-script.zh.md)
- [Release asset pack](docs/release-asset-pack.en.md)
- [发布素材包](docs/release-asset-pack.zh.md)
- [Design flow 0.06](docs/design-flow-v0.06.en.md)
- [设计流程 0.06](docs/design-flow-v0.06.zh.md)
- [Remotion demo](docs/remotion-demo.en.md)
- [Remotion 演示视频](docs/remotion-demo.zh.md)
- [Deployment and commercial chain](docs/deployment-commercial-chain.en.md)
- [部署和商业链条](docs/deployment-commercial-chain.zh.md)
- [Material library](docs/material-library.en.md)
- [素材库](docs/material-library.zh.md)
- [Hosted product blueprint](docs/hosted-product-blueprint.en.md)
- [Broker sharding](docs/sharding.en.md)
- [Broker 分片](docs/sharding.zh.md)
- [托管产品蓝图](docs/hosted-product-blueprint.zh.md)
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
