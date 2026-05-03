# Codex Shared MCP Broker

English: [README.en.md](README.en.md)  
中文：[README.zh.md](README.zh.md)

![Image2 cover](assets/image2/cover.png)

Codex Shared MCP Broker is a Windows-oriented open-source package for documenting, validating, and reproducing a shared MCP setup for Codex Desktop. It targets the specific failure mode where multiple Codex windows each spawn their own heavy MCP stdio process tree, causing the second and third windows to become slow even when the first window is fast.

This repository keeps the high-quality setting intact: `model_reasoning_effort = "xhigh"`. The optimization is not to reduce reasoning quality. The optimization is to move MCP backends behind one shared local HTTP broker and validate that Codex windows connect through HTTP MCP URLs.

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
- [GitHub landscape](docs/github-landscape.en.md)
- [GitHub 相关项目对比](docs/github-landscape.zh.md)
- [Design process](docs/design-process.en.md)
- [设计流程](docs/design-process.zh.md)
