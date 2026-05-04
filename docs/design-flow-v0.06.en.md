# Design Flow for Public Stage 0.06

The design flow is evidence-first:

1. State a narrow pain.
2. Show the architecture pattern.
3. Run diagnostics.
4. Explain benchmark results.
5. Run privacy guard.
6. Publish a safe release asset pack.

## Local Capability Map

| Capability | Available locally | Use in this project |
| --- | --- | --- |
| Image generation skill | Yes, when bitmap assets are needed | Existing Image2 cover and product overview assets. |
| Repo-native SVG editing | Yes | Architecture, workflow, benchmark, and product diagrams. |
| Browser Use plugin | Available | Useful for previewing rendered docs or local pages when needed. |
| Documents / Presentations plugins | Available | Useful for turning the launch story into docs or slides later. |
| Canva MCP | Documentation/design-guideline oriented in this session | Useful for design guidance, not used as a release-pack generator. |
| local-tools MCP | Available | File/Python helper capability, not public content by itself. |

## Design Principles

- Prefer deterministic SVG diagrams for technical proof.
- Use bitmap assets only when they communicate product feel better than diagrams.
- Keep all claims bounded.
- Make every public artifact pass privacy scanning.
- Keep bilingual materials aligned.

## Deliverables For This Stage

- Short demo script.
- Release asset pack.
- Design flow document.
- Updated README and release roadmap.

## Acceptance Criteria

- A user can record a short demo from the script.
- A user can copy launch text from the release asset pack.
- All materials avoid private paths, tokens, account IDs, and routing details.
- CI still runs tests, audit, and privacy guard.
