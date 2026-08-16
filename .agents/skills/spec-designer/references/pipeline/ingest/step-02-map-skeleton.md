---
name: 'step-02-map-skeleton'
description: 'Type 3 专用：生成全景地图并询问深潜目标'
nextStepFile: './step-03-zoom-extract.md'
---

# 步骤 2: 全景制图 (Map & Skeleton)

## 目标
建立项目的“宏观地图”，让用户决定在哪里进行“深潜”。

## 执行逻辑

### A. 检查类型
**如果** `ingest_manifest.type` **不是** "legacy" (即 idea 或 doc):
*   无需制图。
*   直接设置 `deep_dive_targets = []`。
*   **立即跳转** 到 `{nextStepFile}`。

### B. 执行制图 (Level 1 Scan)
0.  **导航预检**:
    *   先消费当前导航收据。
    *   **If `queried`**: 仅围绕命中的目录或叶子证据做 Level 1 制图。
    *   **If `not_needed`**: 可继续，但要在输出里说明为何此阶段不依赖额外项目知识。
    *   **If `insufficient`**: 先走升级链；不得直接对整个 source 盲扫。
    *   **If `escalated`**: 只允许在升级动作收窄后的 scope 内继续。
    *   **If `exhausted`**: 停止 Level 1 制图，回到用户补线索或显式记录知识不足。
1.  **Map (目录树)**:
    *   使用 `list_dir` 扫描 `{ingest_manifest.source}`。
    *   忽略: `test`, `mock`, `node_modules`, `dist`, `.git`。
2.  **Skeleton (骨架)**:
    *   对根目录下的关键文件 (e.g., `README.md`, `package.json`, `pom.xml`) 或核心子目录执行 `view_file_outline`。
    *   提取核心模块列表。

### C. 交互 (Selection)
向用户展示扫描结果：
"已扫描项目全景 🗺️
核心模块如下：
- `src/auth` (User Service)
- `src/order` (Order Logic)
- ...

**请选择 Deep Dive 目标 (Zoom-in)**:
告诉我您此次修改涉及哪个模块？我将深入读取其逻辑和数据结构。
(例如: '重点看 order 模块' 或 '全选')"

### D. 暂存选择
将用户回复解析为目标列表，存入 `ingest_manifest.deep_dive_targets`。

### E. 前进
加载下一步: `{nextStepFile}`。
