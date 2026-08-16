---
name: audit-requirements
description: 审查 requirements 的清晰度、边界和可验证性
next_step: references/step-03-audit-spec-cluster.md
---

# Step 2: Audit Requirements

## 目标

审查 requirements 是否已经具备进入后续工作的最低质量。

## 动作

1. 检查范围、非目标、成功信号是否清楚。
2. 检查需求是否可执行、可验证。
3. 检查是否存在明显冲突、缺失或模糊表达。
4. 检查 requirements 是否存在“来源依据”章节。
5. 检查关键 AC 是否包含：验收标准、来源摘要、上下文判定、证据。
6. 执行正向来源检查：每条正式 AC 是否都有可理解的来源摘要、上下文判定和证据。
7. 执行反向覆盖检查：来源依据中列出的主要来源，其有效需求信息是否已被 AC 覆盖，或被明确标为不采纳、待确认、out of scope。
8. 检查 AI 对话来源是否只以摘要形式进入 requirements；高价值思考是否被建议沉淀到 `docs/thinking/`，而不是塞进需求正文。
9. 检查正式来源选择是否有导航收据，且收据的来源指纹、候选和 AC evidence 可互相回查。
10. 检查导航收据状态是否被正确消费：
    - `queried`: AC evidence 是否确实回链到命中候选或其叶子证据。
    - `not_needed`: 是否明确说明为何 requirements 形成不依赖额外项目知识。
    - `insufficient`: 是否被阻断或进入升级链，而不是被静默略过。
    - `escalated`: 是否保留了结构化升级字段（step / attempt / basis），且范围确实收窄。
    - `exhausted`: 是否显式暴露知识不足，而不是继续伪造正式来源。

## Provenance finding 分级

- `blocker`: 正式 AC 无来源摘要、上下文判定或证据；AI 语义变更缺少变更记录。
- `blocker`: `exhausted` 后仍伪造正式来源，或 `insufficient` 被当作可继续成功处理。
- `major`: 来源中有效需求信息未被 AC 覆盖，且可能影响需求、验收或范围。
- `major`: 升级链仅有自由文本叙述，没有结构化升级字段或可回查 basis。
- `minor`: 证据可回查性不足，但不影响当前设计方向。

## 输出格式

- `requirements_audit_result`
- `requirements_findings`
