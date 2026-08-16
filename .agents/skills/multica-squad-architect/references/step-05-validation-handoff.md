---
name: step-05-validation-handoff
description: 运行验证并输出可交接结果
next_step: null
---

# Step 5: Validation Handoff

## 目标

用证据证明小队模板可发现、可校验、可实例化、可升级，并明确 `squad_quality` 与是否需要同步远端 Multica Workspace。

## 必跑验证

```bash
node packages/maglev-multica-kit/bin/maglev-multica.js template validate <template-id>
node packages/maglev-multica-kit/bin/maglev-multica.js template validate maglev-complete
node --test packages/maglev-multica-kit/test/kit.test.js
git diff --check
```

如果修改了对外文档或 skill：

```bash
./scripts/maglev-python .agents/skills/artifact-purity-keeper/scripts/scanner.py <paths>
```

如果修改了 `10_reality`：

```bash
python3 .agents/skills/crystallization/references/scripts/crystallization_check.py <reality-module>
```

如果已有本地开发态 Multica 配置：

```bash
MULTICA_WORKSPACE_ID=<workspace-id> \
node packages/maglev-multica-kit/bin/maglev-multica.js plan \
  --config .maglev/local/multica/squad-kit.dev.json
```

## 质量声明

验证后必须输出：

```yaml
squad_quality:
  design_level: L1 | L2 | L3
  adapter: maglev
  collaboration_contract: pass | fail
  adapter_contract: pass | fail
  template_validation: pass | fail
  runtime_proof: pass | pending | not_run
  allowed_claim:
    - draft
    - collaboration_designed
    - template_verified
    - runtime_verified
```

`runtime_proof` 不是 `pass` 时，不得包含 `runtime_verified`。

## 验收问题

交付前必须能直接回答：

- 未初始化仓库没有 `entry-router` 时，小队第一步做什么？
- 哪个角色可以决定下一 Agent？
- 成员 Agent 能不能自己 mention 其他 Agent？
- 自动接力失败时先查什么？
- Handoff 必须包含哪些字段？
- 写治理资产前需要什么批准和证据？
- 什么时候才算从准备模式进入仓库 Maglev 能力链路？
- 既有小队升级时名称更新是不是异常 drift？

## 输出

```yaml
validation_handoff:
  template_id:
  squad_quality:
    design_level:
    runtime_proof:
    allowed_claim:
      - ...
  changed_files:
  commands:
    - command:
      result:
  remote_plan:
    required: true | false
    summary:
  remaining_risks:
    - ...
```
