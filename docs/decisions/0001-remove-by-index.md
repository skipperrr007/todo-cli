# Decision 0001: 按 1-based 显示序号删除待办

- Status: accepted
- Date: 2026-10-01
- Owners: project maintainer
- Supersedes: none
- Superseded by: none

## Context

`todo-cli` 需要"删除一条待办"的能力。列表输出是 `1. item`、`2. item`（`main()` 用
`enumerate(..., start=1)`），而存储结构是 Python `list`，下标从 0 开始。需要一次长期决策的点有两个：
对外用哪种寻址方式，以及非法请求（越界、非数字、文件损坏）如何处理。后者尤其重要，
因为删除是本项目第一个不可逆操作，而 `todo.json` 不在 Git 中，也没有备份。

## Decision

- 对外只接受 **1-based 显示序号**：`python src/todo.py remove <序号>`，序号与列表打印的
  序号完全一致；内部按 `index - 1` 换算为 0-based 下标。
- 删除前先校验 `1 <= index <= len(items)`；不满足时抛 `IndexError`，**不调用 `save()`**，
  store 逐字节不变，不会出现"删错了却已经写回"的情况。
- 入口层：缺少参数或多余参数走 usage 分支（退出码 2）；非整数或越界向 stderr 打印错误并返回 1。
- 加载失败（坏 JSON、或内容不是数组）时不做任何写入，原文件逐字节保留，用户仍可手工修复。
- 本次**不做原子替换**：`save()` 继续直接覆盖写入；该已知限制记录在
  `docs/architecture/overview.md` 的"当前限制"和 `docs/handoffs/current.md` 的"下一入口"。

## Alternatives considered

### Alternative A：0-based 下标

- 优点：与 Python 内部表示一致，实现最直接，不需要换算。
- 缺点：界面显示 `1.` 而输入是 `0`，用户必须自己减一，最容易删错一条。
- 未选择原因：对外接口应服从用户可见的编号，换算成本放在代码里由边界测试守住。

### Alternative B：按内容匹配删除（`remove <文本>`）

- 优点：不需要先查序号。
- 缺点：重复文本无法区分删哪一条；必须额外定义部分匹配、大小写、空格处理规则；删除范围不可预测。
- 未选择原因：不可预测的破坏面大于便利性，与"最小且可读"的项目目标不符。

### Alternative C：引入稳定 id（如 UUID）作为标识

- 优点：删除后其余项的标识不漂移，可平滑扩展到 `done`、多列表、并发编辑。
- 缺点：改变数据模型（`list[str]` 变为记录列表），破坏现有 `todo.json` 和 CONTEXT 中
  "item 是一个字符串"的术语定义，超出本次最小需求。
- 未选择原因：当前不变量是"生产代码只依赖标准库、store 是一个字符串数组"，不值得为一个删除功能推翻。

## Consequences

### Positive

- 用户可以直接照抄列表里的序号，无换算负担。
- 所有非法输入都在写盘前被拒绝；越界不会静默删错项，也无法用 `-1` 删到末项。
- 为未来的 `done` 提供现成寻址约定，避免出现两套编号规则。

### Negative or cost

- 删除后其余 item 的序号前移，用户按旧序号继续操作会错位；缓解方式是每次成功删除都打印被删文本。
- 1-based 对外与 0-based 内部的差异需要长期维护，两端边界必须由测试守住。
- 不引入稳定 id，就无法区分同名的两条，也无法在外部编辑或并发场景下可靠引用"同一项"。
- 删除不可逆：`todo.json` 不在 Git 中、无自动备份，且 `save()` 非原子替换，写盘中断可能留下损坏文件。

## Verification

- `tests/test_todo.py` 的 `TodoRemoveTest` 覆盖：中间项删除后的剩余顺序；首/末端点映射；
  0、负索引、len+1 的拒绝；缺失 store 不创建文件；坏 JSON 保留原文件；
  入口层非法参数以非零码退出；成功路径的退出码、stdout 与删除后序号重排。
- 拒绝路径的断言一律包含"文件字节不变"，而不只是"抛出了异常"。
- 手动冒烟步骤见 `docs/runbooks/verification.md`。

## Follow-up

- 在 `docs/handoffs/current.md` 的"下一入口"保留待办：考虑把 `save()` 改为原子替换。
- 若实现 `done`，复用本 decision 的 1-based 序号约定；若转而采用稳定 id，需新建 decision 并双向链接。
- 尚未覆盖："删除唯一一条后 store 为空数组（`[]`）"这一状态没有专门测试。
- 已知限制（编码容错）：`load()` 以 `encoding="utf-8"` 读取，带 UTF-8 BOM 的 `todo.json`
  （例如被记事本保存过）会被判为坏 JSON，导致所有命令失败。建议改用 `utf-8-sig`。
- 已知限制（错误信息）：坏 JSON 时以 Python traceback 形式报错。退出码 1 且不写盘的行为是正确的，
  但缺少面向用户的错误信息；建议在 `main()` 捕获 `JSONDecodeError`/`ValueError`，
  打印一行人类可读错误后返回 1。
