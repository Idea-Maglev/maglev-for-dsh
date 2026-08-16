---
name: suggest-test-layers
description: 根据覆盖策略建议合适的测试层次
next_step: references/step-04-suggest-artifacts.md
---

# Step 3: Suggest Test Layers

## 目标

把覆盖策略映射到合适的测试层次。

## 动作

1. 判断哪些内容适合单元测试。
2. 判断哪些内容适合集成测试。
3. 判断哪些内容适合场景测试或更高层验证。

## 前端测试层设计（当项目含前端组件时）

当检测到前端组件（.vue/.tsx/.jsx/.svelte 等）时，在后端测试层之外额外建议前端特有层次：

| 测试层 | 目标 | 工具建议 | 关键场景 |
|--------|------|---------|---------|
| 组件交互测试 | Props/Events/Slots 契约 | @testing-library/vue 或 react | 输入→事件触发→状态变化 |
| UI 状态转换测试 | 状态机覆盖 | 同上 | 空→加载→成功/错误→重试 |
| 可访问性测试 | ARIA/键盘/对比度 | axe-core / jest-axe | 焦点顺序、朗读、对比度 |
| 快照/视觉回归 | UI 一致性 | 按项目选择 | 关键页面/组件渲染 |

注意：快照测试为可选推荐，不强制要求。工具建议仅作参考，以项目已有测试栈为准。

## 输出格式

- `unit_test_targets`
- `integration_test_targets`
- `scenario_test_targets`
- `frontend_test_targets`（当含前端组件时）
