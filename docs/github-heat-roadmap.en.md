# GitHub Heat Roadmap

Goal: make this repository visible to people searching for Codex Desktop, MCP, AI agents, local agent runtime governance, and developer workstation performance.

## Positioning

This repository should not be positioned as a generic MCP gateway. That space already has strong projects.

The sharper positioning is:

> The practical Windows case study for Codex Desktop multi-window MCP process fan-out, shared local HTTP MCP endpoints, high-effort reasoning, and release-safe runtime validation.

## Audience

- Codex Desktop power users.
- MCP server developers.
- AI coding agent users running multiple windows.
- Developer tooling engineers.
- Agent runtime and local AI security researchers.
- Enterprise AI platform engineers concerned about local tool governance.

## What Makes It Shareable

1. Concrete pain: "the first AI window is fast, the next ones crawl."
2. Specific cause: duplicated MCP stdio subprocess trees.
3. Practical fix: local HTTP broker plus active verification.
4. Clear boundary: keeps `xhigh` reasoning; optimizes the local tool layer.
5. Safety angle: prevents publishing private local config by mistake.

## Milestones

### v0.2.0 — Runtime Diagnostics

- Status: delivered.
- Added a standalone command that reports current MCP entries, broker reachability, and likely stdio fan-out.
- Emits Markdown or JSON diagnostic reports.
- Adds red/yellow/green status for public sharing.

### v0.3.0 — Synthetic Benchmark

- Status: delivered.
- Added a synthetic benchmark command for N windows x M MCP servers.
- Added Markdown and JSON output.
- Added Before/After SVG diagrams for sharing.

### v0.4.0 — Cross-Client MCP Runtime Notes

- Status: delivered.
- Documented how the same process fan-out pattern can appear in other MCP-heavy clients.
- Kept Codex Desktop as the primary tested target.
- Added neutral examples without claiming support for untested products.

### v0.5.0 — Agent Runtime Privacy Guard

- Status: delivered.
- Extracted reusable privacy checks into a dedicated module.
- Detects private machine paths, credentials, local gateway references, and generated session traces.
- Provides a CI template for public repository release safety.

### v0.6.0 — Demo Video

- Add a short visual demo plan.
- Show the synthetic benchmark: N windows x M tool servers before/after process ownership.
- Keep it synthetic and privacy-safe.

## Launch Channels

- GitHub README and release notes.
- Hacker News / Show HN style post.
- X / Twitter thread.
- Reddit communities focused on local AI, programming tools, and MCP.
- MCP community discussions.
- Chinese developer communities such as Linux.do and V2EX.

## Copy Hooks

- "Your AI agent may not be slow. Your local MCP process tree may be exploding."
- "I opened multiple Codex windows and found a local runtime bottleneck."
- "Keep xhigh reasoning. Fix the local tool fan-out."
- "A practical broker pattern for Codex Desktop + MCP power users."

## Non-Goals

- Do not claim infinite concurrency.
- Do not claim to be the first MCP proxy.
- Do not publish private machine configuration.
- Do not include credentials, account state, production queues, or local gateway routing.
