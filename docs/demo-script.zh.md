# 短演示脚本

公开阶段：`0.06`

目标：录制一个 60-90 秒演示，把仓库展示成实用的 agent-runtime 工具包，而不只是文档集合。

## 演示标题

保留 xhigh 推理，修复本地 MCP fan-out。

## 分镜

| 时间 | 场景 | 解说 | 画面 |
| --- | --- | --- | --- |
| 0-10s | 问题 | “多个 Codex Desktop 窗口使用 MCP 工具时，慢的不一定是模型，可能是本地工具进程放大。” | 展示封面图和一句话问题。 |
| 10-25s | 模式 | “不要让每个窗口都启动自己的 stdio 工具树，把 MCP 路由到共享本机 HTTP 端点。” | 展示架构图。 |
| 25-40s | 诊断 | “诊断命令会报告配置策略、实时 MCP transport 形态和 broker 可达性，同时不打印私有路径。” | 运行 `codex-shared-mcp-diagnose --output codex-runtime-report.md`。 |
| 40-55s | Benchmark | “合成 benchmark 解释进程归属变化：直接 stdio 是 80 个单元，共享 broker 是 9 个。” | 展示 benchmark SVG。 |
| 55-70s | 隐私 | “发布前，privacy guard 会检查 token、私有路径、本地网关名和 runtime 痕迹。” | 运行 `agent-runtime-privacy-guard .`。 |
| 70-90s | 收尾 | “范围很窄：Windows、Codex Desktop、MCP 进程放大和发布安全验证。” | 展示 release 页面和仓库链接。 |

## 录制命令

```powershell
python -m pip install -e ".[test]"
python -m pytest
codex-shared-mcp-audit .
codex-shared-mcp-diagnose --output codex-runtime-report.md
codex-shared-mcp-benchmark --windows 10 --servers 8 --output benchmark.md
agent-runtime-privacy-guard .
```

## 录制规则

- 不展示私有终端、账号名、API key、本机路径或真实路由。
- 展示文件时使用脱敏示例配置。
- benchmark 保持合成。
- 不承诺无限并发。
- 不声称这是第一个 MCP gateway。

## 收尾句

Codex Shared MCP Broker 是面向本地 MCP-heavy agent runtime 工作站的发布安全实战模式。
