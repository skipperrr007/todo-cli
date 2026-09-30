# Development Workflow

本指南给出默认开发流程。项目形成自己的发布或验证制度后，应在此基础上收缩或扩展，并将可执行命令放入 `docs/runbooks/`。

## 默认流程

1. 明确需求、非目标和验收标准。
2. 读取 `CONTEXT.md`、当前 handoff 和相关 architecture/decision。
3. 检查 Git 状态，识别用户已有变更。
4. 设计满足需求的最小改动及受影响文件。
5. 同步实现、测试和对应 owner 文档。
6. 运行受影响范围检查。
7. 审查 diff，确认没有无关文件、密钥、生成产物或重复事实。
8. 更新 `docs/handoffs/current.md` 中真正改变的当前状态。
9. 经授权后本地提交；push、发布和部署分别授权。

## 变更与文档映射

| 变更 | 通常需要同步 |
|---|---|
| 新增公共能力 | `README.md`、`CONTEXT.md`、architecture、测试 |
| 改变长期设计 | 新 decision、architecture、测试 |
| 新增配置或环境变量 | `CONTEXT.md`、使用 guide、相关 runbook、`.env.example`（如适用） |
| 改变构建或发布方式 | runbook、CI 配置、根 README 的最短入口 |
| 完成里程碑或改变停止点 | `docs/handoffs/current.md` |
| 淘汰旧方案 | 新 decision 或当前文档更新；旧材料移入 archive 或标明 superseded |

## 分支与提交

模板不强制具体分支模型。项目至少应明确：

- 默认分支；
- 是否允许直接提交；
- commit message 约定；
- review 要求；
- release/tag 规则；
- 本地提交和远程 push 的授权边界。

## 完成定义

一个变更至少应满足：

- 实现与需求一致；
- 相关测试通过；
- 相关文档没有保留冲突旧描述；
- 没有意外生成物或密钥；
- 已明确未验证内容和剩余风险；
- `python3 tools/check_project_layout.py` 与 `git diff --check` 通过。
