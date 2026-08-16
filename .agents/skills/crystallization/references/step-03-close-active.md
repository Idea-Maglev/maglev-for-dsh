---
name: close-active
description: 判断当前 active 是结束、继续还是拆分
next_step: references/step-04-backfill-discovery.md
---

# Step 3: Close Active

## 目标

对当前 `20_evolution/active` 状态做明确收口，而不是让 active 长期悬挂。

## 动作

1. 判断当前 active 是否已完成主题目标。
2. 若未完成，判断应继续还是拆分出新主线。
3. 若已完成，明确当前 active 的结束条件已满足。
4. 输出唯一状态：
   - `close`
   - `continue`
   - `split`

## 判定规则

- `close`：当前主线目标已完成，且后续不再以当前 active 为主工作面。
- `continue`：主线未结束，且继续沿当前 active 推进最清楚。
- `split`：当前 active 已承载过多，后续应拆出新的主线或子主题。

## 输出格式

- `active_decision: close | continue | split`
- `reason`
- `follow_up_path`

## 输出

- 一份 active 状态判断
- 一条明确的后续状态建议
