# Project Context

本文件保存 todo-cli 的规范术语、当前能力边界和长期语义。它描述"现在是什么"，不记录每日进度。

## 项目目的

提供一个最小、可读、零依赖的命令行待办清单工具，并作为项目模板的第一个真实用例。

## 当前支持

- 追加待办：`python src/todo.py add "<内容>"`
- 列出全部待办：`python src/todo.py`
- 按显示序号删除一条：`python src/todo.py remove <序号>`
- 数据以 JSON 数组保存在 `todo.json`

## 当前不支持

- 按内容删除（只能按显示序号删除）；标记完成、编辑、排序、优先级
- 多用户、账号、云同步
- 图形界面、提醒和通知
- 并发写入保护
- 原子写盘：`save()` 直接覆盖写入，不写临时文件
- 空字符串校验

## 术语

| 术语 | 含义 | 不应混淆为 |
|---|---|---|
| item | 一条待办事项，一个字符串 | 一条带状态的记录 |
| store | 保存待办的 JSON 文件 | 数据库 |
| list | 按插入顺序输出全部 item | 排序后的视图 |
| index | 列表打印的 1-based 显示序号，`remove` 使用它 | 内部 0-based 下标 |

删除成功后其余 item 的 index 会前移；被删除的 item 无法恢复。

## 配置

| 名称 | 作用 | 默认值 | 稳定性 |
|---|---|---|---|
| store 路径 | 待办数据的存放位置 | 当前目录的 `todo.json` | stable |

测试通过参数注入临时路径，不会写入默认位置。

## 长期不变量

- 生产代码只依赖 Python 标准库。
- `src/` 不导入 `tests/` 或 `tools/` 中的任何内容。
- `todo.json` 属于本机数据，不进入 Git。
- 一个事实只有一个主要 owner 文档。

## 权威边界

- 当前架构见 `docs/architecture/overview.md`。
- 运行、测试和恢复步骤见 `docs/runbooks/verification.md`。
- 当前进度和下一入口见 `docs/handoffs/current.md`。
- 已接受的决策见 `docs/decisions/`。
