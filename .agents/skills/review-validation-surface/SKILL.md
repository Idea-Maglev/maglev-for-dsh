---
name: review-validation-surface
description: Review 与验证面。对实现结果做统一 review 与 validation，汇总偏差、风险与不一致。
metadata:
  formal_action_name: Review 与验证
  top_level_capability: 综合验证
  system_layer: Quality / Guardrail Layer
  lifecycle_chain: main_flow
  runtime_name_status: canonical_name_active
  distribution_scope: runtime_internal
  author: feiyu.gao
  last_updated: 2026-03-30
---

# Review Validation Surface

## 概览 (Overview)

这是一个质量层结果审查技能。

它负责：

- 加载实现结果与关联依据
- 审查实现是否符合预期约束
- 审查质量风险、边界问题与显著偏差
- 汇总结果层 findings，作为后续综合验证或修正依据

它不负责：

- 直接做 spec 输入审计
- 直接做测试设计
- 直接承担主流程汇聚验证

它的交付结果至少应包含：

- 结果上下文加载结果
- 实现合规性检查结果
- 质量与风险检查结果
- 汇总 findings 与下一步建议

## 何时使用 (When to use)

- 已有代码、结果或实现产物，需要做统一 review 时
- 希望先把结果层偏差与风险收清时
- 希望先在质量层结果面做收口，再决定是否进入综合验证时

## 交互模式 (Interaction)

- 行动前阅读完整步骤文件。
- 先看结果上下文，再看合规性，再看质量风险。
- 严格输出 findings，不替实现对象直接重写代码。

## 判定纪律 (Decision Discipline)

- 先判断“是否符合预期”，再判断“写得是否好”。
- 要明确区分“合规偏差”“质量问题”“风险项”三类结果。
- findings 只标记真正影响结果可信度与可交付性的缺口。

## 必需的参考资料 (References)

- 工作流入口: `references/review-validation-surface.workflow.md`
- `references/step-01-load-review-context.md`
- `references/step-02-check-implementation-compliance.md`
- `references/step-03-check-quality-risks.md`
- `references/step-04-synthesize-review.md`

## 依赖与集成 (Integrations)

- `综合验证（integrated-validator）`
- 实现结果与验证依据

## 示例

User: "代码已经写完了，我想先统一做结果 review，再决定要不要进入综合验证。"

AI: "收到。我会先进入 Review 与验证面，检查实现合规性、质量风险和关键偏差，再汇总 findings。"
