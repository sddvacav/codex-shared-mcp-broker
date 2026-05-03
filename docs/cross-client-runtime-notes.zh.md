# 跨客户端 MCP Runtime 说明

本仓库的主要测试目标是 Codex Desktop。更广泛的 runtime 模式，也可以用于评估其他 MCP-heavy 桌面客户端。

安全的表述不是“本仓库支持所有客户端”。安全表述是：

> 如果某个 MCP 客户端会按窗口、工作区或会话启动本地 stdio 工具 server，它就可能放大本地后端进程树。

## 应该检查什么

检查客户端是否：

- 使用 `npx`、`uvx`、Python 或 shell 命令启动 MCP server；
- 每个窗口或工作区都会启动新的 server 树；
- 窗口关闭后旧 server 树仍然存活；
- 支持 Streamable HTTP 或其他共享远程/server transport；
- 明确说明工具调用是否可以安全并行。

## 可迁移模式

可迁移模式是：

1. 保持模型质量策略不变。
2. 把本地 MCP 后端放到共享 server 或 broker 后面。
3. 在客户端支持时，把它指向共享 HTTP 端点。
4. 用客户端自己的 MCP 列表或日志验证 transport 形态。
5. 只发布脱敏报告。

## 客户端支持矩阵

| 客户端类别 | 本仓库状态 | 说明 |
| --- | --- | --- |
| Windows 上的 Codex Desktop | 主要测试目标 | 这是本项目重点。 |
| 其他 MCP-heavy 桌面客户端 | 只提供概念说明 | 声称兼容前必须验证 transport 支持。 |
| 企业 MCP gateway | 相关生态 | 本仓库不是 gateway 平台替代品。 |
| 无头 agent runner | 后续说明 | 如果它们按 worker 放大 stdio server，则相关。 |

## 表述边界

避免：

- 声称支持所有客户端；
- 发布私有配置路径；
- 发布账号状态或本地网关路由；
- 在没有 server 级并发保证时开启并行工具调用。

优先使用：

- “如果你的 MCP client 重复启动本地 stdio server，这个模式可能适用。”
- “Windows 上的 Codex Desktop 是已测试参考目标。”
- “用诊断和 benchmark 报告作为隐私安全证据。”
