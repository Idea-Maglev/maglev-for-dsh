---
name: step-02-search
description: Scout 模式 - 资源搜索，在外部资源来源中搜索匹配的 skill 并生成候选列表
next_step: references/step-03-evaluate.md
---

# Step 2: Search（资源搜索）

## 目标

基于上一步确认的 SearchIntent，在 Source Registry 注册的外部资源来源中搜索匹配的 skill/workflow/工具，为每个搜索结果生成结构化的 SkillProfile，并按匹配度降序向用户展示候选列表。

## 强制要求

当本轮目标是：

- 新建独立 `skill`
- 重写现有 `skill` 的核心定义
- 为某对象正式定稿并落成 `skill`

则本步骤必须包含“实际联网检索证据”。

仅完成以下动作，不算完成本步骤：

- 只读取 `skill-sources.yaml`
- 只读取 `source-registry.yaml`
- 只凭已有记忆或仓库历史判断候选

至少必须完成：

1. 实际联网检索或打开高相似度来源
2. 记录至少 1 个主基线链接
3. 在 Search 产物中显式写出“联网校验记录”

## 输入

来自 `step-01-parse.md` 的已确认 SearchIntent：

```yaml
search_intent:
  capability_type: string       # 能力类型
  target_scenario: string       # 目标场景
  constraints:                  # 关键约束列表
    - string
  raw_description: string       # 原始自然语言描述
  confirmed: true               # 已确认
```

## 动作

### 1. 计算 Effective Sources（有效来源集合）

通过 Source_Registry_Loader 从两个层级加载、合并来源配置，计算最终的 Effective Sources，再传递给偏好过滤流程。

#### 1a. 两层来源加载（Source_Registry_Loader）

按以下五步流程执行：

**第 1 步：读取内置层**
- 加载 `references/source-registry.yaml` 中的 `sources` 列表作为基础来源集合。
- 若文件不存在或为空，触发错误处理流程（见下方"错误处理"）。
- 解析每个 SourceRegistryEntry，提取 `name`、`url`、`type`、`priority`、`description`。
- 为每个条目标注 `layer: built-in`。

**第 2 步：尝试读取用户层**
- 检查 `skill-sources.yaml` 是否存在。
- 若不存在 → 静默跳过，仅使用内置层，不产生错误或警告。
- 若存在但 YAML 解析失败 → 记录错误日志（说明解析失败原因），跳过用户层，回退到仅使用内置层，向用户展示警告信息。
- 若存在且 `sources` 为空列表 → 正常处理，等同于无用户自定义来源，仅使用内置层。
- 若存在且解析成功 → 进入合并流程。
- 若用户层条目缺少必需字段（`name`/`url`/`type`/`priority`）→ 跳过该条目并记录警告，继续处理其余条目。

**第 3 步：合并 & 冲突解决**
- 以内置层为基础集合，遍历用户层条目：
  - 若条目标记 `disabled: true` 且同名条目存在于内置层 → 从基础集合中移除该内置条目，记录"已屏蔽"。
  - 若同名条目存在于内置层（非 disabled）→ 用用户层条目覆盖内置层条目，记录"已覆盖"，标注 `layer: user`。
  - 若为新条目（内置层中无同名）→ 追加到基础集合，标注 `layer: user`。

**第 4 步：输出合并日志**
- 列出被覆盖的条目（原层级 → 覆盖层级）。
- 列出被屏蔽的条目。
- 统计各层级贡献的来源数量：内置 N 个、用户 M 个、合计 X 个。

**第 5 步：传递给偏好过滤**
- 将合并结果作为 Effective Sources 传递给后续偏好过滤流程。

#### 1b. 偏好过滤（现有机制不变）

若存在 `references/user-source-preferences.yaml`，在 Effective Sources 基础上按以下顺序应用偏好过滤：

1. `enabled_sources` 非空时，仅保留白名单来源
2. 剔除 `disabled_sources`
3. 应用 `preferred_types` 作为同优先级下的排序偏好
4. 应用 `priority_boost` 形成最终搜索权重

- 若 SearchIntent 能映射到某个场景档案（如 `spec_driven_development`），优先应用对应 `scenario_profiles`
- 仅对偏好过滤后的最终来源执行后续搜索，而不是对全量来源表执行盲搜

### 2. 按优先级权重搜索

按最终权重降序排列有效来源列表，从最高优先级来源开始逐一搜索：

1. **构建搜索上下文**：将 SearchIntent 中的 `capability_type`、`target_scenario` 和 `constraints` 组合为搜索关键词。
2. **逐来源搜索**：针对每个有效来源，根据其 `type` 执行对应的搜索策略：
   - `github`：浏览仓库 README、目录结构和子项目，识别与搜索关键词匹配的 skill/工具。
   - `marketplace`：在市场页面中检索与关键词匹配的插件、扩展或工作流模板。
   - `community`：在社区内容中搜索与关键词相关的讨论、教程或共享资源。
3. **记录来源状态**：若某个来源不可访问（网络问题、URL 失效等），标记为"已跳过"并记录原因，继续搜索下一个来源。

### 2.1 联网校验记录（强制）

对进入候选列表的高相似度来源，必须显式记录：

- 实际打开或检索到的链接
- 来源类型
- 该来源与 SearchIntent 的高相似度理由
- 本轮打算如何使用该来源：
  - 主改造基线
  - 辅助参照
  - 低优先级辅证

若无法联网：

- 必须明确记录“本轮缺少实际联网证据”
- 本轮不得进入 `evaluate`

### 3. 生成 SkillProfile

为每个搜索到的候选结果生成一份 SkillProfile，包含以下字段：

```yaml
skill_profile:
  name: string                  # 技能名称
  source_url: string            # 来源 URL
  source_type: string           # 来源类型（github/marketplace/community）
  capability_summary: string    # 能力摘要
  match_score: float            # 与需求的匹配度评分 (0.0 - 1.0)
  adaptation_difficulty: string # 适配难度（low/medium/high）
  tags:                         # 标签列表
    - string
```

**评分规则**：
- `match_score`：综合评估候选 skill 与 SearchIntent 的匹配程度，考虑以下因素：
  - 能力类型匹配度（权重 40%）：候选 skill 的核心能力是否与 `capability_type` 一致。
  - 场景契合度（权重 30%）：候选 skill 的适用场景是否覆盖 `target_scenario`。
  - 约束满足度（权重 20%）：候选 skill 是否满足 `constraints` 中列出的限制条件。
  - 来源质量（权重 10%）：来源的 `priority` 权重归一化后作为加分项。
- `adaptation_difficulty`：根据候选 skill 的复杂度、依赖项数量和与本仓库架构的差异程度评估：
  - `low`：结构简单，少量或无外部依赖，易于改造。
  - `medium`：有一定复杂度或依赖，需要适度改造。
  - `high`：结构复杂，依赖较多，改造工作量大。

### 4. 排序与截断

1. 将所有候选 SkillProfile 按 `match_score` **降序**排列。
2. 截取前 **5** 个候选项作为最终结果。
3. 若候选项不足 5 个，返回全部结果。

## 输出格式

### 候选列表

搜索完成后，以如下格式向用户展示结果：

```
🔍 搜索完成！共找到 {N} 个候选 skill（展示前 {M} 个）：

---

**#1 {name}**
- 来源：{source_url}（{source_type}）
- 能力摘要：{capability_summary}
- 匹配度：{match_score}（{百分比}%）
- 适配难度：{adaptation_difficulty}
- 标签：{tags}

**#2 {name}**
...

---

请选择一个候选项进行详细评估（输入编号），或告诉我需要调整搜索条件。
```

### 搜索元信息

在结果末尾附加搜索元信息，帮助用户了解搜索覆盖范围和来源层级分布：

```
📊 搜索统计：
- 来源层级：内置 {N} 个, 用户 {M} 个, 合计 {X} 个
- 被覆盖：{覆盖条目列表（格式："条目名 (built-in → user)"），若无则显示"无"}
- 被屏蔽：{屏蔽条目列表（格式："条目名 (built-in, 被用户层屏蔽)"），若无则显示"无"}
- 已搜索来源：{已搜索数}/{总来源数}
- 跳过的来源：{跳过列表及原因，若无则显示"无"}
- 搜索关键词：{capability_type} + {target_scenario}
- 联网校验链接：{链接列表，若无则必须写明“无，流程停止于 search”}
- 主基线候选：{名称}
- 辅助参照：{名称列表}
```

## 交互流程

### 正常流程

1. **执行搜索**：按上述动作依次执行，搜索过程中可向用户展示进度提示（如"正在搜索第 2/3 个来源..."）。
2. **展示结果**：按输出格式展示候选列表和搜索元信息。
3. **用户选择**：等待用户选择一个候选项进入详细评估（`step-03-evaluate.md`）。
   - 用户输入编号 → 将对应 SkillProfile 传递给下一步骤。
   - 用户要求调整搜索条件 → 返回 `step-01-parse.md` 重新解析。
   - 用户要求查看更多结果 → 若有更多候选项，展示下一批（每批 5 个）。

### 无结果流程

当搜索未找到任何匹配结果时，执行以下流程：

```
⚠️ 未找到匹配的候选 skill。

可能的原因：
- 搜索意图过于具体或小众
- 当前 Source Registry 中的来源覆盖范围有限

建议：
1. 调整搜索意图（返回需求解析步骤）
2. 扩展 Source Registry（添加更多资源来源）

请选择操作方向，或描述你想如何调整。
```

## 错误处理

| 错误场景 | 处理策略 |
|---------|---------|
| 内置层 `source-registry.yaml` 不存在或为空 | 向用户提示"资源来源注册表为空，请先配置至少一个资源来源"，引导用户执行 Source Registry 管理操作（添加来源），中止当前搜索流程。 |
| 用户层 `skill-sources.yaml` 不存在 | 静默跳过，仅使用内置层，不产生错误或警告。 |
| 用户层文件存在但 YAML 解析失败 | 记录错误日志（说明解析失败原因），跳过用户层，回退到仅使用内置层，向用户展示警告信息（如"⚠️ 用户层来源配置解析失败，已回退到仅使用内置层"）。 |
| 用户层文件存在但 `sources` 为空列表 | 正常处理，等同于无用户自定义来源，仅使用内置层。 |
| 用户层条目缺少必需字段（`name`/`url`/`type`/`priority`） | 跳过该条目并记录警告（如"⚠️ 用户层条目缺少必需字段 {字段名}，已跳过"），继续处理其余条目。 |
| 某个来源不可访问（网络问题/URL 失效） | 跳过该来源，在搜索元信息中标注被跳过的来源及原因（如"网络超时"、"URL 404"），继续搜索其余来源。若所有来源均不可访问，按"无结果流程"处理并额外说明来源不可访问的情况。 |
| 搜索无匹配结果 | 按"无结果流程"处理：说明可能原因，建议用户调整搜索意图或扩展 Source Registry。 |

## 状态流转条件

- 只有在完成“联网校验记录（强制）”后，才允许用户从候选列表中选择一个 SkillProfile 并转入 `step-03-evaluate.md`。
- 当用户要求调整搜索条件时，返回 `step-01-parse.md`。
- 当用户要求管理资源来源时，转入 Source Registry 管理流程。
