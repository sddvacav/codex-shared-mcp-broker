# 发布素材包

公开阶段：`0.06`

这个素材包用于在 `diagnose + benchmark + privacy guard` 流程完成后发布项目。

## 一句话定位

保留 xhigh 推理，修复本地 MCP 进程放大，安全发布 agent-runtime 证据。

## 短介绍

Codex Shared MCP Broker 是一个面向 Windows / Codex Desktop / MCP-heavy 多窗口工作流的工具包。它记录共享本机 HTTP broker 模式，并包含 runtime 诊断、合成 benchmark 和 agent-runtime privacy guard。

## GitHub Release 文案

本版本增加完整发布素材包和短演示脚本。项目现在有清晰的公开叙事：诊断本地 MCP runtime，用合成 benchmark 解释进程放大减少，并在发布前验证隐私安全。

## X / Twitter 长帖

1. 我同时打开多个 Codex Desktop 窗口后发现，瓶颈不只是模型延迟。
2. 本地 runtime 会放大 MCP stdio 工具进程树。
3. Codex Shared MCP Broker 记录了 Windows 上共享本机 HTTP MCP 的实战模式。
4. 它保留 `xhigh` 推理，优化的是本地工具层。
5. v0.2 增加 runtime diagnostics。
6. v0.3 增加合成 benchmark：10 窗口 × 8 MCP server，直接 stdio 是 80 个单元，共享 broker 是 9 个。
7. v0.5 增加 agent-runtime privacy guard。
8. 仓库：https://github.com/sddvacav/codex-shared-mcp-broker

## Linux.do / V2EX

标题：

分享一个 Codex Desktop + MCP 多窗口进程放大的诊断和 broker 模式

正文：

我整理了一个小开源项目，解决一个很具体的本地 AI 工作站问题：多个 Codex Desktop 窗口同时使用 MCP 工具时，后开的窗口可能变慢，因为本地 stdio 工具 server 被按窗口重复启动。

仓库保留高强度推理，把优化重点放在本地工具和进程层。

目前包含：

- runtime 诊断报告；
- 合成进程放大 benchmark；
- agent-runtime 隐私扫描；
- 中英文文档；
- 脱敏示例配置。

仓库：https://github.com/sddvacav/codex-shared-mcp-broker

## 可用视觉资产

使用：

- `assets/image2/cover.png`
- `assets/image2/product-overview.png`
- `assets/svg/architecture.zh.svg`
- `assets/svg/benchmark.zh.svg`
- `assets/svg/workflow.zh.svg`

## 安全检查清单

- 运行 `agent-runtime-privacy-guard .`。
- 只使用合成 benchmark 数据。
- 不展示私有终端路径。
- 不发布本地网关路由。
- 不声称支持所有客户端。
