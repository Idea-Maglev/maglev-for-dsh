---
name: 'step-02-finalize'
description: '清理现场并报告'
---

# 步骤 2: 完成 (Finalize)

## 目标
清理临时文件并通知用户。

## 执行逻辑

### 1. 清理
*   删除 `{input_draft}`。
*   删除 `{input_facts}`。 (已存档，原来的就不需要了)

### 2. 归档源头 (Archive Source)
**如果** 本次 Spec 生成源自 `issues/active/` 下的 Issue (查看 `ingest_manifest` 或询问用户):
*   **Move**: 将源 Issue 文件移动到 `issues/closed/{date}-{slug}.md`。
*   **Log**: 在 `issues/closed/README.md` (如有) 或 Issue 文件末尾追加: "Moved to closed after Spec Crystallization on {date}"。

### 2. 报告
输出最终报告：

"Spec Cluster 已固化！💎
位置: `{output_base}/{slug}/`

**文件清单**:
- 📚 `00_index.md`: 索引
- 📜 `01_requirements.md`: 需求
- 📐 `02_design.md`: 设计
- 🗓️ `03_plan.md`: 计划
- 🏛️ `context/input_facts.md`: 事实基准 (用于交叉验证)
- 📂 `context/`: AI 上下文数据区 (可追加字段规则、代码映射等半结构化文件)

您现在可以开始开发，或运行 `maglev-audit` 进行质量检查。"
