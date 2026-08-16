---
name: step-05-report
description: 编队报告生成 - 生成按关联组组织的 Squadron_Report
next_step: null
---

# Step 5: Report（编队报告生成）

## 目标

汇总编队巡逻和跨 skill 影响分析的所有结果，生成按关联组组织的 Squadron_Report，包含组级优化价值评分、影响等级标注和优化顺序建议，以 Markdown 格式向 Boya 展示。

## 输入

- `patrol_results`：来自 `step-03-patrol.md` 的按组组织的 Patrol_Report 集合
- `cross_impact_analyses`：来自 `step-04-impact.md` 的 Cross_Impact_Analysis 结果（若无优化机会则为空）
- `Relation_Graph`：来自 `step-01-graph.md` 的关系图数据
- `Skill_Group 列表`：来自 `step-02-group.md` 的分组数据

## 动作

### 1. 按组组织报告内容

为每个 Skill_Group 汇总以下信息：

- **组成员列表**：组内所有 skill 名称。
- **组内关系摘要**：组内边数、关系类型分布。
- **各 skill 的 Patrol_Report 摘要**：
  - `opportunities_found`：优化机会数量和最高价值机会摘要。
  - `all_current`：标注"当前能力保持先进"。
  - `scan_failed`：标注"扫描失败"及原因。
- **运行面命名状态**：
  - `active_legacy_name`：结构动作名已稳定，但运行面仍保留历史名称
  - `canonical_name_active`：运行面已切到当前正式对象名称
- **分发范围**：
  - `user_visible`：面向用户显式可见
  - `runtime_internal`：运行面存在，但主要供系统内部协作使用
  - `private_only`：仅 Maglev 私有维护或 Creator 场景使用
- **Cross_Impact_Analysis 结果**：每个有优化机会的 skill 的影响分析。
- **优化顺序建议**：基于依赖关系的优化执行顺序。
- **组语义标签**：若能稳定判断，给组补一个简短标签，例如：
  - `主流程前中段组`
  - `体系级与后段闭环组`
  - `质量层组`

### 2. 计算组级优化价值评分

为每个 Skill_Group 计算 `group_value_score`（0.0 - 1.0），评分维度及权重：

| 维度 | 权重 | 计算方式 |
|------|------|----------|
| 组内 Patrol 优化价值均值 | 50% | 各 skill Patrol_Report 中 `value_score` 的平均值（`scan_failed` 的 skill 不参与计算） |
| 跨 skill 影响复杂度（反向） | 30% | `1.0 - (breaking_count / total_impacts)`，breaking 影响越多评分越低 |
| 组内优化机会比例 | 20% | `opportunities_found_count / total_member_count` |

**特殊情况**：
- 若组内所有 skill 均为 `all_current`，`group_value_score` 为 0.0。
- 若组内所有 skill 均为 `scan_failed`，`group_value_score` 为 0.0，标注"数据不可用"。
- 若无 Cross_Impact_Analysis 数据（所有 skill 无优化机会），影响复杂度维度得满分 1.0。

最终评分保留两位小数。

### 3. 按评分降序排列

将所有 Skill_Group 按 `group_value_score` 降序排列。同分时按组内 skill 数量降序排列。

### 4. 标注影响等级

在每个优化建议旁标注：
- **影响等级**：`safe` 🟢 / `caution` 🟡 / `breaking` 🔴
- **受影响的关联 skill 列表**：当等级为 `caution` 或 `breaking` 时列出。

### 5. 无优化机会处理

当编队巡逻未发现任何优化机会时（所有 skill 均为 `all_current`）：

```yaml
squadron_report:
  generated_at: "..."
  summary: "已完成编队巡逻，当前所有关联组能力保持先进，无需编队优化"
  groups: [...]
  status: "all_current"
```

### 6. 项目样例优先

若当前项目已经提供专用的报告样例或表达偏好，应优先参考项目样例，再回落到本通用模板。

对当前 Maglev 仓库，可参考：

- `specs/20_evolution/active/skill_structural_upgrade/design/02zm_skill_squadron_report_sample_v1.md`

## 输出格式

### Squadron_Report 数据结构

```yaml
squadron_report:
  generated_at: string          # 生成时间（ISO 8601）
  summary: string               # 总体摘要
  groups:
    - group_id: string
      members:
        - string
      relations_summary: string
      patrol_results:
        - skill: string
          runtime_name_status: string
          distribution_scope: string
          status: string        # opportunities_found / all_current / scan_failed
          opportunities_count: integer
          top_opportunity: string
      impact_analysis:
        - target_skill: string
          impacts:
            - affected_skill: string
              overall_level: string
              description: string
      optimization_order:
        - skill: string
          order: integer
          reason: string
      group_value_score: float
      group_label: string        # 可选：组语义标签
  isolated_nodes:
    - string
  status: string                # "opportunities_found" / "all_current"
```

### 报告展示模板（有优化机会）

```
📊 Squadron Report - 编队优化报告

**生成时间**：{generated_at}
**总体摘要**：{summary}

═══════════════════════════════════════

## Group 1: {group_id} [组级评分: {group_value_score}]

**组标签**：{group_label}

**成员**：{member_1}, {member_2}, ...
**关系摘要**：{relations_summary}

### Patrol 巡逻结果

| Skill | 运行面命名状态 | 分发范围 | 状态 | 优化机会 | 最高价值机会 |
|-------|---------------|---------|------|---------|------------|
| {skill_1} | {runtime_name_status} | {distribution_scope} | ✅ 发现机会 | {N} 个 | {top_opportunity} |
| {skill_2} | {runtime_name_status} | {distribution_scope} | ✅ 保持先进 | 0 | - |

### 跨 skill 影响分析

| 优化目标 | 受影响 skill | 影响等级 | 影响描述 |
|---------|-------------|---------|---------|
| {skill_1} | {affected_1} | 🟡 caution | {description} |
| {skill_1} | {affected_2} | 🔴 breaking | {description} |

⚠️ Breaking 影响：
- {affected_2} 需同步修改：{修改建议}

### 优化顺序建议

1. {skill_A} — {reason}
2. {skill_B} — {reason}

═══════════════════════════════════════

## Group 2: {group_id} [组级评分: {group_value_score}]
...

═══════════════════════════════════════

## 孤立节点

以下 skill 无关联关系，建议使用 Skill Scout Patrol 模式独立扫描：
- {isolated_node_1}
- {isolated_node_2}

═══════════════════════════════════════

📊 总体统计：
- 关联组数：{group_count}
- 扫描 skill 总数：{total_skills}
- 发现优化机会：{total_opportunities} 个
- Breaking 影响：{breaking_count} 个
- 孤立节点：{isolated_count} 个
```

### 报告展示模板（无优化机会）

```
📊 Squadron Report - 编队优化报告

**生成时间**：{generated_at}
**总体摘要**：已完成编队巡逻，当前所有关联组能力保持先进，无需编队优化。

✅ 当前所有关联组能力保持先进，无需编队优化。

📊 总体统计：
- 关联组数：{group_count}
- 扫描 skill 总数：{total_skills}
- 孤立节点：{isolated_count} 个
```

## 交互流程

### 正常流程（有优化机会）

1. **生成报告**：向 Boya 提示"正在汇总编队巡逻结果，生成编队优化报告..."。
2. **展示报告**：按报告模板展示完整的 Squadron_Report。
3. **支持浏览**：Boya 可按组浏览，或按影响等级筛选（如"只看 breaking 影响"）。
4. **结束流程**：报告展示完成，编队巡逻流程结束。

### 正常流程（无优化机会）

1. **生成报告**：汇总结果，确认无优化机会。
2. **展示报告**：展示 `all_current` 状态的报告。
3. **结束流程**：编队巡逻流程正常结束。

### 用户干预点

- Boya 可要求查看某个组的详细 Patrol_Report。
- Boya 可要求按影响等级筛选（如"只看 breaking"、"只看 caution 以上"）。
- Boya 可要求导出报告为文件。

## 错误处理

| 错误场景 | 处理策略 |
|---------|---------|
| Patrol_Report 和 Cross_Impact_Analysis 数据不完整 | 基于可用数据生成部分报告，在报告中注明哪些数据缺失 |
| 某个组的数据完全缺失 | 在报告中标注该组为"数据不可用"，列出原因 |

## 状态流转条件

- 报告生成完成后，编队巡逻流程结束。
- `next_step: null` — 这是步骤链的最后一步。
