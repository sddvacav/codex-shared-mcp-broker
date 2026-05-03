# Roadmap

This project is focused on one narrow, practical problem:

> Codex Desktop + Windows + MCP-heavy multi-window workflows can multiply local tool processes faster than users expect.

The goal is to make that failure mode visible, measurable, and fixable without reducing reasoning effort.

## v0.2.0 - Runtime Diagnostics

- Status: delivered.
- Added a standalone diagnostic command for local MCP runtime state.
- Reports Codex MCP entries, broker reachability, and likely stdio fan-out.
- Produces sanitized Markdown or JSON reports that can be attached to GitHub issues.
- Keeps private paths, tokens, account state, and gateway routing out of the report.

## v0.3.0 - Synthetic Benchmark

- Status: delivered.
- Added a synthetic benchmark command for N windows x M MCP servers.
- Added Markdown and JSON output.
- Added Before/After SVG diagrams.
- Kept the benchmark privacy-safe by avoiding live process inspection.

## v0.4.0 - Cross-Client Runtime Notes

- Document how similar MCP process fan-out can appear in other MCP-heavy desktop clients.
- Keep Codex Desktop as the primary tested target.
- Avoid claiming support for untested clients.

## v0.5.0 - Agent Runtime Privacy Guard

- Extract reusable privacy checks into a dedicated module.
- Detect credentials, private machine paths, local gateway references, generated session traces, and accidental config dumps.
- Provide CI templates for release-safe public repositories.

## v0.6.0 - Demo Video

- Add a short demo plan and reproducible benchmark method.
- Compare process ownership patterns before and after the shared broker pattern.
- Keep all benchmark data synthetic and privacy-safe.

## Non-Goals

- Infinite concurrency claims.
- Replacing mature MCP gateways.
- Publishing private machine configuration.
- Handling billing, account quota, routing, or production queues.
