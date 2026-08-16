---
name: maglev-map-maker
description: 项目地图生成器。基于仓库产物生成和更新项目全景地图。
metadata:
  formal_action_name: 项目地图生成
  top_level_capability: 现状表达
  system_layer: Infrastructure Layer
  lifecycle_chain: reality_expression
  runtime_name_status: active_legacy_name
  distribution_scope: runtime_internal
  version: "2.0 (Confidence-Aware Edition)"
---

# Maglev Map Maker (项目地图生成器)

> 结构动作名：`项目地图生成`
> 运行面名称：`maglev-map-maker`
> 这不等于已经完成正式物理改名。

## 核心职责
本技能负责扫描项目产物 (Artifacts)，推断当前生命周期状态，并绘制 **中文 Mermaid 地图**。
它**不依赖**其它技能的通知，而是直接观察文件系统，确保地图反映的是 **客观现实**。

## 适用场景
- **Daily Standup**: 每天早上看一眼，知道项目全貌。
- **Onboarding**: 新人入职，看地图了解进度。
- **Navigation**: 迷路时，用地图判断下一步该做什么。
- **入口与治理协作**: 入口对象、现状同步和后段闭环对象会消费地图结果来理解项目状态。

## 技能产出
*   **Unified Map**: 生成/更新 `docs/ATLAS.md` (项目全景地图)。包含嵌入的 Mermaid 图表，支持 GitHub/IDE 直接预览。
*   **Dashboard Update**: (可选) 将核心状态图同步到根目录 `README.md`。
*   **No More Standalone Files**: 不再生成散落的 `.mmd` 文件。

---

## 置信度标记 (Confidence Score)

为了让下游消费者知道地图的可靠程度，**每次生成地图时必须包含元数据块**：

```markdown
> **Meta**
> - Last Updated: {YYYY-MM-DD HH:MM}
> - Confidence: {High / Medium / Low}
> - Confidence Reason: {简要说明}
```

### 置信度判断标准
| 等级 | 条件 | 说明 |
| :--- | :--- | :--- |
| **High** | `crosscutting/repository-map/repositories.md` 存在且包含有效仓库列表，`specs/` 结构清晰 | 地图基于确定性信息绘制。 |
| **Medium** | 受管仓库清单不存在但发现代码目录 (e.g., `src/`, `code/`) | 地图基于推断，可能有遗漏。 |
| **Low** | 目录结构不规范，大量散落文件，无明确入口 | 地图主要基于猜测，建议人工审查。 |

---

## 状态推断逻辑 (ADSI)
*   **🆕 仓库配置?** <- 优先读取 `specs/10_reality/crosscutting/repository-map/repositories.md` 获取代码仓库路径。
*   **Structure?** <- `10_reality` 中的架构定义。
*   **Design Phase?** <- 存在 `02_ui_design.md` 或 `XXX.fig` 引用。
*   **Dev Phase?** <- 根据受管仓库清单中的路径检查代码是否存在，或 fallback 到 `src/`, `code/`, `code_storages/`。
*   **Tested?** <- 存在 `test/` 代码或 `test_report.md`。

---

## ATLAS.md 输出模板

```markdown
# 🗺️ Project Atlas (项目全景地图)

> **Meta**
> - Last Updated: 2026-02-09 14:00
> - Confidence: Medium
> - Confidence Reason: 发现 specs/ 和 src/ 并存，结构为混合型。

## 1. 🌍 World Map (战略层)
[Mermaid stateDiagram-v2 showing project phase]

## 2. 🏔️ Terrain Map (地形层)
[Mermaid flowchart showing module relationships]

## 3. 🏙️ City Map (管线层)
[Mermaid C4 or ER diagram]

## 4. 🛤️ Street Map (执行层)
[Active feature list with status]
```

---

## 必需的参考资料
*   工作流: `references/map.workflow.md`
*   战略图绘制: `references/step-01-world.md`
*   地形图绘制: `references/step-01b-terrain.md`
*   管线图绘制: `references/step-02-city.md`
*   执行图绘制: `references/step-03-street.md`
