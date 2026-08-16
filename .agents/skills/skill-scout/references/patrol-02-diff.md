---
name: patrol-02-diff
description: Patrol 模式 - 差异分析，对比 Private Skill 与外部资源的功能差异并生成结构化分析报告
next_step: references/patrol-03-report.md
---

# Patrol Step 2: Diff（差异分析）

## 目标

接收 `patrol-01-scan.md` 输出的扫描结果，对每个 Private Skill 与其对应的外部候选资源进行深度对比，识别功能差异、架构改进和新增能力，生成结构化的 DiffAnalysis 报告，为后续报告生成提供数据基础。

## 输入

- `scan_result`：来自 `patrol-01-scan.md` 的扫描结果（含每个 Private Skill 的外部候选列表）
- `.agents/private-catalog.yaml`：私域能力清单（用于获取 Private Skill 的详细信息）

## 动作

### 1. 遍历扫描结果

读取 `scan_result.entries`，筛选出 `path_valid: true` 且 `candidates` 列表非空的条目，逐一进行差异分析。

**规则**：
- 若某个 Private Skill 的 `candidates` 为空，跳过该条目，在汇总中标注"无外部候选资源"。
- 若 `path_valid: false`，跳过该条目（已在 Scan 阶段标注路径缺失）。

### 2. 读取 Private Skill 内容

对每个待分析的 Private Skill：

1. 读取其 `path` 目录下的 `SKILL.md` 和 `references/` 下的步骤文件。
2. 从 `.agents/private-catalog.yaml` 中获取该条目的 `adaptation_summary`，了解原始改造意图。
3. 提取 Private Skill 的核心功能列表、交互流程和架构特征。

### 3. 读取外部候选资源内容

对每个候选资源（`scan_candidate`）：

1. 访问 `external_url`，获取外部资源的完整内容。
2. 提取外部资源的功能列表、架构设计和交互模式。
3. 若外部资源不可访问，标记为"资源不可访问"，跳过该候选项，继续处理下一个。

### 4. 执行功能对比

对 Private Skill 与外部候选资源进行逐维度对比：

#### 4.1 功能差异分析（feature_diff）

| 维度 | 说明 |
|-----|------|
| `added` | 外部资源具备、而 Private Skill 尚未实现的功能 |
| `removed` | Private Skill 具备、而外部资源未提供的功能（可能是私域定制特性） |
| `improved` | 两者均有，但外部资源的实现方式更优（需说明优化点） |

#### 4.2 架构改进分析（architecture_improvements）

从以下角度识别架构层面的改进机会：
- 步骤链设计是否更清晰、更模块化
- 数据模型是否更完整、更规范
- 错误处理是否更健壮
- 与其他工具的集成方式是否更优雅

#### 4.3 工作量评估（estimated_effort）

综合功能差异数量和架构改进复杂度，评估改造工作量：

| 等级 | 说明 |
|-----|------|
| `low` | 改动较小，主要为功能补充或文案优化，预计 1-2 小时内完成 |
| `medium` | 涉及部分步骤重构或新增步骤，预计半天内完成 |
| `high` | 需要大幅重构架构或步骤链，预计超过半天 |

#### 4.4 优化建议（recommendation）

基于差异分析结果，给出明确建议：

| 建议值 | 含义 |
|-------|------|
| `upgrade` | 外部资源明显更优，建议全面升级 Private Skill |
| `partial_merge` | 外部资源部分功能值得借鉴，建议选择性合并 |
| `skip` | 差异不显著或外部资源不适合私域场景，建议跳过 |

### 5. 生成 DiffAnalysis

为每对（Private Skill，外部候选资源）生成一份 DiffAnalysis，格式如下：

```yaml
diff_analysis:
  private_skill: string         # 私域能力名称
  external_resource: string     # 外部资源名称/URL
  feature_diff:
    added:                      # 外部有而私域无的功能
      - string
    removed:                    # 私域有而外部无的功能
      - string
    improved:                   # 外部实现更优的功能
      - feature: string
        description: string
  architecture_improvements:    # 架构层面的改进
    - string
  estimated_effort: string      # 预估改造工作量（low/medium/high）
  recommendation: string        # 建议（upgrade/partial_merge/skip）
```

**示例**：

```yaml
diff_analysis:
  private_skill: "zhiyin"
  external_resource: "https://github.com/example/ai-code-reviewer"
  feature_diff:
    added:
      - "支持多文件批量审查"
      - "集成 CI/CD 流水线触发"
    removed:
      - "中文注释规范检查（私域定制特性）"
    improved:
      - feature: "错误分类"
        description: "外部资源将错误分为 critical/warning/info 三级，比当前的二级分类更细致"
      - feature: "报告格式"
        description: "外部资源支持 Markdown 和 JSON 双格式输出，当前仅支持 Markdown"
  architecture_improvements:
    - "步骤链拆分更细，每个步骤职责更单一"
    - "引入了显式的状态机模型，状态流转更清晰"
  estimated_effort: "medium"
  recommendation: "partial_merge"
```

## 输出格式

### 差异分析进度展示

分析过程中，向用户展示进度：

```
🔍 正在执行差异分析...

[1/3] 分析 {private_skill_name} vs {external_name}
  ✅ 功能对比完成：新增 {N} 项，改进 {M} 项
  📊 建议：{recommendation}

[2/3] 分析 {private_skill_name_2} vs {external_name_2}
  ...
```

### 差异分析汇总

所有分析完成后，展示汇总结果：

```
📋 差异分析完成！共分析 {N} 对（Private Skill × 外部资源）：

---

**{private_skill_name}** vs **{external_name}**
- 新增功能：{added_count} 项
- 改进功能：{improved_count} 项
- 私域特有：{removed_count} 项
- 架构改进：{arch_count} 项
- 工作量：{estimated_effort}
- 建议：{recommendation_label}

---

📊 分析统计：
- 建议升级（upgrade）：{N} 个
- 建议部分合并（partial_merge）：{N} 个
- 建议跳过（skip）：{N} 个
- 跳过分析（资源不可访问）：{N} 个
```

其中 `recommendation_label` 对应：
- `upgrade` → 🔴 建议升级
- `partial_merge` → 🟡 建议部分合并
- `skip` → 🟢 建议跳过

## 交互流程

### 正常流程

1. **开始分析**：向用户提示"正在对 {N} 个 Private Skill 执行差异分析..."。
2. **逐对分析**：按顺序处理每对（Private Skill，外部候选资源），展示进度。
3. **展示汇总**：分析完成后展示汇总结果。
4. **自动流转**：将所有 DiffAnalysis 结果传递给 `patrol-03-report.md` 进行报告生成。
   - 若所有分析结果均为 `skip`，向用户说明"当前所有私域能力均保持先进，无需优化"，结束 Patrol 流程。

### 用户干预点

- 用户可在汇总展示后，要求查看某对分析的完整 DiffAnalysis 详情。
- 用户可手动标记某个分析结果为"忽略"，该条目将不进入后续报告。

## 错误处理

| 错误场景 | 处理策略 |
|---------|---------|
| 外部候选资源 URL 不可访问 | 跳过该候选项，在汇总中标注"资源不可访问"，继续处理其余候选项。 |
| Private Skill 目录存在但内容不完整（缺少 SKILL.md） | 标注该 Skill 为"内容不完整"，仅基于 `adaptation_summary` 进行有限对比，并在结果中注明数据不完整。 |
| 所有候选资源均不可访问 | 向用户提示"所有外部候选资源均无法访问，差异分析无法完成"，建议用户检查网络或更新 Source Registry，中止 Patrol 流程。 |
| 扫描结果为空或无有效条目 | 向用户提示"无有效扫描结果可供分析"，中止 Patrol 流程。 |

## 状态流转条件

- 当至少一个 DiffAnalysis 的 `recommendation` 为 `upgrade` 或 `partial_merge` 时，将所有 DiffAnalysis 结果传递给 `patrol-03-report.md`。
- 当所有 DiffAnalysis 的 `recommendation` 均为 `skip` 时，标注"当前能力保持先进"，结束 Patrol 流程。
- 当差异分析因错误无法完成时，向用户说明原因并中止 Patrol 流程。
