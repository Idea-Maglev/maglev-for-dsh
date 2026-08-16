---
name: step-02-group
description: 分组策略 - 基于连通分量算法将 skill 分为关联组
next_step: references/step-03-patrol.md
---

# Step 2: Group（分组策略）

## 目标

基于 Relation_Graph 的连通分量算法，将能力对象分为若干 Skill_Group（关联组），计算每组的巡逻优先级评分，按评分降序排列，为编队巡逻提供执行顺序。

## 输入

- `Relation_Graph`：来自 `step-01-graph.md` 的关系图数据（邻接表形式）

## 动作

### 1. 执行连通分量分组

基于 Relation_Graph 的邻接表，使用连通分量算法（忽略边的方向，视为无向图）将能力对象分为若干 Skill_Group：

- **同一组内**：任意两个 skill 之间存在直接或间接关系（通过其他 skill 中转）。
- **不同组间**：不存在任何直接或间接关系。
- **孤立节点**：不归入任何 Skill_Group，单独列出。

### 1.1 当前默认巡逻切片

当读取当前 Maglev 项目级治理对象清单，且分组结果与既有预演一致时，可直接沿用以下默认切片来组织巡逻：

- **主流程前中段组**
  - `entry-router`
  - `现状同步（reality-sync）`
  - `requirement-convergence`
  - `方案设计（spec-designer）`
  - `上下文实施（context-implementer）`
  - `综合验证（integrated-validator）`
- **体系级与后段闭环组**
  - `crystallization`
  - `knowledge-check`
  - `maglev-bootstrapper`
  - `maglev-legacy-adopter`
  - `maglev-reverse-spec`
  - `maglev-map-maker`
  - `index-librarian`
  - `skill-scout`
  - `skill-squadron`
- **质量层组**
  - `spec-audit-surface`
  - `review-validation-surface`
  - `test-design-surface`

使用约束：

- 这只是当前对象图下的默认巡逻切片，不是固定白名单。
- 只要 `.agents/private-catalog.yaml` 的 active 对象或 relations 发生变化，必须重新以连通分量结果为准。

### 2. 计算巡逻优先级评分

为每个 Skill_Group 计算 `priority_score`（0.0 - 1.0），评分维度及权重：

| 维度            | 权重 | 计算方式                                                                               |
| --------------- | ---- | -------------------------------------------------------------------------------------- |
| 组内 skill 数量 | 40%  | `min(member_count / 10, 1.0)` — 数量越多评分越高，上限 10 对应满分                     |
| 关系密度        | 35%  | `min(edge_count / node_count / 3.0, 1.0)` — 边数/节点数越高评分越高，上限 3.0 对应满分 |
| 关系类型多样性  | 25%  | `unique_type_count / 4` — 不同类型数越多评分越高，4 种全有对应满分                     |

**最终评分**：`priority_score = 0.4 × 数量分 + 0.35 × 密度分 + 0.25 × 多样性分`，保留两位小数。

### 3. 按评分降序排列

将所有 Skill_Group 按 `priority_score` 降序排列。同分时按组内 skill 数量降序排列。

### 4. 孤立节点处理

将 Relation_Graph 中的孤立节点单独列出，建议 Boya 使用 Skill Scout 的 Patrol 模式独立扫描这些对象。

## 输出格式

### Skill_Group 数据结构

```yaml
skill_group:
  group_id: string              # 组标识（如 "group-1"）
  members:                      # 组成员列表
    - string
  relations_summary:            # 组内关系摘要
    total_edges: integer        # 组内边数
    types:                      # 包含的关系类型
      - string
  priority_score: float         # 巡逻优先级评分 (0.0 - 1.0)
  priority_factors:             # 评分因子明细
    member_count: integer       # 组内 skill 数量
    relation_density: float     # 关系密度（边数/节点数）
    type_diversity: integer     # 关系类型多样性（不同类型数）
```

### 分组结果展示

```
📋 分组结果（按巡逻优先级降序）：

---

**Group 1** [优先级: {priority_score}]
- 成员：{member_1}, {member_2}, ...
- 关系摘要：{total_edges} 条关系，类型包含 {types}
- 评分因子：skill 数量 {N}，关系密度 {density}，类型多样性 {diversity}

**Group 2** [优先级: {priority_score}]
- 成员：{member_1}, {member_2}, ...
- 关系摘要：{total_edges} 条关系，类型包含 {types}
- 评分因子：skill 数量 {N}，关系密度 {density}，类型多样性 {diversity}

---

🔹 孤立节点（无关系的 skill）：
- {isolated_node_1}
- {isolated_node_2}
💡 建议：使用 Skill Scout 的 Patrol 模式独立扫描孤立节点。

---

共 {group_count} 个关联组，{isolated_count} 个孤立节点。
是否确认开始编队巡逻？
```

## 交互流程

### 正常流程

1. **开始分组**：向 Boya 提示"正在基于关系图执行分组..."。
2. **展示结果**：按输出格式展示分组结果、优先级评分和孤立节点。
3. **等待确认**：询问 Boya 是否确认开始编队巡逻。
4. **流转**：
   - Boya 确认 → 将 Skill_Group 列表传递给 `step-03-patrol.md`。
   - Boya 中止 → 结束流程。
   - 关系分析模式 → 展示结果后结束，不进入巡逻。

### 用户干预点

- Boya 可要求调整分组（如手动合并或拆分组）。
- Boya 可排除某些组不参与巡逻。
- Boya 可调整巡逻顺序。

## 错误处理

| 错误场景                      | 处理策略                                                                                               |
| ----------------------------- | ------------------------------------------------------------------------------------------------------ |
| Relation_Graph 为空（无节点） | 提示 "关系图为空，无法执行分组"，中止流程                                                              |
| 所有节点均为孤立节点          | 提示 "所有 skill 均为孤立节点，无法组成关联组。建议使用 Skill Scout Patrol 模式独立扫描"，中止编队巡逻 |

## 状态流转条件

- 当分组完成且 Boya 确认开始巡逻时，将 Skill_Group 列表作为输入，转入 `step-03-patrol.md`。
- 当处于关系分析模式时，展示分组结果后结束流程。
- 当所有节点均为孤立节点时，中止编队巡逻。
