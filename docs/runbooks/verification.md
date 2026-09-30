# Verification Runbook

## 前置条件

- Python 3.12 或更高版本。
- 无第三方依赖，无需安装步骤。
- 不需要网络、凭据、GPU 或外部服务。

## 快速检查

```bash
python tools/check_project_layout.py
python -m unittest discover -s tests -v
git diff --check
```

## 手动冒烟

```bash
python src/todo.py add "冒烟测试"
python src/todo.py
python src/todo.py remove 1
python src/todo.py remove 1
```

预期：第二条输出包含 `1. 冒烟测试`；第三条输出 `removed: 冒烟测试` 且退出码 0；
第四条因序号越界在 stderr 报错、退出码 1，且 `todo.json` 内容不变。

删除不可逆，且 store 路径固定为当前目录的 `todo.json`；若该文件已有真实数据，
先手工复制一份再执行。完成后删除本次生成的 `todo.json` 以恢复干净工作树。

## 结果判定

- 布局检查输出 `layout check passed in project mode`，退出码 0。
- 单元测试全部通过（当前 18 个：5 个项目布局检查器测试 + 13 个 todo 项目测试）。
- 测试的临时文件写在 `tests/_work/`，该目录不进 Git。
- `git diff --check` 无输出。

## 尚未覆盖

- 无集成测试和端到端测试，理由是当前只有单进程命令行入口。
- 无静态检查（formatter/linter/type checker），尚未选定工具。
- 未覆盖"删除唯一一条后 store 变为空数组（`[]`）"这一状态。
- 未验证并发写入和写盘中断：`save()` 不是原子替换，删除不可逆且无自动备份。
- 未覆盖：带 UTF-8 BOM 的 store；坏 store 时入口层的错误信息形态（当前直接输出 Python traceback）。
