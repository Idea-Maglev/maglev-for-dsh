---
name: 'step-05-adversarial-review'
description: '构建差异并调用对抗性审查任务'

workflow_path: '{project-root}/_bmad/bmm/workflows/bmad-quick-flow/quick-dev'
thisStepFile: './step-05-adversarial-review.md'
nextStepFile: './step-06-resolve-findings.md'
---

# 步骤 5: 对抗性代码审查

**目标：** 构建所有更改的 diff，调用对抗性审查任务，呈现发现。

---

## 可用状态

来自之前的步骤：

- `{baseline_commit}` - 工作流开始时的 Git HEAD (对于 diff 而言至关重要)
- `{execution_mode}` - "tech-spec" 或 "direct"
- `{tech_spec_path}` - 技术规范文件 (如果为模式 A)

---

### 1. 构建 Diff

构建自工作流开始以来所有更改的完整 diff。

### 如果 `{baseline_commit}` 是 Git commit hash:

**跟踪的文件更改：**

```bash
git diff {baseline_commit}
```

**新的未跟踪文件：**
仅包含您在此工作流期间创建的未跟踪文件（步骤 2-4）。
不要包含预先存在的未跟踪文件。
对于创建的每个新文件，将其完整内容包含为“新文件”添加。

### 如果 `{baseline_commit}` 是 "NO_GIT":

使用尽力而为的 diff 构建：

- 列出您在步骤 2-4 中修改的所有文件
- 对于每个文件，显示您所做的更改（如果您记得之前/之后，或者只是当前状态）
- 包含您创建的任何新文件的完整内容
- 注意：这不如 Git diff 精确，但仍可实现有意义的审查

### 捕获为 {diff_output}

将所有更改合并到 `{diff_output}` 中。

**注意：** 不要 `git add` 任何东西 - 这是只读检查。

---

### 2. 调用对抗性审查

构建 `{diff_output}` 后，调用审查任务。如果可能，利用信息不对称：在单独的子代理或进程中运行此步骤（且仅运行此步骤），该子代理或进程具有对项目的读取访问权限，但除 `{diff_output}` 外没有任何上下文。

```xml
<invoke-task>Review {diff_output} using {project-root}/_bmad/core/tasks/review-adversarial-general.xml</invoke-task>
```

**平台回退：** 如果任务调用不可用，加载任务文件并内联遵循其说明，传递 `{diff_output}` 作为内容。

任务应：审查 `{diff_output}` 并返回发现列表。

---

### 3. 处理发现

从任务输出中捕获发现。
**如果零发现：** 停止 - 这很可疑。重新分析或请求用户指导。
评估严重性（严重、高、中、低）和有效性（真实、噪音、未定）。
除非明确要求，否则不要根据严重性或有效性排除发现。
按严重性排序发现。
为排序后的发现编号（F1, F2, F3 等）。
如果 TodoWrite 或类似工具可用，将每个发现转换为待办事项，在待办事项中包含 ID、严重性、有效性和描述；否则将发现作为表格呈现，包含列：ID、严重性、有效性、描述

---

## 下一步

有了发现后，完整阅读并遵循：`step-06-resolve-findings.md` 以供用户选择解决方案。

---

## 成功指标

- 从 baseline_commit 构建 diff
- 新文件包含在 diff 中
- 使用 diff 作为输入调用任务
- 收到发现
- 发现处理成待办事项或表格并呈现给用户

## 失败模式

- 缺少 baseline_commit (无法构建准确的 diff)
- 未在 diff 中包含新的未跟踪文件
- 调用任务而不提供 diff 输入
- 接受零发现而不质疑
- 在没有明确指示的情况下呈现比审查任务返回的更少的发现
