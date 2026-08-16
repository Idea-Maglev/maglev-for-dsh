---
name: assess-context
description: 判断当前上下文成熟度，避免过早进入错误下游
next_step: references/step-03-select-route.md
---

# Step 2: Assess Context

## 目标

判断当前上下文是否成熟到足以进入后续对象。

## 动作

1. 判断当前是否缺少项目现状：
   - 缺少时，优先考虑 `现状同步（reality-sync）`
2. 判断当前是否缺少稳定需求边界：
   - 缺少时，优先考虑 `requirement-convergence`
3. 判断当前是否已经有稳定输入可进入：
   - `方案设计（spec-designer）`
   - `上下文实施（context-implementer）`
   - `代码执行插槽（code-execution-slot）`
   - `综合验证（integrated-validator）`
4. 避免因为用户表达模糊，就由入口对象自己继续长篇访谈。

## 判定规则

- 缺少项目现状时，优先补现状，不优先猜需求。
- 缺少稳定边界时，优先做前段收敛，不优先做方案。
- 已具备明确输入时，应直接前推，不回到更前面的泛化整理。

## 输出格式

- `context_maturity`
- `primary_gap`
- `narrowed_route`

## 输出

- 一份上下文成熟度判断
- 一条被收窄的路径候选
