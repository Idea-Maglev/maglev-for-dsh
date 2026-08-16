---
name: step-03-evaluate
description: Scout 模式 - 评估选择，对候选 skill 进行详细评估并确认改造基线
next_step: references/step-04-adapt.md
---

# Step 3: Evaluate（评估选择）

## 目标

对用户从候选列表中选择的 SkillProfile 进行深入评估，获取该 skill 的完整内容并生成详细分析报告，帮助用户做出是否将其作为私域化改造基线的最终决策。

## 输入

来自 `step-02-search.md` 的用户选择的候选 SkillProfile：

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

以及来自 `step-02-search.md` 的联网校验记录：

```yaml
network_evidence:
  checked_urls:
    - string
  primary_baseline_candidate: string
  secondary_references:
    - string
  verified: true
```

## 动作

### 0. 先检查联网证据门槛

在开始评估前，必须先检查：

1. `network_evidence.verified` 是否为 `true`
2. `checked_urls` 是否非空
3. 当前候选是否来自已联网校验过的来源之一

若任一不满足：

- 立即停止本步骤
- 返回 `step-02-search.md`
- 不得继续生成评估结论

### 1. 获取完整内容

根据 SkillProfile 中的 `source_url` 和 `source_type`，获取该 skill 的完整内容：

- **github**：读取仓库的 README、核心源文件、配置文件和目录结构，提取完整的功能定义和实现细节。
- **marketplace**：获取插件/扩展的完整描述页、功能列表、版本信息和用户评价。
- **community**：获取完整的讨论帖/教程内容、附带的代码片段和相关资源链接。

**规则**：
- 若内容获取失败（网络问题、权限限制等），触发错误处理流程（见下方"错误处理"）。
- 获取的内容应尽可能完整，以确保后续分析的准确性。

### 2. 生成详细分析报告

基于获取的完整内容，从以下四个维度生成结构化的详细分析报告：

#### 2.1 能力边界分析

识别该 skill 的能力范围：

- **核心能力**：该 skill 能做什么，列出主要功能点。
- **能力上限**：该 skill 在什么条件下表现最佳。
- **能力局限**：该 skill 不能做什么，或在什么场景下表现不佳。
- **扩展潜力**：该 skill 是否支持扩展或自定义，扩展的难易程度。

#### 2.2 依赖项分析

梳理该 skill 的依赖关系：

- **外部依赖**：需要的第三方库、API、服务或工具。
- **环境依赖**：运行环境要求（操作系统、语言版本、框架版本等）。
- **数据依赖**：需要的输入数据格式、配置文件或预置数据。
- **依赖风险**：依赖项的维护状态、许可证兼容性和安全风险。

#### 2.3 兼容性评估

评估该 skill 与本仓库 Workflow-Driven Step Architecture 的兼容程度：

- **架构契合度**：该 skill 的结构是否接近 SKILL.md + workflow.md + step-*.md 的标准架构。
- **交互模式兼容性**：该 skill 的交互方式是否可适配为步骤链驱动的交互流程。
- **数据格式兼容性**：该 skill 的输入/输出格式是否可与本仓库现有数据模型对接。
- **与现有对象的关系**：是否与当前治理对象清单中的现役对象存在功能重叠、边界冲突或互补关系。

#### 2.4 改造工作量估算

评估将该 skill 私域化改造为符合本仓库标准的工作量：

- **改造难度**：low / medium / high（综合评估）。
- **预估步骤数**：改造后预计包含的 step-*.md 文件数量。
- **主要改造点**：需要修改或重写的核心部分列表。
- **预估耗时**：粗略的时间估算（如"约 1-2 轮对话"、"约 3-5 轮对话"）。

## 输出格式

### 详细分析报告

分析完成后，以如下格式向用户展示报告：

```
📋 详细评估报告：{name}

来源：{source_url}（{source_type}）
匹配度：{match_score}（{百分比}%）

---

### 🎯 能力边界

**核心能力：**
- {功能点 1}
- {功能点 2}
- ...

**能力上限：** {描述}

**能力局限：** {描述}

**扩展潜力：** {描述}

---

### 📦 依赖项

**外部依赖：**
- {依赖 1}（{说明}）
- {依赖 2}（{说明}）

**环境依赖：** {描述}

**数据依赖：** {描述}

**依赖风险：** {风险等级} - {说明}

---

### 🔗 兼容性评估

**架构契合度：** {high/medium/low} - {说明}

**交互模式兼容性：** {high/medium/low} - {说明}

**数据格式兼容性：** {high/medium/low} - {说明}

**与现有 skill 的关系：** {说明}

---

### ⚙️ 改造工作量

**改造难度：** {low/medium/high}

**预估步骤数：** {N} 个 step 文件

**主要改造点：**
1. {改造点 1}
2. {改造点 2}
3. ...

**预估耗时：** {时间估算}

---

✅ 是否将此 skill 作为改造基线？请确认，或选择返回候选列表重新选择。
```

## 交互流程

### 正常流程

1. **获取内容**：根据用户选择的 SkillProfile，获取完整内容。获取过程中可向用户展示进度提示（如"正在获取 {name} 的完整内容..."）。
2. **展示报告**：按输出格式展示详细分析报告。
3. **用户决策**：等待用户确认或调整。
   - 用户确认选择 → 将该 skill 标记为**改造基线**，进入 `step-04-adapt.md`。
   - 用户要求返回候选列表 → 返回 `step-02-search.md` 的候选列表，用户可选择其他候选项。
   - 用户要求评估另一个候选项 → 直接对新选择的 SkillProfile 重新执行本步骤。
   - 用户要求重新搜索 → 返回 `step-01-parse.md` 重新解析需求。

### 改造基线确认

当用户确认选择后，生成改造基线记录：

```yaml
adaptation_baseline:
  skill_name: string            # 选中的 skill 名称
  source_url: string            # 来源 URL
  source_type: string           # 来源类型
  evaluation_summary: string    # 评估摘要（一句话总结）
  confirmed: true               # 已确认
```

该记录作为 `step-04-adapt.md` 的输入。

## 错误处理

| 错误场景 | 处理策略 |
|---------|---------|
| 内容获取失败（网络问题/权限限制） | 向用户说明无法获取该 skill 的完整内容及原因，建议选择其他候选项或稍后重试。若用户坚持，基于已有的 SkillProfile 摘要信息生成简化版分析报告（标注"基于有限信息"）。 |
| 来源 URL 失效（404/仓库已删除） | 向用户说明该来源已不可用，建议从候选列表中选择其他项。将该来源标记为"失效"，建议用户后续清理 Source Registry。 |
| 内容过于简略（无法生成完整分析） | 基于可获取的信息生成部分分析报告，明确标注哪些维度因信息不足而无法评估，由用户决定是否继续。 |

## 状态流转条件

- 当用户确认选择某个候选 skill 作为改造基线（`confirmed: true`）时，将 `adaptation_baseline` 作为输入，转入 `step-04-adapt.md`。
- 当用户要求返回候选列表时，返回 `step-02-search.md`。
- 当用户要求重新搜索时，返回 `step-01-parse.md`。
