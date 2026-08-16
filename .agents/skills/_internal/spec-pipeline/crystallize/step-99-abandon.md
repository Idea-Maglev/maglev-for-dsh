---
name: 'step-99-abandon'
description: '废弃 Spec 并归档关联资产'
---

# 步骤 99: 废弃归档 (Abandonment)

## 目标
优雅地废弃一个 Spec 方案，保留历史痕迹但不干扰主线。

## 执行逻辑

### 1. 移动 Spec 资产
*   **Target**: `{project-root}/specs/20_evolution/active/{slug}/`
*   **Dest**: `{project-root}/specs/90_archive/abandoned/{date}-{slug}/`
*   **Action**: 移动整个文件夹。如果目标存在，追加时间戳后缀。

### 2. 标记原因
*   在 `00_index.md` (或该文件夹下任意显著位置) 顶部追加:
    > `> **ABANDONED**: 于 {Date} 归档。原因: {User Reason}`

### 3. 关闭关联 Issue
**如果** 存在 `issues/active/{slug}.md` 或关联 Issue:
*   **Move**: 将 Issue 移动到 `issues/closed/{date}-{slug}.md`。
*   **Append**: 在 Issue 末尾追加: "Closed via Abandonment Workflow. Reason: {User Reason}"。

### 4. 报告
"已废弃方案 '{slug}'。
- Spec 已归档至: `specs/90_archive/abandoned/...`
- Issue 已关闭。
- 只有 History 记得它来过。🥀"
