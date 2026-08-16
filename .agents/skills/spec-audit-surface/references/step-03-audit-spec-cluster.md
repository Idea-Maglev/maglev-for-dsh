---
name: audit-spec-cluster
description: 审查 spec cluster 的一致性、完备性和前后对齐
next_step: references/step-04-synthesize-findings.md
---

# Step 3: Audit Spec Cluster

## 目标

审查 spec cluster 是否在内部一致，且能承接 requirements。

## 动作

1. 检查 requirements 与 design 是否对齐。
2. 检查 design 与 plan 是否对齐。
3. 检查术语、结构和关键决策是否前后一致。
4. 检查 design 是否存在“来源依据”或“设计依据”章节。
5. 检查关键设计决策是否包含：选择、来源摘要、上下文判定、证据。
6. 检查 design 是否消费了 requirements 的来源摘要和上下文判定，而不是只引用最终 AC 文本。
7. 执行正向来源检查：每条关键 Decision 是否都有可理解的来源摘要、上下文判定和证据。
8. 执行反向覆盖检查：来源依据中列出的主要来源，其有效设计约束是否已被 Decision 覆盖，或被明确标为不采纳、待确认、out of scope。
9. 检查内嵌语义变更记录：当 requirements / design 发生语义变更时，是否在对应文件内记录日期、变更对象、变更内容、变更原因、来源依据。
10. 如果变更记录快速膨胀，应标记项目健康风险，而不是建议拆出独立日志。

## 输出格式

- `spec_audit_result`
- `spec_findings`
