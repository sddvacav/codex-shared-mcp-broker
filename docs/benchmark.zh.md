# 合成 Benchmark

本仓库包含一个用于说明 MCP 进程放大的合成 benchmark。

它不是实时机器 benchmark。它不会检查真实进程列表、私有路径、账号 ID、token 或本地路由状态。

## 运行

```powershell
codex-shared-mcp-benchmark --windows 10 --servers 8 --output benchmark.md
```

也可以输出 JSON：

```powershell
codex-shared-mcp-benchmark --windows 10 --servers 8 --format json
```

## 默认结果

默认场景是 10 个 Codex 窗口，每个窗口 8 个 MCP server。

| 场景 | 进程树 | 后端进程单元 | Broker 进程单元 | 总进程单元 |
| --- | ---: | ---: | ---: | ---: |
| 直接 stdio | 80 | 80 | 0 | 80 |
| 共享 broker | 8 | 8 | 1 | 9 |

合成减少：71 个进程单元，即 88.75%。

![合成 benchmark](../assets/svg/benchmark.zh.svg)

## 如何理解

这个 benchmark 衡量的是本地 runtime 放大。它不声称提升模型智能，不声称无限并发，也不把它解释成模型速度测试。

重点更窄：如果每个窗口都启动自己的 MCP 后端进程树，工作站会重复支付本地 runtime 成本。共享本机 HTTP broker 改变的是进程归属模式。
