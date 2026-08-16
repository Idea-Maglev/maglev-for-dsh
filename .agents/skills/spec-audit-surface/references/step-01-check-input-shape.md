---
name: check-input-shape
description: 检查当前输入是否具备进入审计面的最低结构
next_step: references/step-02-audit-requirements.md
---

# Step 1: Check Input Shape

## 目标

先判断当前输入够不够支撑后续 requirements / spec 审计。

## 动作

1. 检查是否存在 requirements 文档或等价输入。
2. 检查是否存在 spec cluster 或等价设计输入。
3. 区分：
   - 缺输入
   - 输入存在但结构不完整
   - 输入具备审计条件

## 输出格式

- `input_shape_result`
- `available_inputs`
- `blocking_gaps`
