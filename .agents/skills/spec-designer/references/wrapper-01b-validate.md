---
name: 'wrapper-01b-validate'
description: '调用 spec pipeline 的 context guardrail 内部模块'
sub_workflow: './pipeline/validate-context/validate.workflow.md'
nextStepFile: './wrapper-02-draft.md'
---

# Phase 1.5: Validate (门禁)

## 指令

1.  **加载门禁模块**:
    读取并执行 `{sub_workflow}`。
    *   **Interactive Gatekeeper**:
        如果 validator 报错，**不要** 直接退出。向用户展示错误并提供选项：
        > "🛑 **Validation Warning**
        > 检测到上下文存在以下问题: ...
        >
        > 请选择:
        > - **[R]etry**: 我去修复一下上下文/输入，重新验证。(推荐)
        > - **[F]orce**: 我已知晓风险，强制生成。(At your own risk)
        > - **[A]bort**: 停止任务。"

2.  **逻辑分支**:
    *   **[R]**: 重新加载 `{sub_workflow}`。
    *   **[F]**: 继续流程，加载 `{nextStepFile}`。
    *   **[A]**: 终止流程。
    *   **PASS**: 自动加载 `{nextStepFile}`。
