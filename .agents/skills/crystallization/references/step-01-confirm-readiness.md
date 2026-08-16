---
name: confirm-readiness
description: 判断当前是否已具备进入现实结晶阶段的条件
next_step: references/step-02-judge-writeback.md
---

# Step 1: Confirm Readiness

## 目标

确认当前主题的变化是否已经成立到足以进入现实结晶。

## 动作

1. 检查当前结果是否已通过 `综合验证`。
2. 判断哪些变化已经成立，哪些仍只是过程草稿。
3. 若尚未成立，明确指出阻塞项。
4. 输出唯一判断：
   - `ready_to_crystallize`
   - `not_ready_to_crystallize`

## 通过标准

至少同时满足：

1. 当前主题的关键结果已经成立
2. 主要阻塞已被验证或显式解除
3. 当前已能区分“新事实”与“过程草稿”

## 输出格式

- `crystallization_gate`
- `established_changes`
- `blockers`

## 输出

- 一份结晶条件判断
- 一组 blocker 或已成立结果
