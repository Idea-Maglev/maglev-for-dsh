---
name: crystallization
description: 现实结晶器。在综合验证后完成结晶条件确认、现实回写判定、active 收口与可发现性回填。
metadata:
  formal_action_name: 现实结晶
  top_level_capability: 现实结晶
  system_layer: Reality / Context Layer
  lifecycle_chain: crystallization
  runtime_name_status: canonical_name_active
  distribution_scope: user_visible
  author: feiyu.gao
  last_updated: 2026-03-30
---

# Crystallization

## 概览 (Overview)

这是一个后段闭环技能。

**术语**：本 skill 中"**当前主题**"指 `specs/20_evolution/active/` 下当前正在结晶的演进需求（一次结晶调用所聚焦的对象）。

它负责：

- 判断当前结果是否已经成立到可以结晶
- 判断哪些变化应写回 `10_reality`
- 判断当前 `20_evolution/active` 的状态如何收口
- 触发地图与索引的可发现性回填

它不负责：

- 知识沉淀检查
- 复盘 / postmortem
- 用“归档”这个宽泛词混掉状态闭环
- 让 `10_reality` 通过引用 `90_archive` 来解释当前现状

它的交付结果至少应包含：

- 结晶条件判断
- Reality 回写判断
- active 状态结论
- 可发现性回填判断
- 明确的下游回填动作
- 项目看板更新（归档后调用 `project-board` 移除已归档需求）

## 何时使用 (When to use)

- 当前主题已通过 `综合验证`
- 需要把已成立结果沉淀为新的项目现实
- 需要判断 active 是结束、继续还是拆分
- 需要确保新现实能被后续会话发现

## 与 knowledge-check 的边界

| 维度 | crystallization | knowledge-check |
|------|----------------|-----------------|
| 核心动作 | 把已成立的结果写回 reality | 检查知识是否已记录 |
| 比喻 | "发布到生产环境" | "你保存了吗？" |
| 触发场景 | 功能验证通过、需要固化为项目事实 | 会话切换、探索结束、任务收尾 |
| 输出 | reality 回写 + active 收口 + 可发现性回填 | 缺口清单 + 补齐建议 |

### 典型触发意图

用这个技能：
- "功能做完了，帮我判断哪些该写回现实"
- "active 里的东西该收口了"
- "验证通过了，固化结果"

不用这个技能（用 knowledge-check）：
- "帮我看看有没有遗漏的知识资产"
- "会话要切了"
- "这轮讨论先到这里"

### 两者都需要时

先 knowledge-check → 再 crystallization。如果用户直接触发 crystallization 且未做过知识检查，应在开始前询问是否需要先运行 knowledge-check。

## 交互模式 (Interaction)

- 行动前阅读完整步骤文件。
- 严格按后段闭环顺序执行。
- 以事实和状态转换为优先，不混入知识沉淀。
- 需要知识沉淀检查时，转交 `knowledge-check`。

## 判定纪律 (Decision Discipline)

- 只结晶“已经成立的变化”，不结晶进行中推演。
- 结晶前先按四步推导结构（列读者 → 列维度 → 交叉成结构单元 → 收敛），同一方法递归适用于每个层级。
- 回写受 floor/ceiling 双向质量卡点约束：floor = 接手者能解释功能用法；ceiling = 不含过程性/项目管理性信息。
- 先判断是否写回，再判断写回到哪里。
- `active` 的结束、继续、拆分必须给出唯一结论。
- 地图和索引回填只在确实影响可发现性时触发，不机械调用。

## 生命周期边界 (Lifecycle Boundaries)

- `10_reality` 只承接当前已成立的项目事实，不承接历史推演链路。
- `20_evolution` 只承接仍在推进的演进主题，不承接历史归档。
- `90_archive` 只承接历史依据、过程记录和已结束主题，不作为理解当前现状的前置入口。
- 若某项变化已经结晶，写回 `10_reality` 时应直接写"当前事实"，而不是写"去哪里看历史"。
- 若必须保留历史依据，可在索引或思考入口承认其存在，但不得把 Archive 当成 Reality 的解释依赖。

### ⚠️ 归档反模式

- ❌ 将 `20_evolution/active/` 内容直接搬运到 `90_archive/`
- ❌ 在未将结论写入 `10_reality` 的情况下执行归档

正确的归档操作：

1. **提取结论** → 写入 `10_reality`（当前事实）
2. **收口 active** → 标记状态（结束/继续/拆分）
3. **结构化归档**（close 时必选）→ 填写归档日志 + 通过门禁 + 移入 `90_archive`

详见 `references/step-05-archive-with-log.md`。

## 必需的参考资料 (References)

- 工作流入口: `references/crystallization.workflow.md`
- `references/step-01-confirm-readiness.md`
- `references/step-02-judge-writeback.md`
- `references/step-03-close-active.md`
- `references/step-04-backfill-discovery.md`
- `references/scripts/crystallization_check.py`（自检脚本，执行者回写后自检用）

## 依赖与集成 (Integrations)

- `综合验证（integrated-validator）`
- `knowledge-check`
- `maglev-map-maker`
- `index-librarian`

## 示例

User: "这轮结构升级已经做完了，帮我判断哪些该写回现实，哪些只留在 active 里。"

AI: "收到。我会按现实结晶的方式处理：先确认结晶条件，再判断 Reality 回写、active 收口和可发现性回填。"
