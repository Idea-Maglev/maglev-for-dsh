---
name: requirement-convergence
description: 在方案设计前完成入口分流、需求定义、Ready Gate 与下游交接
output_folder: .agents/skills/requirement-convergence
---

# Requirement Convergence Workflow

**Goal**: 在主流程前段完成结构化收束，避免模糊任务直接滑入方案设计，并在需要时于本技能内补齐稳定需求产物，以减少产物漂移并提升下游可消费性。

## 流程 (Process)

1. 入口分流
2. 需求定义
3. Ready Gate
4. 下游交接

当输出模式为 `prd_document` 时：

- 必须额外读取 `references/prd-output-contract.md`
- 用该契约补齐稳定需求产物输出

## 进入条件 (Entry Conditions)

- 当前请求还没有稳定进入 `方案设计`
- 用户目标存在模糊、混合或范围漂移迹象
- 入口对象已判断需要先做前段收敛

## 退出条件 (Exit Conditions)

满足以下任一条件即可结束本轮：

1. 形成完整的收敛结果，并明确交接到唯一主去向或在本技能内完成稳定需求产物输出
2. 明确给出 `not_ready` 与最小补齐项，停止继续前推

## 最小产物 (Minimum Deliverables)

- 入口类型判断
- 需求定义摘要
- `Ready Gate` 结论
- `输出模式` 判断
- 最小交接说明或最小补齐建议

## 步骤架构

- **Micro-Steps**: 严格遵循 `step-*.md`
- **Isolation**: 内存中只加载当前步骤

## 初始化

1. 阅读 `references/step-01-triage-entry.md`
