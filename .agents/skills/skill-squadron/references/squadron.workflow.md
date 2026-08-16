---
name: squadron.workflow
description: 编队巡逻工作流 - 关联 skill 组的批量分析与协同优化
output_folder: .agents/skills
---

# Squadron Workflow (编队巡逻工作流)

**Goal**: 构建 skill 关系图，按关联组编队巡逻，评估跨 skill 影响，生成编队优化报告。

## 模式路由 (Mode Router)

根据用户触发词，分发到对应的步骤链：

| 触发词 | 目标模式 |
|-------|---------|
| `"启动编队巡逻"` / `"squadron 模式"` / `"开始编队分析"` | → **编队巡逻模式**（完整五步链） |
| `"分析 skill 关系"` / `"查看 skill 关系图"` | → **关系分析模式**（仅 graph → group） |

**路由规则**：
1. 解析用户输入，匹配上述触发词或语义等价表达。
2. 若无法判断模式，向用户确认意图后再分发。
3. 关系分析模式在展示分组结果后结束，用户可选择继续进入编队巡逻。

---

## 编队巡逻模式 (完整流程)

**目标**：构建关系图 → 分组 → 按组委托 Patrol 扫描 → 跨 skill 影响分析 → 生成编队报告。

### 步骤链

```
graph → group → patrol → impact → report
```

| 步骤 | 文件 | 说明 |
|-----|------|------|
| 1. Graph (关系图构建) | `step-01-graph.md` | 读取 `.agents/private-catalog.yaml` 构建 Relation_Graph |
| 2. Group (分组策略) | `step-02-group.md` | 基于连通分量算法分组，计算优先级评分 |
| 3. Patrol (编队巡逻执行) | `step-03-patrol.md` | 按组委托 Skill Scout Patrol 模式扫描 |
| 4. Impact (跨 skill 影响分析) | `step-04-impact.md` | 评估优化对关联 skill 的影响 |
| 5. Report (编队报告生成) | `step-05-report.md` | 生成按关联组组织的 Squadron_Report |

### 执行协议
1. 按顺序执行，**不得跳步**。
2. 每个步骤开始前，阅读对应的完整步骤文件。
3. 每个步骤的输出作为下一步骤的输入。
4. 步骤间通过文件化的中间产物（YAML/Markdown）传递数据，不依赖会话记忆。
5. 用户可在任意步骤中止流程。
6. Step 02 (Group) 完成后需等待 Boya 确认再继续巡逻。

---

## 关系分析模式 (简化流程)

**目标**：构建关系图 → 分组 → 展示结果。

### 步骤链

```
graph → group
```

仅执行 Step 01 和 Step 02，展示分组结果后结束。用户可选择继续进入编队巡逻（从 Step 03 开始）。

---

## 步骤架构原则

- **Micro-Steps**: 严格遵循 `step-*.md` 文件定义的原子操作。每个步骤文件是自包含的指令集，包含目标、动作、输入/输出格式和错误处理。
- **Isolation**: 内存中只加载当前步骤文件。步骤间通过文件化的中间产物（YAML/Markdown）传递数据，不依赖会话记忆。

## 初始化
1. 识别用户意图，根据模式路由表分发到对应模式。
2. 编队巡逻模式：阅读 `step-01-graph.md`，开始关系图构建。
3. 关系分析模式：阅读 `step-01-graph.md`，开始关系图构建（完成 group 后结束）。
