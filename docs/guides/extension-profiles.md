# Extension Profiles

核心模板只创建大多数项目都会使用的目录。以下 profile 是按需扩展，不应一次全部启用。

## Research / Numerical

建议增加：

```text
experiments/          # 可复现实验定义，不存放不可控的大型输出
validation/           # 正式指标、参数、阈值、证据摘要和结论
data/README.md        # 数据来源、许可、取得方式；大数据通常不进 Git
notebooks/            # 探索分析；正式结果应有脚本化路径
```

治理建议：区分探索实验、正式验证和历史结果；正式分析尽量读取结构化产物，不依赖临时日志。

## Service / Application

建议增加：

```text
deploy/               # 部署声明和环境模板
ops/                  # 监控、告警和运维配置
docs/api/              # 外部接口与兼容性说明
docs/runbooks/incidents/ # 故障响应和恢复步骤
```

治理建议：密钥不得进入 Git；部署、迁移和回滚应有独立 runbook。

## Reusable Library

建议增加：

```text
include/ or public API package
docs/api/
examples/
benchmarks/           # 只有性能是维护目标时创建
```

治理建议：明确公共 API、兼容性范围、弃用周期和发布版本策略。

## Data / Machine Learning

建议增加：

```text
data/README.md
pipelines/
models/README.md
experiments/
```

治理建议：Git 跟踪 schema、下载/生成脚本和小型 fixture，不默认跟踪大型数据集、模型权重和运行缓存。

## Multi-module / Monorepo

建议增加：

```text
modules/<name>/
packages/<name>/
```

每个独立模块可拥有局部 `README.md` 和 `AGENTS.md`，但根级文件仍负责跨模块规则、共享术语和全局文档路由。

## 启用规则

启用 profile 时：

1. 只创建实际需要的目录；
2. 在根 `README.md` 和 `docs/README.md` 登记职责；
3. 更新 `tools/check_project_layout.py` 的项目必需路径；
4. 明确哪些生成物进入 Git，哪些只保留再现脚本；
5. 不创建与既有目录职责重叠的第二套 owner。
