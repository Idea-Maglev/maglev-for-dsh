---
name: step-01-analyze
description: 环境分析
next_step: references/step-02-inject.md
---

# Step 1: Environment Analysis (环境分析)

## 目标
扫描当前目录，确定初始化策略。

## 动作
1.  **List Files**: 检查根目录是否有文件。
2.  **Determine Mode**:
    *   **Greenfield**: 如果只有 `.git` 或 `README.md`。
    *   **Adoption**: 如果存在 `src`, `package.json`, `pom.xml` 或其他代码文件。
3.  **Confirm**: 告知用户当前判定，并请求确认。

## 交互示例
AI: "正在扫描...检测到这是一个全新的目录 (Greenfield)。"
User: "是的。"
AI: "Setting mode=GREENFIELD. Moving to Injection."

## 输出
更新 Frontmatter: `mode: GREENFIELD` 或 `mode: ADOPTION`。
