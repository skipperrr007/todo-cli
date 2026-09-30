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
```

预期：第二条命令输出包含 `1. 冒烟测试`。完成后删除本次生成的 `todo.json` 以恢复干净工作树。

## 结果判定

- 布局检查输出 `layout check passed in project mode`，退出码 0。
- 单元测试 9 个全部通过（5 个项目布局检查器测试 + 4 个 todo 项目测试）。
- 测试的临时文件写在 `tests/_work/`，该目录不进 Git。
- `git diff --check` 无输出。

## 尚未覆盖

- 无集成测试和端到端测试，理由是当前只有单进程命令行入口。
- 无静态检查（formatter/linter/type checker），尚未选定工具。
