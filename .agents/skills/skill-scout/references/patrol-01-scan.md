---
name: patrol-01-scan
description: Patrol 模式 - 能力扫描，读取项目级治理对象清单并搜索外部相似资源
next_step: references/patrol-02-diff.md
---

# Patrol Step 1: Scan（能力扫描）

## 目标

读取项目级治理对象清单（`.agents/private-catalog.yaml`），针对其中处于 `active` 且 `object_kind: skill` 的条目，在 Source Registry 注册的外部资源来源中搜索相似或更优的资源，为后续差异分析提供候选列表。

## 输入

- `.agents/private-catalog.yaml`：项目级治理对象清单
- `references/source-registry.yaml`：外部资源来源注册表（内置层）
- `skill-sources.yaml`：用户自定义来源注册表（用户层，可选）

## 动作

### 1. 读取项目级治理对象清单

读取 `.agents/private-catalog.yaml`，获取所有已注册的治理对象条目。

**规则**：
- 若文件不存在或为空，触发错误处理流程（见下方"错误处理"）。
- 解析每个 PrivateCatalogEntry，提取 `name`、`path`、`source_url`、`adaptation_summary`、`version`、`status`、`object_kind`。
- **仅处理 `status: active` 且 `object_kind: skill` 的条目**，跳过 `deprecated` 条目与 `workflow` 条目。

### 2. 校验 Skill 路径

对每个 active `skill` 条目，检查其 `path` 指向的目录是否实际存在：

- **路径存在**：标记为"有效"，继续处理。
- **路径不存在**：标记为"路径缺失"，记录到扫描结果中，跳过该条目的外部搜索。

### 3. 计算 Effective Sources（有效来源集合）

通过 Source_Registry_Loader 从两个层级加载、合并来源配置，计算最终的 Effective Sources，再传递给偏好过滤流程。

#### 3a. 两层来源加载（Source_Registry_Loader）

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

#### 3b. 偏好过滤（现有机制不变）

若存在 `references/user-source-preferences.yaml`，在 Effective Sources 基础上按以下顺序应用偏好过滤：

1. `enabled_sources` 非空时，仅保留白名单来源
2. 剔除 `disabled_sources`
3. 应用 `preferred_types` 作为同优先级下的排序偏好
4. 应用 `priority_boost` 形成最终搜索权重

- 仅对偏好过滤后的最终来源执行后续搜索，而不是对全量来源表执行盲搜
- 按 `priority` 字段降序排列最终来源列表。

### 4. 逐项搜索外部相似资源

针对每个有效的私域 `skill`，在 Source Registry 中搜索相似或更优的外部资源：

1. **构建搜索上下文**：从私域 `skill` 的 `name`、`adaptation_summary` 中提取关键能力描述作为搜索关键词。
2. **逐来源搜索**：按优先级从高到低，在每个来源中搜索与当前私域 `skill` 功能相似的资源：
   - `github`：浏览仓库内容，识别功能相似或更优的 skill/工具/工作流。
   - `marketplace`：检索功能相似的插件、扩展或模板。
   - `community`：搜索相关讨论、教程或共享资源中的替代方案。
3. **记录来源状态**：若某个来源不可访问，标记为"已跳过"并记录原因，继续搜索下一个来源。

### 5. 生成候选列表

为每个私域 `skill` 生成对应的外部候选列表，每个候选项包含：

```yaml
scan_candidate:
  private_skill: string         # 对应的私域 skill 名称
  external_name: string         # 外部资源名称
  external_url: string          # 外部资源 URL
  source_type: string           # 来源类型（github/marketplace/community）
  similarity_summary: string    # 与私域 skill 的相似性摘要
  potential_improvements: string # 可能的改进点概述
```

## 输出格式

### 扫描结果

扫描完成后，以如下格式向用户展示结果：

```
🔎 能力扫描完成！共扫描 {N} 个私域 skill：

---

**{skill_name}**（v{version}）
- 路径：{path}
- 状态：✅ 有效
- 发现 {M} 个外部候选资源：
  1. {external_name} - {similarity_summary}
  2. ...

**{skill_name_2}**（v{version}）
- 路径：{path}
- 状态：⚠️ 路径缺失（建议清理清单）
- 外部搜索：已跳过

---

📊 扫描统计：
- 扫描 Skill 数：{有效数}/{总数}
- 路径缺失：{缺失数} 个
- 来源层级：内置 {N} 个, 用户 {M} 个, 合计 {X} 个
- 被覆盖：{覆盖条目列表（格式："条目名 (built-in → user)"），若无则显示"无"}
- 被屏蔽：{屏蔽条目列表（格式："条目名 (built-in, 被用户层屏蔽)"），若无则显示"无"}
- 已搜索来源：{已搜索数}/{总来源数}
- 跳过的来源：{跳过列表及原因，若无则显示"无"}
- 发现候选资源总数：{总候选数}
```

### 扫描结果数据

将完整的扫描结果以结构化格式保留，作为 `patrol-02-diff.md` 的输入：

```yaml
scan_result:
  scanned_at: string            # 扫描时间（ISO 8601 格式）
  total_skills: integer         # 总私域 skill 数
  valid_skills: integer         # 有效私域 skill 数
  missing_paths: integer        # 路径缺失数
  entries:
    - private_skill: string     # 私域 skill 名称
      version: string           # 当前版本
      path: string              # 部署路径
      path_valid: boolean       # 路径是否有效
      candidates:               # 外部候选列表
        - external_name: string
          external_url: string
          source_type: string
          similarity_summary: string
          potential_improvements: string
```

## 交互流程

### 正常流程

1. **开始扫描**：向用户提示"正在读取项目级治理对象清单..."。
2. **逐项搜索**：搜索过程中可向用户展示进度提示（如"正在扫描第 2/3 个 Skill：{name}..."）。
3. **展示结果**：按输出格式展示扫描结果和统计信息。
4. **自动流转**：扫描完成后，将 `scan_result` 传递给 `patrol-02-diff.md` 进行差异分析。
   - 若所有 Skill 均无候选资源，向用户说明"未发现外部相似资源，当前能力保持先进"，结束 Patrol 流程。
   - 若存在路径缺失的条目，建议用户在流程结束后清理项目级治理对象清单。

## 错误处理

| 错误场景 | 处理策略 |
|---------|---------|
| 项目级治理对象清单为空或不存在 | 向用户提示"项目级治理对象清单为空，请先通过 Scout 模式创建私域能力对象"，中止 Patrol 流程。 |
| 某个私域 `skill` 路径不存在 | 在扫描结果中标注该条目为"路径缺失"，建议用户清理清单，跳过该条目的外部搜索，继续扫描其余条目。 |
| 内置层 `source-registry.yaml` 不存在或为空 | 向用户提示"资源来源注册表为空，请先配置至少一个资源来源"，引导用户执行 Source Registry 管理操作，中止 Patrol 流程。 |
| 用户层 `skill-sources.yaml` 不存在 | 静默跳过，仅使用内置层，不产生错误或警告。 |
| 用户层文件存在但 YAML 解析失败 | 记录错误日志（说明解析失败原因），跳过用户层，回退到仅使用内置层，向用户展示警告信息（如"⚠️ 用户层来源配置解析失败，已回退到仅使用内置层"）。 |
| 用户层文件存在但 `sources` 为空列表 | 正常处理，等同于无用户自定义来源，仅使用内置层。 |
| 用户层条目缺少必需字段（`name`/`url`/`type`/`priority`） | 跳过该条目并记录警告（如"⚠️ 用户层条目缺少必需字段 {字段名}，已跳过"），继续处理其余条目。 |
| 某个来源不可访问 | 跳过该来源，在扫描统计中标注被跳过的来源及原因，继续搜索其余来源。若所有来源均不可访问，向用户说明情况并中止 Patrol 流程。 |
| 所有 skill 条目均为 deprecated 状态 | 向用户提示"所有私域 skill 条目均已标记为 deprecated，无需巡逻"，中止 Patrol 流程。 |

## 状态流转条件

- 当扫描完成且至少一个私域 `skill` 存在外部候选资源时，将 `scan_result` 作为输入，转入 `patrol-02-diff.md`。
- 当所有 Skill 均无候选资源时，标注"当前能力保持先进"，结束 Patrol 流程。
- 当项目级治理对象清单为空或 Source Registry 为空时，中止 Patrol 流程。
