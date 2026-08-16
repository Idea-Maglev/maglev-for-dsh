---
name: step-04-adapter-contract
description: 定义目标平台如何承接通用小队设计
next_step: references/step-05-quality-gate.md
---

# Step 4: Adapter Contract

## 目标

把通用小队设计交给具体平台或项目落地，并防止通用方法假设不存在的运行环境。

## 动作

1. 选择 Adapter：
   - `maglev`：落到 Maglev Squad Kit。
   - `custom`：落到其他项目或平台。
   - `none`：只保留设计，不承诺模板可运行。
2. 填写 Adapter Contract：
   - 文件面：模板、说明、角色配置、技能或提示词存放位置。
   - 命令面：校验、测试、同步、发布命令。
   - 身份面：对象归属如何判断，是否依赖 marker、lock 或远端 ID。
   - 权限面：谁可读、谁可写、谁可批准。
   - 写入门禁：外部状态变更前需要什么批准和证据。
   - 验证面：如何证明 L2 与 L3。
3. 检查 Adapter 不得偷换声明：
   - 不能把 L1 设计称为 L2 模板验证。
   - 不能把静态测试称为 L3 Runtime Proof。
   - 不能把未授权写入包装成自动行为。

## 输出

```yaml
adapter_contract:
  adapter: maglev | custom | none
  file_surface:
    - ...
  command_surface:
    - ...
  identity_surface:
    - ...
  permission_surface:
    - ...
  write_gate:
    required: true | false
    evidence:
      - ...
  validation_surface:
    l2:
      - ...
    l3:
      - ...
```
