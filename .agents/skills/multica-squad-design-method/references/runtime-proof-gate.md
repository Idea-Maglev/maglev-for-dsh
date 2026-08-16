# Runtime Proof Gate

Runtime Proof Gate 用于判断小队是否可以声明 `runtime_verified`。

## 必须证据

- Workspace 或等价运行空间 ID。
- 小队、Coordinator、成员 Agent 的对象 ID。
- 触发输入链接或摘要。
- Coordinator 新建评论中的精确 mention markdown。
- 成员终态 Handoff。
- Coordinator 对 Handoff 的消费结果。
- 自动接力失败时的排查记录，或成功接力的可观察证据。

## 最小场景

1. `completed` 场景：
   - Coordinator 委派成员。
   - 成员完成任务并发布 Handoff。
   - Coordinator 结束或派发下一步。
2. `blocked` 场景：
   - 成员识别缺失输入、权限或批准。
   - 成员发布 blocked Handoff。
   - Coordinator 升级给负责人或请求补充输入。

## 不能替代 Runtime Proof 的证据

- 静态模板校验。
- 单元测试。
- 本地 `plan` 或 dry-run。
- 手工阅读提示词。
- 只创建远端对象但没有真实接力。

这些证据可以支撑 L2，不能支撑 L3。
