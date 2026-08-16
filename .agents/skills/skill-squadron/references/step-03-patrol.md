---
name: step-03-patrol
description: 编队巡逻执行 - 按组对 skill 与 workflow 分别执行巡逻
next_step: references/step-04-impact.md
---

# Step 3: Patrol（编队巡逻执行）

## 目标

按 Skill_Group 优先级顺序，逐组对组内对象执行巡逻，收集 Patrol_Report，为后续跨对象影响分析提供数据。

## 输入

- `Skill_Group 列表`：来自 `step-02-group.md` 的排序后关联组列表
- Skill Scout 的 Patrol 模式能力（`patrol-01-scan.md` → `patrol-02-diff.md` → `patrol-03-report.md`）
- `Relation_Graph`：来自 `step-01-graph.md`，用于读取节点的 `object_kind`、`runtime_name_status` 与 `distribution_scope`

## 动作

### 1. 按优先级顺序逐组巡逻

按 `priority_score` 降序，依次处理每个 Skill_Group：

1. 向 Boya 展示当前正在巡逻的组信息。
2. 对组内每个对象按 `object_kind` 选择巡逻方式。
3. 组内所有对象扫描完成后，展示组级进度。
4. 进入下一组。

### 1.1 按组语义切换巡逻重点

当某个 Skill_Group 已被稳定识别为特定组语义时，应优先按该组的默认巡逻重点组织扫描，而不是对所有组一视同仁：

- **主流程前中段组**
  - 优先检查：
    - 入口是否把请求路由到正确下游
    - `requirement-convergence` 是否仍保持三段式边界
    - `方案设计（spec-designer）` / `上下文实施（context-implementer）` / `综合验证（integrated-validator）` 的接口是否顺滑衔接
    - 主流程中是否再次出现阶段语义吞并
    - 仍保留旧运行名的主流程对象，是否已经在文档和交互中造成误导
    - 标记为 `user_visible` 的对象，是否混入了过重的内部治理语义
- **体系级与后段闭环组**
  - 优先检查：
    - `crystallization` 与 `knowledge-check` 是否仍保持链路分离
    - `整体接入`、`现状表达`、`能力进化` 三类能力簇是否仍边界清晰
    - `map-maker` / `librarian` 是否正确挂接在闭环后段
    - 体系级对象之间是否出现职责漂移或关系断裂
    - 已切换到正式运行名的对象，是否仍被旧叙事拖回历史语义
    - `runtime_internal` 与 `private_only` 对象，是否被错误推成用户默认入口
- **质量层组**
  - 优先检查：
    - `spec-audit-surface`、`review-validation-surface`、`test-design-surface` 三面是否仍边界清晰
    - 三面是否分别承接输入审计、结果审查、测试设计，而没有重新混写
    - `综合验证（integrated-validator）` 是否仍保持主流程汇聚验证角色，而没有重新吞并质量层
    - 历史碎片对象是否仍被错误当作现役主对象，而不是专项子对象
    - 新对象当前是否已经完全摆脱旧碎片名称的运行面影响
    - 质量层对象是否被错误包装成用户直接入口，而不是作为运行面内部支撑对象

若当前分组结果无法稳定匹配既有组语义，则退回通用巡逻模式，仅基于对象类型执行巡逻。

### 2. 按对象类型执行巡逻

#### 2a. `skill` 对象

对每个 `skill` 的扫描，通过以下方式委托 Skill Scout：

**委托方式**：
- 引用 Skill Scout 的 Patrol 模式步骤链：`patrol-01-scan.md`（能力扫描）→ `patrol-02-diff.md`（差异分析）→ `patrol-03-report.md`（报告生成）。
- 将当前 skill 的信息（name、path、version、adaptation_summary、runtime_name_status、distribution_scope）作为 Patrol 扫描的输入。
- 接收 Patrol 模式返回的 `Patrol_Report`（包含 `status`、`opportunities`、`value_score`）。

**注意**：
- Squadron 不重复实现 Patrol 的搜索/对比逻辑，完全依赖 Skill Scout 的能力。
- 每个 `skill` 的 Patrol 扫描是独立的，一个 skill 的扫描结果不影响同组其他对象的扫描。

#### 2b. `workflow` 对象

对每个 `workflow` 对象，不委托 Skill Scout，而执行结构巡逻：

- 检查 workflow 的目标、步骤链和边界说明是否完整。
- 检查它与上下游对象的接口描述是否清楚。
- 检查它是否仍符合 `Workflow-first` 的结构定位。

当 workflow 属于特定组语义时，还应追加：

- **主流程前中段组中的 workflow**
  - 优先检查它是否造成主流程前段阶段混写
- **体系级与后段闭环组中的 workflow**
  - 优先检查它是否把知识沉淀、Reality 回写和 active 收口重新混回单一动作
- **质量层组中的 workflow**
  - 优先检查它是否把输入审计、结果审查、测试设计重新混回单一流程
  - 优先检查它是否越界承担 `综合验证（integrated-validator）` 的主流程汇聚职责

输出结果同样写入 `patrol_results`，但标记为 `workflow_reviewed` 或 `workflow_gaps_found`。

### 3. 展示进度信息

巡逻过程中持续向 Boya 展示进度：

```
🚁 编队巡逻进行中...

📍 当前组：{group_id}（{group_member_count} 个对象）
   🧭 组语义：{group_label 或 "未标注"}
   ✅ {completed_object_name} - 巡逻完成（发现 {N} 个问题或机会）
   🔄 {current_object_name} - 正在巡逻...
   ⏳ {pending_object_name} - 等待中

📊 总体进度：{completed_groups}/{total_groups} 组完成，{completed_objects}/{total_objects} 个对象已巡逻
```

### 4. 处理扫描失败

当某个对象的巡逻失败时：

- **记录失败原因**：将失败信息记录到该对象的结果中，标记 `status: scan_failed`。
- **跳过继续**：跳过该对象，继续巡逻同组内的其余对象。
- **同组全部失败**：若同组内所有对象扫描均失败，标记该组为"巡逻失败"，继续处理下一组。
- **所有组全部失败**：若所有组的所有对象扫描均失败，提示 Boya "编队巡逻全部失败"，展示失败原因汇总，中止流程。

### 5. 收集 Patrol_Report

将所有 Patrol_Report 按 Skill_Group 组织存储：

```yaml
patrol_results:
  - group_id: string
    group_label: string        # 可选：组语义标签
    members:
      - object_name: string
        object_kind: string     # skill / workflow
        runtime_name_status: string  # active_legacy_name / canonical_name_active
        distribution_scope: string   # user_visible / runtime_internal / private_only
        status: string          # opportunities_found / all_current / workflow_reviewed / workflow_gaps_found / scan_failed
        patrol_report:          # Patrol 模式返回的报告（scan_failed 时为 null）
          opportunities_count: integer
          top_opportunity: string
          value_score: float
        failure_reason: string  # 仅 scan_failed 时有值
```

## 输出格式

### 巡逻完成展示

```
🚁 编队巡逻完成！

---

**{group_id}** [优先级: {priority_score}]
- {object_1}: ✅ 发现 {N} 个优化机会（最高价值：{top_opportunity}）
- {object_2}: ✅ 当前能力保持先进
- {object_3}: ⚠️ workflow 发现结构缺口
- {object_4}: ❌ 扫描失败（原因：{failure_reason}）

**{group_id}** [优先级: {priority_score}]
- {skill_1}: ✅ 发现 {N} 个优化机会
- ...

---

📊 巡逻统计：
- 扫描组数：{completed_groups}/{total_groups}
- 巡逻对象数：{completed_objects}/{total_objects}
- 发现优化机会：{total_opportunities} 个
- 扫描失败：{failed_skills} 个
```

## 交互流程

### 正常流程

1. **开始巡逻**：向 Boya 提示"编队巡逻开始，按优先级顺序逐组扫描..."。
2. **逐组扫描**：每组开始和完成时展示进度。
3. **展示结果**：所有组扫描完成后，展示巡逻统计。
4. **自动流转**：将 `patrol_results` 传递给 `step-04-impact.md` 进行影响分析。

### 用户干预点

- Boya 可在巡逻过程中跳过某个组或某个对象。
- Boya 可中止巡逻，基于已有结果生成部分报告。

## 错误处理

| 错误场景 | 处理策略 |
|---------|---------|
| Skill Scout Patrol 模式不可用 | 提示 "Skill Scout Patrol 模式不可用，请检查 skill-scout 是否正确部署"，中止流程 |
| 某个对象的巡逻失败 | 记录失败原因，标记 `scan_failed`，跳过继续巡逻同组其余对象 |
| 同组内所有对象巡逻均失败 | 标记该组为 "巡逻失败"，继续处理下一组 |
| 所有组的所有对象巡逻均失败 | 提示 "编队巡逻全部失败"，展示失败原因汇总，中止流程 |

## 状态流转条件

- 当巡逻完成且至少一个对象存在优化机会或结构缺口时，将 `patrol_results` 作为输入，转入 `step-04-impact.md`。
- 当所有对象均无优化机会（`all_current` / `workflow_reviewed`）时，跳过影响分析，直接进入 `step-05-report.md` 生成报告。
- 当所有对象巡逻均失败时，中止流程。
