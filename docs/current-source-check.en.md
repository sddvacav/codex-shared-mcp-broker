# Current Source Check

Checked on: 2026-05-04

This project sits in a fast-moving area, so the public positioning should stay tied to current upstream behavior and related projects.

## Sources Checked

- MCP Streamable HTTP transport specification: <https://modelcontextprotocol.io/specification/2025-06-18/basic/transports>
- MCP basic overview: <https://modelcontextprotocol.io/specification/2025-06-18/basic/index>
- OpenAI MCP docs: <https://developers.openai.com/learn/docs-mcp>
- OpenAI Codex config reference: <https://developers.openai.com/codex/config-reference>
- OpenAI Codex configuration documentation: <https://github.com/openai/codex/blob/main/docs/config.md>
- IBM ContextForge MCP gateway: <https://github.com/IBM/mcp-context-forge>
- Microsoft MCP Gateway: <https://github.com/microsoft/mcp-gateway>
- GitHub Secret Scanning detection scope: <https://docs.github.com/en/code-security/reference/secret-security/secret-scanning-detection-scope>
- GitHub Secret Protection: <https://github.com/security/advanced-security/secret-protection>
- OWASP Secrets Management Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html>
- Recent community signals on Codex/MCP configuration visibility and Windows setup friction:
  - <https://www.reddit.com/r/codex/comments/1srxc56/mcp_server_shows_up_in_codex_cli_but_doesnt_show/>
  - <https://www.reddit.com/r/codex/comments/1rlked7/codex_windows_app_wrong_configtoml/>

## Implications

- Streamable HTTP is the right public framing for shared MCP endpoints.
- Codex MCP configuration belongs under the `mcp_servers` configuration area.
- Parallel MCP tool calls should not be enabled broadly unless a server is known to be safe for concurrent calls.
- This repository should not position itself as a general-purpose enterprise gateway.
- The stronger angle is the practical Windows/Codex Desktop runtime case study: multi-window local MCP process fan-out, shared local HTTP broker, and release-safe validation.
- Community posts are useful operational hints, not authority. They support the need for explicit config-source checks and clear Windows instructions.
- The privacy guard should complement platform secret scanning. Its differentiator is local agent runtime privacy: private paths, runtime home references, local gateway names, generated traces, and risky release artifacts.

## Public Claim Boundary

Safe claims:

- The repository documents a reproducible pattern for reducing duplicated local MCP process trees.
- The examples preserve `xhigh` reasoning and optimize the local tool layer.
- The audit tooling checks public repository artifacts for common secret and privacy leaks.

Claims to avoid:

- "First MCP gateway."
- "Unlimited concurrency."
- "Works for every MCP client."
- "Enterprise-grade gateway replacement."
