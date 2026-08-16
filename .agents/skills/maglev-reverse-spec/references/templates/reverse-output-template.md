# Reality Output Template

> 这是一个“标准偏完整”的 reality 产物样板。实际输出可以根据 `Lean / Standard / Deep` 三档裁剪。
>
> 语言约束：除非用户明确要求其他语言，本模板生成的章节标题、解释性正文、结论、风险、建议与问题队列都应以中文为主。

## 00_index.md

```markdown
# Index: {Feature Name} (Reality Snapshot)

## 元数据
- Feature: {Feature Name}
- Status: Draft / Structural / Ready-to-Engineer / Verifiable
- Entry Type: UI-First / API-First / Event-First / Data-First / CLI-First
- Confidence: High / Medium / Low
- Scope:
  - {file_a}
  - {file_b}

## 关联文档
- [Requirements](./01_requirements.md)
- [Design](./02_design.md)
- [RMM Scorecard](./03_rmm_scorecard.md)
- [Expert Review Queue](./99_expert_review_queue.md)
```

## 01_requirements.md

```markdown
# Requirements - {Feature Name}

## 1. Feature Summary
- 该功能解决什么问题
- 主要用户是谁
- 核心输入与输出是什么

## 2. Evidence Summary
- [FACT] ...
- [INFERENCE] ...
- [UNKNOWN] ...

## 3. User Stories
- 作为 {user}，我希望 {goal}，以便 {benefit}

## 4. Acceptance Criteria
- AC-01: ...
- AC-02: ...

## 5. Domain Model
- 核心业务对象
- 术语对齐
- 边界定义

## 6. Unknowns / Quests
- [Q-01] ...
- [Q-02] ...

## 7. Implementation Trace
- {module_a}: {path}
- {module_b}: {path}
```

## 02_design.md

```markdown
# Design - {Feature Name}

## 1. Architecture Overview
- 入口
- 关键组件
- 依赖关系

## 2. Feature Map
- Page / Route / API / Command / Event

## 3. Data Structure Map

### 3.1 Core Structures
| Name | Kind | Defined In | Purpose |
|---|---|---|---|
| Record | Entity | backend/models/record.py | 核心记录结构 |
| RecordDetailResponse | DTO | backend/schemas/record.py | 详情接口返回 |
| useRecordStore | Store | frontend/stores/record.ts | 前端状态存储 |

### 3.2 Data Dictionary
| Structure | Field | Type | Required | Meaning | Notes |
|---|---|---|---|---|---|
| Record | id | string | yes | 主键 | |
| Record | state | enum | yes | 当前状态 | 待确认具体枚举 |

### 3.3 Mapping
- CreateRecordRequest -> Record -> RecordDetailResponse
- Record -> useRecordStore.currentRecord -> RecordPanel props

## 4. Main Flow
1. 用户触发
2. 前端调用
3. 后端处理
4. 数据持久化
5. 响应返回

## 5. State Machine
| State | Trigger | Next State | Guard |
|---|---|---|---|
| draft | submit | pending | 字段校验通过 |
| pending | pay_success | paid | 支付回调成功 |

## 6. Runtime Behavior
- 并发点
- 缓存点
- 异步点

## 7. Error Taxonomy
- 用户输入错误
- 业务校验错误
- 外部依赖错误

## 8. Security Surface
- 身份校验
- 权限点
- 敏感字段

## 9. Observability
- 日志锚点
- 指标锚点
- Trace 锚点

## 10. Change Risk
- 热点文件
- 高风险改动路径

## 11. Assumptions / Unknowns
- [INFERENCE] ...
- [UNKNOWN] ...

## 12. Implementation Trace
- {path_a}
- {path_b}
```

## 03_rmm_scorecard.md

```markdown
# RMM Scorecard

## Summary
- Current Level: RL-3
- Ready for Engineering: Yes

## Scores
| Dimension | Score | Note |
|---|---:|---|
| Reqs | 3 | AC 基本完整 |
| Arch | 3 | 组件与时序已明确 |
| Data | 3 | 数据字典已补齐 |
| Runtime | 2 | 并发策略仍有疑问 |
| Risk | 2 | 回滚路径未完全确认 |

## Gaps
1. ...
2. ...
```

## 99_expert_review_queue.md

```markdown
# Expert Review Queue

## Architectural Intent
- [Q-01] 该缓存结构是否跨会话共享？

## Data Semantics
- [Q-02] `status=9` 的业务含义是什么？

## Risk & Debt
- [R-01] 回调重复触发时是否已有幂等保护？
```

## 档位建议

### Lean
- 只保留 Feature Map、Evidence Log、Main Flow、Core Data Structures、Unknowns
- 文件建议:
  - `00_index.md`
  - `01_requirements.md` 摘要版
  - `02_design.md` 精简版

### Standard
- 在 Lean 基础上增加 Data Dictionary、State Machine、Test Mapping、Change Risk
- 文件建议:
  - `00_index.md`
  - `01_requirements.md`
  - `02_design.md`
  - 可选 `03_test_mapping.md`

### Deep
- 在 Standard 基础上增加 Runtime Behavior、Security Surface、Error Taxonomy、Observability、RMM Scorecard
- 文件建议:
  - `00_index.md`
  - `01_requirements.md`
  - `02_design.md`
  - `03_rmm_scorecard.md`
  - `99_expert_review_queue.md`

## 档位到章节映射

| Section | Lean | Standard | Deep |
|---|---|---|---|
| Feature Summary | yes | yes | yes |
| Evidence Summary | yes | yes | yes |
| Domain Model | optional | yes | yes |
| Feature Map | yes | yes | yes |
| Core Data Structures | yes | yes | yes |
| Data Dictionary | no | yes | yes |
| Main Flow | yes | yes | yes |
| State Machine | optional | yes | yes |
| Dependency Topology | no | yes | yes |
| Runtime Behavior | no | optional | yes |
| Security Surface | no | no | yes |
| Error Taxonomy | no | optional | yes |
| Configuration Matrix | no | no | yes |
| Observability | no | no | yes |
| Test Mapping | no | yes | yes |
| Change Risk | no | yes | yes |
| RMM Scorecard | no | optional | yes |
| Expert Review Queue | no | optional | yes |
