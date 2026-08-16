---
name: stage-evidence-rules
description: 流程阶段判定的证据规则参考
---

# 阶段证据规则 (Stage Evidence Rules)

## 评估模式：全段评估

对每个 ActiveItem，**逐阶段评估所有 5 个阶段**的完成状态（不是"命中即停"）。
每个阶段产出三种状态之一：`completed` / `in_progress` / `not_started`。

这允许一个 spec 同时处于多个阶段（叠加态），例如"方案设计已完成但仍在迭代需求"。

## 阶段证据要求

| 阶段 | 人话名 | 完成条件 | 进行中条件 |
|------|--------|---------|-----------|
| 需求收敛 | 意图与需求定义 | `00_intent.md` 有问题陈述 + `01_requirements.md` 有 FR/AC 定义 | `00_intent.md` 存在（含问题陈述） |
| 方案设计 | 技术方案设计 | `02_design.md` 有架构决策内容 | `01_requirements.md` 有 FR/AC 定义 |
| 编码实施 | 代码与 Skill 实现 | `02_design.md` 有架构决策内容 + 有相关代码提交 | `02_design.md` 存在 + 有任何相关提交 |
| 综合验证 | 测试与验证 | `02_design.md` 有架构决策内容 + 有实质提交 + 有测试文件 | 有实质提交 + 测试文件开始出现 |
| 结晶归档 | 知识沉淀与归档 | 意图/需求/设计/计划齐备 + 有验证记录 + 有实质提交 + 有测试通过记录 | 所有文件齐备 + 部分验证开始 |

> **注意**：已归档的 spec（在 `90_archive/` 下）不会被扫描。归档由 crystallization 负责。

## 进度可视化

每个 spec 的进度用 emoji 序列表示：

```
✅ 需求收敛 → ✅ 方案设计 → ⏳ 编码实施 → ⬜ 综合验证 → ⬜ 结晶归档
```

| 图标 | 含义 |
|------|------|
| ✅ | 已完成 (completed) |
| ⏳ | 进行中 (in_progress) |
| ⬜ | 未开始 (not_started) |

**当前阶段** = 最高的 `in_progress` 或 `completed` 阶段中，状态为 `in_progress` 的那个。
若所有已评估阶段都是 `completed`，当前阶段 = 最高 `completed` 阶段。

## 文件别名（面向用户的人话）

在看板和状态输出中，使用以下别名替代文件名：

| 文件名 | 人话别名 |
|--------|---------|
| `00_intent.md` | 意图文档 |
| `01_requirements.md` | 需求文档 |
| `02_design.md` | 设计文档 |
| `03_plan.md` | 计划文档 |
| 全部齐备 | 意图/需求/设计/计划齐备 |

## 内容质量标记词

用于判断文件内容是否充实（非空壳模板）：

| 文件 | 人话名 | 关键标记词 |
|------|--------|-----------|
| `00_intent.md` | 意图文档 | `## 意图`、`## 问题陈述`、`## 目标` |
| `01_requirements.md` | 需求文档 | `## 功能需求`、`### F-`、`AC-` |
| `02_design.md` | 设计文档 | `## 架构`、`## 设计决策`、`## 模块`、`## 组件` |
| `03_plan.md` | 计划文档 | `## 任务`、`T-`、`Phase` |

## 有效内容行数阈值

- 最低阈值：20 行有效内容
- 有效内容 = 总行数 - 空行 - 纯 Markdown 结构行（仅含 `#`、`---`、`|---|`）

## 代码证据查询规则

```bash
# 查询模板（{spec_name} 替换为实际 spec 目录名）
# 排除看板自身产出文件，避免自证预言
git --no-pager log --oneline --since="90 days ago" -- "**/{spec_name}*" ":!specs/20_evolution/active/*/status.md" ":!specs/20_evolution/board.md" | head -5
```

- 返回 ≥ 1 条提交 → `code_evidence = true`
- 查询范围限制为最近 90 天（覆盖常规 spec 生命周期）
- 结果可缓存到 `board_cache.json`

## 测试证据查询规则

```bash
# 查询模板
find tests/ -name "*{spec_name}*" -type f 2>/dev/null | head -3
```

- 找到 ≥ 1 个文件 → `test_evidence = true`

## 置信度判定

| 场景 | confidence |
|------|------------|
| 当前阶段的所有证据均满足 | `confirmed` |
| 文件存在但内容质量未通过阈值检查 | `inferred` |
| 相邻阶段证据冲突或两阶段同时 in_progress | `uncertain` |
| type=issue（无 spec 文件） | `confirmed`（固定为需求收敛 ⏳，其余 ⬜） |
