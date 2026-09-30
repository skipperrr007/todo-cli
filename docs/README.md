# 文档地图

本文件只回答"从哪里开始读"和"哪类事实由哪里负责"，不保存详细状态或执行流水。

## 建议阅读顺序

```text
README.md
  -> config/project.json
  -> AGENTS.md
  -> CONTEXT.md
  -> docs/handoffs/current.md
  -> 与任务相关的 architecture / decisions / guides / runbooks
  -> archive（仅在需要历史背景时）
```

## 权威顺序

发生冲突时按以下顺序核对：

```text
当前代码和自动化测试
  -> AGENTS.md 的项目规则与授权边界
  -> CONTEXT.md 的当前语义
  -> 已接受 decision 与当前 architecture
  -> guides 和 runbooks
  -> current handoff
  -> archive 和外部材料
```

## 文档职责

| 路径 | 负责内容 | 不负责内容 |
|---|---|---|
| `architecture/` | 当前组件、依赖和数据流 | 历史流水、候选想法 |
| `decisions/` | 已接受的重要决策及理由 | 尚未接受的提案 |
| `guides/` | 开发方法和协作方式 | 必须逐步执行的运维命令 |
| `runbooks/` | 可复制执行的验证和恢复步骤 | 架构论证 |
| `handoffs/current.md` | 当前完成项、阻塞项和下一入口 | 详细设计、完整测试日志 |
| `archive/` | 被取代材料和历史背景 | 当前实现和授权 |

## 写作规则

- 新事实写入前先确定唯一 owner。
- 导航文件只保留一句摘要和链接。
- 已接受 decision 不直接改写，需要变化时新建并双向链接。
- 相对时间改为绝对日期。
