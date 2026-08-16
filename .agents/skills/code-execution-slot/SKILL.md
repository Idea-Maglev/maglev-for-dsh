---
name: code-execution-slot
description: 代码执行插槽。在 Maglev 方案完成且包含代码交付物时，从 `.maglev/extensions.lock` 解析已启用的代码执行扩展，由 Agent 选择能力或使用原生代码执行，并将结果交给综合验证。
metadata:
  formal_action_name: 代码执行插槽
  top_level_capability: 上下文实施
  system_layer: Core Flow Layer
  lifecycle_chain: main_flow
  runtime_name_status: canonical_name_active
  distribution_scope: user_visible
  author: feiyu.gao
  last_updated: 2026-07-13
---

# Code Execution Slot

这是 Maglev 代码交付物的通用执行入口。它只定义插槽协议，不安装扩展，也不绑定具体 provider。

## 何时使用

- 需求与方案已经稳定，交付物包含产品代码、修复或重构。
- `delivery_type` 为 `code` 或 `mixed`，或实施清单明确包含代码文件。
- 用户明确要求进入代码执行阶段。

纯文档、配置、分析和 Maglev 治理改动继续使用 `context-implementer`。

## 执行流程

1. 运行确定性 resolver：

   ```bash
   ./scripts/maglev-python .agents/skills/code-execution-slot/protocol/scripts/resolve_slot.py \
     --workspace-root . --json
   ```

2. 在选择 provider 或进入 `agent-native` fallback 前，校验实施上下文的 `index-librarian` 导航收据。收据必须未过期，并按状态处理：
   - `queried`: 允许继续，将候选、证据和指纹随上下文包交给 provider。
   - `not_needed`: 允许继续，但必须说明为何当前代码执行不依赖额外项目知识。
   - `insufficient`: 不得进入代码执行；必须先进入受控升级链。
   - `escalated`: 仅允许在升级链收窄后的来源范围内继续选择 provider 或 `agent-native` fallback，不得恢复成无边界代码搜索。
   - `exhausted`: 不得进入代码执行；必须显式保留“实施知识不足”，并先补一个区分知识域的线索。
   - 如需显式记录升级链，使用 `task_navigate.py` 的 `--escalation-step`、`--escalation-attempt`、`--scope-hint`、`--known-source-hint`、`--escalation-note` 与 `--exhausted` 参数。

3. 若存在候选，按以下顺序选择：
   - 用户显式指定的扩展；
   - `selection_hint` 与当前任务的匹配程度；
   - spec 约束、任务上下文和候选能力边界；
   - `priority` 仅作为同等匹配时的排序提示，不替代语义判断。
4. 选择候选后，通过当前 Agent 平台的 skill 机制加载其 `entry_skill`。不得直接导入、复制或改写 provider 资产。
5. 没有候选或没有候选适合当前任务时，使用 `agent-native` fallback，在现有 spec、测试和仓库纪律约束下直接实施代码。
6. 收集变更 diff、测试结果、review 发现和剩余风险，交给 `integrated-validator`。

## 选择纪律

- 只使用 resolver 返回的 enabled 候选；不要从 registry 搜索结果推断已启用状态。
- external integration 必须保持 `detected: true`，否则不能选择。
- 不因候选存在就自动选择；必须给出与任务匹配的判断依据。
- 多个候选同样适用且会改变执行方法时，向用户说明差异后再选择。
- 外部 skill 不得绕过 `entry-router`、需求收敛或 `spec-designer` 自动触发。

## 输出契约

执行结果至少包含：

- Slot 解析结果与选择依据；
- 实际使用的 `entry_skill`，或 `agent-native` fallback 原因；
- 代码变更范围；
- 测试与 review 证据；
- 可交给 `integrated-validator` 的验证包。
