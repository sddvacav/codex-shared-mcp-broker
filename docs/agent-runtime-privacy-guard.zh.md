# Agent Runtime Privacy Guard

公开阶段：`0.05`

Agent Runtime Privacy Guard 是面向 AI-agent 仓库的发布前安全层。

它补充平台级 secret scanning，但不替代 GitHub Secret Scanning、push protection、Gitleaks、GitGuardian 或企业级数据防泄漏系统。它的范围更窄，重点是 agent runtime 泄漏：

- 本地 agent home 目录；
- 私有 Windows 用户路径；
- 本地网关名称；
- 机器名形态标识；
- 生成的会话痕迹；
- 常见 API key 和 token 赋值形态；
- 高风险密钥文件名。

## 运行

```powershell
agent-runtime-privacy-guard .
```

项目内等价命令：

```powershell
codex-shared-mcp-privacy-guard .
```

写出报告：

```powershell
agent-runtime-privacy-guard . --output privacy-report.md
```

JSON 输出：

```powershell
agent-runtime-privacy-guard . --format json
```

## 输出策略

报告会输出：

- 规则 ID；
- 严重级别；
- 分类；
- 相对仓库的文件路径；
- 行号；
- 简短说明。

报告不会输出匹配到的密钥值或私有路径内容。

## 默认检测内容

默认规则覆盖：

- OpenAI 风格 API key 形态；
- GitHub token 形态；
- 泛化 key、token、bearer、password 赋值形态；
- 私有本地网关引用；
- 私有 Codex runtime 目录标记；
- Windows 用户目录路径；
- 非示例型私有盘符路径；
- 机器名形态标识；
- 高风险环境变量或凭证文件名。

## 与 GitHub 的关系

如果可用，仍然应该启用 GitHub Secret Scanning 和 push protection。这个 guard 增加的是本地发布前检查，重点覆盖通用 secret scanner 不一定会识别成凭证的 AI-agent runtime 产物。

本轮核对来源：

- GitHub Secret Scanning detection scope: <https://docs.github.com/en/code-security/reference/secret-security/secret-scanning-detection-scope>
- GitHub Secret Protection: <https://github.com/security/advanced-security/secret-protection>
- OWASP Secrets Management Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html>

## 边界

这个工具刻意偏保守。发现项在发布前应作为阻塞项处理。若某条规则对公开模板过严，应使用精确 allowlist，而不是全局关闭隐私检查。
