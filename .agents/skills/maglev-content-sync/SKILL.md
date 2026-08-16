---
name: maglev-content-sync
description: 内容写作前同步器。重载当前版本的 Maglev 定义、边界与运营写作规则，降低新会话写作跑偏风险。
metadata:
  formal_action_name: 内容写作同步
  top_level_capability: 非核心主流程能力
  system_layer: Specialized Support Layer
  lifecycle_chain: specialized_support
  runtime_name_status: active_legacy_name
  distribution_scope: runtime_internal
  author: feiyu.gao
  last_updated: 2026-03-30
  version: "1.0.0"
---

# Maglev Content Sync

> 结构动作名：`内容写作同步`
> 运行面名称：`maglev-content-sync`
> 这不等于已经完成正式物理改名。

## 概览
这是一个专为运营内容、案例文章、首页文案与对比文写作准备的前置同步器。

它的目标不是直接写正文，而是先做一件更关键的事：

> **在开始写之前，重新理解“当前版本的 Maglev 到底是什么、不是什 么、应该怎么讲”。**

## 为什么需要它？

新的会话很容易出现一种高风险问题：

- AI 能写得很顺
- 风格看起来也对
- 但对 Maglev 的理解已经漂了

这种漂移通常不是简单事实错误，而是：

- 定位漂移
- 范围漂移
- 边界漂移
- 版本漂移

`maglev-content-sync` 的作用，就是在内容写作前先进行一次 **Re-grounding**。

## 来源边界

`maglev-content-sync` 必须先从当前事实层建立定义，再读取内容生产指南：

### 当前事实（canonical）

- `specs/10_reality/positioning.md`
- `specs/10_reality/glossary.md`
- `specs/10_reality/reality-knowledge/operations/agent-context.md`

### 内容生产指南（editorial guide）

- `docs/marketing/strategy/message_house.md`
- `docs/marketing/strategy/audience_map.md`
- `docs/marketing/strategy/content_style_guide.md`
- `docs/marketing/registry/lifecycle.md`
- `docs/marketing/registry/context_injection_protocol.md`
- `docs/marketing/templates/`

`docs/marketing/strategy/maglev_current_definition.md` 只是面向写作者的定义快照，不是事实源。它与 Reality 冲突时，以 Reality 为准。`docs/marketing/assets/`、`welcome.md`、`start_here.md` 和 `docs/publishing/` 不得作为当前事实来源。

## 核心能力

1. **Definition Sync**
   先读取 Reality canonical sources，再读取 `maglev_current_definition.md` 进行受众化表达同步。

2. **Message Sync**
   读取 `docs/marketing/strategy/message_house.md`，同步统一口径。

3. **Audience Sync**
   读取 `docs/marketing/strategy/audience_map.md`，明确本次内容的目标受众与禁用表达。

4. **Style Sync**
   读取 `docs/marketing/strategy/content_style_guide.md`，同步文风、阅读体验与表达形式约束。

5. **Boundary Guard**
   在写作前显式指出本次内容最容易跑偏的边界，并阻止历史资产、发布包或未登记来源覆盖 Reality。

## 何时使用

- 准备写任何一篇新的运营内容时
- 准备修改已有对外文章时
- 感觉 AI 对 Maglev 的理解开始泛化、漂移或混入无关概念时

## 不负责什么

- 代替正文写作本身
- 改写主流程 skill 的结构边界
- 把营销表达凌驾于当前 reality 之上

## 预期输出

完成同步后，应先输出一份简短的 **Content Sync Brief**，至少包含：

- 当前版本里 Maglev 是什么
- 当前版本里 Maglev 不是什么
- 本次写作的主要问题域
- 本次最需要避免的跑偏方向

然后再进入后续 `content-write` 或正文草拟阶段。
