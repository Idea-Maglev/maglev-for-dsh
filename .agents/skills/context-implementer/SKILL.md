---
name: context-implementer
description: 上下文实施器。在方案依据清楚后完成受控的非代码实施、自检与对抗性审查。
metadata:
  formal_action_name: 上下文实施
  top_level_capability: 上下文实施
  system_layer: Core Flow Layer
  lifecycle_chain: main_flow
  runtime_name_status: canonical_name_active
  distribution_scope: user_visible
  author: feiyu.gao
  last_updated: 2026-05-31
---

# 上下文实施 (Context Implementer)

## 概览 (Overview)

这是一个主流程中的**非代码实施**技能。

当前说明：

- 结构动作名：`上下文实施`
- 运行面名称：`context-implementer`
- 兼容 workflow 入口：`/quick-dev`

它负责：

- 在方案和上下文已清楚的前提下实施**非代码类改动**
- 在实施后执行自检
- 在必要时执行对抗性审查并修复发现

**非代码类改动**包括：
- 文档编写与更新（`.md`、README、指南等）
- 配置文件（`.yaml`、`.json`、`.toml` 等）
- 分析与研究产出
- Maglev 自身 skill/协议维护（SKILL.md、AGENTS.md 等，即使含代码片段）

它**不负责**：

- 产品代码、修复和重构 → 由 `code-execution-slot` 选择 enabled 扩展或 agent-native fallback
- 吞并需求收敛
- 代替方案设计
- 跳过验证纪律直接交付

## 与 code-execution-slot 的分工

| 交付物类型 | 负责者 | 示例 |
|-----------|--------|------|
| 产品代码 | code-execution-slot | 实现新功能、修 bug、重构 |
| 文档 | context-implementer | 写 spec、更新 README、记录思考 |
| 配置 | context-implementer | 修改 yaml/json 配置 |
| Maglev 治理 | context-implementer | 改 SKILL.md、AGENTS.md、catalog |
| 分析产出 | context-implementer | 竞品分析、架构评估 |
| 混合（代码+非代码） | 先 Slot 后 CI | Slot 做代码部分，CI 做文档/配置部分 |

它的交付结果至少应包含：

- 已完成的受控改动
- 自检结果
- 对抗性审查结果
- 已处理或显式保留的剩余问题

## 何时使用

- 需求和方案已经清楚，需要进入**非代码**实施时
- 范围受控、可以按步骤执行实现与自检时
- 用户明确要求进入 `上下文实施（context-implementer）` 路径时
- spec 的 `delivery_type` 为 `docs` 或 `ops` 时

## 何时不使用

- 需求和方案仍不清楚时
- **spec 含代码交付物时** → 应路由到 `code-execution-slot`
- 当前任务更适合先进入方案设计或综合验证时
- 你不在 Maglev 项目上下文中

## 交互模式 (Interaction)

- 在行动前阅读完整的步骤文件；绝不略读。
- 在需要时使用 `advanced-elicitation`。
- 在指示时运行对抗性审查任务。
- 不要跳过步骤；严格遵循顺序。
- **背景纪律**：本 skill 执行期间持续遵循 `maglev-discipline` 红线（闭环验证 / 事实驱动 / 穷尽方法），每个 step 起始前先做 `[MAGLEV-DIAGNOSIS]` 自检

## 判定纪律 (Decision Discipline)

- 先确认是否达到可实施状态，再开始改动
- 保持实施、自检、对抗性审查三段闭环
- 不用“快”作为默认价值承诺，优先保证上下文正确和边界受控
- 不把兼容入口 `/quick-dev` 误解为当前运行名仍是旧值

## 必需的参考资料

- 工作流入口：`references/quick-dev.workflow.md`
- 步骤：`references/step-01-mode-detection.md` 到 `references/step-06-resolve-findings.md`
- 协议：`references/advanced-elicitation.workflow.xml`
- 审查任务：`references/review-adversarial-general.xml`

## 快速参考

- 步骤 01: 模式检测 (mode detection)
- 步骤 02: 上下文收集 (context gathering)
- 步骤 03: 执行 (execute)
- 步骤 04: 自检 (self-check)
- 步骤 05: 对抗性审查 (adversarial review)
- 步骤 06: 解决发现 (resolve findings)

## 示例
用户：“按当前方案把这个修复落下去。”
你：“我会进入上下文实施流程，先确认输入和范围，再执行改动、自检和对抗性审查。”

## 常见错误
- 跳过对抗性审查
- 忽略必要的诱导步骤
- 在未完成先前步骤的情况下跳跃
