---
name: ready-gate
description: 判断是否已具备进入方案设计的最低条件
next_step: references/step-04-handoff.md
---

# Step 3: Ready Gate

## 目标

明确判断当前是否已经足够稳定，可以进入明确的唯一主去向。

## 动作

1. 判断范围是否足够稳定。
2. 判断是否仍有会显著影响后续设计的关键未知。
3. 判断当前成功信号是否已足够清楚。
4. 判断当前唯一主去向更适合：
   - `方案设计（spec-designer）`
   - `requirement-convergence`
   - 其中选择 `requirement-convergence` 时，必须说明是为了在本技能内补齐稳定需求产物，以抑制漂移或提升下游可消费性，而不是笼统因为“需要 PRD”
5. 输出唯一结论：
   - `ready`
   - `not_ready`
6. 若 `not_ready`，明确指出最小补齐项，而不是笼统说“信息不够”。

## Ready Gate 通过标准

至少同时满足：

1. 本轮核心对象明确
2. `In Scope` / `Out of Scope` 已能区分
3. 成功信号已可用于后续设计判断
4. 没有会直接改变设计方向的关键未知悬空
5. 已能判断唯一主去向

## 输出格式

必须输出：

- `gate_result: ready | not_ready`
- `next_object_candidate`
- `reason`
- `consumption_rationale`
- `prd_mode_required: true | false`
- `missing_items`（若无则写空）

## 输出

- 一份 Ready Gate 结果
- 一组最小补齐项
