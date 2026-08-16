---
name: 'wrapper-02-draft'
description: '调用 spec pipeline 的 draft 内部模块'
sub_workflow: '../../_internal/spec-pipeline/draft/draft.workflow.md'
nextStepFile: './wrapper-03-crystallize.md'
draft_file: '{project-root}/.maglev/temp/draft_unified.md'
layout_api_gate: './layout-api-binding-gate.md'
---

# Phase 2: Draft (起草)

## 指令

1.  **加载 draft 模块**:
    读取并执行 `{sub_workflow}` 中的所有步骤。
    *   请完整执行 `load-context` 和 `polymorphic-design`。

2.  **Layout-to-API Binding Gate**:
    读取 `{layout_api_gate}` 并执行其中的触发判断。
    *   如果项目同时包含 UI 和后端/API 依赖，确认 `{draft_file}` 中包含 `<!-- FILE: 02_design_fe_be_contract.md -->`。
    *   如果缺失，先在 `{draft_file}` 中补齐 `02_design_fe_be_contract.md`，再进入人工审查。
    *   如果补齐时发现 FE 方案、BE 方案或字段/API 草案本身不足，先回修对应 02 设计内容；不要把缺口推迟到 `03_plan.md` 或验证阶段处理。
    *   如果项目不触发 gate，在设计方向摘要中说明跳过原因。

3.  **Human-in-the-Loop (人工审查)**:
    在 Draft 生成后，向用户展示文件路径：`{draft_file}`。

    **展示设计方向摘要**:
    从 draft 中提取关键决策，向用户展示：

    **技术设计决策**（从 02 技术蓝图的设计决策表提取）：
    - 每个决策的选择理由（一句话）

    **前后端契约决策**（如果生成 `02_design_fe_be_contract.md`）：
    - 页面锚点覆盖范围
    - 首屏与关键交互请求顺序
    - 字段计算责任与空错态边界

    **交互设计决策**（如果存在交互设计部分）：
    - UI 架构选择
    - 关键状态流转概要
    - 响应式策略概要

    **询问用户**:
    "以上设计方向是否正确？（含技术设计和交互设计）
    您想：
    1. **直接因化 (Proceed)**: 我将为您拆分文件。
    2. **手动修改 (Edit)**: 您修改 Draft 后，我再拆分。
    3. **重新生成 (Retry)**: 重新运行 Draft 步骤。"

    **等待明确确认**：只接受明确选择（1/2/3 或对应关键词），不将模糊回复解读为确认。

    **记录审批**：
    ```yaml
    approval_log:
      - checkpoint: design_draft
        result: proceed | edit | retry
        artifacts_reviewed:
          - 02_design.md
          - 02_design_interaction.md  # 仅含 UI 项目
          - 02_design_fe_be_contract.md # 仅 UI + API 项目
        summary: "{用户确认或修改的内容摘要}"
        timestamp: "{ISO 8601}"
    ```

4.  **前进**:
    如果用户选择 1 或 2，加载 `{nextStepFile}` 进入 Phase 3。
