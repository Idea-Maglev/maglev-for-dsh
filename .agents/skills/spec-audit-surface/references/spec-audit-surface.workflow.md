---
name: spec-audit-surface
description: 在实施前对 requirements 与 spec cluster 做统一输入质量审计
output_folder: .agents/skills/spec-audit-surface
---

# Spec Audit Surface Workflow

**Goal**: 在进入实施或综合验证前，先把 requirements 与 spec cluster 的输入质量审清。

## 流程 (Process)

1. 检查输入结构
2. 审计 requirements
3. 审计 spec cluster
4. 汇总 findings

## 进入条件 (Entry Conditions)

- 当前已经有 requirements 或 spec cluster 可审
- 需要在实施前先确认输入层质量

## 退出条件 (Exit Conditions)

1. 已输出统一 findings
2. 已明确下一步是继续、补齐还是转交

## 最小产物 (Minimum Deliverables)

- 输入结构结果
- requirements 审计结果
- spec cluster 审计结果
- findings 汇总
