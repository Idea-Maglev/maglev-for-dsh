# Collaboration Quality Rubric

## L0: Draft

满足任一条件即为 L0：

- 只有角色名称或角色清单。
- 没有唯一 Coordinator。
- 没有标准 Handoff。
- 没有说明成员能否横向委派。
- 没有失败排查顺序。

允许声明：`draft`。

## L1: Collaboration Designed

必须全部满足：

- 唯一默认 Coordinator。
- 每轮只委派一个主责任角色。
- 使用精确 mention markdown。
- 新评论触发，不编辑旧评论补 mention。
- 禁止裸 `@name`。
- 成员默认交回 Coordinator。
- 禁止横向委派，并定义一次性只读并行审查例外。
- 标准 Handoff 字段完整。
- 自动接力失败排查顺序完整。

允许声明：`draft`、`collaboration_designed`。

## L2: Template Verified

必须满足 L1，并且 Adapter 提供：

- 模板或配置资产已经落地。
- 资产可被目标平台发现或加载。
- 静态校验通过。
- 至少覆盖关键协同协议的测试或检查。
- 写入门禁有明确证据要求。

允许声明：`draft`、`collaboration_designed`、`template_verified`。

## L3: Runtime Verified

必须满足 L2，并且完成真实 Workspace 验证：

- 使用真实 Task 或等价触发机制。
- Coordinator 能成功 mention 目标成员并创建任务。
- 成员能发布终态 Handoff。
- Coordinator 能消费 Handoff 并决定下一步或结束。
- 至少覆盖 completed 与 blocked 两类终态。
- Runtime Proof 记录包含时间、Workspace、对象 ID、触发输入和验证结果。

允许声明：`draft`、`collaboration_designed`、`template_verified`、`runtime_verified`。
