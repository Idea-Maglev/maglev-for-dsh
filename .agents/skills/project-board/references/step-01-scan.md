---
name: step-01-scan
description: 扫描活跃需求，构建 ActiveItem 列表
next_step: references/step-02-judge-stage.md
---

# Step 1: Scan (活跃需求扫描)

## 目标

识别当前项目中所有正在推进的需求和未启动的任务。

## 动作

### 1. 扫描 Spec 目录

列出 `specs/20_evolution/active/` 下的所有子目录。

对每个子目录：
- 检查 `00_intent.md` 是否存在
- 若存在，提取第一个 `## 意图` 或 `## 问题陈述` 段的首行作为意图摘要
- 列出目录下已有的全部文件名
- 记录为 `type: spec`

### 2. 扫描 Issue 目录

列出 `issues/active/` 下的所有 `.md` 文件。

对每个文件：
- 提取文件首行（通常是标题）作为意图摘要
- 检查是否在 `specs/20_evolution/active/` 下有同名（去掉前缀后）的 spec 目录
  - 有 → 跳过（已由 spec 覆盖）
  - 无 → 记录为 `type: issue`（未启动需求）

### 3. 检测嵌套关系

对每个 type=spec 的 ActiveItem，检查其 `00_intent.md` 是否包含 `## 子需求` 章节。

若存在，解析子需求列表（每行一个 spec 名称），建立 parent→children 关联：

```markdown
## 子需求

- child_spec_name_1
- child_spec_name_2
```

- 子需求必须也存在于 `specs/20_evolution/active/` 中才建立关联
- 不存在的子需求名标记为 `missing_child`
- 一个 spec 只能有一个 parent（不支持多重父级）

### 4. 构建 ActiveItem 列表

每个 ActiveItem 包含：

| 字段 | 说明 |
|------|------|
| name | spec 目录名 或 issue 文件名（不含扩展名） |
| path | 相对于项目根的路径 |
| type | `spec` 或 `issue` |
| intent | 意图摘要（一句话） |
| files | 该目录/路径下已有的文件列表 |
| parent | 父需求 name（若有） |
| children | 子需求 name 列表（若有） |

## 输出

- ActiveItem 列表，传递给 Step 2
- 在终端输出扫描摘要："发现 {n} 个活跃 spec，{m} 个未启动 issue"
