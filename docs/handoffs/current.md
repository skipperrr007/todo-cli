# Current Handoff

- Updated: 2026-10-01
- Project phase: bootstrapped + remove 功能已实现（未提交）
- Current owner: project maintainer

本文件是当前项目状态和接手边界的唯一入口。保持紧凑；详细设计链接到 architecture，详细操作链接到 runbook。

## Current objective

把"按序号删除一条待办"落地为可验证的功能，并保持项目化检查通过。

## Completed and verified

- 已从模板 0.1.0 复制并初始化独立 Git 历史，默认分支 `main`。
- 已把根 README、CONTEXT、架构、验证 runbook 和本 handoff 改写为项目事实。
- 已移除模板维护专属文档。
- 已实现 `src/todo.py` 的 add/list 能力和 `tests/test_todo.py` 的项目测试。
- 已实现 `remove <序号>`：对外 1-based 显示序号、内部 0-based 下标；越界、非法参数和坏 JSON 均在写盘前拒绝，store 逐字节不变。
- 已按 decision 0001 记录该接口选择；已新增 9 个 remove 测试（含坏 JSON 保留原文件）。
- 已把两项"本仓库必须仍是模板"的过时测试改写为项目断言。
- 已把 todo 测试改为直接使用临时文件，避开 `TemporaryDirectory` 在受限执行环境中的清理失败。
- 结构检查（project 模式）与 18 个单元测试全部通过。
- 已创建 3 个提交：bootstrap、测试断言修正、测试写法修正。

## In progress

- remove 的改动已实现并通过检查，**尚未提交**：工作树保持未提交状态，等待独立复查。

## Blocked or undecided

- 是否实现 `done` 尚无结论；`remove` 的接口选择已由 decision 0001 确定为 1-based。
- 尚未创建 GitHub 远程仓库，`origin` 未配置。
- 许可证未选择。
- 环境限制：`tests/_work/` 下由 `mkdtemp` 创建的早期残留空目录在当前沙箱内无法删除，不影响 Git 状态。

## Stop boundaries

- push、发布和部署需要明确授权。
- 不引入第三方依赖。
- 不预先创建 `data/`、`experiments/` 等扩展目录。

## Next entry point

1. 决定下一步功能范围（`done` 或 JSON 格式校验）；若做 `done`，复用 decision 0001 的 1-based 序号约定。
2. 考虑把 `save()` 改为原子替换（先写临时文件再整体替换）。
3. 错误处理与编码容错（BOM 容错 + 坏 store 的友好报错），含 2 个新测试。
4. 如需发布：创建 GitHub 仓库、配置 `origin`，然后请求授权 push。
5. 每次收工前更新本文件的完成项和下一入口。

## Relevant documents

- [`../../CONTEXT.md`](../../CONTEXT.md)
- [`../architecture/overview.md`](../architecture/overview.md)
- [`../decisions/0001-remove-by-index.md`](../decisions/0001-remove-by-index.md)
- [`../runbooks/verification.md`](../runbooks/verification.md)
- [`../guides/development-workflow.md`](../guides/development-workflow.md)
