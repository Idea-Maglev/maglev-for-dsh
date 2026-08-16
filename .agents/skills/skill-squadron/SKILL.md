---
name: skill-squadron
description: 编队巡逻 - 关联 skill 组的批量分析与协同优化。
metadata:
  formal_action_name: 编队巡逻
  top_level_capability: 能力进化
  system_layer: Evolution & Governance Layer
  lifecycle_chain: governance_loop
  runtime_name_status: active_legacy_name
  distribution_scope: runtime_internal
  author: feiyu.gao
  last_updated: 2026-06-13
---

# Skill Squadron (编队巡逻)

> 结构动作名：`编队巡逻`
> 运行面名称：`skill-squadron`
> 这不等于已经完成正式物理改名。

## 概览 (Overview)

这是一个**关联能力对象组的批量分析与协同优化工具**。它弥补了 Skill Scout Patrol 模式逐个独立扫描对象、不考虑对象间协作关系的盲区。通过构建关系图、分组策略和跨对象影响分析，实现"关系发现 → 分组 → 编队巡逻 → 影响分析 → 编队报告"的上层编排。

核心能力：

- **关系图构建**：从 `.agents/private-catalog.yaml` 读取已纳入治理范围的能力对象间关系，构建邻接表形式的 Relation_Graph
- **智能分组**：基于连通分量算法将 skill 分为关联组，计算巡逻优先级
- **编队巡逻**：按组委托 Skill Scout 的 Patrol 模式执行单 skill 扫描
- **影响分析**：评估优化某个 skill 对关联 skill 的接口兼容性、数据流和行为影响
- **编队报告**：按关联组组织优化建议，标注影响等级和优化顺序
- **运行面命名状态感知**：显式识别 `runtime_name_status`，判断结构动作名与运行面名称之间是否仍存在理解成本或迁移风险
- **分发范围感知**：显式识别 `distribution_scope`，区分用户可见对象、运行面内部对象和私有对象，避免把不同分发面的治理逻辑混为一体
- **当前态清单原则**：`.agents/private-catalog.yaml` 只表示当前现役治理对象，不承担历史日志、旧名存根或 tombstone 记录职责；已被替代的对象不应继续以并列现役身份占位，历史脉络应写入 archive / thinking / release 文档

## 何时使用 (When to use)

- 想要批量分析多个能力对象之间的协作关系和优化机会时。
- 想要了解优化某个对象对其关联对象的影响时。
- 想要获得按关联组组织的系统性优化建议时。
- 想要可视化对象之间的调用链和数据共享关系时。
- 想要识别哪些对象仍在沿用历史运行名、哪些对象已经切到正式对象名时。

## 触发条件 (Triggers)

### 编队巡逻模式

以下触发词将进入完整的编队巡逻流程（关系图 → 分组 → 巡逻 → 影响分析 → 报告）：

- `"启动编队巡逻"`
- `"squadron 模式"`
- `"开始编队分析"`

### 关系分析模式

以下触发词将仅执行关系图构建和分组展示（不执行巡逻和影响分析）：

- `"分析 skill 关系"`
- `"查看 skill 关系图"`

## 交互模式 (Interaction)

- **Role**: 你是 **Squadron Commander (编队指挥官)**。
- **Protocol**: 行动前必须阅读完整的步骤文件，严格遵循步骤顺序，不得跳步。
  - 编队巡逻流程：`graph → group → patrol → impact → report`
  - 关系分析流程：`graph → group`（展示分组结果后结束）
- **Memory**: 所有中间产物（Relation_Graph、Skill_Group、Patrol_Report、Cross_Impact_Analysis、Squadron_Report）以 Markdown/YAML 文件持久化，不依赖会话记忆。
- **委托协作**: 编队巡逻阶段委托 Skill Scout 的 Patrol 模式执行单 skill 扫描，不重复实现搜索/对比逻辑。
- **命名状态**: 关系图、巡逻和报告阶段都应读取 `.agents/private-catalog.yaml` 中的 `runtime_name_status`，把命名状态视为正式巡逻维度，而不是补充备注。
- **分发范围**: 关系图、巡逻和报告阶段都应读取 `.agents/private-catalog.yaml` 中的 `distribution_scope`，把分发范围视为正式巡逻维度，而不是补充备注。
- **当前态优先**: 关系图、巡逻和报告阶段只以现行清单中的有效对象为准；如果清单里还残留旧名、替代项或历史占位，先按数据污染处理，不把它们展开成当前节点或历史叙事。

## 必需的参考资料 (References)

- 工作流入口: `references/squadron.workflow.md`
- 步骤定义:
  - `references/step-01-graph.md`（关系图构建）
  - `references/step-02-group.md`（分组策略）
  - `references/step-03-patrol.md`（编队巡逻执行）
  - `references/step-04-impact.md`（跨 skill 影响分析）
  - `references/step-05-report.md`（编队报告生成）
- 外部依赖:
  - `.agents/private-catalog.yaml`（项目级治理对象清单，含 `skills:` / `workflows:`、`relations`、`runtime_name_status`、`distribution_scope` 等字段；不是文件系统镜像）
  - Skill Scout 的 Patrol 模式（`patrol-01-scan.md` → `patrol-03-report.md`）

## 快速参考

- **Pattern**: Entry → Workflow → Micro-Steps（单模式，五步链）
- **Isolation**: 所有引用资源必须在 `references/` 下。
- **协作**: 编队巡逻阶段委托 Skill Scout Patrol 模式执行单 skill 扫描。
- **清单语义**: `.agents/private-catalog.yaml` 是现状清单，不是日志；巡逻时默认忽略历史占位与旧名存根。
- **当前默认编队**:
  - 主流程前中段组
  - 体系级与后段闭环组
  - 质量层组
- **当前额外巡逻维度**:
  - 运行面命名状态（`active_legacy_name` / `canonical_name_active`）
  - 分发范围（`user_visible` / `runtime_internal` / `private_only`）

## 示例

User: "启动编队巡逻"
AI: "收到。Squadron 模式已启动，正在读取私域能力清单并构建 skill 关系图... 发现 4 个 active skill，其中 3 个存在关系数据。关系图构建完成：4 个节点、5 条边、1 个孤立节点。正在执行分组..."

User: "分析 skill 关系"
AI: "收到。正在读取治理对象清单构建关系图... 当前发现主流程前中段组、体系级与后段闭环组、质量层组三类稳定对象组。"

User: "启动编队巡逻，顺便看下还有哪些对象在用旧运行名"
AI: "收到。Squadron 模式已启动，正在读取治理对象清单并构建关系图。除关系分组外，我还会显式检查各对象的运行面命名状态，识别哪些对象仍在使用历史运行名。"
