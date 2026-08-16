---
description: maglev-reverse-spec Step 4 Support - Intent Enrichment & Quests
---

# Step 4 Support: Intent Enrichment (意图补强)

## 目标
在事实层已经建立的前提下，补充“为什么会这样设计”的候选解释，并把无法确认的问题整理为 `Quests`，而不是把推测直接写进需求或设计。

## 执行逻辑

### 1. 提取意图线索
基于调用链、数据结构和状态变化，寻找以下高价值线索：
- Magic Numbers / Magic Strings
- 复杂校验与异常分支
- 幂等、防重、锁、重试、熔断等保护逻辑
- 具有业务含义的命名
- 注释、测试、配置中的语义补充

### 2. 生成候选解释
对每条线索，只能生成“带证据边界的解释”，例如：
- `[INFERENCE]` 该锁机制可能用于避免高并发重复写入
- `[INFERENCE]` 该硬编码状态值可能表示归档态
- `[UNKNOWN]` 该税率常量来源不明，无法确认是法规要求还是临时策略

### 3. 形成 Quest List
当出现以下情况时，必须进入 `Quest`：
- 找到关键分支，但无法确认业务语义
- 同一概念在不同层结构中含义不一致
- 状态值、枚举值或策略常量来源不明
- 实现行为与推测意图可能冲突

### 4. 输出要求
- 已确认的解释，仍需保留 `[FACT] / [INFERENCE] / [UNKNOWN]` 标签
- 不得把 Quest 消化掉后悄悄写成已确认结论
- 若用户未确认，Quest 应进入最终产物中的 `Unknowns / Expert Review Queue`

## 输出结构
生成 `intent_context.md` 或等价章节：

```markdown
# Intent Context

## Intent Signals
- Signal: `dedupe_key` + retry guard
  Interpretation: [INFERENCE] 该流程可能要求幂等
- Signal: `state == 9`
  Interpretation: [UNKNOWN] 状态语义待确认

## Quests
- [Q-01] `state == 9` 的业务含义是什么？
- [Q-02] 锁机制是防重提交、并发写保护，还是补偿流程的一部分？
```
