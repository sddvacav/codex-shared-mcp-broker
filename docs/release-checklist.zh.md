# 发布检查清单

发布前检查：

- [ ] 没有真实 API key、OAuth token、路由 token、账号 ID、计费信息或私有生产路径。
- [ ] `python -m pytest` 通过。
- [ ] `codex-shared-mcp-audit .` 返回 `audit-ok`。
- [ ] `scripts/check-no-secrets.ps1` 返回 `secret-scan-ok`。
- [ ] README 链接可用。
- [ ] 英文和中文文档都存在。
- [ ] SVG 图示能在 GitHub 渲染。
- [ ] 如果生成 Image2 位图资产，只提交 `assets/` 下的脱敏图片。
- [ ] GitHub 仓库描述不宣称“第一个 MCP gateway”。

建议仓库描述：

```text
Windows-oriented Codex Desktop shared MCP broker setup, bilingual docs, diagrams, and validation tools for high-effort multi-window workloads.
```

