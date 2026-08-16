---
name: patrol-04-optimize
description: Patrol 模式 - 优化执行，根据用户选择备份原文件并生成更新后的私域 skill，更新项目级治理对象清单版本信息
next_step: null
---

# Patrol Step 4: Optimize（优化执行）

## 目标

接收 `patrol-03-report.md` 输出的 PatrolReport 和用户选择的优化条目，展示详细变更点，在用户确认后备份原有文件，基于 DiffAnalysis 和原有 Adaptation Spec 生成更新后的私域 `skill` 文件，并更新项目级治理对象清单中的版本号和最后优化日期。

## 输入

- `patrol_report`：来自 `patrol-03-report.md` 的巡逻报告
- `selected_opportunities`：用户选择的优化条目列表（来自 PatrolReport 的 `opportunities`）
- `.agents/private-catalog.yaml`：项目级治理对象清单

## 动作

### 1. 展示详细变更点

对每个用户选择的优化条目，读取对应的完整 DiffAnalysis，向用户展示详细变更信息：

**展示内容**：
- 新增功能列表（`feature_diff.added`）
- 改进功能列表（`feature_diff.improved`，含具体优化说明）
- 架构改进列表（`architecture_improvements`）
- 私域特有功能保留说明（`feature_diff.removed` 中的私域定制特性）
- 预估改造工作量（`estimated_effort`）

**等待用户逐项确认**：用户可对每个优化条目选择"确认执行"或"跳过"。

### 2. 备份原有文件

对每个用户确认执行的优化条目，在生成更新文件前，将原有私域 `skill` 的所有文件备份到版本化目录：

**备份目录结构**：

```
.agents/skills/{skill-name}/.backup/{version}/
```

其中 `{version}` 为当前 `.agents/private-catalog.yaml` 中该条目的版本号（如 `1.0.0`）。

**备份规则**：
1. 创建备份目录 `.agents/skills/{skill-name}/.backup/{version}/`。
2. 将 `{skill-name}/` 目录下的所有文件（含 `SKILL.md` 和 `references/` 下的所有步骤文件）完整复制到备份目录。
3. 在备份目录下创建 `backup-meta.yaml`，记录备份元信息：

```yaml
backup_meta:
  skill_name: string            # 私域 skill 名称
  backed_up_version: string     # 备份的版本号
  backup_time: string           # 备份时间（ISO 8601 格式）
  backup_reason: string         # 备份原因（如"Patrol 优化前备份"）
  files:                        # 备份的文件列表
    - string
```

4. 备份完成后，向用户确认"备份成功，共备份 {N} 个文件到 {backup_path}"。

### 3. 生成更新文件

备份成功后，基于以下输入生成更新后的私域 `skill` 文件：

**输入来源**：
- 原有私域 `skill` 文件（保留私域定制特性）
- DiffAnalysis 中的 `feature_diff.added`（新增功能）
- DiffAnalysis 中的 `feature_diff.improved`（改进功能）
- DiffAnalysis 中的 `architecture_improvements`（架构改进）
- 原有 `adaptation_summary`（确保私域定制意图不丢失）

**生成规则**：
1. **保留私域特性**：`feature_diff.removed` 中的私域定制功能必须保留，不得删除。
2. **合并新增功能**：将 `feature_diff.added` 中的功能整合到对应步骤文件中。
3. **应用改进**：按 `feature_diff.improved` 的描述更新对应功能的实现方式。
4. **架构优化**：若 `architecture_improvements` 涉及步骤链重构，相应调整步骤文件结构。
5. **文件结构合规**：更新后的私域 `skill` 必须仍包含符合 Workflow-Driven Step Architecture 标准的 `SKILL.md`、`workflow.md` 和所有 `step-*.md` 文件。

### 4. 校验更新文件

生成更新文件后，执行完整性校验：

**校验项**：
- `SKILL.md` 存在且包含有效 frontmatter
- `references/` 目录下存在 `workflow.md`（或对应的工作流文件）
- `references/` 目录下至少存在一个 `step-*.md` 文件
- 所有步骤文件的 `next_step` 串联完整（最后一步为 `null`）

**校验失败处理**：若校验未通过，自动回滚到备份版本（见"错误处理"）。

### 5. 更新项目级治理对象清单

校验通过后，更新 `.agents/private-catalog.yaml` 中对应条目的版本信息：

**更新字段**：
- `version`：版本号递增（遵循语义化版本规范，小版本优化递增 patch 位，如 `1.0.0` → `1.0.1`；架构重构递增 minor 位，如 `1.0.0` → `1.1.0`）
- `last_optimized`：更新为当前日期（ISO 8601 格式，如 `2025-07-15`）

**更新示例**：

```yaml
# 更新前
- name: "zhiyin"
  version: "1.0.0"
  last_optimized: "2025-07-11"

# 更新后（小版本优化）
- name: "zhiyin"
  version: "1.0.1"
  last_optimized: "2025-07-15"
```

## 输出格式

### 变更摘要展示

优化完成后，向用户展示完整的变更摘要：

```
✅ 优化执行完成！

---

### 变更摘要：{skill_name}（{old_version} → {new_version}）

**修改的文件列表**：
- `SKILL.md`：{修改说明，如"更新触发词描述"}
- `references/step-02-search.md`：{修改说明，如"新增多文件批量处理逻辑"}
- `references/step-03-evaluate.md`：{修改说明，如"优化错误分类为三级体系"}
- ...

**能力变化说明**：
- ✨ 新增：{新增功能描述}
- 🔧 改进：{改进功能描述}
- 🏗️ 架构：{架构改进描述}
- 🔒 保留：{保留的私域定制特性}

**备份位置**：`.agents/skills/{skill-name}/.backup/{old_version}/`
**新版本**：{new_version}
**优化日期**：{current_date}

---
```

### 多条目优化汇总

若用户选择了多个优化条目，在所有条目完成后展示总体汇总：

```
🎉 本次巡逻优化全部完成！

**优化统计**：
- 成功优化：{N} 个私域 skill
- 跳过：{M} 个（用户选择跳过）
- 失败回滚：{K} 个（已恢复到备份版本）

**项目级治理对象清单已更新**，所有版本号和优化日期已同步。
```

## 交互流程

### 正常流程

1. **展示变更点**：逐条展示用户选择的优化条目的详细 DiffAnalysis，等待用户逐项确认。
2. **执行备份**：对每个确认执行的条目，先备份原有文件，向用户确认备份成功。
3. **生成更新文件**：基于 DiffAnalysis 和原有 Adaptation Spec 生成更新后的文件。
4. **校验文件结构**：执行完整性校验，确保更新后的文件结构合规。
5. **更新清单**：校验通过后，更新 `.agents/private-catalog.yaml` 中的版本号和优化日期。
6. **展示变更摘要**：向用户展示完整的变更摘要（修改文件列表 + 能力变化说明）。
7. **结束流程**：Patrol 流程正常结束。

### 用户干预点

- 用户可在查看详细变更点后，选择"确认执行"或"跳过"某个优化条目。
- 用户可在备份完成后、生成更新文件前，选择"中止"当前条目的优化（备份将保留，原文件不变）。
- 用户可在变更摘要展示后，要求查看某个文件的具体修改内容。

## 错误处理

| 错误场景 | 处理策略 |
|---------|---------|
| 备份目录创建失败（如权限不足） | 中止当前条目的优化操作，向用户提示"备份失败，优化已中止，请检查文件系统权限"，跳过该条目，继续处理下一个。 |
| 备份过程中文件复制失败 | 中止当前条目的优化操作，清理已创建的不完整备份目录，向用户提示"备份不完整，优化已中止"，跳过该条目。 |
| 更新文件生成后校验失败（文件结构不合规） | 自动回滚：删除生成的更新文件，将备份目录中的文件恢复到原路径，向用户提示"校验失败，已自动回滚到备份版本 {version}"。 |
| 回滚操作失败 | 向用户提示"回滚失败，请手动从备份目录 {backup_path} 恢复文件"，提供备份目录路径和文件列表。 |
| `.agents/private-catalog.yaml` 更新失败 | 向用户提示"版本信息更新失败，请手动更新 `.agents/private-catalog.yaml` 中 {skill_name} 条目的 version 和 last_optimized 字段"，提供应更新的值。 |
| 用户选择的优化条目在 PatrolReport 中不存在 | 向用户提示"未找到对应的优化条目，请重新选择"，展示当前 PatrolReport 中的有效条目列表。 |

## 备份策略说明

```
.agents/skills/{skill-name}/
├── SKILL.md                          # 当前版本（已更新）
├── references/
│   ├── workflow.md                   # 当前版本（已更新）
│   └── step-*.md                     # 当前版本（已更新）
└── .backup/
    └── {old-version}/                # 备份目录（如 1.0.0/）
        ├── SKILL.md                  # 备份的原始文件
        ├── references/
        │   ├── workflow.md
        │   └── step-*.md
        └── backup-meta.yaml          # 备份元信息
```

**备份保留策略**：
- 每次优化前均创建新的版本化备份目录，历史备份不自动删除。
- 用户可随时从备份目录手动恢复任意历史版本。

## 状态流转条件

- 当所有用户确认的优化条目均成功完成（或跳过/回滚）后，Patrol 流程正常结束。
- 当用户选择跳过所有优化条目时，向用户提示"已跳过所有优化条目，Patrol 流程结束"，不执行任何文件修改。
- 当备份失败或校验失败触发回滚时，该条目标记为"失败"，继续处理下一个条目，不中止整体流程。
