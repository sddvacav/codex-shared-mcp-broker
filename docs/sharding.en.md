# Broker Sharding

Broker sharding is for the heavier case where the shared broker pattern is already active, but many Codex windows still pile onto one local broker port.

The goal is not to remove MCP servers. Each shard runs the same named MCP server registry. The only change is that different Codex homes point at different local broker ports.

## When To Use

Use this mode when you run many windows or slot homes at the same time, for example:

- 30 Codex windows;
- 5 to 10 agents per active window;
- full MCP tool availability must stay enabled;
- `codex-shared-mcp-diagnose` shows high connection pressure on one broker port.

## Plan Shards

```powershell
codex-shared-mcp-shards `
  --config C:/Users/example/.codex `
  --config D:/codex_cli_launcher/homes/slot1 `
  --config D:/codex_cli_launcher/homes/slot2 `
  --ports 38808,38809,38810,38811 `
  --from-ports 38808 `
  --named-server-config D:/codex_project/mcp_broker/named_servers.json
```

The command prints a plan by default. It does not rewrite files unless `--apply` is passed.

## Apply Shards

```powershell
codex-shared-mcp-shards `
  --config D:/codex_cli_launcher/homes/slot1 `
  --config D:/codex_cli_launcher/homes/slot2 `
  --ports 38808,38809 `
  --from-ports 38808 `
  --apply
```

Applying creates one backup beside every changed `config.toml`.

## Start Broker Shards

Run one broker process per port with the same named server config. The shard command can print the exact command lines for your paths.

Each shard owns its own backend pool. That increases local backend process count compared with a single broker, but it still avoids the much worse `windows x servers` stdio fan-out.

## Verify

```powershell
codex-shared-mcp-diagnose --broker-ports 38808,38809,38810,38811
```

The report includes a broker port pressure table with listening state, HTTP status, and TCP connection counts.
