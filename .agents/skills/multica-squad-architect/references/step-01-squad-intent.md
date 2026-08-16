---
name: step-01-squad-intent
description: 消费通用小队设计包并确认 Maglev 落地目标
next_step: references/step-02-role-topology.md
---

# Step 1: Consume Generic Design

## 目标

确认通用 `multica-squad-design-method` 已经给出小队意图、角色拓扑、协同契约和目标质量等级，再决定是否进入 Maglev Adapter 落地。

## 动作

1. 读取或整理通用设计包：
   - `squad_intent`
   - 角色拓扑
   - 协同契约
   - Adapter Contract 预期
   - 目标 `squad_quality`
2. 判断是否达到 Maglev 落地前置：
   - 至少达到 L1 协同契约完整。
   - 明确是否需要 L2 模板验证或 L3 Runtime Proof。
   - 明确是否支持未初始化仓库。
3. 明确 Maglev 运行边界：
   - 已完成 Maglev 初始化并可加载 `entry-router`。
   - 未初始化，只能走 Bridge 自包含准备模式。
   - 混合状态，需要双路径入口。
4. 若通用设计未达到 L1，停止 Adapter 落地，返回 `multica-squad-design-method`。

## 输出

```yaml
maglev_adapter_intake:
  generic_method: multica-squad-design-method
  display_name:
  template_id:
  target_quality: L1 | L2 | L3
  repository_state: initialized | uninitialized | mixed
  generic_design_ready: true | false
  missing_inputs:
    - ...
```
