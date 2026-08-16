---
name: check-implementation-compliance
description: 检查当前实现是否符合前置依据与预期约束
next_step: references/step-03-check-quality-risks.md
---

# Step 2: Check Implementation Compliance

## 目标

先判断实现是否符合前置依据，而不是直接进入风格或最佳实践问题。

## 动作

1. 检查实现是否覆盖目标要求。
2. 检查接口、行为、结构是否与前置依据一致。
3. 标记缺失、偏差或冲突。

## 前端实现合规检查（当项目含前端代码时）

当检测到前端代码（.vue/.tsx/.jsx/.svelte 等）时，额外执行以下检查：

### 组件状态管理
- 检查是否有未处理的异步状态（loading 态缺失）
- 检查是否有直接的状态突变（应通过 store/action）
- 找到问题标记为 WARNING

### 可访问性实现
- 表单元素：是否有 label 或 aria-label
- 交互元素：是否处理键盘事件（Enter/Escape）
- 动态内容：错误/成功提示是否有 aria-live
- 找到缺失标记为 WARNING

### 响应式实现
- 如果 spec 定义了断点策略
- 检查 CSS/组件中是否存在对应的媒体查询或条件渲染
- 完全缺失标记为 WARNING

## 输出格式

- `compliance_result`
- `compliance_findings`
