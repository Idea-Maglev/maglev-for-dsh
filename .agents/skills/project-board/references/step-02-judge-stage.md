---
name: step-02-judge-stage
description: 基于交叉证据，对每个活跃需求进行全段评估
next_step: references/step-03-map-roles.md
---

# Step 2: Judge Stage (流程阶段判断)

## 目标

对每个 ActiveItem 进行**全段评估**，确定 5 个阶段各自的完成状态，支持叠加态。

## 前置依赖

- 读取 `references/stage-evidence-rules.md` 获取完整判定规则

## 动作

对每个 type=spec 的 ActiveItem：

### 1. 文件证据检查

检查以下文件是否存在：
- `00_intent.md`（意图文档）
- `01_requirements.md`（需求文档）
- `02_design.md`（设计文档）
- `03_plan.md`（计划文档）

### 2. 内容质量检查

对存在的文件，检查内容是否充实（非空壳）：
- 文件有效内容 > 20 行（排除空行和纯结构行）
- 存在关键标记词（见 `stage-evidence-rules.md` 中的标记词表）

### 3. 代码证据检查（可缓存）

先检查 `.maglev/temp/board_cache.json` 中该条目是否有有效缓存。

若无缓存或缓存过期（文件证据变化）：

```bash
git --no-pager log --oneline --since="90 days ago" -- "**/{spec_name}*" ":!specs/20_evolution/active/*/status.md" ":!specs/20_evolution/board.md" | head -5
```

- 返回 ≥1 条提交 → `code_evidence = true`
- 返回 0 条 → `code_evidence = false`
- 排除看板产出文件（`status.md`、`board.md`），避免自证预言

### 4. 测试证据检查

搜索与 spec 名称相关的测试文件：

```bash
find tests/ -name "*{spec_name}*" -type f 2>/dev/null | head -3
```

- 找到文件 → `test_evidence = true`

### 5. 全段评估

**不是"命中即停"，而是逐阶段独立评估。** 按 `stage-evidence-rules.md` 的证据要求，对每个阶段判定：

| 状态 | 判定条件 |
|------|---------|
| `completed` | 该阶段的全部完成条件均满足 |
| `in_progress` | 该阶段的进行中条件满足，但完成条件未全满足 |
| `not_started` | 该阶段的进行中条件也未满足 |

**当前阶段** = 最高的 `in_progress` 阶段。若无 `in_progress`，取最高 `completed` 阶段。

### 6. 置信度标注

| 场景 | confidence |
|------|------------|
| 当前阶段的所有证据均满足 | `confirmed` |
| 文件存在但内容质量未验证 | `inferred` |
| 相邻阶段证据冲突或多阶段同时 in_progress | `uncertain` |

### 7. 单条目容错

若某个 ActiveItem 在判定过程中遇到异常（文件编码错误、git 命令失败等）：
- 标记为 `stage: unknown, confidence: error`
- 在 `evidence` 中记录错误原因
- **继续处理其余条目**，不终止整个流程

对 type=issue 的 ActiveItem：
- 直接标记为进度 `⏳⬜⬜⬜⬜`（需求收敛 in_progress，其余 not_started）
- confidence = `confirmed`

## 输出

每个 ActiveItem 附加 StageResult：
- `current_stage`: 当前主阶段（5 个阶段之一）
- `progress`: 5 元素数组，每个为 `completed` / `in_progress` / `not_started`
- `progress_display`: emoji 进度条（如 `✅→✅→⏳→⬜→⬜`）
- `confidence`: confirmed / inferred / uncertain
- `evidence`: 已收集的证据列表（使用人话别名）
- `missing`: 缺失的证据列表
