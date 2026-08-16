---
name: step-02-city
description: 绘制城市地图 (战术层/流水线)
next_step: references/step-03-street.md
---

# Step 2: City Map (城市地图)

## 目标
可视化 `specs/20_evolution/` 下的资产流动。

## 绘制指令
1.  **统计数据**: Count `issues/active`, `specs/evolution/*`.
2.  **追加章节**: 向 `docs/ATLAS.md` **追加** 内容。
3.  **写入标题**: `## 3. 🏙️ City Map (管线层)`。
4.  **嵌入图表**: 使用 \`\`\`mermaid 包裹 Flowchart LR 代码。
5.  **必须使用中文 Label**。
2.  **Count Drafts**: 统计 `specs/evolution/draft/` 数量 -> "草稿箱"。
3.  **Count Active**: 统计 `specs/evolution/active/` 数量 -> "施工中"。
4.  **Count Landed**: 统计 `specs/10_reality/` 变更 -> "已落地"。

### 模板
```mermaid
graph LR
    Inbox[📥 意图池 (5)] -->|Ingest| Draft[📄 草稿箱 (2)]
    Draft -->|Crystallize| Active[🏗️ 施工中 (3)]
    Active -->|Dev & QA| Landed[✅ 已落地 (12)]

    style Active fill:#f96,stroke:#333
    style Inbox fill:#eee,stroke:#333
```
