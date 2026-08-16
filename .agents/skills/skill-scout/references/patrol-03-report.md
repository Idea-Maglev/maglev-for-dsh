---
name: patrol-03-report
description: Patrol 模式 - 报告生成，汇总差异分析结果并按优化价值排序生成巡逻报告
next_step: references/patrol-04-optimize.md
---

# Patrol Step 3: Report（报告生成）

## 目标

接收 `patrol-02-diff.md` 输出的所有 DiffAnalysis 结果，筛选出具有优化价值的条目，按优化价值评分降序排序，生成结构化的 PatrolReport，为用户提供清晰的优化决策依据。若无任何优化机会，标注当前能力保持先进状态。

## 输入

- `diff_analyses`：来自 `patrol-02-diff.md` 的所有 DiffAnalysis 结果列表

## 动作

### 1. 筛选有效分析结果

遍历所有 DiffAnalysis 条目，按以下规则筛选：

**纳入报告**：
- `recommendation` 为 `upgrade` 的条目
- `recommendation` 为 `partial_merge` 的条目

**排除报告**：
- `recommendation` 为 `skip` 的条目
- 标记为"资源不可访问"或"内容不完整"的条目

若筛选后无任何有效条目，直接进入"无优化机会"处理流程（见步骤 4）。

### 2. 计算优化价值评分

对每个纳入报告的 DiffAnalysis 条目，综合以下维度计算 `value_score`（0.0 - 1.0）：

| 维度 | 权重 | 说明 |
|-----|------|------|
| 建议类型 | 40% | `upgrade` → 0.8-1.0；`partial_merge` → 0.4-0.7 |
| 新增功能数量 | 30% | 新增功能越多，评分越高（上限 5 项对应满分） |
| 架构改进数量 | 20% | 架构改进越多，评分越高（上限 3 项对应满分） |
| 改造工作量（反向） | 10% | `low` → 高分；`medium` → 中分；`high` → 低分 |

**评分规则**：
- 最终 `value_score` 保留两位小数，范围 0.00 - 1.00。
- 同等评分时，`upgrade` 优先于 `partial_merge`。

### 3. 生成 PatrolReport

将筛选并评分后的条目按 `value_score` 降序排列，构建 PatrolReport：

```yaml
patrol_report:
  generated_at: string          # 生成时间（ISO 8601 格式）
  summary: string               # 总体摘要（如"发现 N 个优化机会，涉及 M 个 Private Skill"）
  opportunities:
    - target_skill: string      # 目标 Private Skill 名称
      external_resource: string # 发现的外部资源（名称或 URL）
      diff_summary: string      # 差异摘要（基于 DiffAnalysis 的 feature_diff 和 architecture_improvements 提炼）
      suggested_action: string  # 建议的优化动作（如"全面升级步骤链架构"、"合并多文件批量处理能力"）
      value_score: float        # 优化价值评分 (0.0 - 1.0)
  status: string                # "opportunities_found" / "all_current"
```

**示例**：

```yaml
patrol_report:
  generated_at: "2025-01-15T10:30:00Z"
  summary: "发现 2 个优化机会，涉及 2 个 Private Skill"
  opportunities:
    - target_skill: "zhiyin"
      external_resource: "https://github.com/example/ai-code-reviewer"
      diff_summary: "外部资源新增多文件批量审查和 CI/CD 集成能力，错误分类更细致（三级），报告支持双格式输出"
      suggested_action: "部分合并：引入三级错误分类和双格式报告输出，保留中文注释规范检查"
      value_score: 0.72
    - target_skill: "zhiyin-archivist"
      external_resource: "https://github.com/example/smart-archiver"
      diff_summary: "外部资源支持自动标签推断和跨仓库归档，步骤链设计更模块化"
      suggested_action: "全面升级：重构步骤链架构，引入自动标签推断能力"
      value_score: 0.65
  status: "opportunities_found"
```

### 4. 无优化机会处理

当所有 DiffAnalysis 的 `recommendation` 均为 `skip`，或筛选后无有效条目时：

```yaml
patrol_report:
  generated_at: "2025-01-15T10:30:00Z"
  summary: "已扫描全部 Private Skill，当前能力均保持先进，无需优化"
  opportunities: []
  status: "all_current"
```

向用户展示：

```
✅ 巡逻完成！当前所有私域能力均保持先进，无需优化。
```

并结束 Patrol 流程，**不进入** `patrol-04-optimize.md`。

## 输出格式

### 报告展示（有优化机会）

```
📊 巡逻报告生成完成！

**总体摘要**：{summary}
**生成时间**：{generated_at}

---

### 优化机会列表（按价值评分排序）

**#1 [{value_score}] {target_skill}**
- 外部资源：{external_resource}
- 差异摘要：{diff_summary}
- 建议动作：{suggested_action}

**#2 [{value_score}] {target_skill}**
- 外部资源：{external_resource}
- 差异摘要：{diff_summary}
- 建议动作：{suggested_action}

---

📌 共发现 {N} 个优化机会。请告知是否进入优化执行阶段，或指定要优先处理的条目。
```

### 报告展示（无优化机会）

```
✅ 巡逻报告生成完成！

**总体摘要**：{summary}
**生成时间**：{generated_at}
**状态**：当前能力保持先进（all_current）

无需进入优化阶段，Patrol 流程结束。
```

## 交互流程

### 正常流程（有优化机会）

1. **生成报告**：向用户提示"正在汇总差异分析结果，生成巡逻报告..."。
2. **展示报告**：按输出格式展示完整的 PatrolReport。
3. **等待用户决策**：询问用户是否进入优化执行阶段，或指定优先处理的条目。
4. **流转到优化**：用户确认后，将 PatrolReport 和用户选择的条目传递给 `patrol-04-optimize.md`。

### 正常流程（无优化机会）

1. **生成报告**：汇总分析结果，确认无优化机会。
2. **展示报告**：展示 `all_current` 状态的报告。
3. **结束流程**：Patrol 流程正常结束，不进入优化阶段。

### 用户干预点

- 用户可在报告展示后，要求查看某个优化机会对应的完整 DiffAnalysis 详情。
- 用户可手动排除某个优化机会，该条目将不进入优化执行阶段。
- 用户可选择"全部优化"或"仅优化指定条目"。

## 错误处理

| 错误场景 | 处理策略 |
|---------|---------|
| DiffAnalysis 结果列表为空 | 向用户提示"差异分析结果为空，无法生成报告"，中止 Patrol 流程。 |
| 所有条目均为 `skip` 或不可访问 | 生成 `status: "all_current"` 的报告，结束 Patrol 流程，不进入优化阶段。 |
| 单个 DiffAnalysis 数据不完整（缺少必需字段） | 跳过该条目，在报告末尾注明"N 个条目因数据不完整被跳过"。 |

## 状态流转条件

- 当 `patrol_report.status` 为 `"opportunities_found"` 且用户确认进入优化阶段时，将 PatrolReport 和用户选择传递给 `patrol-04-optimize.md`。
- 当 `patrol_report.status` 为 `"all_current"` 时，Patrol 流程正常结束，不进入 `patrol-04-optimize.md`。
- 当报告生成因错误无法完成时，向用户说明原因并中止 Patrol 流程。
