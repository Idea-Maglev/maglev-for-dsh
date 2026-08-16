---
name: create-spec-coordinator
description: 方案设计协调工作流，编排追问、摄入、起草、固化与验证。
---

# Specification Design Coordinator Workflow


**目标**: 在需求边界已基本稳定后，通过必要追问与结构化编排完成端到端方案设计。

## 步骤序列

## 步骤序列

### Phase 00: Integrity Check (启动自检)
读取 `references/step-00-integrity-check.md`。
*   检查环境依赖和状态。
*   如果不通过，直接终止。

### Phase 0: Socratic Interview (苏格拉底式访谈) 🆕
读取 `references/step-00-socratic-interview.md`。
*   **强制性**: 除非用户明确说 "我已经想清楚了，直接开始"。
*   负责挖掘用户的隐性意图和未明假设。
*   产出: `clarified_context.md` (关键共识记录)。

### Phase 1: Ingest (摄入)
读取 `references/wrapper-01-ingest.md`。
*   负责规范化摄入当前设计输入。
*   调用内部 ingest 模块生成 Context。

### Phase 1.5: Validate (门禁)
读取 `references/wrapper-01b-validate.md`。
*   调用内部 context guardrail。
*   如果校验失败，流程在此终止。

### Phase 2: Draft (起草)
读取 `references/wrapper-02-draft.md`。
*   调用内部 draft 模块生成 Unified Draft。
*   (Checkpoint): 允许用户在这里暂停并修改 Draft。

### Phase 2.5: Layout-to-API Binding Gate (页面/API 绑定门禁)
读取 `references/layout-api-binding-gate.md`。
*   当项目同时包含 UI 与后端/API 依赖时，检查 Draft 是否包含 `02_design_fe_be_contract.md`。
*   若缺失，先补齐页面锚点、请求编排、逐字段契约和联调验证清单，再进入固化。
*   定位为 02 技术方案阶段的收口门禁：它必须在 03 计划拆分前完成；04 验证阶段只复核，不首次生成。

### Phase 3: Crystallize (固化)
读取 `references/wrapper-03-crystallize.md`。
*   调用内部 crystallize 模块完成拆分和落盘。

### Phase 4: Verify (验证)
读取 `references/step-04-verify-output.md`。
*   验证产出的 Spec 文件和 Context 归档。
*   输出最终报告。
