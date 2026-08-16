# Scout Evidence

通用多 Agent 协作原则已沉淀到 `multica-squad-design-method`。本文件记录 Maglev Adapter 继续引用的证据来源，用于说明为什么 Maglev Squad Kit 仍要坚持清晰角色、单一下一责任人、层级委派、防循环和终止条件。

## 联网校验记录

### AutoGen Selector Group Chat

- URL: https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/selector-group-chat.html
- 类型：官方文档
- 高相似度理由：
  - 说明通过参与者名称与描述选择下一 Agent。
  - 强调一次选择一个下一发言者。
  - 提供终止条件，避免多 Agent 循环。
- 本技能使用方式：
  - 作为“角色描述必须可被路由消费”“每轮只选择一个下一责任者”“必须定义终止/阻塞条件”的辅助参照。

### CrewAI Collaboration

- URL: https://docs.crewai.com/v1.15.8/en/concepts/collaboration.md
- 类型：官方文档
- 高相似度理由：
  - 强调清晰角色定义、层级协作、委派权限和防止 delegation loop。
  - 明确协作失败常见问题包括角色不清、上下文不足和过度往返。
- 本技能使用方式：
  - 作为“Coordinator 才能委派”“成员默认不横向委派”“任务描述必须包含上下文和退出条件”的辅助参照。

## 分层取舍

- 通用层只保留 Multica 原生协作方法：Coordinator、精确 mention、新评论、Handoff、禁止横向委派和 Runtime Proof Gate。
- Maglev Adapter 保留 Maglev 专属边界：`entry-router` 双路径、Bridge 自包含准备模式、`packages/maglev-multica-kit/` 模板资产、managed marker / lock、Work Graph、lease、基线提交、允许文件范围和项目负责人批准。
- 因此，分享通用方法时不会携带 Maglev 私域假设；落到 Maglev 时也不会丢失项目治理门禁。
