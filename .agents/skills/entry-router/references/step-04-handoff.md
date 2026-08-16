---
name: handoff
description: 向目标对象完成最小必要交接
next_step: null
---

# Step 4: Handoff

## 目标

用最小必要信息把会话交接给目标对象。

## 动作

1. 输出简洁交接说明：
   - 当前识别到的任务类型
   - 当前选择的目标对象
   - 进入该对象前最关键的上下文
2. 不重复展开后续对象本应负责的完整工作。
3. 如目标对象是 workflow，明确指出应进入哪个 workflow。
4. 如目标对象是 skill，明确指出应调用哪个 skill。

## 交接规则

- 只交接后续对象必需消费的上下文。
- 不在 handoff 中提前展开后续对象完整工作。
- 若目标对象已有正式动作名，可同时给出对象名与动作名，降低混淆。

## 输出格式

- `target_object`
- `target_action`
- `handoff_summary`

## 输出

- 一份最小必要的 handoff 指令
- 结束入口层处理
