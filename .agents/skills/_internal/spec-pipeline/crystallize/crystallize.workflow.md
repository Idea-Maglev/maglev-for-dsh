---
name: spec-crystallize
description: spec pipeline 共享内部模块：将 Draft 拆分为标准文件簇并存档 Facts。
input_draft: '{project-root}/.maglev/temp/draft_unified.md'
input_facts: '{project-root}/.maglev/temp/input_facts.md'
output_base: '{project-root}/specs/20_evolution/active'
---

# Spec Crystallize Workflow

**目标**: 将瞬态的 Draft 和 Facts 固化为持久态的 Spec Cluster。

## 步骤序列

### 1. Split & Persist (拆分与存档)
读取 `./step-01-split-files.md`。
*   读取 `draft_unified.md`。
*   解析章节，写入 `00-03` 文件。
*   复制 `input_facts.md` 到 `context/`。

### 2. Finalize (完成)
读取 `./step-02-finalize.md`。
*   清理 `.maglev/temp/`。
*   自动处理 Issue 归档 (Success Case)。
*   报告最终结果。

### 3. Abandon (废弃) [Optional]
仅当用户明确要求 "废弃/Abandon" 时跳转此步。
读取 `./step-99-abandon.md`。
*   移动 Spec 到 `90_archive`。
*   关闭 Issue。
