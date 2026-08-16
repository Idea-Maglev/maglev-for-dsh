---
description: maglev-reverse-spec Step 5 - Spec Handoff to Standard Draft Skill
---

# Step 5: Spec Handoff (规格交接)

## 目标
将前序步骤获取的事实 (Facts) 转化为标准输入格式，并调用 spec pipeline 的 draft 内部模块生成符合 Maglev v2.0 标准的 reality 规格。

## 强约束
- 本步骤一次只能处理一个 `module_slug`
- 本步骤必须先读取 Reality Profile；`module_slug` 不得直接成为 Reality 目录名
- 如果当前上下文中仍混有多个模块，必须先回到 `step-02b-module-partition.md` 做切分，不允许继续落盘

## 1. 整理 Facts
你需要将之前步骤收集到的、且仅属于当前 `module_slug` 的 Entry Context、Evidence Log、Flow Trace 和 Unknowns 整理为 `input_facts.md`。

**Path**: `.maglev/temp/input_facts.md`

**Content Template**:
```markdown
# Current Reality Facts

## User Intent & Hypotheses
Capture current reality for: {Selection Name}
{Content from intent_context.md/Hypotheses}

## Module Identity
- module_name: {Module Name}
- module_slug: {module_slug}
- primary_entry: {Primary Entry}
- boundary_reason: {Why this is a standalone reality unit}

## Evidence Log
- [FACT] ...
- [INFERENCE] ...
- [UNKNOWN] ...

## Unresolved Quests (Action Items)
{Content from intent_context.md/Quests}

## Frontend Facts
{Summary of content from Step 2 Page Analysis}

## Backend Facts
{Summary of content from Step 3 Stack Trace}

## Data Structure Facts
{Summary of DTO / Entity / Schema / ViewModel / Event Payload / Cache Object}

## Router/Structure
{Summary of Router Analysis}
```

## 2. 准备 Context
生成 `ingest_context.json` 以模拟 Ingest 技能的产出。

**Path**: `.maglev/temp/ingest_context.json`

```json
{
  "meta": {
    "intent": "Capture current reality for {Selection}",
    "slug": "{module_slug}",
    "type": "reality-capture"
  },
  "project": {
    "hasUI": {HasUI_Boolean}
  }
}
```
> **注意**: `hasUI` 字段至关重要，它将触发 shared draft 模块的 "Backend Bias Fix" 逻辑。

## 3. 调用 Draft 内部模块
调用共享 internal draft 模块 `../../_internal/spec-pipeline/draft/step-02-polymorphic-design.md`。

> "现在，请作为架构师，基于上述 Facts 生成 Unified Draft。
>
> **Critical Instruction for Reality Spec**:
> 本轮只允许分析一个 `module_slug`；写回前必须映射到 Profile 的主域和槽位。
> 如果发现当前 facts 同时覆盖多个模块，必须先停止生成并回到 `Module Partition`。
>
> 由于现状事实细节极多，为了避免丢分，**必须**使用 Smart Chunking，并保留事实 / 推断 / 未知项的边界，将设计拆分为：
> - `02_design_frontend.md` (详细记录组件/交互)
> - `02_design_backend.md` (详细记录接口/模型)
> - `02_design_core.md` (仅包含架构图和数据库ER图)"

## 4. 完成
Draft 完成后，进入后续验证与归档流程。
