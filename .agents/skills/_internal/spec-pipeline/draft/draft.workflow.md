---
name: spec-draft
description: spec pipeline 共享内部模块：读取 Context 并生成 Unified Draft。
input_context: '{project-root}/.maglev/temp/ingest_context.json'
output_draft: '{project-root}/.maglev/temp/draft_unified.md'
---

# Spec Draft Workflow

**目标**: 消费 Ingest 产物，生产 `draft_unified.md`。

## 步骤序列

### 1. Load & Strategize (加载与策略)
读取 `./step-01-load-context.md`。
*   读取 `ingest_context.json`。
*   决定多态策略 (Strategy: Frontend / Backend / Generic)。

### 2. Generate Draft (生成草稿)
读取 `./step-02-polymorphic-design.md`。
*   读取 `./unified-draft-template.md`。
*   根据策略填充 00-03 章节。
*   将结果写入 `draft_unified.md`。
