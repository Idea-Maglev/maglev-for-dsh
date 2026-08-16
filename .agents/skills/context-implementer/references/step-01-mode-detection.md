---
name: 'step-01-mode-detection'
description: '确定执行模式（技术规范 vs 直接），处理升级，设置状态变量'

workflow_path: '{project-root}/_bmad/bmm/workflows/bmad-quick-flow/quick-dev'
thisStepFile: './step-01-mode-detection.md'
nextStepFile_modeA: './step-03-execute.md'
nextStepFile_modeB: './step-02-context-gathering.md'
---

# 步骤 1: 模式检测

**目标：** 确定执行模式，捕获基线，并在需要时处理升级。

---

## 状态变量 (立即捕获，全程持久化)

这些变量必须在此步骤中设置，并可供所有后续步骤使用：

- `{baseline_commit}` - 工作流开始时的 Git HEAD (如果不是 git 仓库，则为 "NO_GIT")
- `{execution_mode}` - "tech-spec" (技术规范) 或 "direct" (直接)
- `{tech_spec_path}` - 技术规范文件的路径 (如果为模式 A)

---

## 执行序列

### 1. 捕获基线

首先，检查项目是否使用 Git 版本控制：

**如果 Git 仓库存在** (`.git` 目录存在或 `git rev-parse --is-inside-work-tree` 成功):

- 运行 `git rev-parse HEAD` 并将结果存储为 `{baseline_commit}`

**如果不是 Git 仓库:**

- 设置 `{baseline_commit}` = "NO_GIT"

### 2. 加载项目上下文

检查 `{project_context}` 是否存在 (`**/project-context.md`)。如果找到，将其作为所有实施决策的基础参考加载。

### 3. 解析用户输入

分析用户的输入以确定模式：

**模式 A: 技术规范 (Tech-Spec)**

- 用户提供了技术规范文件的路径 (例如，`quick-dev tech-spec-auth.md`)
- 加载规范，提取任务/上下文/验收标准 (AC)
- 设置 `{execution_mode}` = "tech-spec"
- 设置 `{tech_spec_path}` = 提供的路径
- **下一步:** 完整阅读并遵循：`step-03-execute.md`

**模式 B: 直接指令 (Direct Instructions)**

- 用户直接提供任务描述 (例如，`refactor code_storages/main/src/foo.ts...`)
- 设置 `{execution_mode}` = "direct"
- **下一步:** 评估升级阈值，然后继续

---

## 升级阈值 (仅限模式 B)

以最少的 token 使用情况评估用户输入（不加载文件）：

**触发升级 (如果存在 2+ 个信号):**

- 提到多个组件 (dashboard + api + database)
- 系统级语言 (platform, integration, architecture)
- 对方法的不确定性 ("how should I", "best way to")
- 多层范围 (UI + backend + data together)
- 延长时间框架 ("this week", "over the next few days")

**降低信号:**

- 简单标记 ("just", "quickly", "fix", "bug", "typo", "simple")
- 专注于单个文件/组件
- 自信、具体的请求

使用整体判断，而不是机械的关键词匹配。

---

## 升级处理

### 无升级 (简单请求)

显示： "**选择：** [P] 先计划 (tech-spec) [E] 直接执行"

#### 菜单处理逻辑：

- 如果 P: 指导用户到 `{quick_spec_workflow}`。 **退出 Quick Dev。**
- 如果 E: 询问是否有任何额外的指导，然后 **下一步:** 完整阅读并遵循：`step-02-context-gathering.md`

#### 执行规则：

- 始终 在展示菜单后停止并等待用户输入
- 仅 当用户做出选择时才继续

---

### 升级触发 - 级别 0-2

呈现： "这一起来像是一个具有多个组件的重点功能。"

显示：

**[P] 先计划 (tech-spec)** (推荐)
**[W] 似乎比 quick-dev 更大** - 推荐完整的 BMad Flow PRD 流程
**[E] 直接执行**

#### 菜单处理逻辑：

- 如果 P: 指导用户到 `{quick_spec_workflow}`。 **退出 Quick Dev。**
- 如果 W: 指导用户运行 PRD 工作流。 **退出 Quick Dev。**
- 如果 E: 询问指导，然后 **下一步:** 完整阅读并遵循：`step-02-context-gathering.md`

#### 执行规则：

- 始终 在展示菜单后停止并等待用户输入
- 仅 当用户做出选择时才继续

---

### 升级触发 - 级别 3+

呈现： "这听起来像平台/系统工作。"

显示：

**[W] 开始 BMad 方法** (推荐)
**[P] 先计划 (tech-spec)** (轻量级规划)
**[E] 直接执行** - 感觉运气好

#### 菜单处理逻辑：

- 如果 P: 指导用户到 `{quick_spec_workflow}`。 **退出 Quick Dev。**
- 如果 W: 指导用户运行 PRD 工作流。 **退出 Quick Dev。**
- 如果 E: 询问指导，然后 **下一步:** 完整阅读并遵循：`step-02-context-gathering.md`

#### 执行规则：

- 始终 在展示菜单后停止并等待用户输入
- 仅 当用户做出选择时才继续

---

## 下一步指令

**关键：** 当此步骤完成时，明确说明要加载哪个步骤：

- 模式 A (技术规范): "**下一步:** 完整阅读并遵循：`step-03-execute.md`"
- 模式 B (直接，选择 [E]): "**下一步:** 完整阅读并遵循：`step-02-context-gathering.md`"
- 升级 ([P] 或 [W]): "**退出 Quick Dev。** 遵循指导的工作流。"

---

## 成功指标

- `{baseline_commit}` 捕获并存储
- `{execution_mode}` 确定 ("tech-spec" 或 "direct")
- `{tech_spec_path}` 设置 (如果为模式 A)
- 项目上下文加载 (如果存在)
- 适当评估升级 (模式 B)
- 提明确的下一步指令

## 失败模式

- 在未捕获基线提交的情况下继续
- 未设置 execution_mode 变量
- 当模式 A (提供技术规范) 时加载 step-02
- 尝试在升级后“返回”而不是退出
- 步骤完成时没有明确的下一步指令
