---
name: knowledge-check
description: 知识沉淀检查器。在高价值探索、会话切换或任务收尾前，检查思考、方案、参考资料和贡献记录是否已经沉淀；同时负责 9 段记忆宫殿 / 位段（segments）归类判断。
metadata:
  formal_action_name: 知识沉淀检查
  top_level_capability: 思考沉淀
  system_layer: Quality / Guardrail Layer
  lifecycle_chain: thinking_archive
  runtime_name_status: canonical_name_active
  distribution_scope: runtime_internal
  author: feiyu.gao
  last_updated: 2026-06-14
---

# Knowledge Check

## 概览 (Overview)

这是一个知识沉淀检查技能，也是 **9 段记忆宫殿 / 位段（segments）归类的 canonical 检查入口**。

它的职责是：

- 检查高价值思考是否已记录
- 检查方案是否已落地
- 检查参考资料和保留价值的废案是否已归位
- 检查贡献记录是否已更新

它不负责：

- 需求归档
- reality writeback
- active 状态收口

这些动作应由 `crystallization` 或其他后段对象承担。

它的交付结果至少应包含：

- 本轮知识资产清单
- 记录完整性判断
- 生命周期边界判断
- 缺口与最小补齐动作

## 快速识别

如果你的问题里出现下面任一类关键词，优先考虑这个 skill：

- `位段` / `segments`
- `9 段记忆宫殿`
- `thinking` 文档归类
- 知识资产是否已经落盘
- 会话切换前要不要补沉淀

## 何时使用 (When to use)

- 一段高价值探索结束后
- 会话准备切换前
- 任务收尾前
- 怀疑本轮有价值思考可能流失时

## 与 crystallization 的边界

用户说"归档"或"收尾"时，需要区分两个技能：

- **knowledge-check**："你保存了吗？" — 检查知识资产是否已记录，适用于会话切换和探索结束
- **crystallization**："发布到生产" — 把已验证的成果写回 reality 并收口 active，适用于功能完成后

两者都需要时：先 knowledge-check → 再 crystallization。详见 `crystallization/SKILL.md` 的边界说明。

## 交互模式 (Interaction)

- 行动前阅读完整的步骤文件。
- 严格遵循步骤顺序。
- 作为检查器工作，而不是替代后续生命周期动作。
- 若发现缺口，明确指出缺什么，而不是模糊地说“还没归档”。

## 判定纪律 (Decision Discipline)

- 只检查“是否已沉淀”，不替代沉淀对象本身重写内容。
- 只把 blocker 级缺口单独升级，不把轻微缺口都说成阻塞。
- 一旦问题属于 Reality 回写或 active 收口，立即切边界并转交。

## 必需的参考资料 (References)

- 工作流入口: `references/knowledge-check.workflow.md`
- `references/step-01-scan-assets.md`
- `references/step-02-audit-records.md`
- `references/step-03-check-boundaries.md`
- `references/step-04-report-gaps.md`
- `references/segments-canonical.yaml` — 思考位段 canonical 数据（机器读）
- `references/segments-canonical.md` — 思考位段方法论说明（人读）

## 持有的方法论资产

本 skill 是 Maglev 思考分类方法论（"9 段记忆宫殿"）的 canonical 来源。位段语义本体（00_meta / 10_critique / 20_architecture / 30_philosophy / 40_paper / 50_alignment / 60_case / 70_retrospective / 90_archive）由 `references/segments-canonical.yaml` + `references/segments-canonical.md` 持有, 在判断"某条思考归到哪个位段"时直接消费。

任何项目实例（如 `docs/thinking/INDEX.md` 的 `segments:` 字段）应以 canonical 为内容来源, 在文件头标注 `segments_source: .agents/skills/knowledge-check/references/segments-canonical.yaml`。

**与 index-librarian 的边界**: index-librarian 是基础设施层, 只规约 `segments` 字段的 schema 格式, 不消费本 canonical。两个 skill 互不依赖。

## 依赖与集成 (Integrations)

- `crystallization`
- `contribute_methodology`
- `skill-scout`

## 示例

User: "这轮讨论先到这里，帮我看看有没有什么知识资产还没沉淀。"

AI: "收到。我会按知识沉淀检查的方式核对思考、方案、参考资料和贡献记录，不把这一步和 Reality 回写或 active 收口混在一起。"
