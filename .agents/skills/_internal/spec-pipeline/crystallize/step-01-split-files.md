---
name: 'step-01-split-files'
description: '执行物理拆分与存档'
---

# 步骤 1: 拆分与存档 (Split & Persist)

## 目标
将 Unified Draft 转化为物理文件簇。

## 执行逻辑

### 1. 准备目录
*   从 `draft_unified.md` 的内容或 Frontmatter 中提取 `slug`。
*   创建目录: `{output_base}/{slug}/`
*   创建目录: `{output_base}/{slug}/context/`

`context/` 是 **AI 上下文数据区**——存放方案设计与实施过程中产生的半结构化上下文数据。
与 `ref/`（外部不可变引用）不同，`context/` 内容随 spec 演化，由执行者与 AI 协作生成。

典型内容包括：
*   `input_facts.md`（必需）——方案设计输入事实基准
*   字段规则 / 数据映射（`.csv`、`.json`）
*   代码结构分析 / 接口映射（`.md`）
*   配置快照 / 状态表（`.json`、`.yaml`）

文件名须具有语义（如 `field_visibility_rules.csv`），格式不限。

### 2. 存档 Facts (Premise)
*   **Action**: 将 `{input_facts}` 复制到 `{output_base}/{slug}/context/input_facts.md`。
*   **意义**: 确立此 Spec 的 "输入事实基准"。后续可在 `context/` 中追加更多上下文文件。

### 3. 拆分 Draft (Robust Splitting)
读取 `{input_draft}`，使用 Regex `<!-- FILE: (.*?) -->` 进行内容拆分。

**逻辑**:
1.  找到所有匹配 `<!-- FILE: {filename} -->` 的行。
2.  将该行之后、直到下一个 `<!-- FILE: ... -->` 之前的内容，写入 `{output_base}/{slug}/{filename}`。
3.  如果文件已存在，直接覆盖。

**支持的文件列表 (Expected)**:
*   `00_index.md`
*   `01_requirements.md`
*   `01_requirements_interaction.md`（含 UI 项目时）
*   `02_design.md`
*   `02_design_interaction.md`（含 UI 项目时）
*   `03_plan.md`
*   `02_design_fe_be_contract.md`（UI + API 项目触发 Layout-to-API Binding Gate 时）
*   *(以及任何 AI 动态生成的附加文件)*

### 4. 前进
加载下一步: `./step-02-finalize.md`。
