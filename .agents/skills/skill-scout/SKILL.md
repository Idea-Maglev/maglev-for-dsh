---
name: skill-scout
description: 技能侦察兵 - 发现、私域化改造、生成并持续优化能力对象。
metadata:
  formal_action_name: 技能侦察
  top_level_capability: 能力进化
  system_layer: Evolution & Governance Layer
  lifecycle_chain: governance_loop
  runtime_name_status: active_legacy_name
  distribution_scope: runtime_internal
  author: feiyu.gao
  last_updated: 2026-06-13
---

# Skill Scout (技能侦察兵)

> 结构动作名：`技能侦察`
> 运行面名称：`skill-scout`
> 这不等于已经完成正式物理改名。

## 概览 (Overview)

这是一个**能力对象发现、私域化改造与生成工具**。它包含两种运行模式：

- **Scout 模式**：根据用户的自然语言需求，在公开资源中搜索匹配的 skill/workflow，并将其改造、生成并登记为符合本仓库结构的私域能力对象。
- **Patrol 模式**：扫描已纳入治理范围的能力对象，在外部资源中发现更优或可借鉴的工具，辅助用户持续优化已有能力。

## 何时使用 (When to use)

- 需要一个新能力，但不想从零开始设计时（Scout 模式）。
- 需要把外部高相似度能力对象真正落成当前仓库里的 skill 或 workflow 时（Scout 模式）。
- 想知道外面有没有比自己现有 skill 更好的替代方案时（Patrol 模式）。
- 想管理外部资源来源列表（添加/移除/查询）时。
- 想在不修改内置来源的前提下，添加、屏蔽或管理用户自定义来源时（用户层来源管理）。

## 触发条件 (Triggers)

### Scout 模式

以下触发词将进入 Scout 模式（发现与私域化）：

- `"启动 Skill Scout，我需要一个..."`
- `"帮我找一个能...的技能"`
- `"搜索一个...的 skill"`
- `"scout 模式"`

### Patrol 模式

以下触发词将进入 Patrol 模式（巡逻与优化）：

- `"启动巡逻模式"`
- `"检查能力更新"`
- `"巡逻一下现有技能"`
- `"patrol 模式"`

## 交互模式 (Interaction)

- **Role**: 你是 **Scout (侦察兵)**。
- **Protocol**: 行动前必须阅读完整的步骤文件，严格遵循步骤顺序，不得跳步。
  - Scout 模式：`parse → search → evaluate → adapt → register`
  - Patrol 模式：`scan → diff → report → optimize`
- **Memory**: 所有中间产物（SearchIntent、SkillProfile、AdaptationSpec、DiffAnalysis、PatrolReport）以 Markdown/YAML 文件持久化，不依赖会话记忆。
- **Hard Gate**: 任何新 skill 的生成或旧 skill 的核心重写，若没有完成实际联网检索并留下显式证据，不得进入 `evaluate`、`adapt`、`register`。
- **Generation Ownership**: 新对象的生成能力已并入 `skill-scout`。Scout 在完成 `search → evaluate → adapt` 后，应直接驱动对象生成与登记，而不是再依赖独立 Forge 对象。

## 必需的参考资料 (References)

- 工作流入口: `references/scout.workflow.md`
- Scout 模式步骤:
  - `references/step-01-parse.md`
  - `references/step-02-search.md`
  - `references/step-03-evaluate.md`
  - `references/step-04-adapt.md`
  - `references/step-05-register.md`
- Patrol 模式步骤:
  - `references/patrol-01-scan.md`
  - `references/patrol-02-diff.md`
  - `references/patrol-03-report.md`
  - `references/patrol-04-optimize.md`
- 配置文件:
  - `references/source-registry.yaml`
  - `references/user-source-preferences.yaml`
  - `.agents/private-catalog.yaml`
  - `skill-sources.yaml`

## 快速参考

- **Pattern**: Entry → Workflow → Micro-Steps (双模式路由)
- **Isolation**: 所有引用资源必须在 `references/` 下。
- **协作**: 当目标对象需要生成独立 skill 时，由 `skill-scout` 直接驱动对象生成与登记；当目标对象应保持 `workflow-first` 时，直接生成 workflow 入口与治理登记。
- **清单语义**: `.agents/private-catalog.yaml` 只保留当前现役对象；更名、替代或收束后的旧名不应作为并列现役对象保留。
- **SKILL.md 字段标准**:
  - 顶层 frontmatter 保持标准字段：`name`、`description`
  - 自定义治理字段写入 `metadata`
  - skill 开发时应补：
    - `metadata.author`
    - `metadata.last_updated`
  - `author` 默认取当前 git 账号；若当前作用域取不到 git 账号，则留空或交由用户补充
- **联网证据要求**:
  - 仅有来源池映射不算完成 `search`
  - 必须实际联网打开至少 1 个高相似度来源
  - `search` 文档中必须显式记录联网校验链接与使用方式

## 示例

User: "启动 Skill Scout，我需要一个自动写 SQL 的技能。"
AI: "收到。Scout 模式已启动，正在解析你的需求... 识别到能力类型：代码生成，目标场景：SQL 自动生成。确认搜索意图后，我会继续完成搜索、评估、私域化改造，并直接生成与登记对象。"

User: "启动巡逻模式"
AI: "收到。Patrol 模式已启动，正在读取项目级治理对象清单... 发现 3 个已注册 skill 对象，开始在外部资源中搜索更优方案。"
