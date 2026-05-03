# Launch Post Draft

Title options:

1. I opened multiple Codex windows and found the bottleneck was local MCP process fan-out
2. Keep xhigh reasoning, fix local MCP fan-out
3. Codex Shared MCP Broker: a practical Windows setup for multi-window AI coding

## Short Version

I built a small open-source setup for Codex Desktop users who run multiple windows with MCP tools enabled.

The issue: the first window can be fast, while later windows slow down because each window may spawn its own local MCP stdio subprocess tree.

The pattern: put MCP backends behind one local HTTP broker, point Codex MCP entries at shared local URLs, and verify that Codex no longer lists direct `npx`, `uvx`, `python`, or `powershell` MCP commands.

The important detail: this does not reduce reasoning effort. It keeps `xhigh` reasoning and attacks the local tool/runtime bottleneck instead.

Repository:

https://github.com/sddvacav/codex-shared-mcp-broker

## Longer Post

I was debugging a local AI coding workstation problem: the first Codex Desktop window was fast, but the second and third windows became painfully slow.

The model was not the only variable. The local runtime was multiplying work. Each window could start its own MCP stdio subprocess tree: Node, Python, `npx`, `uvx`, Git, fetch, filesystem, memory, and other tool servers.

So I turned the problem into a local runtime governance problem:

- one shared local HTTP MCP broker;
- named endpoints such as `http://127.0.0.1:38808/servers/git/mcp`;
- Codex windows connect to the shared URLs;
- broker owns backend process lifecycle;
- preflight and audit checks verify the setup;
- public examples stay sanitized.

The repository includes bilingual docs, diagrams, Image2 assets, example configs, CI, secret/privacy scanning, and a release package.

This is not the first MCP proxy or gateway. The useful scope is narrower: Codex Desktop, Windows, multi-window MCP fan-out, high-effort reasoning, and practical validation.

