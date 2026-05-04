# Remotion 演示视频

公开阶段：`0.07`

本阶段把发布叙事做成真正的 Remotion 动画。

## 本地能力决策

你要求的是 Remotion-first 工作流：

- 用 Remotion 管理动画时间线；
- 用仓库内 SVG 和 Image2 资产作为品牌素材；
- 用 `staticFile()` 和 Remotion `<Img>` 引用资产；
- 保持输出隐私安全、可复现。

当前会话没有暴露单独的内置 Remotion MCP 工具，所以实现方式是在仓库内建立标准 Remotion 工程。

## 渲染产物

- MP4：`assets/remotion/codex-shared-mcp-demo.mp4`
- Poster：`assets/remotion/codex-shared-mcp-demo-poster.png`

## 命令

安装依赖：

```powershell
npm install
```

预览：

```powershell
npm run video:preview
```

渲染 poster：

```powershell
npm run video:still
```

渲染 MP4：

```powershell
npm run video:render
```

## 动画结构

Composition 是 `CodexSharedMcpDemo`。

时间线：

1. Hero：项目标题和阶段。
2. Problem：后开的 Codex 窗口可能变慢。
3. Pattern：共享本机 HTTP MCP broker。
4. Toolchain：diagnose、benchmark、privacy guard。
5. Benchmark：80 个合成单元到 9 个。
6. Privacy：发布前 guard。
7. Close：仓库链接和范围边界。

## 隐私规则

- 视频不出现私有机器路径。
- 视频不出现账号 ID。
- 视频不出现 token。
- Benchmark 数据是合成数据。
- 公开表述限定在 Windows + Codex Desktop + MCP fan-out。
