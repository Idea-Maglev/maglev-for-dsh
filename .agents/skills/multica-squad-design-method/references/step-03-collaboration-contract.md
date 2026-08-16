---
name: step-03-collaboration-contract
description: 定义 Multica 原生接力、Handoff、横向委派边界和失败排查
next_step: references/step-04-adapter-contract.md
---

# Step 3: Collaboration Contract

## 目标

让小队通过明确协议协作，而不是依赖成员“读懂上下文”的聊天默契。

## 必须写入的协议点

1. Coordinator 是唯一默认路由者。
2. Coordinator 每轮只委派一个主责任角色。
3. 委派必须使用 Squad Roster 中的精确 mention markdown：`[@名称](mention://agent/<uuid>)`。
4. 必须发布新评论触发，不得编辑旧评论补 mention。
5. 不得使用裸 `@name`。
6. 成员只响应属于自己的新委派 Task。
7. 成员完成、阻塞或失败时必须发布标准终态 Handoff。
8. 成员默认交回 Coordinator 评估。
9. 成员不得横向互相委派。
10. 只有 Coordinator 委派评论明确授权“一次性只读并行审查”时，成员才可以 mention 指定协作者。
11. 自动接力失败时按顺序检查：
    - 目标 Agent 是否对 Workspace 可调用。
    - Runtime 是否在线。
    - mention markdown 是否为 `mention://agent/<uuid>` 或 `mention://squad/<uuid>` 精确格式。
    - 评论是否为新建评论而不是编辑旧评论。

## 通用标准 Handoff

```markdown
## Multica 小队 Handoff

- 状态：completed / blocked / failed
- 当前角色：
- 当前阶段：
- 输入证据：
- 输出产物：
- 事实结论：
- 推断结论：
- 未知项：
- 是否修改外部状态：
- 修改范围：
- 基线：
- 验证命令或验证动作：
- 阻塞原因：
- 下一建议责任人：
- 是否需要负责人确认：
```

## Handoff 规则

- `状态` 必须三选一：`completed` / `blocked` / `failed`。
- 有证据的内容进入“事实结论”；没有证据的内容进入“推断结论”或“未知项”。
- 成员只能提出“下一建议责任人”，不能把它当成已委派任务。
- 如修改了外部状态，必须写明修改范围、基线和验证动作。

## 输出

- 协同协议段落。
- Handoff 格式。
- 横向委派边界。
- 自动接力失败排查顺序。
