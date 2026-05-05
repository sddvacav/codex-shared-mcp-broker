# Broker 分片

Broker 分片用于更高并发的场景：共享 broker 已经启用，但大量 Codex 窗口仍然压在同一个本地端口上。

目标不是减少 MCP。每个分片运行同一套 named MCP server registry。唯一变化是不同 Codex home 指向不同本地 broker 端口。

## 适用场景

当你同时运行很多窗口或 slot home 时使用，例如：

- 30 个 Codex 窗口；
- 每个活跃窗口 5 到 10 个 agent；
- 必须保留完整 MCP 工具能力；
- `codex-shared-mcp-diagnose` 显示单个 broker 端口连接压力过高。

## 规划分片

```powershell
codex-shared-mcp-shards `
  --config C:/Users/example/.codex `
  --config D:/codex_cli_launcher/homes/slot1 `
  --config D:/codex_cli_launcher/homes/slot2 `
  --ports 38808,38809,38810,38811 `
  --from-ports 38808 `
  --named-server-config D:/codex_project/mcp_broker/named_servers.json
```

默认只输出计划，不改文件。只有传入 `--apply` 才会重写配置。

## 应用分片

```powershell
codex-shared-mcp-shards `
  --config D:/codex_cli_launcher/homes/slot1 `
  --config D:/codex_cli_launcher/homes/slot2 `
  --ports 38808,38809 `
  --from-ports 38808 `
  --apply
```

应用时会在每个被修改的 `config.toml` 旁边生成备份。

## 启动 Broker 分片

每个端口运行一个 broker 进程，并使用同一份 named server 配置。分片命令可以按你的路径打印对应启动命令。

每个分片都有自己的后端池。相比单 broker 会增加一些本地后端进程，但仍然避免了更糟糕的 `窗口数 x server 数` stdio 扇出。

## 验证

```powershell
codex-shared-mcp-diagnose --broker-ports 38808,38809,38810,38811
```

报告会包含 broker 端口压力表，显示监听状态、HTTP 状态和 TCP 连接数。
