---
description: integrated-validator Step 2 - Cross-Reference
---

# Step 2: Cross-Reference (交叉比对)

## 目标
对 Step 1 收集的上下文进行多维度一致性检查。

## 比对维度

### Layer 1: PRD ↔ Spec (需求 ↔ 设计)
**检查项**:
- 每个 User Story 是否有对应的 API 设计？
- 每个 AC 是否可追溯到技术实现？

**匹配逻辑**:
```python
for story in prd_context.user_stories:
    linked_apis = spec_context.apis.filter(linked_to=story.id)
    if not linked_apis:
        report.add_issue("CRITICAL", f"{story.id} 无对应 API 设计")
```

**产出**:
```yaml
prd_spec_match:
  matched: 4
  unmatched: 1
  score: 80%
  issues:
    - type: CRITICAL
      message: "US-005 无对应 API 设计"
```

---

### Layer 2: Spec ↔ Code (设计 ↔ 代码)
**检查项**:
- Spec 定义的 API 是否在 Controller 中实现？
- 是否存在 Ghost Code (代码有，Spec 无)？

**匹配逻辑**:
```python
for api in spec_context.apis:
    implemented = code_context.has_api(api.path)
    if not implemented:
        report.add_issue("CRITICAL", f"{api.path} 未实现")

for controller_api in code_context.all_apis:
    if not spec_context.has_api(controller_api):
        report.add_issue("WARNING", f"{controller_api} 为 Ghost Code")
```

**产出**:
```yaml
spec_code_match:
  backend_score: 80% (API Impl)
  frontend_score: 90% (Component Impl)
  issues:
    - type: CRITICAL
      message: "Component 'OrderList' defined in 02_frontend.md not found"
```

---

### Layer 2b: Spec ↔ Code (Frontend) — 前端实质性验证

> 当项目含前端代码（.vue/.tsx/.jsx 等）且存在交互设计文档时触发。

**组件一致性检查**:
- 交互设计文档（02_design_interaction.md）的组件清单 vs 实际组件文件
- 缺失的组件标记为 CRITICAL
- 多余的组件（spec 中未定义的）标记为 WARNING

**UI 状态覆盖检查**:
- 交互设计文档中 stateDiagram 定义的状态 vs 组件代码中的状态处理
- 检查关键状态是否有对应代码分支（loading/error/empty/success）
- 缺失的状态处理标记为 WARNING

**Props/Events 契约检查**:
- 交互设计文档中组件 API 表的 Props/Events vs 实际组件定义
- 类型不匹配标记为 CRITICAL
- 缺失的 Props/Events 标记为 WARNING

**可访问性基线检查**（如果 I 系 AC 中有可访问性要求）:
- 表单元素是否有关联 label 或 aria-label
- 交互元素是否有 focus 处理
- 错误提示是否有 aria-live 属性
- 缺失标记为 WARNING

**产出**:
```yaml
frontend_deep_match:
  component_coverage: 85%
  state_coverage: 70%
  contract_match: 90%
  a11y_baseline: 60%
  issues:
    - type: CRITICAL
      message: "LoginForm 组件在 spec 中定义但代码中不存在"
    - type: WARNING
      message: "UserProfile 组件缺少 error 状态处理"
```

---

### Layer 2c: AC 引用一致性检查

> 当需求文档包含结构化 AC（AC-F{N}-{M} 编号）时触发。

**检查项**:
- 扫描所有下游文档（02_design.md、03_plan.md）中引用的 AC 编号
- 检查每个引用的 AC-F{N}-{M} 在源需求文档中是否存在
- 不存在的标记为 CRITICAL: "AC-F2-5 在设计中被引用但需求中不存在"
- 检查需求中的每个 AC 是否在设计的需求覆盖表中至少出现一次
- 未覆盖的标记为 WARNING: "AC-F3-2 未被任何设计节引用"

**跨系 AC 覆盖检查**（当同时存在 F 系和 I 系 AC 时）:
- 检查 02_design.md 的需求覆盖表是否覆盖了所有 F 系 AC
- 检查 02_design_interaction.md 的需求覆盖表是否覆盖了所有 I 系 AC
- 检查 03_plan.md 的任务列表是否同时引用了 F 系和 I 系 AC
- I 系 AC 完全缺失于 plan 时标记为 WARNING: "I 系 AC 在实施计划中完全缺失"

**文档变更同步提醒**:
当检测到以下情况时，输出 INFO 级提醒（不阻塞流程）：
- 01_requirements.md 修改日期 > 01_requirements_interaction.md → "功能需求已更新，请检查交互需求是否需要同步"
- 02_design.md 修改日期 > 02_design_interaction.md → "技术设计已更新，请检查交互设计是否需要同步"
- F 系 AC 数量变化但 I 系 AC 未变 → "功能需求数量变化，请检查是否有新增功能需要交互覆盖"

**产出**:
```yaml
ac_consistency:
  total_acs: 15
  referenced_in_design: 14
  referenced_in_plan: 13
  orphaned_references: 0
  uncovered_acs: 1
  issues:
    - type: WARNING
      message: "AC-F3-2 未被任何设计节引用"
```

---

### Layer 3: Spec ↔ Tests (设计 ↔ 测试)
**检查项**:
- **Backend Tests**: 是否覆盖了 AC 和 API？
- **Frontend Tests**: 是否覆盖了组件交互和 UI 状态？

**产出**:
```yaml
spec_test_match:
  backend_coverage: 70%
  frontend_coverage: 60% (3 Component Tests missing)
  issues:
    - type: WARNING
      message: "OrderList.vue 无对应 spec 文件"
```

---

### Layer 4: Code ↔ Tests (代码 ↔ 测试)
**检查项**:
- Service 方法是否有单元测试？
- Frontend 组件是否有 Spec 文件？

**产出**:
```yaml
code_test_match:
  backend_ratio: 80%
  frontend_ratio: 50%
```

---

## 健康度计算

```python
# 基础 4 层评分
base_score = (
    prd_spec_match.score * 0.25 +
    spec_code_match.score * 0.35 +
    spec_test_match.score * 0.25 +
    code_test_match.score * 0.15
)

# 含前端深度验证时的附加评分（加权混入 spec_code 维度）
if frontend_deep_match:
    frontend_factor = (
        frontend_deep_match.component_coverage * 0.4 +
        frontend_deep_match.state_coverage * 0.3 +
        frontend_deep_match.contract_match * 0.2 +
        frontend_deep_match.a11y_baseline * 0.1
    )
    # 前端评分替代 spec_code 中的 frontend_score 部分
    spec_code_combined = spec_code_match.backend_score * 0.5 + frontend_factor * 0.5
    overall_score = (
        prd_spec_match.score * 0.25 +
        spec_code_combined * 0.35 +
        spec_test_match.score * 0.25 +
        code_test_match.score * 0.15
    )
else:
    overall_score = base_score

# AC 一致性作为独立校验（不计入百分比，但 CRITICAL 会降低信任度）
if ac_consistency.orphaned_references > 0:
    report.add_issue("CRITICAL", "存在悬空 AC 引用，请修正")
```

权重说明:
- Spec ↔ Code 权重最高 (35%)，因为"设计与实现不一致"是最严重的问题。
- PRD ↔ Spec 和 Spec ↔ Tests 各 25%。
- Code ↔ Tests 权重最低 (15%)，因为部分代码可能不需要单测。

## Checkpoint 输出模板
```
[CHECKPOINT - Step 2 Complete]

交叉比对完成。

📊 健康度评分:
- PRD ↔ Spec: 80% 🟡
- Spec ↔ Code: 75% 🟡
- Spec ↔ Tests: 70% 🟡
- Code ↔ Tests: 80% 🟢
- **综合: 76%** 🟡

🔴 Critical: 2 个
🟡 Warning: 5 个
🟢 Info: 3 个

是否生成详细报告？[Y/n]
```
