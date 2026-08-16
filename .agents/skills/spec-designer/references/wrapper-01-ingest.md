---
name: 'wrapper-01-ingest'
description: '调用 spec pipeline 的 ingest 内部模块'
sub_workflow: './pipeline/ingest/ingest.workflow.md'
nextStepFile: './wrapper-01b-validate.md'
---

# Phase 1: Ingest (摄入)

## 指令
作为协调器，请按照以下指示调用内部模块链：

1.  **加载 ingest 模块**:
    读取并执行 `{sub_workflow}` 中的所有步骤。
    *   注意：这是一次 "子程序调用" (Subroutine Call)。
    *   **Context Injection**: 确保 `{project-root}/.maglev/temp/interview_context.md` 被作为 `input_facts` 的一部分读取 (如果存在)。
    *   请完整执行 `identify-source` 和 `extract-facts`。
    *   **导航门禁**: 在目录扫描或手选深潜目标前，先消费未过期的 `index-librarian` 导航收据；将其候选、证据与选择理由写入 `input_facts`。
    *   **状态约束**:
        *   `queried`: 允许继续，并继续读取命中的叶子证据或目录下钻来源。
        *   `not_needed`: 允许继续，但必须说明当前步骤为何不依赖额外项目知识。
        *   `insufficient`: 不得以盲扫替代，必须进入受控升级链。
        *   `escalated`: 表示正在执行补救动作；只能继续收窄 scope / 复用已有线索 / 最小补线索交互 / 受控 deep scan，不得伪装成已拿到充分来源。
        *   `exhausted`: 停止继续扩大扫描；在 `input_facts` 中显式记录“当前知识不足”，必要时向用户补一个区分知识域的问题。
    *   **CLI 提示**: 如需显式记录升级链，使用 `task_navigate.py` 的 `--escalation-step`、`--escalation-attempt`、`--scope-hint`、`--known-source-hint`、`--escalation-note` 与 `--exhausted` 参数，而不是自由文本描述“已经升级”。

2.  **验证产物**:
    检查以下文件是否生成：
    *   `{project-root}/.maglev/temp/ingest_context.json`
    *   `{project-root}/.maglev/temp/input_facts.md`

3.  **前进**:
    一旦确认产物存在，加载 `{nextStepFile}` 进入 Phase 2。
