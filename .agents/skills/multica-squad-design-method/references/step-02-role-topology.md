---
name: step-02-role-topology
description: 设计 Coordinator 与成员角色拓扑
next_step: references/step-03-collaboration-contract.md
---

# Step 2: Role Topology

## 目标

把任务能力拆成稳定角色拓扑，避免多个 Agent 都能决策、都能写入或互相循环委派。

## 动作

1. 选择唯一默认 Coordinator：
   - Coordinator 负责分流、评估 Handoff、升级阻塞和决定下一责任人。
   - Coordinator 不应替代成员产出主体结论。
2. 为每个成员定义：
   - 角色名。
   - 职责。
   - 读写边界。
   - 准入条件。
   - 必要输入。
   - 输出产物。
   - 阻塞条件。
   - 默认交回对象。
3. 检查职责互补：
   - 避免两个成员负责同一最终结论。
   - 避免审计者审计自己主持的流程。
   - 避免成员既执行又批准自己的写入。
4. 检查并发：
   - 默认串行接力。
   - 只有只读、互不依赖、Coordinator 明确授权时才允许一次性并行。
5. 检查权限：
   - 哪些角色只读。
   - 哪些角色可能写入。
   - 哪些角色需要外部系统权限。

## 输出

| role | 职责 | 读写边界 | entry_conditions | outputs | default_return |
|---|---|---|---|---|---|
| coordinator | 选择下一责任人 | 只读或按 Adapter 限制 | 已获得任务上下文 | 委派、评估、升级 | requester |
