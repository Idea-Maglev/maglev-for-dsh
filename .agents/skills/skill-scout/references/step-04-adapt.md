---
name: step-04-adapt
description: Scout 模式 - 私域化改造，收集个性化需求并生成适合的私域能力对象
next_step: references/step-05-register.md
---

# Step 4: Adapt（私域化改造）

## 目标

在用户确认改造基线后，引导用户提供个性化改造要求，将其结构化为 AdaptationSpec，然后根据对象形态选择：

- 生成独立 `skill`
- 或保持 `workflow-first`，直接生成 workflow 入口与配套治理信息

## 输入

来自 `step-03-evaluate.md` 的改造基线记录：

```yaml
adaptation_baseline:
  skill_name: string            # 选中的 skill 名称
  source_url: string            # 来源 URL
  source_type: string           # 来源类型
  evaluation_summary: string    # 评估摘要
  confirmed: true               # 已确认
```

以及本轮已通过校验的联网证据：

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

- 不得进入 AdaptationSpec 生成
- 不得调用 Skill Forge
- 必须返回 `step-02-search.md`

### 1. 引导用户提供改造要求

逐步引导用户明确以下个性化改造维度：

#### 1.1 功能裁剪（feature_trim）

向用户展示基线 skill 的功能列表，询问：
- "基线 skill 中有哪些功能是你**不需要**的？可以裁剪掉以保持精简。"
- 若用户无裁剪需求，记录为空列表。

#### 1.2 功能扩展（feature_extend）

询问用户：
- "你希望在基线 skill 的基础上**新增**哪些功能或能力？"
- 引导用户描述扩展需求的具体场景和预期行为。
- 若用户无扩展需求，记录为空列表。

#### 1.3 命名规范（naming_convention）

询问用户：
- "你希望这个私域对象叫什么名字？请提供一个符合 kebab-case 的名称（如 `my-sql-writer`）。"
- 检查名称是否与目标承载位置中的现有对象冲突。

#### 1.4 交互风格偏好（interaction_style）

询问用户：
- "你偏好什么样的交互风格？例如：简洁直接、详细引导、对话式、静默执行等。"
- 提供示例帮助用户选择。

#### 1.5 集成关系（integrations）

询问用户：
- "这个新对象需要与现有的哪些能力对象协作？请说明关系类型。"
- 展示当前已有的治理对象列表（从 `.agents/private-catalog.yaml` 读取）供参考。
- 关系类型包括：`调用`、`被调用`、`互补`。
- 若无集成需求，记录为空列表。

**规则**：
- 每个维度收集完毕后，向用户确认该维度的内容。
- 所有维度收集完毕后，汇总生成 AdaptationSpec 并请求用户最终确认。

### 2. 生成 AdaptationSpec

将用户的改造要求结构化为 AdaptationSpec：

```yaml
adaptation_spec:
  baseline_skill: string        # 改造基线 skill 名称
  baseline_source: string       # 基线来源 URL
  object_kind: string           # skill / workflow
  customizations:
    feature_trim:               # 功能裁剪
      - string
    feature_extend:             # 功能扩展
      - string
    naming_convention: string   # 命名规范（kebab-case）
    interaction_style: string   # 交互风格偏好
    integrations:               # 与现有 skill 的集成关系
      - skill_name: string
        relation: string        # "调用" / "被调用" / "互补"
  created_at: string            # ISO 8601 日期（自动填充）
```

生成后向用户展示完整的 AdaptationSpec，请求最终确认：

```
📝 私域化改造规格（AdaptationSpec）

基线 Skill：{baseline_skill}
基线来源：{baseline_source}
对象形态：{object_kind}

定制内容：
  功能裁剪：{feature_trim 列表或"无"}
  功能扩展：{feature_extend 列表或"无"}
  命名规范：{naming_convention}
  交互风格：{interaction_style}
  集成关系：{integrations 列表或"无"}

创建时间：{created_at}

✅ 请确认以上改造规格。确认后将按对象形态继续生成：
   - `skill` → 调用 Skill Forge
   - `workflow` → 直接生成 workflow 入口与治理登记
   如需修改，请指出需要调整的部分。
```

### 3. 选择对象生成路径

用户确认 AdaptationSpec 后，根据 `object_kind` 选择执行路径。

#### 3a. `skill` 路径：由 AI 助手直接生成独立 Skill

当 `object_kind: skill` 时，由 AI 助手根据 AdaptationSpec 直接生成符合当前仓库约定的 skill 文件结构。

##### 3a.1 组装生成输入

从 AdaptationSpec 中提取生成独立 skill 所需的核心输入：

- **`{{skill_name}}`**：取自 `customizations.naming_convention`
- **`{{description}}`**：基于 `baseline_skill` 的能力摘要 + 用户的 `feature_extend` 描述，生成一句话描述
- **`{{steps}}`**（List）：基于基线 skill 的步骤结构，结合 `feature_trim`（移除对应步骤）和 `feature_extend`（新增对应步骤）推导出最终步骤列表

同时确定以下辅助参数：

- **target_path**：`.agents/skills`
- **interaction_style**：用户的交互风格偏好
- **integrations**：与现有对象的集成关系
- **baseline_source**：基线来源 URL

Scout 需将上述输入组装为 `skill_metadata` 对象，格式如下：

```yaml
skill_metadata:
  skill_name: string        # ← customizations.naming_convention
  description: string       # ← 生成的一句话描述
  steps:                    # ← 推导后的最终步骤列表
    - string
  target_path: .agents/skills
```

##### 3a.2 直接生成 skill 文件结构

基于 `skill_metadata` 和当前仓库的 skill 结构约定，直接生成以下文件：

1. `{target_path}/{skill_name}/SKILL.md`
2. `{target_path}/{skill_name}/references/{skill_name}.workflow.md`
3. `{target_path}/{skill_name}/references/step-XX-{name}.md`

生成要求：

- 必须符合当前仓库的 `SKILL.md + workflow + step-*` 结构约定
- `SKILL.md` 顶层 frontmatter 只保留标准字段：`name`、`description`
- 自定义治理字段统一写入 `metadata`
- steps 必须形成完整的 `next_step` 链
- 文件内容应直接体现 AdaptationSpec 中的边界、交互风格和集成关系

##### 3a.2.1 `metadata` 字段要求

新生成的 `SKILL.md` 应至少补以下 `metadata` 字段：

- `formal_action_name`
- `top_level_capability`
- `system_layer`
- `lifecycle_chain`
- `runtime_name_status`
- `distribution_scope`
- `author`
- `last_updated`

其中：

- `author` 默认读取当前仓库作用域下的 git 账号（`git config user.name`）
- 若当前作用域取不到 git 账号，则不要伪造作者名；可留空或提示用户后补
- `last_updated` 使用当前日期，格式为 `YYYY-MM-DD`

##### 3a.3 Scout 后处理：注入定制内容

对象生成完成后，由 Scout（本步骤）执行以下定制内容注入：

- 将 `interaction_style` 写入 SKILL.md 的"交互模式"部分和各步骤文件的交互指令中
- 将 `integrations` 信息写入 SKILL.md 的"依赖与集成"部分中
- 在 SKILL.md 中记录 `baseline_source` 作为来源溯源信息
- 检查 `metadata.author` 与 `metadata.last_updated` 是否已按规则补齐

##### 3a.4 协作接口说明

Scout 与 AI 助手内建生成能力的职责边界：

| 职责 | Scout（本步骤） | AI 助手内建生成能力 |
|-----|----------------|-------------|
| 收集改造需求 | ✅ | — |
| 生成 AdaptationSpec | ✅ | — |
| 组装 `skill_metadata` | ✅ | — |
| 生成 skill 文件结构 | — | ✅ |
| 确保文件结构合规（Verify） | — | ✅ |
| 注入定制内容（interaction_style / integrations / baseline_source） | ✅ | — |
| 文件完整性最终校验 | ✅ | — |

#### 3b. `workflow` 路径：保持 `workflow-first`

当 `object_kind: workflow` 时，不调用额外的 skill 生成器，而直接生成：

- `.agents/workflows/{naming_convention}.md`
- 与该 workflow 对应的治理登记信息（供 `.agents/private-catalog.yaml` 使用）

处理规则：

1. workflow 文件必须说明：
   - 目标
   - 入口语义
   - 关键步骤或阶段
   - 与上下游对象的关系
2. workflow 不应伪装成 skill，也不应强行生成 `.agents/skills/{name}/` 目录。
3. 若该对象后续被证明适合独立 skill 化，应重新进入 `skill-scout` 回合，而不是在当前回合直接越级。

### 4. 展示文件清单与能力摘要

对象生成完成后，向用户展示完整的文件清单和能力摘要：

```
🎉 私域对象生成完成！

📁 文件清单：
  {根据 object_kind 展示 skill 或 workflow 的实际文件清单}

📋 能力摘要：
  名称：{naming_convention}
  描述：{description}
  基线来源：{baseline_source}
  步骤数：{N}
  交互风格：{interaction_style}
  集成关系：{integrations 摘要}

🔍 请审核以上文件清单和能力摘要。
   确认无误后，将进入注册部署阶段（step-05-register）。
   如需调整，请说明需要修改的部分。
```

**规则**：
- 展示前执行文件完整性校验：
  - `skill`：确认 `SKILL.md`、workflow.md 和所有 step-*.md 文件均已生成。
  - `workflow`：确认 workflow 文件和关键结构说明已生成。
- 若校验发现缺失文件，列出缺失项并提示用户选择重新生成或手动补充。

## 错误处理

| 错误场景 | 处理策略 |
|---------|---------|
| skill 文件生成失败（文件写入失败/结构不完整） | 保留已生成的 AdaptationSpec，向用户展示 Spec 内容，提示重新生成对象文件结构。 |
| 命名冲突（目标位置已存在同名对象） | 提示用户该名称已被占用，建议修改 `naming_convention` 或确认是否覆盖已有对象。 |
| 生成的文件结构不完整（缺少 SKILL.md/workflow.md/step-*.md） | 列出缺失文件清单，提示用户选择：(1) 重新生成对象文件结构；(2) 手动补充缺失文件。 |
| 用户中途取消改造 | 保留当前已收集的 AdaptationSpec（若已生成），提示用户可随时恢复流程。 |

## 状态流转条件

- 当用户审核通过私域对象的文件清单和能力摘要后，将以下数据作为输入，转入 `step-05-register.md`：
  - 生成的对象文件路径
  - AdaptationSpec 完整内容
  - 能力摘要
- 当用户要求返回评估阶段时，返回 `step-03-evaluate.md`。
- 当用户要求重新搜索时，返回 `step-01-parse.md`。
