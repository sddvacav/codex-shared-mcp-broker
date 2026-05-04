# 部署和商业链条

公开阶段：`0.08`

## GitHub Pages 是什么

GitHub Pages 是静态托管。它可以服务：

- HTML；
- CSS；
- 在访问者浏览器里运行的 JavaScript；
- 图片；
- 视频文件；
- 文档。

它不会运行你的后端代码。它不托管数据库、登录系统、任务队列、付费 API 逻辑、定位服务或模型推理。

对这个仓库来说，GitHub Pages 适合放：

- 产品 landing page；
- Remotion 演示视频；
- 发布文案；
- benchmark 图；
- GitHub releases 和文档链接。

## 资源占用

GitHub Pages 不占用你自己的服务器。访问者加载的是 GitHub Pages 基础设施上的静态文件。

但仍然有现实限制：

- 仓库和站点大小限制；
- 构建和部署限制；
- GitHub 当前策略下的带宽/流量限制；
- GitHub 账号和服务条款边界。

所以 GitHub Pages 适合做曝光和线索入口，不适合承载重型产品执行。

## 什么需要真实服务器

你的材料智能设计平台和这个 landing page 不是一类东西。完整平台通常需要：

- 前端应用托管；
- 后端 API；
- 数据库；
- 文件和生成产物对象存储；
- 认证；
- 计费；
- 任务队列；
- GPU/CPU worker；
- 监控和日志；
- 如有需要，定位或区域化服务；
- 隐私和合规控制。

## 商业闭环

商业链条应该是：

1. GitHub 仓库证明可信度。
2. GitHub Pages 用一分钟讲清价值。
3. Remotion 视频让项目可传播。
4. 诊断和 benchmark 形成证据。
5. Privacy guard 建立信任。
6. 用户 star、试用、提交 issue。
7. 认真用户进入托管产品或付费咨询路径。
8. 材料智能设计平台成为高价值付费面。

## 推荐基础设施拆分

| 层 | 推荐平台 | 作用 |
| --- | --- | --- |
| 静态发布页 | GitHub Pages | 公开曝光和 SEO。 |
| 文档 | GitHub repo + Pages | 信任和开发者采用。 |
| 演示视频 | GitHub release asset + Pages 嵌入 | 传播证据。 |
| 托管产品前端 | Vercel、Cloudflare Pages 或类似平台 | 交互式 SaaS UI。 |
| 后端 API | Fly.io、Render、Railway、AWS、Azure 或 GCP | 账号、计费、工作流。 |
| 数据库 | Postgres 兼容服务 | 用户、任务、元数据。 |
| 对象存储 | S3 兼容存储 | PDF、视频、生成材料。 |
| 计算 worker | GPU/CPU worker 池 | 材料仿真、ML、蒸馏、分析。 |

## 边界

不要把密钥、私有路由、账号状态或生产队列放进 GitHub Pages。它是公开静态托管。
