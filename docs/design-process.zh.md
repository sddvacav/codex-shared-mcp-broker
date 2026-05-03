# 设计流程

本文记录本次 GitHub 公开发布的完整设计流程。

## 1. 设计目标

仓库需要说明一个明确的运行优化：

- 多个 Codex Desktop 窗口复用一个共享 MCP broker；
- 本地 MCP stdio 后端进程不再按窗口重复放大；
- 对复杂科研任务保留 `xhigh` 推理强度；
- 公开资产必须脱敏、可复现、可验证。

## 2. 资产体系

设计资产分两层：

1. **确定性 SVG 图示**：用于架构图、运行逻辑图、作用图、产品说明图。
2. **Image2 位图资产**：用于 GitHub 展示、产品介绍和视觉吸引力。

这样既能保证展示效果，也能保证仓库可审计。

## 3. 视觉方向

视觉语言：

- 技术感明确、结构清晰；
- 深色中性背景，使用青色和绿色连接线；
- 中央是本机共享 broker；
- 左侧是多个 Codex 窗口，右侧是共享工具端点；
- 不出现私有路径、token、真实应用截图。

## 4. Image2 成品

### 封面图

![Image2 封面图](../assets/image2/cover.png)

用途：README 首图和仓库社交预览候选图。

提示词来源：

- [../assets/image2-prompts/cover.en.md](../assets/image2-prompts/cover.en.md)
- [../assets/image2-prompts/cover.zh.md](../assets/image2-prompts/cover.zh.md)

### 产品说明图

![Image2 产品说明图](../assets/image2/product-overview.png)

用途：解释“重复 MCP 子进程”和“一个共享 broker”之间的前后对比。

提示词来源：

- [../assets/image2-prompts/product.en.md](../assets/image2-prompts/product.en.md)
- [../assets/image2-prompts/product.zh.md](../assets/image2-prompts/product.zh.md)

## 5. 中英文交付

最终仓库包含以下中英文版本：

- README；
- 架构说明；
- GitHub 相关项目对比；
- 发布检查清单；
- 设计流程；
- 图题和 SVG 图示；
- Image2 提示词。

## 6. 验证

设计资产已检查：

- 没有可见私有 token 字符串；
- 没有私有本地路径；
- 不依赖真实软件截图；
- 概念链路正确：多窗口到一个 broker，再到共享端点；
- GitHub README 布局可读。

仓库审计也会要求 Image2 成品文件存在。

