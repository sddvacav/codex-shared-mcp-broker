# Design Process

This document records the complete design flow used for the public GitHub release.

## 1. Design Brief

The repository needs to explain a specific operational improvement:

- many Codex Desktop windows can reuse one shared MCP broker;
- local MCP stdio backend processes should not multiply per window;
- the setup keeps `xhigh` reasoning for complex scientific work;
- public artifacts must be sanitized and reproducible.

## 2. Asset System

The design package uses two asset layers:

1. **Deterministic SVG diagrams** for exact architecture, workflow, impact, and product explanation.
2. **Image2 bitmap assets** for polished GitHub presentation and product storytelling.

This keeps the repository both attractive and auditable.

## 3. Visual Direction

The visual language is:

- technical and precise;
- dark neutral base with cyan and green routing lines;
- clear local-broker center;
- multiple windows on the left, tool endpoints on the right;
- no private paths, no tokens, no real app screenshots.

## 4. Image2 Outputs

### Cover

![Image2 cover](../assets/image2/cover.png)

Purpose: README hero image and repository social preview candidate.

Prompt source:

- [../assets/image2-prompts/cover.en.md](../assets/image2-prompts/cover.en.md)
- [../assets/image2-prompts/cover.zh.md](../assets/image2-prompts/cover.zh.md)

### Product Overview

![Image2 product overview](../assets/image2/product-overview.png)

Purpose: before/after explanation of duplicated MCP subprocesses versus one shared broker.

Prompt source:

- [../assets/image2-prompts/product.en.md](../assets/image2-prompts/product.en.md)
- [../assets/image2-prompts/product.zh.md](../assets/image2-prompts/product.zh.md)

## 5. Bilingual Delivery

The final repository includes English and Chinese versions for:

- README;
- architecture notes;
- GitHub landscape comparison;
- release checklist;
- design process;
- diagram captions and SVG diagrams;
- Image2 prompts.

## 6. Validation

The design assets were checked for:

- no visible private token strings;
- no private local paths;
- no real screenshot dependency;
- correct conceptual flow: many windows to one broker to shared endpoints;
- readable GitHub README layout.

The repository audit also requires the Image2 output files to exist.

