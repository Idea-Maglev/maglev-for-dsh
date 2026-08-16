---
name: step-04-template-authoring
description: 将通用设计落成 Maglev Squad Kit 模板资产
next_step: references/step-05-validation-handoff.md
---

# Step 4: Template Authoring

## 目标

把通用设计与 Maglev Adapter Contract 落实到仓库可校验的 Squad Kit 文件，而不是只保存在会话里。

## 文件面

新增或修改：

```text
packages/maglev-multica-kit/assets/squad-templates/<template-id>/
├── manifest.yaml
├── squad.json
├── 说明.md
├── agents/
│   └── <role>.json
└── skills/
    └── multica-maglev-bridge/
        └── SKILL.md
```

同时检查：

- `packages/maglev-multica-kit/assets/squad-templates/catalog.yaml`
- `packages/maglev-multica-kit/test/kit.test.js`
- `packages/maglev-multica-kit/README.md`
- `docs/multica/10_getting_started/squad_kit_configuration.md`
- 若新增 active spec，则同步 `specs/20_evolution/active/INDEX.md` 与 `README.md`。
- 如技能本身发生变化，则更新 `.agents/private-catalog.yaml` 并重新生成 `.claude/skills/` 适配层。

## 写作规则

- `manifest.yaml` 是角色集合和模板元数据的机器入口。
- `squad.json` 写小队级协作协议，不写实现细节。
- Agent JSON 写角色准入、输入、执行、输出、阻塞、禁止事项和协同边界。
- Bridge Skill 写运行时入口、仓库能力关联、fallback 边界和 Handoff。
- `说明.md` 面向使用者，回答“这是什么、何时用、何时不用、第一步做什么”。
- 测试必须断言协议关键短语，而不是只校验文件存在。
- 每个模板都应输出或能推导 `squad_quality`，不能把 L2 静态验证写成 L3 Runtime Proof。

## 命名与身份

- 展示名称可以 humanize `project_slug`，避免 `Maglev Maglev ...`。
- 受管身份必须依赖 description marker（如 `project:<project_slug>`）与 lock 文件。
- 文档必须说明名称更新可能是预期 drift。

## 输出

- 模板文件清单。
- 需要新增的测试断言。
- 文档更新点。
- 与已有模板的复用/差异说明。
