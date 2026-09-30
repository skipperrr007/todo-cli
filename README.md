# todo-cli

一个最小的命令行待办清单工具，同时是项目模板的第一个真实使用案例。

## 这是什么

在命令行里记录和查看待办事项，数据保存为一个本地 JSON 文件。目标用户是想要一个"二十分钟能读完源码"的待办工具的开发者。

非目标：多用户、云同步、图形界面、提醒通知。

## 最短使用路径

不需要安装任何依赖，只用 Python 标准库。

```bash
python src/todo.py add "写文档"
python src/todo.py add "跑测试"
python src/todo.py
python src/todo.py remove 1
```

无参数的那条命令会按 `1.`、`2.` 的序号列出全部待办；`remove` 使用同一个序号删除其中一条，
删除后其余待办重新编号前移。数据默认写入当前目录的 `todo.json`（该文件不进 Git）。

## 快速接手

```text
config/project.json            # 这是模板还是项目
  -> AGENTS.md                 # AI 代理规则和权限边界
  -> CONTEXT.md                # 术语、能力边界
  -> docs/README.md            # 文档地图
  -> docs/handoffs/current.md  # 当前进度和下一步
```

## 目录职责

| 路径 | 唯一职责 |
|---|---|
| `src/` | 生产代码 |
| `tests/` | 自动化测试 |
| `tools/` | 项目结构检查工具 |
| `config/` | 可提交的配置 |
| `examples/` | 最小示例 |
| `docs/` | 设计、决策、操作和交接文档 |

## 检查

```bash
python tools/check_project_layout.py
python -m unittest discover -s tests -v
git diff --check
```

## 来源

本项目由上游项目模板 `0.1.0` 实例化，来源记录在 `config/project.json`。本项目不自动跟随模板升级。
