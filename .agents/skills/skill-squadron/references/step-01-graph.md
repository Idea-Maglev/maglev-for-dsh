---
name: step-01-graph
description: 关系图构建 - 读取 .agents/private-catalog.yaml 构建 Relation_Graph
next_step: references/step-02-group.md
---

# Step 1: Graph（关系图构建）

## 目标

读取项目级治理对象清单（`.agents/private-catalog.yaml`），提取所有 `status: active` 的能力对象条目及其 `relations` 字段，构建邻接表形式的 Relation_Graph，为后续分组和编队巡逻提供基础数据结构。该清单只表示当前现状，不承担历史日志职责；旧名、替代项和历史占位不进入图。

## 输入

- `.agents/private-catalog.yaml`：项目级治理对象清单

## 动作

### 1. 读取私域能力清单

读取 `.agents/private-catalog.yaml`，获取所有已注册且纳入治理范围的能力对象条目。

**规则**：
- 若文件不存在或为空，触发错误处理流程。
- 同时读取 `skills:` 与 `workflows:` 列表。
- 解析每个 PrivateCatalogEntry，提取 `name`、`path`、`object_kind`、`status`、`runtime_name_status`、`relations`。
- **仅处理 `status: active` 的条目**，跳过 `deprecated` 状态的条目。
- 现状清单只认当前现役对象；如果清单里仍残留旧名、替代项或历史占位，视为需要清理的数据污染，不把它们展开成当前节点或历史叙事。
- 未被登记到清单中的文件系统对象，不视为图构建输入；若需要巡逻，先评估是否应纳入治理清单。
- 若所有条目都不是 `status: active`，触发错误处理流程。

### 2. 提取关系数据

对每个 active 条目，读取其 `relations` 字段：

- **`relations` 存在且非空**：逐条解析 RelationEntry，提取 `target`、`type`、`direction`、`description`。
- **`relations` 缺失或为空**：将该 skill 标记为孤立节点候选。

**字段校验**：
- `type` 必须属于 `{calls, called_by, complements, shares_data, precedes, preceded_by}`，否则跳过该条关系并记录日志。
- `direction` 必须属于 `{outbound, inbound, bidirectional}`，否则跳过该条关系并记录日志。

### 3. 构建邻接表

将所有有效的 RelationEntry 转化为邻接表形式的 Relation_Graph：

- **节点**：所有 `status: active` 的能力对象名称。
- **边**：每条有效的 RelationEntry 对应一条边，包含 source（声明方）、target、type、direction、description。

### 4. 检测不一致关系

遍历所有边，检测不一致的关系声明：

- **不一致定义**：skill A 声明与 skill B 存在某种关系（如 A calls B），但 B 未声明对应的反向关系（如 B called_by A）。
- **处理方式**：以声明方的关系为准纳入图中，在构建日志中标注该不一致。
- **悬空引用**：若 `target` 指向不存在于 active 节点列表中的 skill，该边仍纳入图中但标记为悬空引用，在构建日志中标注。

### 5. 识别孤立节点

将以下对象归入孤立节点列表：
- `relations` 字段缺失或为空的 active 对象。
- `relations` 中所有条目均因校验失败被跳过的 active 对象。

### 6. 生成图摘要

计算并展示 Relation_Graph 的摘要信息：
- 总节点数（active skill 数量）
- 总边数（有效 RelationEntry 数量）
- 孤立节点列表
- 关系类型分布（calls / called_by / complements / shares_data / precedes / preceded_by 各多少条）
- 不一致关系列表（若有）

## 输出格式

### Relation_Graph 数据结构

```yaml
relation_graph:
  built_at: string              # 构建时间（ISO 8601）
  nodes:                        # 节点列表
    - name: string
      object_kind: string       # skill / workflow / cluster
      path: string
      runtime_name_status: string  # active_legacy_name / canonical_name_active
  edges:                        # 边列表
    - source: string            # 源 skill（声明方）
      target: string            # 目标 skill
      type: string              # 关系类型
      direction: string         # 关系方向
      description: string       # 关系描述
  summary:
    total_nodes: integer        # 总节点数
    total_edges: integer        # 总边数
    isolated_nodes:             # 孤立节点列表
      - string
    type_distribution:          # 关系类型分布
      calls: integer
      called_by: integer
      complements: integer
      shares_data: integer
    inconsistencies:            # 不一致关系列表
      - description: string     # 不一致描述
        resolved_by: string     # 解决方式（"以声明方为准"）
```

### 图摘要展示

```
🔗 Relation_Graph 构建完成！

📊 图摘要：
- 节点数：{total_nodes} 个 active 对象
- 边数：{total_edges} 条关系
- 孤立节点：{isolated_nodes 列表，若无则显示"无"}
- 关系类型分布：
  - calls: {N} 条
  - called_by: {N} 条
  - complements: {N} 条
  - shares_data: {N} 条

⚠️ 不一致关系（若有）：
- {不一致描述}（处理方式：以声明方为准）

🔍 悬空引用（若有）：
- {source} → {target}（目标 skill 不存在于 active 节点中）
```

## 交互流程

### 正常流程

1. **开始构建**：向 Boya 提示"正在读取私域能力清单，构建 skill 关系图..."。
2. **展示摘要**：按输出格式展示 Relation_Graph 摘要。
3. **自动流转**：将 Relation_Graph 传递给 `step-02-group.md` 进行分组。

### 中止流程

- 若所有 active 对象均无 `relations` 字段，向 Boya 提示"未发现任何对象关系数据，请先为对象补充 relations 字段"，中止编队巡逻流程。

## 错误处理

| 错误场景 | 处理策略 |
|---------|---------|
| `.agents/private-catalog.yaml` 不存在或为空 | 提示 Boya "私域能力清单为空，请先通过 Skill Scout 创建私域能力"，中止流程 |
| 所有 active 对象均不存在 | 提示 "清单中无有效现役对象（仅剩历史占位或旧名残留），无需编队巡逻"，中止流程 |
| 所有 active 对象均无 `relations` 字段 | 提示 "未发现任何对象关系数据，请先为对象补充 relations 字段"，中止流程 |
| `relations` 中 `target` 指向不存在的对象 | 在构建日志中标注 "目标对象不存在"，该边仍纳入图中但标记为悬空引用 |
| `relations` 中 `type` 或 `direction` 值不合法 | 跳过该条关系，在构建日志中标注 "无效的关系类型/方向" |

## 状态流转条件

- 当 Relation_Graph 构建完成且至少存在一个非孤立节点时，将 Relation_Graph 作为输入，转入 `step-02-group.md`。
- 当所有 active 对象均无 `relations` 字段时，提示并中止流程。
- 当 `.agents/private-catalog.yaml` 不存在或所有对象为 deprecated 时，中止流程。
