# 安全政策 · Security Policy

## 安全范围

本项目为静态文章站、Markdown/PDF/DOCX 构建器和 Agent Skill。主要风险包括：

- 将来源不可信的 Markdown 直接转换为可执行 HTML，导致 XSS；
- 读取包含路径穿越的 article.json 或 meta.json，意外访问仓库外文件；
- 构站脚本删除不受控制的输出目录；
- GitHub Actions 权限过大、命令注入或泄漏令牌；
- 将敏感信息、受保护的原始素材或未许可字体发布到公开仓库。

网页设计上无需登录、账户、服务器数据库或外部追踪服务。即使如此，GitHub Actions 环境和构建输入仍须按不可信数据处理。

## 报告问题

**不要在公开 Issue、Pull Request 或讨论中贴出漏洞利用细节、令牌、个人信息或他人的非公开资料。**

若 GitHub 仓库的 **Security → Advisories → Report a vulnerability** 可用，请优先通过该私密入口提交。若该功能未启用，建议先向仓库维护者请求一个可安全传递信息的私密渠道，而不是公开披露详细利用流程。普通的无敏感信息错误可以提交公开 Issue。

报告时尽量包含：受影响的文件和 commit、可复现现象、预期行为、可能影响，以及无需提交密钥或个人资料的最小验证案例。

## 修复原则

先复核输入边界，再补回归测试，最后修复并验收；不依赖“只在 CI 运行”作为安全保证。优先限制路径、消除未经转义的可执行内容、避免任意目录删除，并采用最小权限 GitHub Actions。任何漏洞修复都不应隐蔽改变文章原文或作者归属。

更多技术说明见 [架构与安全边界](docs/architecture.md)、[维护手册](docs/maintainer-runbook.md) 与 [AGENTS.md](AGENTS.md)。
