---
name: entry-router
description: 会话入口路由器。在任务开始时识别请求类型、判断下游路径，并把会话交接给最合适的 Maglev 能力。
metadata:
  formal_action_name: 入口路由
  top_level_capability: 需求收敛
  system_layer: Entry / Routing Layer
  lifecycle_chain: main_flow
  runtime_name_status: canonical_name_active
  distribution_scope: user_visible
  author: feiyu.gao
  last_updated: 2026-03-30
---

# Entry Router

## 概览 (Overview)

这是一个入口路由技能。

如果用传统项目流程来理解，它更像：

- 一个“研发流程前台”
- 一个“项目分诊台”
- 一个“当前该找谁处理”的判断入口

它不是业务 owner，也不是方案设计师，更不是实现者。
它的价值在于先判断当前问题属于：

- 先看现状
- 先收需求
- 先做方案
- 直接实施
- 还是进入验证

它只负责三件事：

- 识别当前请求是什么
- 判断当前最合适的下游路径
- 将会话交接给后续专长对象

它的路由规则不是一次定死的。

- 当 Maglev 后续新增稳定 skill 或 workflow 时
- 需要回补这里的下游路径与 handoff 规则

它不负责吞并：

- 主流程能力本体
- 质量层能力
- 地图、Reality、方案设计、实施、验证等专长对象

它的交付结果至少应包含：

- 当前任务类型判断
- 唯一路由结果
- 路由理由
- 最小必要交接说明

## 何时使用 (When to use)

- 用户刚进入会话，但请求还比较模糊时
- 需要先判断应该走 `现状同步`、`需求收敛`、`方案设计`、`上下文实施` 还是 `综合验证` 时
- 需要一个统一入口，但不希望入口对象继续吞并下游专长时

## 给人的理解方式 (Human Framing)

如果面对传统项目角色，当前更适合这样解释：

- 对产品经理：
  它像“需求分诊入口”，先判断你现在缺的是现状、边界还是方案。
- 对技术负责人：
  它像“研发流转台”，避免问题直接跳进实现或验证，导致阶段错位。
- 对开发：
  它像“先别急着写，先判断现在到底该进哪一步”的入口。
- 对测试：
  它像“确认当前是不是已经到了可验证阶段”的前置判断点。

所以它不是一个抽象 AI 路由器，而是：

> 在传统项目协作里，先判断当前问题该流到哪个阶段的人机入口。

## 交互模式 (Interaction)

- 行动前阅读完整的步骤文件。
- 严格遵循步骤顺序。
- 自己只做入口判断，不延长停留在入口层的时间。
- 一旦路由已足够清楚，立即 handoff 到后续对象。

## 判定纪律 (Decision Discipline)

- 一轮只选一个主去向，不同时把请求交给多个对象。
- 若并列候选存在，优先选择更前置、更能降低后续误判风险的对象。
- 入口层只做识别、判断与交接，不吞并下游职责。
- 新增稳定入口目标后，应回补路由规则，不靠临场发挥扩路由。

## 必需的参考资料 (References)

- 工作流入口: `references/entry-router.workflow.md`
- `references/step-01-scan-entry.md`
- `references/step-02-assess-context.md`
- `references/step-03-select-route.md`
- `references/step-04-handoff.md`

## 依赖与集成 (Integrations)

- `现状同步（reality-sync）`
- `requirement-convergence`
- `方案设计（spec-designer）`
- `上下文实施（context-implementer）`
- `代码执行插槽（code-execution-slot）`
- `综合验证（integrated-validator）`
- `maglev-map-maker`
- `maglev-tutor`
- `知识沉淀检查（knowledge-check）`
- `现实结晶（crystallization）`

## 维护约束 (Maintenance)

- 当新增稳定、可被入口直接路由的对象时，必须评估是否需要更新本技能的路由表。
- 新对象不应默认自动进入入口层，只有在确实属于会话入口常见分流目标时才加入。

## 示例

User: "我有个想法，但我也不确定是先写方案还是先看现状。"

AI: "收到。入口路由已启动，我会先判断当前请求是否需要先做现状同步或需求收敛，再把会话交接到合适的能力。"
