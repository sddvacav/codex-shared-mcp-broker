# GitHub Landscape

This project is related to, but narrower than, existing MCP proxy and gateway work.

## Existing Related Projects

| Project | Scope | Relevance |
| --- | --- | --- |
| [supercorp-ai/supergateway](https://github.com/supercorp-ai/supergateway) | Converts MCP stdio servers into SSE, WebSocket, or Streamable HTTP services. | Closely related transport bridge. |
| [sparfenyuk/mcp-proxy](https://github.com/sparfenyuk/mcp-proxy) | Proxy between MCP stdio and HTTP/SSE transports. | Similar proxy layer. |
| [IBM/mcp-context-forge](https://github.com/IBM/mcp-context-forge) | MCP gateway, registry, and management layer. | Broader enterprise gateway. |
| [smart-mcp-proxy/mcpproxy-go](https://github.com/smart-mcp-proxy/mcpproxy-go) | MCP proxy focused on tool filtering and context bloat reduction. | Related performance/control motivation. |
| [mcp-router/mcp-router](https://github.com/mcp-router/mcp-router) | MCP server management and routing. | Related routing layer. |
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | Reference and community MCP servers. | Backend ecosystem reference. |

## Differentiation

This repository should not claim to be the first MCP gateway.

The defensible positioning is:

> A Windows-oriented Codex Desktop multi-window shared MCP broker setup, with sanitized examples, bilingual docs, diagrams, preflight checks, and repository audit tooling.

## Why It Is Still Useful

Existing gateway/proxy projects usually focus on MCP transport or server management in general. This repository focuses on one operational problem:

- Codex Desktop multi-window use;
- local process explosion from repeated stdio MCP backends;
- high-effort research workloads where `xhigh` must remain enabled;
- reproducible Windows checks and public release hygiene.

