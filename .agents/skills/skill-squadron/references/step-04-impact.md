---
name: step-04-impact
description: 跨对象影响分析 - 评估优化对关联对象的影响
next_step: references/step-05-report.md
---

# Step 4: Impact（跨 skill 影响分析）

## 目标

对编队巡逻中发现的每个存在优化机会或结构缺口的对象，执行 Cross_Impact_Analysis，评估优化该对象对其关联对象在接口兼容性、数据流变化和行为变化三个维度的影响，标注影响等级，并生成每个 Skill_Group 的优化顺序建议。

## 输入

- `patrol_results`：来自 `step-03-patrol.md` 的按组组织的 Patrol_Report 集合
- `Relation_Graph`：来自 `step-01-graph.md` 的关系图数据

## 动作

### 1. 筛选有优化机会的对象

遍历 `patrol_results`，仅对 `status` 为 `opportunities_found` 或 `workflow_gaps_found` 的对象执行影响分析：

- `opportunities_found`：执行 Cross_Impact_Analysis。
- `workflow_gaps_found`：执行 Cross_Impact_Analysis。
- `all_current`：跳过，无需影响分析。
- `workflow_reviewed`：跳过，无需影响分析。
- `scan_failed`：跳过，无法评估。

若所有对象均为 `all_current`、`workflow_reviewed` 或 `scan_failed`，跳过影响分析，直接进入 `step-05-report.md`。

### 1.1 按组语义切换影响分析重点

若对象所属 Skill_Group 已带有稳定组语义，则影响分析应优先关注：

- **主流程前中段组**
  - 入口路由变化是否会影响下游主流程衔接
  - 前段 workflow 变化是否会影响 `方案设计 / 上下文实施 / 综合验证` 的进入条件
  - 主流程动作之间是否产生新的阶段边界混淆
- **体系级与后段闭环组**
  - `crystallization` 与 `knowledge-check` 的链路分离是否被破坏
  - `整体接入`、`现状表达`、`能力进化` 对象之间的协作关系是否受影响
  - 可发现性回填、逆向接入、能力进化是否因此断链
- **质量层组**
  - 三个质量面之间的边界是否被破坏
  - `综合验证（integrated-validator）` 与三面的协作接口是否发生漂移
  - 历史碎片对象是否会因为当前优化再次被抬升为并列主对象

### 2. 三维度影响评估

对每个有优化机会的 skill，基于 Relation_Graph 找到其所有关联 skill，逐一评估以下三个维度：

#### 2a. 接口兼容性 (Interface Compatibility)

评估优化后是否影响调用方或被调用方的接口约定：

- **评估要素**：
  - 该 skill 的输入/输出格式是否变化
  - 步骤链的入口/出口接口是否变化
  - 被其他 skill 引用的数据结构是否变化
- **等级判定**：
  - `safe`：接口无变化，或变化仅限内部实现
  - `caution`：接口有新增字段但保持向后兼容
  - `breaking`：接口有删除或修改字段，破坏现有约定

#### 2b. 数据流变化 (Data Flow Change)

评估共享数据的格式或语义是否发生变化：

- **评估要素**：
  - 共享的 YAML/Markdown 文件结构是否变化
  - 数据字段的语义是否变化（如字段含义改变）
  - 数据流向是否变化（如从单向变为双向）
- **等级判定**：
  - `safe`：数据格式和语义无变化
  - `caution`：数据格式有新增但不影响现有消费方
  - `breaking`：数据格式或语义有破坏性变更

#### 2c. 行为变化 (Behavior Change)

评估互补 skill 的协作行为是否受影响：

- **评估要素**：
  - 工作流步骤的执行顺序是否变化
  - 触发条件或前置条件是否变化
  - 输出结果的质量或范围是否变化
- **等级判定**：
  - `safe`：协作行为无变化
  - `caution`：行为有微调但不影响核心协作
  - `breaking`：行为变化导致协作流程中断

### 3. 标注影响等级

为每个影响项计算综合影响等级：

- **综合等级取最高**：三个维度中最高的等级作为该影响项的综合等级。
  - 例：接口 `safe` + 数据流 `caution` + 行为 `safe` → 综合 `caution`
  - 例：接口 `safe` + 数据流 `safe` + 行为 `breaking` → 综合 `breaking`

- **`breaking` 级别特殊处理**：当综合等级为 `breaking` 时，必须在结果中明确标注：
  - 受影响的关联 skill 列表
  - 具体影响描述（哪个维度导致 breaking）
  - 建议的同步修改方案

### 4. 生成优化顺序建议

基于 Cross_Impact_Analysis 结果，为每个 Skill_Group 生成优化顺序建议：

**排序原则**：被依赖的 skill 优先于依赖方进行优化。

- 若 B calls A（B 依赖 A），则 A 的优化顺序应先于 B。
- 若存在循环依赖，标注循环并建议同步优化。
- 无依赖关系的 skill 按 Patrol_Report 的 `value_score` 降序排列。

## 输出格式

### Cross_Impact_Analysis 数据结构

```yaml
cross_impact_analysis:
  target_skill: string          # 被优化的 skill 名称
  optimization_summary: string  # 优化内容摘要（来自 Patrol_Report）
  impacts:                      # 影响列表
    - affected_skill: string    # 受影响的关联 skill
      relation_type: string     # 与被优化 skill 的关系类型
      dimensions:
        interface_compatibility:
          level: string         # safe / caution / breaking
          description: string
        data_flow:
          level: string
          description: string
        behavior_change:
          level: string
          description: string
      overall_level: string     # 综合影响等级
  optimization_order:
    - skill: string
      order: integer            # 建议优化顺序（1 = 最先）
      reason: string
```

### 影响分析展示

```
🔍 跨 skill 影响分析完成！

---

**{target_skill}** 的优化影响：
优化摘要：{optimization_summary}

| 受影响 skill | 关系类型 | 接口兼容性 | 数据流变化 | 行为变化 | 综合等级 |
|-------------|---------|-----------|-----------|---------|---------|
| {skill_1} | {type} | 🟢 safe | 🟡 caution | 🟢 safe | 🟡 caution |
| {skill_2} | {type} | 🟢 safe | 🟢 safe | 🔴 breaking | 🔴 breaking |

⚠️ Breaking 影响详情：
- {skill_2}：{具体影响描述}
  建议：{同步修改方案}

---

📋 优化顺序建议（{group_id}）：
1. {skill_A}（原因：被 {skill_B} 依赖，需先优化）
2. {skill_B}（原因：依赖 {skill_A}，需后优化）
```

## 交互流程

### 正常流程

1. **开始分析**：向 Boya 提示"正在执行跨 skill 影响分析..."。
2. **逐 skill 分析**：对每个有优化机会的 skill 执行影响评估。
3. **展示结果**：按输出格式展示影响分析结果和优化顺序建议。
4. **自动流转**：将 Cross_Impact_Analysis 结果传递给 `step-05-report.md`。

### 无优化机会

若所有 skill 均无优化机会，跳过影响分析，直接进入 `step-05-report.md`。

## 错误处理

| 错误场景 | 处理策略 |
|---------|---------|
| 无任何 skill 存在优化机会 | 跳过影响分析，直接进入报告生成（标注 "all_current"） |
| 关联 skill 的详细信息无法读取 | 将该影响项标注为 "无法评估"，在报告中注明原因 |

## 状态流转条件

- 当影响分析完成时，将 Cross_Impact_Analysis 结果作为输入，转入 `step-05-report.md`。
- 当无优化机会时，跳过影响分析，直接进入 `step-05-report.md`（标注 "all_current"）。
