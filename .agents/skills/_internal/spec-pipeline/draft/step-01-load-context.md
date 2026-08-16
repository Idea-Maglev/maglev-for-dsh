---
name: 'step-01-load-context'
description: '读取 Context 并决定设计策略'
nextStepFile: './step-02-polymorphic-design.md'
---

# 步骤 1: 加载与策略 (Load & Strategize)

## 目标
读取上游产出的 Json，并决定生成策略。

## 交互流程

### 1. 读取 Context
*   使用 `read_file` 读取 `{input_context}`。
*   提取 `intent` 和 `legacy_references`。

### 2. 决定策略 (Polymorphism)
向用户确认项目类型 (如果 Context 中未明确):
"为了生成最精准的设计蓝图，请确认当前工作区类型：
1. **Frontend / App**: 侧重页面交互与视觉还原。
2. **Backend / API**: 侧重接口定义与数据结构。
3. **Agent / Workflow**: 侧重 Prompt flow 与 Tool use。"

### 3. 设置策略变量
暂存 `design_strategy` = "frontend" | "backend" | "agent".

### 4. 前进
加载下一步: `{nextStepFile}`。
