---
description: integrated-validator Step 1 - Collect Context
---

# Step 1: Collect Context (收集上下文)

## 目标
调用现有质量层能力面 + 内置扫描器，收集所有待验证的上下文信息。

## 执行逻辑

### 1.1 调用 spec-audit-surface
**目的**: 获取 requirements 与 spec cluster 的输入审计结果
**产出**:
```yaml
spec_audit_context:
  requirements_findings:
    - type: structure_gap
      summary: acceptance 范围不完整
  spec_findings:
    - type: alignment_gap
      summary: 设计链路缺少回溯
```

### 1.2 调用 review-validation-surface
**目的**: 获取结果层 review 与 validation 的结构化信息
**产出**:
```yaml
review_context:
  implementation_findings:
    - type: compliance_gap
      summary: 实现偏离设计约束
  quality_findings:
    - type: risk
      summary: 边界校验不足
```

### 1.3 调用 test-design-surface
**目的**: 获取测试设计、覆盖策略与验证支撑建议
**产出**:
```yaml
test_design_context:
  targets:
    - CheckoutService
    - checkout page
  coverage_strategy:
    - 核心主链路
    - 边界失败路径
```

### 1.4 Code Scanner (内置)
**目的**: 扫描代码目录，识别已实现的 API 和方法
**扫描规则**:
- Java: `*Controller.java` → 提取 `@RequestMapping`
- Python: `routers/*.py` → 提取 `@app.get/post`
- Node: `routes/*.js` → 提取 `router.get/post`

**产出**:
```yaml
code_context:
  backend:
    controllers:
      - file: OrderController.java
        apis_implemented: [GET /api/orders]
    services:
      - file: OrderService.java
  frontend:
    components:
      - file: OrderList.vue
      - file: OrderItem.tsx
    stores:
      - file: orderStore.ts
```

### 1.5 Test Scanner (内置)
**目的**: 扫描测试目录，识别已覆盖的场景
**扫描规则**:
- **Backend**: `*Test.java`, `test_*.py`
- **Frontend**: `*.spec.ts`, `*.test.tsx`, `__tests__/**/*.js`

**产出**:
```yaml
test_context:
  backend:
    - file: OrderControllerTest.java
  frontend:
    - file: OrderList.spec.ts
```

## Checkpoint 输出模板
```
[CHECKPOINT - Step 1 Complete]

上下文收集完成。

📊 统计:
- Spec Audit: 2 findings
- Review: 2 findings
- Test Design: 2 targets
- Code: 3 Controllers, 5 Services
- Tests: 8 Test Files, 15 Test Methods

是否继续交叉比对？[Y/n]
```
