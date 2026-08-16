---
name: requirement-convergence
description: 需求收敛器。在方案设计前完成入口分流、需求定义、Ready Gate 与最小交接，避免模糊任务直接滑入方案设计。
metadata:
  formal_action_name: 需求收敛
  top_level_capability: 需求收敛
  system_layer: Core Flow Layer
  lifecycle_chain: main_flow
  runtime_name_status: canonical_name_active
  distribution_scope: user_visible
  author: feiyu.gao
  last_updated: 2026-03-30
---

# Requirement Convergence

## 概览 (Overview)

这是一个前段收敛技能。

它负责：

- 把入口任务先收窄成可处理对象
- 固定本轮必须满足什么与明确不做什么
- 给出成功信号与关键未知
- 执行 Ready Gate，判断是否能进入 `方案设计`
- 在最小交接不足以支撑下游消费时，在本技能内补齐稳定需求产物输出
- 在通过后向下游输出最小必要交接

它不负责：

- 直接生成完整方案
- 把前段稳定需求产物输出再次外包给独立 PRD skill
- 直接进入编码实施
- 用长篇访谈替代结构判断

它的交付结果至少应包含：

- 本轮核心对象
- `In Scope`
- `Out of Scope`
- 成功信号
- 关键未知
- `Ready Gate` 结论
- 明确的下游交接目标
- 必要时的 `输出模式` 判断

## 何时使用 (When to use)

- 任务入口还比较模糊时
- 知道“要做点什么”，但边界还不稳时
- 不希望问题直接滑进 `方案设计（spec-designer）` 时
- 需要先判断是进入方案设计，还是先在本技能内补齐稳定需求产物时
- 需要明确判断“现在能不能进入方案设计”时
- 需要判断当前是否必须先沉淀一份稳定需求文档，才能避免后续漂移时

## 交互模式 (Interaction)

- 行动前阅读完整步骤文件。
- 严格按前段收束顺序执行，不跳步。
- 以结构化收敛为主，不扩成大而全访谈器。
- 一旦 Ready Gate 通过，立即交接给下游对象。
- 如果当前最小 handoff 不足以支撑下游消费，应在本技能内补齐稳定需求产物，再决定是否结束前段或进入方案设计。
- 若未通过 Ready Gate，优先给出最小补齐项，而不是要求用户重讲一遍。
- 正式来源、范围或 AC provenance 落笔前，先消费 `index-librarian` 导航收据；收据缺失、过期或为 `insufficient` 时不得静默继续。

## 判定纪律 (Decision Discipline)

- 优先收边界，不优先收细节。
- 优先收“这次不做什么”，避免范围自然膨胀。
- 关键未知只保留会影响下游设计的未知，不收泛化疑问。
- 一轮收敛只输出一个主去向，不同时交给多个下游对象。
- 若最小 handoff 无法避免需求漂移或无法满足下游消费强度，应在 `需求收敛` 内部完成稳定需求产物输出，而不是再路由到独立 PRD skill。

## 必需的参考资料 (References)

- 工作流入口: `references/requirement-convergence.workflow.md`
- `references/step-01-triage-entry.md`
- `references/step-02-define-requirements.md`
- `references/step-03-ready-gate.md`
- `references/step-04-handoff.md`
- `references/prd-output-contract.md`

## 依赖与集成 (Integrations)

- `现状同步（reality-sync）`
- `方案设计（spec-designer）`
- `entry-router`
- `skill-squadron`

## 示例

User: "我想做 skill 升级，但我现在其实也说不清到底是先收结构还是先动手。"

AI: "收到。我会先做需求收敛，固定本轮边界、非目标和成功信号，再判断是否已经具备进入方案设计的条件。"
