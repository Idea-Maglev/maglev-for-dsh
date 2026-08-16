---
name: 'step-06-resolve-findings'
description: '交互式处理审查发现，应用修复，用最终状态更新技术规范'

workflow_path: '{project-root}/_bmad/bmm/workflows/bmad-quick-flow/quick-dev'
thisStepFile: './step-06-resolve-findings.md'
---

# 步骤 6: 解决发现

**目标：** 交互式处理对抗性审查发现，应用修复，定稿技术规范。

---

## 可用状态

来自之前的步骤：

- `{baseline_commit}` - 工作流开始时的 Git HEAD
- `{execution_mode}` - "tech-spec" 或 "direct"
- `{tech_spec_path}` - 技术规范文件 (如果为模式 A)
- 来自 step-05 的发现表

---

## 解决方案选项

呈现： "您想如何处理这些发现？"

显示：

**[W] 逐个排查 (Walk through)** - 逐个讨论发现
**[F] 自动修复 (Fix automatically)** - 自动修复分类为 "real" 的问题
**[S] 跳过 (Skip)** - 确认并继续提交

### 菜单处理逻辑：

- 如果 W: 执行下方的 逐个排查 部分
- 如果 F: 执行下方的 自动修复 部分
- 如果 S: 执行下方的 跳过 部分

### 执行规则：

- 始终 在展示菜单后停止并等待用户输入
- 仅 当用户做出选择时才继续

---

## 逐个排查 [W]

对于每个发现（按顺序）：

1. 呈现带有上下文的发现
2. 询问： **fix now (现在修复) / skip (跳过) / discuss (讨论)**
3. 如果 fix: 立即应用修复
4. 如果 skip: 记录为已确认，继续
5. 如果 discuss: 提供更多上下文，重新询问
6. 移动到下一个发现

处理完所有发现后，总结已修复/跳过的内容。

---

## 自动修复 [F]

1. 过滤发现，只保留分类为 "real" 的发现
2. 对每个真实发现应用修复
3. 报告已修复内容：

```
**已应用自动修复：**
- F1: {修复描述}
- F3: {修复描述}
...

已跳过 (噪音/不确定): F2, F4
```

---

## 跳过 [S]

1. 确认所有发现都已审查
2. 注意用户选择在不修复的情况下继续
3. 继续完成

---

## 更新技术规范 (仅限模式 A)

如果 `{execution_mode}` 是 "tech-spec":

1. 加载 `{tech_spec_path}`
2. 将状态更新为 "Completed" (已完成)
3. 添加审查说明：
   ```
   ## Review Notes
   - Adversarial review completed
   - Findings: {count} total, {fixed} fixed, {skipped} skipped
   - Resolution approach: {walk-through/auto-fix/skip}
   ```
4. 保存更改

---

## 完成输出

```
**审查完成。准备提交。**

**实施摘要：**
- {实施了什么}
- 修改的文件： {count}
- 测试： {status}
- 审查发现： {X} 已解决, {Y} 已跳过

{根据 user_skill_level 解释实施了什么}
```

---

## 工作流完成

这是最后一步。Quick Dev 工作流现在已完成。

用户可以：

- 提交更改
- 运行额外测试
- 开始新的 Quick Dev 会话

---

## 成功指标

- 向用户呈现解决方案选项
- 正确执行所选方法
- 清晰地应用修复（如果适用）
- 使用最终状态更新技术规范（模式 A）
- 提供完成摘要
- 用户了解实施了什么

## 失败模式

- 未呈现解决方案选项
- 自动修复 "noise" 或 "uncertain" 发现
- 解决后未更新技术规范（模式 A）
- 无完成摘要
- 让用户不清楚下一步该做什么
