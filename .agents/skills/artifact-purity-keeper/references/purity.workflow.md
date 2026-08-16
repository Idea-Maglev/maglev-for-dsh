---
name: purity-keeper
description: 产物洁净度守护工作流
output_folder: .agents/skills/artifact-purity-keeper
---

# Purity Keeper Workflow

**Goal**: 在 AI 产出对外产物前后, 识别会话痕迹并按受众分级处置.

## 流程

1. 受众分级判断
2. 机械扫描
3. Finding 解读
4. 选择性修复

## 进入条件

- 产出 `artifact-external` 文件前 / 后
- 用户主动触发
- 上游流程在收尾节点显式转交

## 退出条件

满足任一:
1. 全部 finding 已处置 (修复 / 标记为协议引用 / 标记为可保留)
2. `artifact-external` 文件无 hard finding
3. 用户明确停止

## 最小产物

- 受众分级结论
- finding 报告 (按 severity 分组)
- 处置清单 (修复了哪些 / 保留了哪些 / 为什么)

## 步骤架构

- **Micro-Steps**: 严格按 `references/audience-rules.md` 与 `references/finding-interpretation.md`
- **Tool**: 本 skill 目录下 `scripts/scanner.py`

## 初始化

1. 阅读 `references/audience-rules.md`
2. 阅读 `references/finding-interpretation.md`
