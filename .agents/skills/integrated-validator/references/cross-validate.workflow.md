---
description: integrated-validator Workflow
---

# Cross-Validate Workflow

## 流程概览

```mermaid
graph TD
    Start[开始验证] --> S1[Step 1: Collect Context]
    S1 --> C1{确认继续?}
    C1 -->|Y| S2[Step 2: Cross-Reference]
    C1 -->|n| Exit[退出]
    S2 --> C2{生成报告?}
    C2 -->|Y| S3[Step 3: Generate Report]
    C2 -->|n| Exit
    S3 --> End[输出报告]
```

## 编排规则

### 调用的子技能
| 技能 | 阶段 | 产出 |
|------|------|------|
| `spec-audit-surface` | Step 1 | 输入审计上下文 |
| `review-validation-surface` | Step 1 | 结果审查上下文 |
| `test-design-surface` | Step 1 | 测试设计上下文 |

### 内置扫描器
| 扫描器 | 阶段 | 产出 |
|--------|------|------|
| Code Scanner | Step 1 | Code Context |
| Test Scanner | Step 1 | Test Context |

## Checkpoint 规则
1.  Step 1 后：展示上下文统计
2.  Step 2 后：展示健康度评分
3.  Step 3 后：输出报告路径
