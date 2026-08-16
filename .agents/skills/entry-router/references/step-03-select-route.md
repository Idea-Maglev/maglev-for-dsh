---
name: select-route
description: 从候选对象中选定唯一主去向
next_step: references/step-04-handoff.md
---

# Step 3: Select Route

## 目标

从候选下游中选出唯一主去向，避免入口层继续停留。

## 动作

1. 按以下优先级判断主去向：
   - 现状不清 -> `现状同步（reality-sync）`
   - 需求边界不稳 -> `requirement-convergence`
   - 已有稳定输入、需要方案 -> `方案设计（spec-designer）`
   - 已有明确代码改动目标、需要实现 -> `代码执行插槽（code-execution-slot）`
   - 已有明确非代码改动目标、需要实现 -> `上下文实施（context-implementer）`
   - 已有代码/结果、需要系统验证 -> `综合验证（integrated-validator）`
   - 需要地图或导航 -> `maglev-map-maker`
   - 需要仓库导览或学习 -> `maglev-tutor`
   - 任务收尾、知识资产检查 -> `知识沉淀检查（knowledge-check）`
   - 成果已验证、需写回现实并收口 -> `现实结晶（crystallization）`
2. 若存在并列候选，优先选择更前置的对象。
3. 生成一句话说明：
   - 为什么去这个对象
   - 为什么不直接去其他对象
4. 若后续新增了稳定且常用的入口目标，应回补本步骤的路由规则，而不是让入口对象临场即兴扩张。

## 选择规则

- `现状同步（reality-sync）` 优先于任何依赖当前现状的中后段对象。
- `requirement-convergence` 优先于 `方案设计（spec-designer）`，只要边界还不稳。
- `方案设计（spec-designer）` 优先于实施入口，只要仍缺方案设计。
- `综合验证（integrated-validator）` 只在已有结果可验证时进入。
- `知识沉淀检查（knowledge-check）` 优先于 `现实结晶（crystallization）`，除非用户明确要求写回 reality 或收口 active。
- `现实结晶（crystallization）` 只在有已验证成果需要固化时进入。
- 若用户说"归档"且上下文不明确，先路由到 `knowledge-check`（安全默认）。

## 前置纪律检查

在路由到下游对象之前，必须检查以下纪律条件：

1. **新需求 / 新功能 → 必须在 feature 分支上**
   - 如果当前在 main/master 分支，且路由目标是 `requirement-convergence`、`spec-designer`、`code-execution-slot`、`context-implementer` 之一（意味着即将开始新工作），必须先提示用户创建 feature 分支。
   - 检查方式：`git branch --show-current`
   - 若在主分支上：暂停路由，先告知用户需要切换分支，待确认后再继续。

2. **归档操作 → 禁止直接搬运**
   - 若路由到 `crystallization`，提醒正确的归档流程（结晶回写 10_reality → 收口 active → 结构化归档，close 时必选）。

## 输出格式

- `selected_route`
- `route_reason`
- `rejected_alternatives`

## 输出

- 唯一主去向
- 路由理由
