---
name: board-workflow
description: 项目看板工作流，编排扫描、判断、映射与渲染。
---

# Project Board Workflow

**目标**: 扫描活跃需求，判断流程阶段，映射角色状态，输出持久化看板。

## 步骤序列

### Step 1: Scan (扫描)
读取 `references/step-01-scan.md`。
- 扫描 `specs/20_evolution/active/` 和 `issues/active/`
- 产出：ActiveItem 列表

### Step 2: Judge Stage (阶段判断)
读取 `references/step-02-judge-stage.md`。
- 对每个 ActiveItem 交叉验证证据
- 参考 `references/stage-evidence-rules.md`
- 产出：每个需求的 StageResult

### Step 3: Map Roles (角色映射)
读取 `references/step-03-map-roles.md`。
- 读取项目级配置和 spec 级覆盖
- 基于阶段推断角色状态
- 产出：每个需求的 RoleMapping

### Step 4: Render Board (渲染与持久化)
读取 `references/step-04-render-board.md`。
- 使用 `references/board-template.md` 渲染 Mermaid 看板
- 输出总看板和子看板
- 更新缓存

## 进入条件 (Entry Conditions)

- 当前在 Maglev 化项目仓库中
- 用户主动调用，或由其他 Skill 触发

## 退出条件 (Exit Conditions)

- `specs/20_evolution/board.md` 已更新
- 所有活跃 spec 的 `status.md` 已更新
- 缓存已刷新

## 容错规则

- 单条 ActiveItem 判定失败不终止整个流程
- 异常条目标记为 `stage: unknown, confidence: error`，附带错误原因
- 看板仍渲染其余正常条目，异常条目以 `uncertain` 样式展示并注明错误
