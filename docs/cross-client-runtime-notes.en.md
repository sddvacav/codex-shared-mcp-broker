# Cross-Client MCP Runtime Notes

Codex Desktop is the primary tested target for this repository. The broader runtime pattern can still be useful when evaluating other MCP-heavy desktop clients.

The safe claim is not "this repository supports every client." The safe claim is:

> MCP clients that launch local stdio tool servers per window, workspace, or session can multiply local backend process trees.

## What To Look For

Check whether a client:

- starts MCP servers with `npx`, `uvx`, Python, or shell commands;
- starts a new server tree for each window or workspace;
- keeps old server trees alive after a window closes;
- supports Streamable HTTP or another shared remote/server transport;
- documents whether tool calls can safely run in parallel.

## Portable Pattern

The portable pattern is:

1. Keep the model quality policy unchanged.
2. Move local MCP backends behind a shared server or broker.
3. Point the client at shared HTTP endpoints when supported.
4. Verify transport shape with the client's own MCP listing or logs.
5. Publish only sanitized reports.

## Client Support Matrix

| Client family | Status in this repo | Notes |
| --- | --- | --- |
| Codex Desktop on Windows | Primary tested target | This is the project focus. |
| Other MCP-heavy desktop clients | Conceptual notes only | Validate transport support before claiming compatibility. |
| Enterprise MCP gateways | Related ecosystem | This repo is not a replacement for gateway platforms. |
| Headless agent runners | Future notes | Useful if they multiply stdio servers per worker. |

## Claim Boundary

Avoid:

- claiming universal client support;
- publishing private config paths;
- publishing account state or local gateway routing;
- enabling parallel tool calls without server-level concurrency guarantees.

Prefer:

- "This pattern may apply if your MCP client duplicates local stdio servers."
- "Codex Desktop on Windows is the tested reference target."
- "Use the diagnostic and benchmark reports as privacy-safe evidence."
