# Architecture

![Architecture](../assets/svg/architecture.en.svg)

## Goal

The goal is to keep Codex Desktop usable under multi-window, high-effort workloads by removing duplicated local MCP process trees.

The target workload is complex research. Therefore, this setup keeps:

- `model_reasoning_effort = "xhigh"`;
- a documented `400000` context policy target;
- shared MCP tools through a local HTTP broker.

## Components

### Codex Desktop Windows

Multiple Codex Desktop windows are allowed to run concurrently. They should not each own an independent heavy MCP stdio backend tree.

### Shared HTTP MCP Broker

The broker listens locally, commonly on:

```text
127.0.0.1:38808
```

It exposes named endpoints:

```text
http://127.0.0.1:38808/servers/git/mcp
http://127.0.0.1:38808/servers/filesystem/mcp
http://127.0.0.1:38808/servers/fetch/mcp
```

### MCP Backends

Backends may still be stdio tools. The important change is ownership: the broker owns the backend lifecycle, not every Codex window.

## Verification Invariants

A machine is considered correctly configured when:

- `codex mcp list` shows HTTP URL entries for local MCP servers;
- direct `npx`, `uvx`, `python`, and `powershell` MCP command entries are not visible in Codex's active MCP list;
- the broker port is listening on localhost;
- process checks show no MCP backend process outside the broker tree;
- public config examples contain no tokens or private credentials.

## Context Window and xhigh

The local config can request:

```toml
model_context_window = 400000
model_auto_compact_token_limit = 360000
model_reasoning_effort = "xhigh"
```

Codex Desktop can still report a smaller live runtime context window under `xhigh`, because the runtime may reserve budget for reasoning. This repository treats that as a runtime behavior and optimizes the local MCP/process layer instead of downgrading reasoning quality.

