---
name: report-gaps
description: 汇总缺口并给出最小补齐建议
next_step: null
---

# Step 4: Report Gaps

## 目标

把知识沉淀缺口汇总成清晰可执行的检查结果。

## 动作

1. 列出已完成沉淀项。
2. 列出未完成沉淀项。
3. 对 blocker 级缺口单独标记。
4. 给出最小必要补齐建议。

## 输出规则

- 已完成项和未完成项必须分开列出。
- blocker 级缺口单独标记，避免和普通建议混在一起。
- 建议必须是最小补齐动作，不生成新的大计划。

## 输出格式

- `completed_items`
- `pending_items`
- `blockers`
- `minimum_followups`

## 输出

- 一份知识沉淀检查结果
- 一组最小必要补齐动作
