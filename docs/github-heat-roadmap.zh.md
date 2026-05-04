# GitHub 热度路线图

目标：让这个仓库被搜索 Codex Desktop、MCP、AI agent、本地 agent runtime 治理、开发者工作站性能的人看到。

## 定位

不要把这个仓库定位成泛泛的 MCP gateway。这个方向已经有很多强项目。

更锋利的定位是：

> Windows 上 Codex Desktop 多窗口 MCP 进程放大的实战案例：共享本机 HTTP MCP 端点、高强度推理、可验证运行时治理和安全发布。

## 目标人群

- Codex Desktop 重度用户。
- MCP server 开发者。
- 同时开多个 AI 编程窗口的用户。
- 开发者工具工程师。
- agent runtime / 本地 AI 安全研究者。
- 关心本地工具治理的企业 AI 平台工程师。

## 为什么容易传播

1. 痛点具体：“第一个 AI 窗口很快，后面的越来越慢。”
2. 原因具体：重复 MCP stdio 子进程树。
3. 方案具体：本机 HTTP broker + 主动验证。
4. 边界清楚：保留 `xhigh` 推理，只优化本地工具层。
5. 安全角度明确：防止把私有本机配置误发到公开仓库。

## 版本路线

### v0.2.0 — Runtime Diagnostics

- 状态：已交付。
- 增加独立诊断命令，报告当前 MCP 列表、broker 可达性和潜在 stdio 进程放大。
- 输出 Markdown 或 JSON 诊断报告。
- 用红/黄/绿状态方便公开分享。

### v0.3.0 — Synthetic Benchmark

- 状态：已交付。
- 增加 N 个窗口 x M 个 MCP server 的合成 benchmark 命令。
- 增加 Markdown 和 JSON 输出。
- 增加可传播的 Before/After SVG 图示。

### v0.4.0 — Cross-Client MCP Runtime Notes

- 状态：已交付。
- 说明类似进程放大模式也可能出现在其他 MCP-heavy 客户端。
- Codex Desktop 仍作为主要测试目标。
- 对未测试产品只给中性说明，不声称支持。

### v0.5.0 — Agent Runtime Privacy Guard

- 状态：已交付。
- 把隐私检查抽成独立模块。
- 检测私有机器路径、凭证、本地网关引用、生成会话痕迹。
- 提供公开仓库发布前的 CI 模板。

### v0.6.0 — Demo and Release Asset Pack

- 状态：已交付。
- 增加短视频演示脚本。
- 增加 GitHub、X/Twitter、Hacker News、Reddit、Linux.do、V2EX 发布文案。
- 增加演示分镜 SVG 和设计流程文档。

### v0.7.0 — Demo Video

- 按脚本录制或组装短演示。
- 展示合成 benchmark：N 个窗口 x M 个工具 server 的进程归属对比。
- 保持合成数据和隐私安全。

## 发布渠道

- GitHub README 和 Release notes。
- Hacker News / Show HN 风格帖子。
- X / Twitter 长帖。
- local AI、programming tools、MCP 相关 Reddit 社区。
- MCP 社区讨论区。
- 中文开发者社区，如 Linux.do、V2EX。

## 传播钩子

- “你的 AI agent 可能不是模型慢，而是本地 MCP 进程树爆炸。”
- “我同时打开多个 Codex 窗口，发现真正瓶颈在本地 runtime。”
- “保留 xhigh 推理，修复本地工具放大。”
- “面向 Codex Desktop + MCP 重度用户的实战 broker 模式。”

## 非目标

- 不承诺无限并发。
- 不声称自己是第一个 MCP proxy。
- 不发布私有机器配置。
- 不包含凭证、账号状态、生产队列或本地网关路由。
