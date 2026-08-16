---
name: step-01-profile
description: 深度用户侧写
next_step: references/step-02-curriculum.md
---

# Step 1: Deep Profiling (深度侧写)

## 目标
诊断用户的 **Maglev 掌握度**，而非仅仅询问身份。
(Mode: **Deep**)

## ⚠️ 核心法则
*   **Don't Assumption**: 用户声称是"专家"，未必真的懂。
*   **Challenge Them**: 用问题测试理解深度。

## 引导脚本
> **Opening**: "Maglev 上下文已加载。在开始指引前，我想先了解一下你当前对 Maglev 的熟悉程度。"

### 诊断问题 (Diagnostic Questions)
请依次（或随机）询问以下问题中的 1-2 个：

1.  **Q1 (Philosophy)**: "你认为 Maglev 和传统的 Agile 流程 (Jira/Epic) 最大的区别是什么？"
2.  **Q2 (Mechanism)**: "如果 Spec 和 Code 冲突了，Maglev 协议规定谁是 Source of Truth？" (Answer: Spec)
3.  **Q3 (Workflow)**: "当你想修改一个功能时，第一步应该做什么？" (Answer: Find/Create Issue or Update Spec, NOT touch code)

## 动作序列
1.  **Ask**: 抛出诊断问题。
2.  **Listen**: 等待用户回答。
3.  **Judge**:
    *   *回答准确*: 标记为 **[Veteran]** (老手)。跳过基础概念。
    *   *回答模糊*: 标记为 **[Apprentice]** (新手)。推荐基础课程。
    *   *回答错误*: 标记为 **[Risk]** (高危)。必须强制进行 "Safety Briefing"。
4.  **Confirm**: "当前建议路径为 [Veteran/Apprentice] 对应课程。"
