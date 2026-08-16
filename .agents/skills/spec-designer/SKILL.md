---
name: spec-designer
description: 方案设计器。在需求边界稳定后，通过受控对话与结构化流程形成可执行的技术方案。
metadata:
  formal_action_name: 方案设计
  top_level_capability: 方案设计
  system_layer: Core Flow Layer
  lifecycle_chain: main_flow
  runtime_name_status: canonical_name_active
  distribution_scope: user_visible
  author: feiyu.gao
  last_updated: 2026-03-30
  version: "3.0 (Plain Speak Edition)"
---

# 方案设计 (Spec Designer)

## 概览 (Overview)

这是一个主流程中的方案设计技能。

当前说明：

- 结构动作名：`方案设计`
- 运行面名称：`spec-designer`
- 兼容 workflow 入口：`/create-spec`

它负责：

- 读取已经过需求收敛的输入
- 通过必要追问补齐关键设计前提
- 形成可执行、可验证的方案草稿
- 组织输出到当前 spec 目录

它不负责：

- 吞并需求收敛
- 直接进入实现
- 充当质量层输入审计

它的交付结果至少应包含：

- 方案范围与设计边界
- 核心结构、流程或接口设计
- UI + API 项目的页面锚点、请求编排与字段绑定契约
- 关键约束与待验证点
- 已落盘的 spec 输出

## 实施交接

- 代码交付物交给 `code-execution-slot`，由 Slot 解析 enabled 扩展或使用 agent-native fallback。
- 纯文档、配置、分析和 Maglev 治理交付物交给 `context-implementer`。
- 混合交付物先完成代码执行，再处理非代码部分，最终统一进入 `integrated-validator`。

## 何时使用 (When to use)

- 需求边界已经稳定，需要进入方案设计时
- 已有 requirements、上下文或会议输入，需要收成可执行方案时
- 希望在进入实施前先把设计依据固定下来时

## 交互模式 (Interaction)

- 行动前先确认输入是否达到可设计状态
- 必要时追问关键缺口，但不重新承担前段收敛职责
- 先产出设计草稿，再完成物理落盘
- **背景纪律**：本 skill 执行期间持续遵循 `maglev-discipline` 红线（闭环验证 / 事实驱动 / 穷尽方法），每个 step 起始前先做 `[MAGLEV-DIAGNOSIS]` 自检

## 判定纪律 (Decision Discipline)

- 先确认“设计什么”，再确认“如何落盘”
- 保持方案设计和需求收敛分离
- 只补设计所需前提，不无限扩展到前段问题定义
- 输出必须能被后续实施和验证直接消费
- 不把兼容入口 `/create-spec` 误解为当前运行名仍是旧值

## 必需的参考资料

- 工作流: `references/coordinator.workflow.md`
- `references/step-00-socratic-interview.md`
- `references/step-00-integrity-check.md`
- `references/wrapper-01-ingest.md`
- `references/wrapper-01b-validate.md`
- `references/wrapper-02-draft.md`
- `references/layout-api-binding-gate.md`
- `references/wrapper-03-crystallize.md`
- `references/step-04-verify-output.md`
