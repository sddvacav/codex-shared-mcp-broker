# 当前来源核对

核对日期：2026-05-03

这个项目处在变化很快的方向，所以公开定位必须和当前上游文档、相关项目保持一致。

## 已核对来源

- MCP Streamable HTTP transport 规范：<https://modelcontextprotocol.io/specification/2025-06-18/basic/transports>
- MCP basic overview：<https://modelcontextprotocol.io/specification/2025-06-18/basic/index>
- OpenAI MCP 文档：<https://developers.openai.com/learn/docs-mcp>
- OpenAI Codex 配置参考：<https://developers.openai.com/codex/config-reference>
- OpenAI Codex 配置文档：<https://github.com/openai/codex/blob/main/docs/config.md>
- IBM ContextForge MCP gateway：<https://github.com/IBM/mcp-context-forge>
- Microsoft MCP Gateway：<https://github.com/microsoft/mcp-gateway>
- 最近关于 Codex/MCP 配置可见性和 Windows 配置摩擦的社区信号：
  - <https://www.reddit.com/r/codex/comments/1srxc56/mcp_server_shows_up_in_codex_cli_but_doesnt_show/>
  - <https://www.reddit.com/r/codex/comments/1rlked7/codex_windows_app_wrong_configtoml/>

## 对本项目的影响

- 共享 MCP 端点应以 Streamable HTTP 作为公开表述。
- Codex MCP 配置应围绕 `mcp_servers` 配置区域说明。
- 不应默认广泛开启并行 MCP 工具调用，除非明确知道对应 server 可以安全并发。
- 不应把本项目定位成通用企业级 MCP gateway。
- 更强的定位是 Windows/Codex Desktop 的实战 runtime 案例：多窗口本地 MCP 进程放大、共享本机 HTTP broker、可验证的安全发布。
- 社区帖子只能作为操作提示，不作为权威来源。它们说明公开文档里需要写清楚配置来源核对和 Windows 说明。

## 公开表述边界

可以安全表述：

- 本仓库记录一种减少重复本地 MCP 进程树的可复现模式。
- 示例保留 `xhigh` 推理，把优化重点放在本地工具层。
- 审计工具检查公开仓库产物里的常见密钥和隐私泄漏。

应避免表述：

- “第一个 MCP gateway。”
- “无限并发。”
- “适用于所有 MCP client。”
- “替代企业级 gateway。”
