---
name: prd-output-contract
description: requirement-convergence 进入 PRD 文档输出模式时的最小稳定需求产物契约
---

# PRD Output Contract

## 目标

当 `requirement-convergence` 判断最小 handoff 仍不足以支撑下游消费时，必须在本技能内产出一份稳定、可被后续充分消费的需求产物契约，而不是把任务再次路由给独立 PRD skill。

这份契约的作用是：

1. 抑制前段需求产物继续漂移
2. 为后续方案设计、评审与验证提供稳定输入基线
3. 让后续协作复用同一份需求约束面

## 触发条件

仅当以下条件同时成立时，才进入本契约：

1. `Ready Gate` 已通过
2. 主去向暂不进入 `方案设计（spec-designer）`
3. 已明确说明为什么最小 handoff 不足以支撑下游消费

## 最小字段

进入 PRD 模式时，`handoff_summary` 至少应包含以下字段：

```yaml
prd_output_package:
  core_object: string
  target_user: string
  collaboration_context: string
  in_scope:
    - string
  out_of_scope:
    - string
  success_signal:
    - string
  key_unknowns:
    - string
  drift_risk: string
  why_minimum_handoff_is_not_enough: string
  expected_prd_outcome:
    - string
  downstream_consumers:
    - string
  functional_requirements:        # 可选。简单任务或修复类留空
    - id: "F-1"
      name: "{功能名称}"
      user_story: "作为 {角色}，我希望 {功能}，以便 {价值}"
      acceptance_criteria:
        - id: "AC-F1-1"
          criterion: "当 {触发条件} 时，系统应 {响应行为}"
          source_summary: "{来源表达的完整含义，不摘孤立关键词}"
          context_judgement: "{如何从完整上下文推导为该 AC；冲突、补充或取舍如何处理}"
          evidence: "{可回查位置 / 用户确认 / 会议或聊天摘要 / AI 对话摘要}"
        - id: "AC-F1-2"
          criterion: "若 {前置条件}，则系统应 {响应行为}"
          source_summary: "{来源表达的完整含义，不摘孤立关键词}"
          context_judgement: "{如何从完整上下文推导为该 AC；冲突、补充或取舍如何处理}"
          evidence: "{可回查位置 / 用户确认 / 会议或聊天摘要 / AI 对话摘要}"
      boundary_cases:              # 可选
        - "{边界情况描述}"
  source_basis:                    # 当存在结构化需求时必填
    - name: "{来源名称}"
      type: "doc | meeting | chat | design | code | user_confirmation | ai_dialog_summary"
      usage: "{该来源用于固定什么结论}"
```

## 字段解释

- `core_object`
  - 本轮真正要沉淀成文档的核心对象
- `target_user`
  - 这份 PRD 主要服务的阅读者或协作角色
- `collaboration_context`
  - 当前为什么需要显性需求文档，例如评审、跨角色同步、方案设计前固定基线
- `in_scope`
  - 本轮明确要覆盖的内容
- `out_of_scope`
  - 本轮明确不覆盖的内容
- `success_signal`
  - 文档完成后如何判断这份需求产物已经成立
- `key_unknowns`
  - 仍未解决但必须被显式带入文档的未知项
- `drift_risk`
  - 当前若不生成文档，需求最可能如何继续漂移
- `why_minimum_handoff_is_not_enough`
  - 为什么只靠结构化摘要还不足以支撑下游
- `expected_prd_outcome`
  - 希望稳定需求产物最终固定住的关键结果
- `downstream_consumers`
  - 后续会直接消费这份 PRD 的对象或角色
- `functional_requirements`（可选）
  - 结构化功能需求列表，每条含用户故事 + 可测试的验收标准（AC）
  - AC 编号采用 `AC-F{N}-{M}` 格式（F=功能需求序号，M=AC 序号），全局唯一
  - AC 描述采用行为级格式："当 [触发条件] 时，系统应 [响应行为]" 或 "若 [前置条件]，则系统应 [响应行为]"
  - 每条关键 AC 应包含来源摘要、上下文判定和证据，最终验收标准必须能从这些字段推导出来
  - AI 对话可作为来源摘要，但不要求保存完整原始对话；高价值思考应沉淀到 `docs/thinking/`
  - 简单任务、修复类、不需要行为级验收标准时留空——此时下游行为与当前一致
- `source_basis`
  - 本轮实际消费过的来源列表，用于说明需求依据从哪里来
  - 类型可以是文档、会议、聊天、设计稿、代码观察、用户确认或 AI 对话摘要
  - 不用于记录会话过程，只保留读者理解需求所需的来源、用途和可回查线索

## 质量要求

进入 PRD 模式时，这份交接契约必须满足：

1. 能单独阅读，不依赖大量上下文补充
2. 不把长期愿景混进本轮需求产物
3. 能直接解释“为什么现在必须形成文档”
4. 能被后续 `方案设计（spec-designer）`、评审或验证直接复用
5. 不依赖独立 `maglev-create-prd` skill 继续加工
6. 关键 AC 不应只有结论，必须携带足以支撑结论的来源摘要、上下文判定和证据
7. 需求正文只保留读者可消费的信息，不写会话中的内部取舍、被放弃方案或写作过程

## 当前结论

当 `requirement-convergence` 进入 `prd_document` 模式时，真正的交付不应只是“说明需要 PRD”，而应是：

> 先交付一份稳定需求产物契约，再决定是否进入后续方案设计或评审。
