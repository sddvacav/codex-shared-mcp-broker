# 发布帖草稿

标题选项：

1. 我同时打开多个 Codex 窗口后发现：瓶颈不是模型，而是本地 MCP 进程放大
2. 保留 xhigh 推理，修复本地 MCP fan-out
3. Codex Shared MCP Broker：面向多窗口 AI 编程的 Windows 实战配置

## 短版

我做了一个小型开源项目，面向同时运行多个 Codex Desktop 窗口、并且启用 MCP 工具的用户。

问题是：第一个窗口很快，但后面的窗口可能越来越慢，因为每个窗口都会重复启动自己的 MCP stdio 子进程树。

解决模式是：把 MCP 后端放到一个本机 HTTP broker 后面，让 Codex MCP 配置指向共享本机 URL，并验证 Codex 不再直接列出 `npx`、`uvx`、`python`、`powershell` 这类 MCP 启动命令。

关键点：这不是降低推理强度。它保留 `xhigh` 推理，优化的是本地工具和 runtime 层。

仓库：

https://github.com/sddvacav/codex-shared-mcp-broker

## 长版

我在排查一个本地 AI 编程工作站问题：第一个 Codex Desktop 窗口运行很快，但第二、第三个窗口会变得很慢。

问题不只在模型。真正放大的部分是本地 runtime。每个窗口都可能启动一套自己的 MCP stdio 子进程树：Node、Python、`npx`、`uvx`、Git、fetch、filesystem、memory 和其他工具 server。

所以我把它当成本地 runtime governance 问题来处理：

- 一个共享本机 HTTP MCP broker；
- 命名端点，例如 `http://127.0.0.1:38808/servers/git/mcp`；
- Codex 窗口连接共享 URL；
- broker 统一管理后端进程生命周期；
- 通过 preflight 和 audit 检查验证；
- 公开示例全部脱敏。

仓库包含中英文文档、图示、Image2 成品图、示例配置、CI、密钥/隐私扫描和 release 包。

这不是第一个 MCP proxy 或 gateway。它的价值更具体：Codex Desktop、Windows、多窗口 MCP 进程放大、高强度推理和可验证实战配置。

