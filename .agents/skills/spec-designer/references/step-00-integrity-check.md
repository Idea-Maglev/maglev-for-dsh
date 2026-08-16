---
description: spec-designer Step 00 - Integrity Check
---

# Step 00: Integrity Check (启动自检)

## 目标
确保 Spec 生成所需的运行环境和内部 pipeline 模块均已就绪。

## 自检列表

### 1. 环境准备
*   **Action**: 检查工作区根目录下的 `.maglev/temp` 目录。
*   **Logic**: 如果不存在，自动创建它。

### 2. 内部模块检查
检查以下关键内部模块是否存在：
1.  `ingest` 内部模块 (用于信息摄入)
    *   Path: `./pipeline/ingest/ingest.workflow.md`
2.  `draft` 共享内部模块 (用于生成 Spec Draft)
    *   Path: `../../_internal/spec-pipeline/draft/step-02-polymorphic-design.md`
3.  `crystallize` 共享内部模块 (用于拆分与归档)
    *   Path: `../../_internal/spec-pipeline/crystallize/crystallize.workflow.md`

### 3. 状态重置
*   **Action**: 清理 `.maglev/temp` 目录下的旧数据 (`draft_unified.md`, `input_facts.md`, `ingest_context.json`)。
*   **Reason**: 防止上一次任务的残留数据污染本次 Spec 生成。

## Checkpoint
如果上述检查全部通过，输出：
```
[CHECKPOINT - System Ready]
✅ 环境完整性检查通过。
- Temp Dir: OK
- Dependencies: OK
- Clean Slate: OK
```
否则，报错并中止。
