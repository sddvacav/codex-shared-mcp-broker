# Demo and Benchmark Plan

The launch needs a simple, privacy-safe proof point. The benchmark should measure local runtime fan-out, not model quality.

## Demo Story

1. Show the user opening multiple Codex Desktop windows with MCP-heavy tooling.
2. Show local process growth in a sanitized counter view.
3. Switch to shared local HTTP MCP endpoints.
4. Show Codex MCP entries resolving to `http://127.0.0.1:38808/servers/.../mcp`.
5. Show the broker owning backend process lifecycle.
6. Run the public audit and preflight checks.

## Metrics

Recommended metrics:

- number of MCP-related backend processes;
- number of backend process trees outside the broker;
- broker HTTP reachability;
- `codex mcp list` transport shape;
- local CPU and memory trend during a synthetic workload.

Do not publish:

- real project names;
- account IDs;
- private paths;
- tokens;
- production queue names;
- local gateway routing.

## Synthetic Scenario

Use a table like this in the final demo:

| Scenario | Windows | MCP servers per window | Expected process pattern |
| --- | ---: | ---: | --- |
| Direct stdio | 10 | 8 | duplicated backend trees |
| Shared broker | 10 | 8 | one broker-owned backend pool |

The numbers should be generated from a synthetic local test, then reviewed by the privacy scanner before publication.

## Deliverables

- A short GIF or video.
- A Markdown benchmark report.
- A sanitized screenshot of the broker endpoints.
- A short explanation that the benchmark is about local runtime process fan-out, not model intelligence.
