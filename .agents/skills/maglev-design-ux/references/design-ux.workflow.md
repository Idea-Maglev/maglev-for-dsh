---
name: design-ux
description: 体验设计工作流 (Empathy -> Journey -> Visual -> Handoff)
input_spec: '{project-root}/specs/20_evolution/active/{slug}/01_requirements.md'
output_design: '{project-root}/specs/20_evolution/active/{slug}/02_ui_design.md'
---

# Design UX Workflow

**目标**: 将需求转化为具体的体验设计文档。

## 步骤序列

### 1. Empathy (同理心)
读取 `references/step-01-empathy.md`。
*   分析 `01_requirements.md`。
*   定义 Persona (核心用户) 和 Emotional Goal (情感目标)。

### 2. Journey (旅程设计)
读取 `references/step-02-journey.md`。
*   绘制 Mermaid User Journey Map。
*   识别 "Moment of Truth" (关键时刻)。

### 3. Visual (视觉逻辑)
读取 `references/step-03-visual.md`。
*   识别关键 UI 组件。
*   绘制 Mermaid State Diagram (Idle/Loading/Error/Success)。

### 4. Handoff (交付)
读取 `references/step-04-handoff.md`。
*   组装所有内容到 `02_ui_design.md`。
*   邀请用户审阅。
