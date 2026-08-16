---
name: spec-audit-surface
description: Spec 审计面。在实施前对 requirements 与 spec cluster 做统一输入质量和一致性审查。
metadata:
  formal_action_name: Spec 审计
  top_level_capability: 综合验证
  system_layer: Quality / Guardrail Layer
  lifecycle_chain: main_flow
  runtime_name_status: canonical_name_active
  distribution_scope: runtime_internal
  author: feiyu.gao
  last_updated: 2026-03-30
---

# Spec Audit Surface

## 概览 (Overview)

这是一个质量层输入审计技能。

它负责：

- 审查 requirements 是否具备清晰、可执行、可验证的输入质量
- 审查 spec cluster 是否具备一致性、完备性与前后对齐
- 汇总输入层 findings，作为后续方案设计、实施或综合验证的前置判断

它不负责：

- 直接做结果审查
- 直接做测试设计
- 直接承担主流程汇聚验证

它的交付结果至少应包含：

- 输入结构检查结果
- requirements 审计结果
- spec cluster 审计结果
- 汇总 findings 与下一步建议

## 何时使用 (When to use)

- 准备进入实施，但需要先确认输入文档质量时
- requirements 与 spec cluster 已存在，但质量与一致性还不稳定时
- 希望先把输入层问题收清，再决定是否进入后续实施或综合验证时

## 交互模式 (Interaction)

- 行动前阅读完整步骤文件。
- 先审输入，再审 requirements，再审 spec cluster。
- 严格输出 findings，不替对象补写大段正文。

## 判定纪律 (Decision Discipline)

- 输入质量先于实现质量。
- 要明确区分“结构缺失”“语义模糊”“跨文档不一致”三类问题。
- findings 只标记真正影响后续工作的缺口，不把所有风格问题都升级。

## 必需的参考资料 (References)

- 工作流入口: `references/spec-audit-surface.workflow.md`
- `references/step-01-check-input-shape.md`
- `references/step-02-audit-requirements.md`
- `references/step-03-audit-spec-cluster.md`
- `references/step-04-synthesize-findings.md`

## 依赖与集成 (Integrations)

- `综合验证（integrated-validator）`
- requirements 与 spec cluster

## 示例

User: "这轮 requirements 和 spec 都写完了，但我想先做输入审计，再决定能不能继续。"

AI: "收到。我会先进入 Spec 审计面，依次检查输入结构、requirements 质量和 spec cluster 一致性，再汇总 findings。"
