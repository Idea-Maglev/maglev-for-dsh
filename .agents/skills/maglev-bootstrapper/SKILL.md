---
name: maglev-bootstrapper
description: 自动初始化 Maglev 环境 (Greenfield/Brownfield)，包含交互式仓库注册。
metadata:
  formal_action_name: 整体接入初始化
  top_level_capability: 整体接入
  system_layer: Infrastructure Layer
  lifecycle_chain: system_enablement
  runtime_name_status: active_legacy_name
  distribution_scope: runtime_internal
  version: "2.0 (Repo-Aware Edition)"
---

# Maglev Bootstrapper (启动器)

> 结构动作名：`整体接入初始化`
> 运行面名称：`maglev-bootstrapper`
> 这不等于已经完成正式物理改名。

## 概览 (Overview)

将 `maglev_init_guide.md` 的初始化流程自动化。它负责分析当前目录状态，注入 Maglev 核心结构，并**交互式收集代码仓库信息**。

## 何时使用 (When to use)

- 对一个新仓库进行 Maglev 初始化时 (Greenfield)。
- 对一个现有仓库进行 Maglev 改造时 (Brownfield/Adoption)。
- 用户输入 `/maglev-init` 或 "Initialize Maglev" 时。

## 交互模式 (Interaction)

Skill 扮演 **[Architect]** 角色，执行以下阶段：

### Phase 1: Analyze (环境分析)

扫描当前目录，确定接入策略 (Greenfield vs Adoption)。

### Phase 2: Inject (骨架注入)

物理复制核心骨架：`.agents/`, `.maglev/`, `specs/`, `docs/`, `issues/`。

### Phase 3: Configure & Register (配置与仓库登记)

**交互式询问用户以下信息**:

```markdown
### 请告诉我您的代码仓库信息

为了让我更好地理解您的项目，请告诉我：

1. **代码仓库路径**: 哪些目录是代码仓库？(相对于当前目录)
   - 例如：`./frontend-repo`, `./backend-repo`, `./src`

2. **仓库类型**: 每个仓库是什么类型？
   - Frontend (前端)
   - Backend (后端)
   - Library (库)
   - Monorepo (单体仓库)
   - Other (其他)

3. **简要描述**: 每个仓库做什么？(一句话)
   - 例如："Vue 3 SPA 前端应用" 或 "Spring Boot RESTful API"

---

**示例输入**:
| 路径 | 类型 | 描述 |
| :--- | :--- | :--- |
| `./collab-hub` | Frontend | Vue 3 协作平台前端 |
| `./collabhub` | Backend | Spring Boot 协作平台后端 |
```

**根据用户回答，生成/更新 `specs/10_reality/crosscutting/repository-map/repositories.md`，并在存在 Profile 时登记该页。**

### Phase 4: Verify (自检)

运行自检，确认所有核心文件与 AI context 都达到最小可用标准。

---

## 受管仓库清单输出格式

```markdown
# 受管仓库清单

> 本文件记录当前 Maglev 治理范围内的所有代码仓库。
> **Last Updated**: {DATE}

## 代码仓库列表

| 仓库名称 | 路径     | 类型                                | 状态   | 描述       |
| :------- | :------- | :---------------------------------- | :----- | :--------- |
| {name}   | `{path}` | {Frontend/Backend/Library/Monorepo} | Active | {简要描述} |
```

---

## 必需的参考资料 (References)

- 工作流入口: `references/bootstrapper.workflow.md`
- 步骤 1: `references/step-01-analyze.md`
- 步骤 2: `references/step-02-inject.md`
- 步骤 3: `references/step-03-config.md`
- 步骤 4: `references/step-04-ai-context-check.md`

## 快速参考

- **Greenfield**: 直接创建完整骨架，询问用户代码仓库信息。
- **Adoption**: 仅创建治理层，扫描现有目录并询问用户确认哪些是代码仓库。
- **AI Context Check**: 初始化结束后，检查 `AGENTS.md` / `llms.txt` 是否已经足以辅助 AI 理解项目与 Maglev 操作。

## 示例

```
User: "Initialize Maglev here."
AI: "收到。启动 Bootstrapper。正在扫描目录结构..."
AI: "检测到 2 个可能的代码目录：`./frontend`, `./backend`。请确认它们是代码仓库吗？分别是什么类型？"
User: "是的，frontend 是 Vue 前端，backend 是 Go 后端。"
AI: "已记录。正在生成受管仓库清单..."
```
