---
description: maglev-reverse-spec Step 00b - Output Profile Selection
---

# Step 00b: Output Profile Selection

## 目标
在开始大规模逆向前，先决定这次输出的密度和边界，避免默认走向过轻或过重。

## 三档定义

### Lean
适合：
- 只想快速理解模块
- 用户只需要定位入口和主流程
- 当前证据不足，不适合展开大量增强项

默认包含：
- Feature Map
- Evidence Log
- Core Data Structures
- Main Flow
- Unknowns / Quests

建议产物：
- `00_index.md`
- `01_requirements.md` 的摘要版
- `02_design.md` 中的 `Architecture Overview / Feature Map / Core Data Structures / Main Flow / Unknowns`

### Standard
适合：
- 需要交接、重构准备、补文档
- 希望结果可读、可继续深入
- 模块复杂度中等以上

默认包含：
- Lean 全部内容
- Data Dictionary
- Domain Model
- State Machine
- Dependency Topology
- Test Mapping
- Change Risk

建议产物：
- `00_index.md`
- 完整 `01_requirements.md`
- 完整 `02_design.md`
- 如有必要，增加 `03_test_mapping.md` 或在 `02_design.md` 中保留 `Test Mapping`

### Deep
适合：
- 高风险、高复杂度、关键主链路
- 逆向结果要直接服务设计、审计或大改
- 用户明确要“严谨完整”

默认包含：
- Standard 全部内容
- Runtime Behavior
- Security Surface
- Error Taxonomy
- Configuration Matrix
- Observability Map
- RMM Scorecard
- Expert Review Queue

建议产物：
- `00_index.md`
- 完整 `01_requirements.md`
- 完整 `02_design.md`
- `03_rmm_scorecard.md`
- `99_expert_review_queue.md`
- 如需要，可将 `Security / Runtime / Observability` 拆成附录

## 决策输入
至少综合以下因素：
- 目标用途: 理解 / 交接 / 重构 / 审计 / 开发输入
- 项目复杂度: Low / Medium / High
- 证据完整度: Low / Medium / High
- 风险暴露: Low / Medium / High

## 推荐输出模板
```markdown
[Output Profile Suggestion]
- Target: {目标用途}
- Complexity: {Low/Medium/High}
- Evidence Coverage: {Low/Medium/High}
- Risk Exposure: {Low/Medium/High}

- Suggested Profile: `Standard`
- Why:
  - 需要支持后续重构
  - 数据结构与状态流较复杂
  - 当前证据足以支撑 Recommended Layer

- Optional Upgrade:
  - 如需补齐安全与运行时，可升级到 `Deep`
```

## 默认策略
- 用户未指定时，默认 `Standard`
- 证据明显不足时，即使用户想要 `Deep`，也要提示其中哪些维度将是低置信度

## 质量边界

### Lean 的最低标准
- 能回答“这个模块做什么”
- 能指出入口和主流程
- 能列出核心数据结构
- 能明确未知项

### Standard 的最低标准
- 在 Lean 基础上，可支撑交接和中等规模改动前分析
- 数据字典、状态机、依赖与风险至少有一版可读结果

### Deep 的最低标准
- 在 Standard 基础上，可支撑重构、审计或高风险设计讨论
- 安全、运行时、错误传播、配置差异等高风险维度不能只是标题，必须有证据支撑
