---
name: 'step-01-validate-schema'
description: '校验 JSON 结构和引用完整性'
context_file: '{project-root}/.maglev/temp/ingest_context.json'
---

# 步骤 1: 协议校验 (Protocol Validation)

## 规则
你必须扮演严格的编译器。任何不符合协议的地方都是 Error。

## 执行指令

1.  **Read Context**: 读取 `{context_file}`。

2.  **Schema Validation**:
    检查 JSON 是否包含以下必填字段 (参考 `solutions/templates/standards/protocol_spec_context.md`)：
    *   `meta.slug` (String, Non-empty)
    *   `meta.intent` (String, Non-empty)
    *   `facts.input_facts_path` (String, Valid Path)

3.  **Integrity Validation**:
    *   使用 `read_file` (head only) 或 `ls` 检查 `facts.input_facts_path` 指向的文件是**真实存在**的。

4.  **Decision**:
    *   **PASS**: 如果通过，输出 "✅ Context Validated." 并结束。
    *   **FAIL**: 如果失败，输出 "❌ Context Validation Failed: [Reason]" 并**请求用户终止流程**。
