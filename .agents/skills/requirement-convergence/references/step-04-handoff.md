---
name: handoff
description: 将已收敛结果以最小必要信息交接给下游对象
next_step: null
---

# Step 4: Handoff

## 目标

当 Ready Gate 通过时，用最小必要信息交接给 `方案设计（spec-designer）`，或在本技能内完成稳定需求产物输出后结束前段收敛。

## 动作

1. 输出当前已经固定的：
   - 本轮核心对象
   - In Scope
   - Out of Scope
   - 成功信号
2. 指出是否通过 Ready Gate。
3. 若通过，明确交给哪个下游对象。
4. 若未通过，输出最小补齐建议并结束本轮收敛。
5. 若输出模式为 `prd_document`，必须按 `references/prd-output-contract.md` 输出完整稳定需求产物契约。

## 交接规则

- 通过 Ready Gate 后，只交给一个主下游对象。
- 交接说明只保留下游真的需要消费的信息，不重复长背景。
- 若下游是 `方案设计（spec-designer）`，重点交接范围、非目标、成功信号与关键未知。
- 若主去向仍停留在 `requirement-convergence`，重点输出目标用户、范围边界、成功信号，以及为什么当前必须先形成稳定需求文档。
- 若主去向仍停留在 `requirement-convergence`，禁止只输出一句泛化结论；必须给出完整 `prd_output_package`。

## 审批检查点

当 Ready Gate 通过且将交接给下游时，在交接前执行以下步骤：

1. **展示产物摘要**：向用户展示以下内容的精简版：
   - 核心对象（core_object）
   - InScope / OutScope
   - 功能需求关键 AC（F 系前 3 条）
   - 如果存在交互需求：交互需求关键 AC（I 系前 3 条）

2. **等待明确确认**：
   - 询问："以上需求边界是否准确？确认后将进入方案设计。"
   - 只接受明确肯定信号（"确认"/"是"/"approved" 等）
   - 不可将模糊回复（"差不多吧"/"看看再说"）解读为确认

3. **处理修改请求**：
   - 若用户提出修改，回到 step-02 补齐，重新走 Ready Gate
   - 不强制继续交接

4. **记录审批**：
   - 在 spec context 中追加审批记录：
     ```yaml
     approval_log:
       - checkpoint: requirement_handoff
         result: approved | rejected
         artifacts_reviewed:
           - functional_requirements
           - interaction_requirements  # 仅含 UI 项目
         summary: "{用户确认的内容摘要}"
         timestamp: "{ISO 8601}"
     ```

## 输出格式

若 `ready`：

- `next_object`
- `handoff_summary`
- `prd_output_package`（仅当 `next_object = requirement-convergence` 且 `prd_mode_required = true` 时必填）

若 `not_ready`：

- `next_action`
- `minimum_fill_gaps`

## 输出

- 一份最小必要交接说明
- 一个明确的下一步
