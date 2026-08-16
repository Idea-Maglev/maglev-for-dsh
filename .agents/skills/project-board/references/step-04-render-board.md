---
name: step-04-render-board
description: 渲染看板视图并持久化到仓库
---

# Step 4: Render Board (渲染与持久化)

## 目标

将扫描结果、阶段判断和角色映射合成为**人类可读**的看板视图，持久化到仓库。

## 渲染原则

1. **面向人类阅读**：所有输出使用人话，不使用文件名代号（如"00-03"）
2. **可导航**：每个需求有相对链接，可直接跳转到详情
3. **完整进度**：展示全流程进度条，而非仅当前阶段
4. **层级清晰**：父子需求有缩进关系

## 动作

### 1. 读取模板

读取 `references/board-template.md` 获取 Mermaid 看板的固定模式。

### 2. 渲染总看板

输出到 `specs/20_evolution/board.md`：

#### 2a. 头部信息
```markdown
# 项目看板

> 最后更新: {ISO 8601 timestamp} | 活跃需求: {n} | 未启动: {m}
```

#### 2b. 图例
```markdown
## 图例

| 符号 | 含义 |
|------|------|
| ✅ | 阶段已完成 |
| ⏳ | 阶段进行中 |
| ⬜ | 阶段未开始 |
| 🟢 | 当前主导阶段 (Mermaid) |
| 🟠 | 阶段待确认 (Mermaid) |

**流程阶段**: 需求收敛 → 方案设计 → 编码实施 → 综合验证 → 结晶归档
```

#### 2c. Mermaid 看板视图

按 `board-template.md` 的模式生成 Mermaid 流程图：
- 每个阶段是一个 subgraph（使用 ASCII ID + 中文标签）
- 每个需求是一个节点，放在其**当前主阶段**的 subgraph 中
- 节点文本包含：需求名称 + 意图摘要（截取前 15 字）+ 主导角色
- 使用 `<br/>` 换行（不是 `\n`）
- 父需求节点使用粗边框或特殊标记
- 空阶段保留占位节点维持布局

#### 2d. 需求明细表

在 Mermaid 下方输出 `## 活跃需求` 详情表，**使用人话**：

```markdown
## 活跃需求

| 需求 | 意图 | 进度 | 主导 | 信心度 | 导航 |
|------|------|------|------|--------|------|
| {name} | {intent_summary} | {progress_emoji} | {role} ({person}) | {confidence} | [详情](active/{name}/) |
```

- `进度` 列使用 emoji 进度条：如 `✅→✅→⏳→⬜→⬜`
- `导航` 列使用相对路径链接到 spec 目录
- 父子需求在表中用缩进表示：子需求名前加 `├` 或 `└`

#### 2e. 未启动需求

列出所有 `type: issue` 的 ActiveItem，附意图摘要和导航链接。

#### 2f. 变更摘要

对比上次看板内容（若存在），标注阶段变化：
```markdown
## 本次变更摘要

- {name}: {old_stage} → {new_stage}
```

若为首次生成，标注"首次生成看板"。

### 3. 渲染子看板

对每个活跃 spec，输出到 `specs/20_evolution/active/{spec}/status.md`：

```markdown
# 状态: {spec_name}

> 最后更新: {timestamp}

## 意图

{intent_summary}

## 流程进度

{progress_emoji_with_labels}

例如：✅ 需求收敛 → ✅ 方案设计 → ⏳ 编码实施 → ⬜ 综合验证 → ⬜ 结晶归档

## 当前主阶段

{current_stage} ({confidence})

## 证据

| 阶段 | 状态 | 关键证据 |
|------|------|---------|
| 需求收敛 | ✅ | 意图文档: 有问题陈述；需求文档: 7 FR / 18 AC |
| 方案设计 | ✅ | 设计文档: 有架构决策 (385 行) |
| 编码实施 | ⏳ | 代码提交: 3 commits；测试: 无 |
| 综合验证 | ⬜ | — |
| 结晶归档 | ⬜ | — |

## 角色状态

| 角色 | 人员 | 状态 |
|------|------|------|
| VO | {person} | {status} |
| TP | {person} | {status} |
| XG | {person} | {status} |

## 子需求（若有）

| 子需求 | 进度 | 导航 |
|--------|------|------|
| {child_name} | {progress_emoji} | [详情]({relative_path}/) |

## 已知阻塞

- {blocker_description}（无则写"无"）
```

### 4. 更新缓存

写入 `.maglev/temp/board_cache.json`：
- 每个条目的 current_stage、progress、confidence、updated_at、evidence_hash
- last_full_update 时间戳

### 5. 模式治理检查

若本次渲染涉及 Mermaid 模式变更（增减阶段列、修改样式类等）：
- 暂停并向用户展示变更内容
- 等待 AI + 用户确认后再写入
- 记录确认结果

数据更新（需求位置变化）不需要确认，直接执行。

## 输出

- `specs/20_evolution/board.md` 已更新
- 每个活跃 spec 下的 `status.md` 已更新
- `.maglev/temp/board_cache.json` 已刷新
- 在终端输出看板摘要
