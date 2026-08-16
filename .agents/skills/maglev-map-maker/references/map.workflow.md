---
description: 地图生成工作流 (Scan -> Infer -> Draw -> Embed)
metadata:
  formal_action_name: 项目地图生成
  object_kind: workflow_reference
  output_map: '{project-root}/docs/ATLAS.md'
---

# Map Maker Workflow

**目标**: 无论项目处于什么混乱状态，强制生成一张清晰的可视化地图 (`docs/ATLAS.md`)。

## 步骤序列

### 1. Scan & Infer (扫描与推断)
读取全项目目录结构。
*   不修改任何文件。
*   推断每个 Active Feature 的阶段 (Spec/Design/Code/Test)。

### 2. Draw World Map (绘制世界地图)
读取 `references/step-01-world.md`。
*   动作: **Initialize** `docs/ATLAS.md`.
*   宏观视角 (Time)。
*   Output: Embed in `docs/ATLAS.md`.

### 2b. Draw Terrain Map (绘制地形图)
读取 `references/step-01b-terrain.md`。
*   动作: **Append** to `docs/ATLAS.md`.
*   结构视角 (Space).
*   Output: Embed in `docs/ATLAS.md`.

### 3. Draw City Map (绘制城市地图)
读取 `references/step-02-city.md`。
*   动作: **Append** to `docs/ATLAS.md`.
*   中观视角 (Issue/Spec 流水线)。
*   Output: Embed in `docs/ATLAS.md`.

### 4. Draw Street Map (绘制街道地图)
读取 `references/step-03-street.md`。
*   动作: **Append** to `docs/ATLAS.md`.
*   微观视角 (找出最活跃的 Feature 进行详情绘制)。
*   Output: Embed in `docs/ATLAS.md`.

### 5. Publish (发布)
可选：将 World Status 图同步到根目录 `README.md` 的 Dashboard 区域。
