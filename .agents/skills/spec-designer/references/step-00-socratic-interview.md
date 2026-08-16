# Step 0: Socratic Interview (苏格拉底式访谈)

> **Role**: Product Architect (产品架构师)
> **Template**: 使用当前仓库内的深度访谈方式，围绕价值、边界、成功标准和关键假设进行追问。

---

## 目标 (Goal)
在 Spec 生成流程开始前，与用户进行 **2-3 轮深度对话**，挖掘隐性意图和未明假设。

---

## 触发条件 (When to Run)

**必须执行**:
- 用户意图模糊 (e.g., "做个类似 X 的东西")
- 输入信息不完整 (缺少用户画像、成功标准)

**可跳过**:
- 用户明确说 "我已经想清楚了，直接开始"
- 输入已有完整的 PRD 或 Spec 文档

---

## 核心问题 (Dynamic Guidelines)

不是死板的问卷调查，而是像一位经验丰富的架构师那样进行对话。

### 0. 破冰与定性 (Ice Breaking & Typing) 🆕
*   **Check**: 首先确认项目类型："该项目是否包含前端界面？(Does this project have a UI?)"。
*   **Result**:
    *   **Has UI**: 必须进入 "体验 (Experience)" 维度。
    *   **Headless**: 跳过 "体验" 维度，聚焦 API/Security。

### 🌟 动态追问策略 (Adaptive Probing)
*   **Response**: 用户的回答太简单 ("要做个商城")？-> **Challenge**: "具体卖什么？用户是谁？竞品是谁？"
*   **Response**: 用户回答很详细？-> **Skip**: 跳过基础问题，直接确认边缘情况。
*   **Tone**: 专业、好奇、苏格拉底式 (Socratic)。

### 关键维度 (Key Dimensions)
确保你（作为 Agent）获取了以下信息（顺序不限）：

1.  **Value**: "解决了谁的什么痛点？" (Why)
2.  **Boundary**: "不做什麽？" (Non-Goals)
3.  **Success**: "MVP 包含什么？" (Done Definition)
4.  **Experience (If Has UI)**: 🆕
    *   "界面长什么样？" (视觉锚点)
    *   "用户怎么操作？" (交互流)

---

## Checkpoint 格式

```markdown
> **[INTERVIEW CHECKPOINT]**
>
> 在继续之前，我有几个问题想和你确认：
>
> 1. [价值根因问题]
> 2. [边界条件问题]
> 3. [成功标准问题]
>
> 请回答后我再开始 Spec 生成。
> 或者，如果你已经想清楚了，输入 `skip` 直接进入下一阶段。
```

---

## 产出 (Output)

### 上下文交接 (Context Handoff) 🆕
将澄清后的信息写入共享上下文文件，供下游技能复用：

**目标路径**: `{project-root}/.maglev/temp/interview_context.md` (System Temp)

```markdown
---
title: "{Feature Name} - 共享上下文"
created_by: "spec-designer"
last_updated: "{date}"
---

## 用户画像 (Persona)
- **Who**: [从对话中提取]
- **Pain Point**: [从对话中提取]

## 核心问题 (Problem Statement)
- **Why**: [从对话中提取]
- **Non-Goals**: [从对话中提取]

## 成功标准 (Success Criteria)
- **MVP**: [从对话中提取]
- **North Star**: [从对话中提取]

## 假设日志 (Assumptions Log)
| 假设 | 状态 | 来源 |
|------|------|------|
| [记录被挑战或确认的假设] | Confirmed/Challenged | create-spec |
```

> **注意**: 必须写入 `{project-root}/.maglev/temp/interview_context.md` 并使用中文。

---

## 完成条件 (Exit Criteria)

当满足以下条件时，可进入 Phase 1 (Ingest)：
- [ ] 用户角色/Persona 已明确
- [ ] 核心痛点/问题已确认
- [ ] 成功标准已定义 (至少 MVP 范围)
- [ ] 无明显遗漏的关键假设
- [ ] 上下文已写入 `.maglev/temp/interview_context.md` 🆕
