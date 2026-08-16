---
name: 'step-03-zoom-extract'
description: '执行深度提取并生成最终产物'
output_json: '{project-root}/.maglev/temp/ingest_context.json'
output_facts: '{project-root}/.maglev/temp/input_facts.md'
---

# 步骤 3: 聚焦提取 (Zoom & Extract)

## 目标
根据类型和深潜目标，生成最终的 Facts 和 Context。

## 执行逻辑

### Scenario A: Fast Track (Low Complexity)
**Condition**: `complexity == "low"`
*   **Action**: 无需扫描。
*   **Generate JSON**: `{ "intent": "{intent}", "type": "fast-track", "refs": {} }`
*   **Generate Facts**:
    ```markdown
    # Input Facts: Fast Track
    *   **Intent**: {intent}
    *   **Note**: Simple change, skipped deep scan.
    ```

### Scenario B: Incremental (Has Spec)
**Condition**: `has_spec == true`
*   **Action**: 读取 `{project-root}/specs/20_evolution/active/{slug}/02_design.md`。
*   **Generate JSON**: `{ "intent": "{intent}", "type": "incremental", "base_spec": "{path}" }`
*   **Generate Facts**:
    ```markdown
    # Input Facts: Incremental
    *   **Base Spec**: {path}
    *   **Intent**: {intent}
    ```

### Scenario C: Full Scan (Idea/Doc/Legacy)
**Condition**: `complexity == "high"` AND `has_spec == false`

**导航前置条件**:
*   `queried`: 继续读取命中的叶子证据，并把候选、理由、证据写入 `input_facts.md`。
*   `not_needed`: 可以继续，但必须写明为什么当前提取阶段不依赖额外项目知识。
*   `escalated`: 只能在升级链限定的 scope 内继续提取；不得恢复成全域扫描。
*   `exhausted`: 停止提取，不得伪造正式来源；只允许显式记录当前知识不足并返回补线索。

#### Type 1: Idea / Type 2: Docs
*   参考原逻辑，直接生成 JSON 和 Facts。

#### Type 3: Legacy (Level 2 Deep Dive)
1.  **加载目标**: 读取 `ingest_manifest.deep_dive_targets`。
2.  **Deep Scan (深潜)**:
    *   遍历目标目录。
    *   **Data Model**: 使用 `read_file` 读取 Entity/DTO/SQL (保证 Schema 100% 准确)。
    *   **Core Logic**: 使用 `view_file_outline` 提取复杂类的签名；如果用户特别强调某文件，可使用 `read_file` 读取关键片段。
    *   *Compatibility Note*: 非 Antigravity Agent 请人工调整指令。
3.  **Synthesis (合成)**:
    *   将 Level 1 的全景图作为 "Background"。
    *   将 Level 2 的详细信息作为 "Core Context"。

## 生成产物

### A. Context JSON ({output_json})
```json
{
  "intent": "{user_intent}",
  "type": "{type}",
  "legacy_references": {
    "map": ["..."],
    "deep_dive": {
      "order_service": { "signatures": [...], "schema": [...] }
    }
  }
}
```

### B. Input Facts ({output_facts})
```markdown
# Input Facts: {type}

## 1. Project Map (Level 1)
{summary_of_map}

## 2. Deep Dive Analysis (Level 2)
> Focus: {deep_dive_targets}

> **Traceability Rule**: All code snippets MUST be cited with their **Project-Relative Path** (e.g., `src/domain/User.java`). DO NOT use absolute paths.

### 2.1 Data Schema
> Ref: `{relative_path_to_schema_file}`
{schema_details}

### 2.2 Core Interfaces
> Ref: `{relative_path_to_interface_file}`
{signature_details}
```

## 结束
报告：
"Facts 提取完毕！✨
已生成: `{output_facts}`
(包含全景图 + 重点模块的深度分析)"
