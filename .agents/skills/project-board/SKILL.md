---
name: project-board
description: 项目看板。扫描活跃需求，交叉判断流程阶段，映射角色状态，输出持久化看板。
metadata:
  formal_action_name: 项目看板
  top_level_capability: 项目看板
  system_layer: Observation Layer
  lifecycle_chain: auxiliary
  runtime_name_status: canonical_name_active
  distribution_scope: user_visible
  author: feiyu.gao
  last_updated: 2026-04-15
---

# Project Board (项目看板)

## 概览 (Overview)

这是一个观测层技能，用于展示项目的活跃需求、流程阶段和角色状态。

它负责：

- 扫描 `specs/20_evolution/active/` 和 `issues/active/` 识别活跃需求
- 基于文件证据 + 内容质量 + 代码变更 + 测试覆盖交叉判断流程阶段
- 映射 VO/TP/XG 铁三角角色在每个需求上的参与状态
- 输出两级看板（总看板 `board.md` + 需求子看板 `status.md`）
- 持久化到仓库固定路径，支持缓存与增量更新

它不负责：

- 修改需求或方案内容
- 执行流程推进（只观测，不驱动）
- Gantt/timeline 视图、工时统计、人员绩效
- 外部系统集成（Jira/GitLab Board 等）
- Git commit 级细粒度追踪

## 何时使用 (When to use)

- 需要了解"当前有哪些需求在跑、各自到哪了、谁在主导"时
- 手动调用 `/board` 或通过 reality-sync 自动展示时
- 其他 Skill（如 crystallization）触发看板更新时

## 交互模式 (Interaction)

- 行动前阅读 `references/board.workflow.md`
- 按 4 步串行执行：扫描 → 阶段判断 → 角色映射 → 渲染持久化
- 在阶段判断不确定时标记"待确认"，不默认猜测
- 缓存 git 查询结果，避免重复执行

## 判定纪律 (Decision Discipline)

- 文件存在是必要不充分条件——需交叉验证内容质量和下游证据
- 证据不足时标记 `uncertain`，不强行归类
- 看板模式（Mermaid 结构/样式）变更需 AI + 用户确认；数据更新自动执行
- 人员-角色映射以项目级配置为主，spec 级可覆盖

## 必需的参考资料 (References)

- 工作流: `references/board.workflow.md`
- `references/step-01-scan.md`
- `references/step-02-judge-stage.md`
- `references/step-03-map-roles.md`
- `references/step-04-render-board.md`
- `references/stage-evidence-rules.md`
- `references/board-template.md`

## 依赖与集成 (Integrations)

- **reality-sync**: 会话启动时读取 `board.md` 并展示摘要（只读，不触发更新）
- **crystallization**: 归档完成后调用本 Skill 更新看板，移除已归档需求

## 输出产物

- `specs/20_evolution/board.md` — 总看板（Mermaid 流程图 + 降级 Markdown 表格）
- `specs/20_evolution/active/{spec}/status.md` — 需求级子看板
- `.maglev/temp/board_cache.json` — 缓存文件（不提交到仓库）
