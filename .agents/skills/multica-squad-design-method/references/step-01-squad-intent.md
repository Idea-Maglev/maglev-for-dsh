---
name: step-01-squad-intent
description: 固定小队目标、受众、边界和成功信号
next_step: references/step-02-role-topology.md
---

# Step 1: Squad Intent

## 目标

确认这支 Multica 小队为什么存在、为谁服务、接收什么输入，以及明确不承担什么。

## 动作

1. 命名小队，让技术和非技术读者都能理解用途。
2. 固定目标受众：
   - 请求发起者。
   - 小队成员的监督者或负责人。
   - 需要消费 Handoff 的下游角色。
3. 判断小队类型：
   - 完整交付小队。
   - 诊断/接入小队。
   - 审查/验证小队。
   - 运营/维护小队。
   - 决策/研究小队。
4. 明确输入边界：
   - 输入来自评论、工单、文档、仓库、外部系统或人工描述。
   - 哪些输入缺失时必须阻塞。
5. 写出 In Scope / Out of Scope。
6. 写出成功信号：
   - 能确定下一责任角色。
   - 能产出终态 Handoff。
   - 能解释阻塞原因。
   - 能被 Adapter 转成可验证资产。

## 输出

```yaml
squad_intent:
  display_name:
  squad_type:
  target_users:
    - ...
  inputs:
    - ...
  in_scope:
    - ...
  out_of_scope:
    - ...
  success_signals:
    - ...
```
