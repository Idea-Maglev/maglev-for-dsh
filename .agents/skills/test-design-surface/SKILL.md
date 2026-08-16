---
name: test-design-surface
description: 测试设计面。对 requirements、spec 与实现结果形成统一测试设计、覆盖策略与验证支撑。
metadata:
  formal_action_name: 测试设计
  top_level_capability: 综合验证
  system_layer: Quality / Guardrail Layer
  lifecycle_chain: main_flow
  runtime_name_status: canonical_name_active
  distribution_scope: runtime_internal
  author: feiyu.gao
  last_updated: 2026-03-30
---

# Test Design Surface

## 概览 (Overview)

这是一个质量层测试设计技能。

它负责：

- 识别测试对象与测试重点
- 设计覆盖策略与验证边界
- 给出测试层次建议
- 给出验证支撑产物建议

它不负责：

- 直接做 spec 输入审计
- 直接做结果 review
- 直接承担主流程汇聚验证

它的交付结果至少应包含：

- 测试对象识别结果
- 覆盖策略结果
- 测试层次建议
- 验证支撑产物建议

## 何时使用 (When to use)

- requirements、spec 或实现结果已经存在，需要先做统一测试设计时
- 希望先把测试对象、覆盖策略和验证支撑收清时
- 希望先形成测试设计面，再决定是否进入综合验证时

## 交互模式 (Interaction)

- 行动前阅读完整步骤文件。
- 先识别对象，再设计覆盖，再建议测试层次与支撑产物。
- 严格输出设计建议，不直接生成大段测试代码。

## 判定纪律 (Decision Discipline)

- 先明确“测什么”，再明确“怎么测”。
- 要区分覆盖策略、测试层次和交付产物，不混成一个建议块。
- 只标记真正影响验证完整性的缺口。

## 必需的参考资料 (References)

- 工作流入口: `references/test-design-surface.workflow.md`
- `references/step-01-identify-test-targets.md`
- `references/step-02-design-coverage.md`
- `references/step-03-suggest-test-layers.md`
- `references/step-04-suggest-artifacts.md`

## 依赖与集成 (Integrations)

- `综合验证（integrated-validator）`
- requirements、spec 与实现结果

## 示例

User: "我不想直接写测试代码，先帮我把这轮需求和实现应该怎么测收清。"

AI: "收到。我会先进入测试设计面，识别测试对象、覆盖策略、测试层次和验证支撑产物。"
