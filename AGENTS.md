# AGENTS.md

本文件是项目内 AI 代理规则的根级权威。若其他代理平台需要 `CLAUDE.md`、`GEMINI.md` 等入口，优先将其链接或简短路由到本文件，不复制一套可能漂移的规则。

## Codex 启动协议

每次从项目根目录开始工作时，按固定顺序建立最小上下文：

1. 读取 `config/project.json`，先确认当前是 `template` 还是 `project`。
2. 读取本文件、`README.md`、`CONTEXT.md`、`docs/README.md` 和 `docs/handoffs/current.md`。
3. 检查 Git 分支、工作树状态和 remote；默认已有变更属于用户。
4. 读取目标子树中更具体的 `AGENTS.md`（如果存在）。
5. 只继续读取当前任务关联的 architecture、decision、guide、runbook 和测试；普通任务不扫描全部 archive。
6. 在采取修改前，应能明确：项目目的、仓库角色、当前目标、停止边界、相关 owner 文档和验收命令。

如果 `repositoryRole=template`，不得把模板维护 handoff 当成派生项目进展。如果用户正在创建新项目，必须遵循 `docs/runbooks/bootstrap-new-project.md`，并在完成项目模式检查前保持 `repositoryRole=template`。

## 通用工作规则

- 优先做满足需求的最小变更，保留不相关编辑。
- 代码、配置、测试和文档应在职责明确的位置修改。
- 不在 `README.md`、roadmap 或聊天记录中复制详细执行台账。
- 破坏性操作、外部发布、远程写入、密钥处理和不可逆数据迁移需要明确授权。
- 诊断请求默认只确定原因并报告；只有用户要求修复时才修改实现。
- 实现请求应运行与风险相称的检查，并明确未验证内容。
- 本地提交不自动授权 push、发布、部署、Issue/PR 修改或数据删除。
- 模板仓库的 `origin` 与派生项目的 `origin` 必须不同；发现相同 remote 时停止 push 并修正 remote。
- 不提交密钥、生成产物、缓存、大型运行输出或本机专属配置。

## 文档路由

| 事实类型 | 主要 owner |
|---|---|
| 项目简介和最短使用路径 | `README.md` |
| 代理规则、权限和安全边界 | `AGENTS.md` |
| 术语、配置语义和当前能力边界 | `CONTEXT.md` |
| 当前架构和组件关系 | `docs/architecture/` |
| 已接受的重要决策及理由 | `docs/decisions/` |
| 开发和使用方法 | `docs/guides/` |
| 可执行的构建、验证、发布和恢复步骤 | `docs/runbooks/` |
| 当前接手状态、停止点和下一入口 | `docs/handoffs/current.md` |
| 被取代材料和历史流水 | `docs/archive/` |
| 仓库角色、项目名称、模板版本和来源 | `config/project.json` |

发生冲突时，先核对当前代码和测试，再按 `docs/README.md` 定义的权威顺序处理。历史文档不能覆盖当前政策。

## 验证与交付

变更前确定验收标准。完成后至少：

1. 运行受影响范围的自动化测试或静态检查；
2. 运行 `python3 tools/check_project_layout.py`；
3. 修改模板检查器时运行 `python3 -m unittest discover -s tests -v`；
4. 运行 `git diff --check`；
5. 检查 `git status --short`，区分本次改动和既有改动；
6. 在最终报告中列出实际文件、检查结果、未验证内容和后续边界。

如果项目后来需要更严格的角色分工、独立审查或阶段合同，应在项目内新增明确规则，不把个人用户级配置当作项目事实。`.codex/` 等平台配置属于可选实现，不是本模板快速接手能力的前置条件。
