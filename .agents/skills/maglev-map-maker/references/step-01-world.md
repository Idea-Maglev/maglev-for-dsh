---
name: step-01-world
description: 绘制世界地图 (战略层)
next_step: references/step-01b-terrain.md
---

# Step 1: World Map (世界地图)

## 目标
回答 "项目整体处于什么阶段？"

## 绘制指令
1.  **初始化 Atlas**: 创建或覆盖 `docs/ATLAS.md`。
2.  **写入 Header**: 包含标题 `# 🗺️ Maglev Atlas` 和 `> Last Updated: {YYYY-MM-DD}`。
3.  **绘制章节 1**: 写入 `## 1. 🌍 World Map (战略层)`。
4.  **嵌入图表**: 使用 \`\`\`mermaid 包裹 State Diagram 代码。
5.  **必须使用中文 Label**。

### 模板 (ATLAS.md 内容)
```markdown
# 🗺️ Maglev Atlas

> Last Updated: 2026-02-02

## 1. 🌍 World Map (战略层)

\`\`\`mermaid
stateDiagram-v2
    [*] --> 孵化期
    孵化期 --> 开发期: 首个 Spec 通过
    开发期 --> 稳定期: v1.0 发布
    稳定期 --> 维护期: 仅 Bugfix

    note right of 开发期
        当前状态: 🔥 活跃
        活跃特性: 3 个
    end note
```

## AI 引导摘要过期检查

在绘制世界地图之前，先检查 `crosscutting/repository-map/repositories.md` 中已有的 AI 引导摘要是否过期：

1. 对每个仓库摘要：
   - 对比当前 package.json dependencies 与摘要中记录的技术栈
   - 对比当前 src/ 结构与摘要中记录的代码结构
2. 如果检测到显著变化（核心依赖版本大变、新增/删除主要目录）：
   - 标记为"摘要可能过期"
   - 提醒用户："{仓库} 的 AI 引导摘要可能过期，是否重新生成？"
3. 用户确认后重新扫描生成（复用 bootstrapper 的摘要生成逻辑）
4. 如果没有 AI 引导摘要，提醒用户可通过 maglev-bootstrapper 生成
