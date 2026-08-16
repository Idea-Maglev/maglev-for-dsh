---
name: synthesize-findings
description: 汇总输入审计 findings，给出质量评分与唯一下一步建议
next_step: null
---

# Step 4: Synthesize Findings

## 目标

把 requirements 与 spec 的审计结果汇总成统一输入质量判断，输出量化评分。

## 动作

1. 合并所有 findings。
2. 区分 blocker、major、minor。
3. 计算质量评分（见下文）。
4. 给出唯一下一步建议：
   - 继续推进
   - 先补输入
   - 转交其他质量对象
5. 汇总 provenance findings：
   - AC / Decision → 来源的正向覆盖结果
   - 来源 → AC / Decision 的反向覆盖结果
   - AI 语义变更记录结果
   - AI 对话摘要与 `docs/thinking/` 分流结果

## 质量评分

对审计发现按 5 个维度打分，各 20 分：

| 维度 | 检查内容 | 评分依据 |
|------|---------|---------|
| 完整性 | 需求是否全覆盖、设计是否处理了所有需求 | Critical finding 每个 -10，Warning -5 |
| 清晰度 | 表达是否无歧义、结构是否易消费 | 悬空引用 -10，格式不一致 -5 |
| 可行性 | 技术选型是否匹配、约束是否合理 | 不可行的技术选型 -15，风险未缓解 -5 |
| 一致性 | 需求↔设计↔计划是否对齐、AC 引用是否正确 | 断裂 AC 每个 -10，不存在的引用 -15 |
| 来源覆盖 | 来源依据、AC/Decision provenance、双向覆盖、语义变更记录 | blocker 每个 -15，major -10，minor -5 |

综合分 = 算术平均，同时高亮最低维度。

注意：
- 未生成结构化 AC 的简单任务，一致性维度标为 N/A
- 评分是参考信号，不是硬门禁

## 交互 Spec 审计（当存在 I 系 AC 时）

在合并 findings 后、生成评分前，额外检查交互文档：

### 状态完整性
- 每个交互组件应定义状态集：空/加载/成功/错误/骨架屏
- 至少覆盖 3 种状态（空+成功为最低底线）
- 缺失关键状态标记为 WARNING

### 跨系引用有效性
- I 系 AC 引用的 F 系 AC 是否在功能需求文档中存在
- 无效引用标记为 CRITICAL

### 响应式策略检查
- 如果 in_scope 提及移动端/多端适配
- 检查是否存在响应式断点策略
- 缺失标记为 WARNING

### 可访问性要求检查
- 如果 in_scope 提及可访问性/无障碍/WCAG
- 检查是否有对应的 I 系 AC
- 缺失标记为 WARNING

## 输出格式

评分输出（固定格式）：

| 维度 | 得分 | 关键发现 |
|------|------|---------|
| 完整性 | {N}/100 | {最关键的 finding} |
| 清晰度 | {N}/100 | {或 "—"} |
| 可行性 | {N}/100 | |
| 一致性 | {N}/100 | |
| 来源覆盖 | {N}/100 | |
| **综合** | **{N}/100** | {🟢≥85 / 🟡70-84 / 🔴<70} ⚠️ 最低维度: {name} {score} |

Findings 汇总：

- `consolidated_findings`
- `severity_split`
- `provenance_findings`
- `next_action`

写入位置：`context/audit_score.md`，按阶段覆盖最新结果。
