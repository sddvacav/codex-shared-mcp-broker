# 演示和 Benchmark 方案

发布时需要一个简单、可传播、隐私安全的证明点。Benchmark 应该测本地 runtime 进程放大，而不是测模型质量。

## 演示故事线

1. 展示用户同时打开多个 Codex Desktop 窗口，并启用 MCP-heavy 工具。
2. 用脱敏计数视图展示本地进程增长。
3. 切换到共享本机 HTTP MCP 端点。
4. 展示 Codex MCP 条目指向 `http://127.0.0.1:38808/servers/.../mcp`。
5. 展示 broker 统一管理后端进程生命周期。
6. 运行公开 audit 和 preflight 检查。

## 指标

推荐指标：

- MCP 相关后端进程数量；
- broker 外部的后端进程树数量；
- broker HTTP 可达性；
- `codex mcp list` 的 transport 形态；
- 合成负载下本机 CPU 和内存趋势。

不要公开：

- 真实项目名；
- 账号 ID；
- 私有路径；
- token；
- 生产队列名；
- 本地网关路由。

## 合成场景

最终演示可以使用这样的表：

| 场景 | 窗口数 | 每窗口 MCP server 数 | 预期进程模式 |
| --- | ---: | ---: | --- |
| 直接 stdio | 10 | 8 | 重复后端进程树 |
| 共享 broker | 10 | 8 | 一个 broker 管理的后端池 |

这些数字应该来自合成本机测试，并且发布前必须经过隐私扫描。

## 交付物

- 短 GIF 或视频。
- Markdown benchmark 报告。
- 脱敏后的 broker 端点截图。
- 简短说明：这个 benchmark 衡量的是本地 runtime 进程放大，不是模型智能水平。
