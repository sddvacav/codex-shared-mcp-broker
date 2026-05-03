# GitHub 相关项目对比

本项目与已有 MCP proxy / gateway 项目相关，但定位更窄。

## 已有相关项目

| 项目 | 范围 | 相关性 |
| --- | --- | --- |
| [supercorp-ai/supergateway](https://github.com/supercorp-ai/supergateway) | 把 MCP stdio server 转成 SSE、WebSocket 或 Streamable HTTP 服务。 | 传输层桥接高度相关。 |
| [sparfenyuk/mcp-proxy](https://github.com/sparfenyuk/mcp-proxy) | MCP stdio 与 HTTP/SSE 之间的代理。 | 与 proxy 层相似。 |
| [IBM/mcp-context-forge](https://github.com/IBM/mcp-context-forge) | MCP gateway、registry 和管理平台。 | 更宽的企业级 gateway。 |
| [smart-mcp-proxy/mcpproxy-go](https://github.com/smart-mcp-proxy/mcpproxy-go) | 面向工具过滤和上下文膨胀控制的 MCP proxy。 | 性能和控制目标相关。 |
| [mcp-router/mcp-router](https://github.com/mcp-router/mcp-router) | MCP server 管理和路由。 | 路由层相关。 |
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | 官方/社区 MCP server 集合。 | 后端生态参考。 |

## 差异化定位

本项目不应宣称自己是第一个 MCP gateway。

更稳妥的定位是：

> 面向 Windows 和 Codex Desktop 多窗口并发的共享 MCP broker 配置方案，包含脱敏示例、中英文文档、图示、预检脚本和仓库审计工具。

## 为什么仍然有价值

已有 gateway/proxy 项目通常关注通用 MCP 传输或 server 管理。本项目关注一个具体运行问题：

- Codex Desktop 多窗口使用；
- 重复 stdio MCP 后端导致本机进程爆炸；
- 复杂科研任务要求保留 `xhigh` 推理强度；
- Windows 下可复现的检查和公开发布卫生。

