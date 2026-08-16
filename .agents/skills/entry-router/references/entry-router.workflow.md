---
name: entry-router
description: 在会话入口识别请求、判断路径并交接给后续专长对象
output_folder: .agents/skills/entry-router
---

# Entry Router Workflow

**Goal**: 在会话入口完成 triage、route 与 handoff，避免入口对象继续吞并主流程能力。

## 流程 (Process)

1. 扫描入口信号
2. 评估上下文成熟度
3. 选择下游路径
4. 执行 handoff

## 进入条件 (Entry Conditions)

- 当前会话刚开始，尚未进入明确专长对象
- 用户表达混合了多个阶段或多个可能路径
- 需要先判断“现在最该进入哪条主线”

## 退出条件 (Exit Conditions)

满足以下条件即可结束入口层：

1. 已选定唯一主去向
2. 已给出最小必要交接说明

## 最小产物 (Minimum Deliverables)

- 入口类型判断
- 唯一路由结果
- 一句路由理由
- 最小 handoff 指令

## 步骤架构

- **Micro-Steps**: 严格遵循 `step-*.md`
- **Isolation**: 内存中只加载当前步骤

## 初始化

1. 阅读 `references/step-01-scan-entry.md`
