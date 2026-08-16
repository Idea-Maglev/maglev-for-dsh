---
name: step-05-register
description: Scout 模式 - 注册部署，将审核通过的私域能力对象部署并注册到能力清单
next_step: null
---

# Step 5: Register（注册部署）

## 目标

将用户审核通过的私域能力对象部署到目标位置，记录来源溯源信息，并将其注册到 `.agents/private-catalog.yaml` 项目级治理对象清单中，完成 Scout 模式的最后一步。

## 输入

来自 `step-04-adapt.md` 的审核通过数据：

```yaml
registration_input:
  object_name: string           # 私域对象名称（kebab-case）
  object_kind: string           # skill / workflow
  object_path: string           # 生成的文件所在路径（临时路径或目标路径）
  adaptation_spec:              # 完整的 AdaptationSpec
    baseline_skill: string
    baseline_source: string
    object_kind: string
    customizations:
      feature_trim:
        - string
      feature_extend:
        - string
      naming_convention: string
      interaction_style: string
      integrations:
        - skill_name: string
          relation: string
    created_at: string
  capability_summary: string    # 能力摘要（一句话描述）
```

以及本轮 Scout 的联网证据：

```yaml
network_evidence:
  checked_urls:
    - string
  primary_baseline_candidate: string
  verified: true
```

## 动作

### 0. 先检查联网证据门槛

若本轮缺少已通过校验的联网证据，则：

- 不得执行注册部署
- 不得写入 `.agents/private-catalog.yaml`
- 必须返回 `step-02-search.md`

### 1. 文件结构完整性校验

在部署前，对私域能力对象的文件结构执行完整性校验。

#### 1.1 `skill` 对象校验

| 文件 | 说明 |
|-----|------|
| `SKILL.md` | 技能入口文件，包含触发条件和 references 列表 |
| `references/{name}.workflow.md` | 工作流定义文件，包含步骤链路由 |
| `references/step-*.md`（至少一个） | 步骤文件，定义具体执行逻辑 |

**校验规则**：

1. 检查 `SKILL.md` 是否存在且包含有效的 frontmatter（`name`、`description` 字段）。
2. 检查自定义治理字段是否写在 `metadata` 下，而不是 frontmatter 顶层。
3. 检查 `metadata.author` 与 `metadata.last_updated` 是否存在；若 git 账号不可得，则允许 `author` 缺失，但不得伪造。
4. 检查 `references/` 目录下是否存在 `{name}.workflow.md` 文件。
5. 检查 `references/` 目录下是否存在至少一个 `step-*.md` 文件。
6. 检查所有 step 文件的 `next_step` 是否形成完整的链式串联（最后一个步骤的 `next_step` 为 `null`）。

**校验结果展示**：

```
🔍 文件结构校验中...

✅ SKILL.md — 存在，frontmatter 有效
✅ metadata — 结构字段位置正确，作者/更新时间已校验
✅ references/{name}.workflow.md — 存在
✅ references/step-01-{step1}.md — 存在
✅ references/step-02-{step2}.md — 存在
...（共 {N} 个步骤文件）
✅ 步骤链串联完整（step-01 → step-02 → ... → null）

校验通过，准备部署。
```

#### 1.2 `workflow` 对象校验

当 `object_kind: workflow` 时，至少检查：

1. workflow 文件存在。
2. 文件中清楚说明：
   - 目标
   - 步骤或阶段
   - 与上下游对象的关系
3. 路径位于 `.agents/workflows/{object_name}.md`。

若校验失败，列出缺失或异常项，中止部署并提示用户处理（见"错误处理"）。

### 2. 部署到目标位置

根据对象类型部署到目标路径：

- `skill`：`.agents/skills/{object_name}/`
- `workflow`：`.agents/workflows/{object_name}.md`

**部署操作**：
- 确认目标路径不存在同名对象（若存在，触发命名冲突处理）。
- 将生成文件复制/移动到目标路径。
- 部署完成后，再次确认目标路径下所有文件均已就位。

### 3. 记录来源溯源信息

从 `adaptation_spec` 中提取溯源信息，构建 PrivateCatalogEntry：

```yaml
# 溯源信息提取规则：
# - source_url: 取自 adaptation_spec.baseline_source
# - adaptation_date: 取自 adaptation_spec.created_at（ISO 8601 日期部分）
# - author: 优先取当前 git 账号；若取不到则留空或交由用户补充
# - last_updated: 使用当前日期（ISO 8601）
# - adaptation_summary: 基于 capability_summary + adaptation_spec.customizations 生成一句话摘要
```

**摘要生成规则**：

将以下信息组合为一句话摘要（不超过 100 字）：
- 基线 skill 名称（`baseline_skill`）
- 核心能力描述（`capability_summary`）
- 主要定制点（`feature_extend` 或 `feature_trim` 中最重要的 1-2 项）

示例：`"基于 {baseline_skill} 改造，{capability_summary}。主要定制：{主要定制点}。"`

### 4. 更新 `.agents/private-catalog.yaml`

将新的 PrivateCatalogEntry 写入 `.agents/private-catalog.yaml` 的对应列表中。这个文件只表示当前现状，不承担历史日志职责；旧名、替代项和历史占位不应作为并列现役对象长期保留。

- `object_kind: skill` → 追加到 `skills:`
- `object_kind: workflow` → 追加到 `workflows:`

```yaml
# PrivateCatalogEntry 格式
- name: string                  # 私域对象名称（与 object_name 一致）
  path: string                  # 部署路径
  formal_action_name: string    # 正式动作名
  top_level_capability: string  # 所属顶层能力
  object_kind: string           # skill / workflow
  source_url: string            # 原始来源 URL（取自 adaptation_spec.baseline_source）
  adaptation_date: string       # 改造日期（ISO 8601 格式，如 "2025-07-15"）
  adaptation_summary: string    # Adaptation Spec 摘要（见上方生成规则）
  author: string                # 作者（优先取当前 git 账号）
  version: string               # 初始版本号，固定为 "1.0.0"
  last_updated: string          # 最后更新时间（ISO 8601 格式）
  last_optimized: string        # 最后优化日期（与 adaptation_date 相同，初始值）
  status: string                # 初始状态，固定为 "active"
```

**写入规则**：
- 对于真正新增、仍处于现役的对象，在对应列表（`skills:` 或 `workflows:`）末尾追加新条目。
- 对于更名、替代、收束后的对象，不得同时保留旧名与新名作为并列现役对象；应先清理或改写被替代条目，再写入当前条目。
- 保留文件顶部的注释说明（`# Private Catalog - 私域能力清单` 等），但不要把它写成历史记录。
- 写入完成后，读取文件验证新条目已正确写入，且清单仍只反映当前现状。

## 输出格式

### 注册完成确认

注册成功后，向用户展示完整的注册结果：

```
🎉 私域对象注册部署完成！

📁 部署路径：{object_path}

📋 项目级治理对象清单已更新：
   名称：{object_name}
   来源：{source_url}
   改造日期：{adaptation_date}
   版本：1.0.0
   状态：active
   摘要：{adaptation_summary}

✅ {object_name} 已成功加入项目级治理对象清单。

Scout 模式流程完成。如需继续发现新技能，请重新触发 Skill Scout。
```

## 交互流程

### 正常流程

1. **执行校验**：对私域对象文件结构执行完整性校验，展示校验结果。
2. **确认部署**：向用户展示即将部署的目标路径，请求最终确认：
   ```
   📦 准备将 {object_name} 部署到 {object_path}
      并更新 `.agents/private-catalog.yaml`。

   确认部署？（确认后操作不可撤销）
   ```
3. **执行部署**：用户确认后，依次执行部署、溯源记录、清单更新。
4. **展示结果**：按输出格式展示注册完成确认信息。

### 用户取消流程

若用户在确认部署前选择取消：

```
⏸️ 部署已取消。

私域对象文件已生成但尚未部署。你可以：
1. 重新触发注册部署（返回本步骤）
2. 手动将文件复制到目标路径并更新 `.agents/private-catalog.yaml`
3. 放弃本次 Scout 流程
```

## 错误处理

| 错误场景 | 处理策略 |
|---------|---------|
| 文件结构校验失败（缺少 SKILL.md） | 列出缺失文件清单，提示用户选择：(1) 返回 `step-04-adapt.md` 重新生成；(2) 手动补充缺失文件后重新触发注册。 |
| 文件结构校验失败（缺少 workflow.md） | 同上，明确指出缺少工作流定义文件，建议重新生成对象文件结构。 |
| 文件结构校验失败（无 step-*.md 文件） | 同上，明确指出缺少步骤文件，建议重新生成对象文件结构。 |
| 步骤链串联不完整（next_step 断链） | 列出断链位置（如"step-02 的 next_step 指向不存在的文件"），提示用户手动修复对应步骤文件的 frontmatter。 |
| 目标路径已存在同名对象（命名冲突） | 提示用户该名称已被占用，展示已有对象的信息，询问：(1) 修改命名（返回 `step-04-adapt.md`）；(2) 覆盖已有对象（需二次确认，操作不可撤销）。 |
| `.agents/private-catalog.yaml` 写入失败 | 向用户展示应写入的 PrivateCatalogEntry 内容，提示手动追加到 `.agents/private-catalog.yaml` 的对应列表末尾。 |
| 部署过程中文件写入失败 | 中止部署，提示用户检查文件系统权限，展示已成功写入和未成功写入的文件列表，建议清理后重试。 |

## 状态流转条件

- 当 PrivateCatalogEntry 成功写入 `.agents/private-catalog.yaml` 且所有文件已部署到目标路径后，Scout 模式流程**完成**（`next_step: null`）。
- 当用户要求返回改造阶段时，返回 `step-04-adapt.md`。
- 当用户要求重新搜索时，返回 `step-01-parse.md`。
