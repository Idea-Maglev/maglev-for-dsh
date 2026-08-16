---
name: multica-squad-architect
description: Maglev 的 Multica 小队构造 Adapter。基于通用 Multica 小队设计方法，把小队设计落到 Maglev Squad Kit 模板、active spec、catalog、测试、文档和 Workspace 同步验证。
metadata:
  formal_action_name: Maglev 小队构造 Adapter
  top_level_capability: 能力进化
  system_layer: Evolution & Governance Layer
  lifecycle_chain: squad_template_lifecycle
  runtime_name_status: canonical_name_active
  distribution_scope: user_visible
  author: feiyu.gao
  last_updated: 2026-07-29
---

# Multica Squad Architect（Maglev 小队构造 Adapter）

这是 Maglev 对通用 `multica-squad-design-method` 的落地 Adapter。通用方法负责小队意图、角色拓扑、协同契约、Adapter Contract 和质量分级；本技能负责把这些设计落到 Maglev 的 Squad Kit 文件、active spec、catalog、验证命令和 Workspace 同步流程中。

## 负责

- 消费 `multica-squad-design-method` 产出的意图、角色拓扑、协同契约和质量目标。
- 将通用 Adapter Contract 填写为 Maglev 版本：Squad Kit 文件面、`maglev-multica` 命令面、managed marker/lock 身份面、写入门禁和验证面。
- 生成或维护 `packages/maglev-multica-kit/assets/squad-templates/<template-id>/` 下的模板资产。
- 维护 `.agents/private-catalog.yaml`、相关 README、配置指南、active spec 和测试。
- 区分已初始化仓库的 `entry-router` 能力链路与未初始化仓库的 Bridge 自包含准备模式。
- 输出 `squad_quality`，明确最多可声明到 L1/L2/L3 哪个等级。

## 不负责

- 不替代 `multica-squad-design-method` 做通用小队方法设计。
- 不替代 `spec-designer` 产出复杂产品方案；复杂小队仍应先完成需求与方案设计。
- 不直接安装或更新远端 Multica Workspace；安装、`plan`、`apply` 和 drift 处理仍由 `maglev-multica` 命令执行。
- 不替代 `integrated-validator` 做最终综合验证。
- 不把业务 Agent 的任务能力写成小队协同协议；业务能力仍由对应仓库 skill 或 Bridge 自包含模式承担。
- 不把 Maglev 的 `entry-router`、Work Graph、lease 或目录结构写成通用 Multica 必备条件。

## 何时使用

- 通用小队设计已经稳定，需要落到 Maglev Squad Kit。
- 现有 Maglev 小队模板只有角色描述，缺少稳定接力协议、Handoff、测试或质量声明。
- 小队要支持“仓库已初始化”和“仓库未初始化”两类 Maglev 运行边界。
- 需要将小队模板同步到 Maglev 的 catalog、文档、active spec 和验证链路。

## 何时不用

- 只是做通用 Multica 小队设计且不落到 Maglev：使用 `multica-squad-design-method`。
- 只是选择、安装、启用或更新已有模板：使用 `maglev-multica` CLI 或相关操作指南。
- 只是给某个 Agent 改一句提示词：走 `context-implementer` 的受控文档/配置修改即可。
- 只是验证已有实现：走 `integrated-validator`。
- 需要发现外部通用 skill：走 `skill-scout`。

## 工作流

1. **读取通用设计包**：确认小队意图、角色拓扑、协同契约和目标质量等级。
2. **填写 Maglev Adapter Contract**：映射文件面、命令面、身份面、权限面、写入门禁和验证面。
3. **落地 Squad Kit 模板**：生成 manifest、squad、agents、Bridge Skill、说明文档、catalog 和测试。
4. **对齐 Maglev 治理资产**：同步 active spec、README、配置指南、artifact purity 和索引/结晶相关检查。
5. **验证与质量声明**：运行 Maglev 验证命令，输出 `squad_quality` 和是否需要远端 `plan/apply`。

## 输出契约

一次完整小队构造至少输出：

- 通用设计包引用或摘要。
- Maglev Adapter Contract。
- Squad Kit 文件修改清单。
- active spec / catalog / 文档 / 测试更新清单。
- 验证命令与结果。
- `squad_quality` 质量声明。
- 是否需要远端 `plan/apply` 同步的判断。

## 判定纪律

- 通用方法不等于 Maglev 落地；没有 Adapter Contract 的设计不得声明为 Maglev 模板已验证。
- 小队模板不是角色名集合；没有接力协议、Handoff 和验证测试的小队最多只能声明到 L0/L1。
- Coordinator 是默认唯一接力决策者；成员默认交回 Coordinator，不横向委派。
- `entry-router` 不可加载不是失败，而是接入准备或 Bridge 自包含模式；不得假装进入仓库 Maglev 主流程。
- 写入任务必须具备 Work Graph、lease、基线提交、允许文件范围和项目负责人批准。
- 受管对象身份以 managed marker 和 lock 为准，不以展示名称为准。
- 未完成真实 Workspace 接力验证时，不得声明 `runtime_verified`。

## 来源溯源

本技能的私域基线来自 Maglev 对 `maglev-complete` 与 `maglev-legacy-onboarding` 的 Squad Kit 实践。通用方法已沉淀到 `multica-squad-design-method`；本技能只保留 Maglev Adapter 所需的文件、命令、治理和验证细节。

## 必需的参考资料

- 工作流：[`references/multica-squad-architect.workflow.md`](references/multica-squad-architect.workflow.md)
- 阶段一：[`references/step-01-squad-intent.md`](references/step-01-squad-intent.md)
- 阶段二：[`references/step-02-role-topology.md`](references/step-02-role-topology.md)
- 阶段三：[`references/step-03-collaboration-contract.md`](references/step-03-collaboration-contract.md)
- 阶段四：[`references/step-04-template-authoring.md`](references/step-04-template-authoring.md)
- 阶段五：[`references/step-05-validation-handoff.md`](references/step-05-validation-handoff.md)
- Maglev 检查清单：[`references/squad-contract-checklist.md`](references/squad-contract-checklist.md)
- Scout 证据：[`references/scout-evidence.md`](references/scout-evidence.md)

## 依赖与集成

- 上游：`multica-squad-design-method`、`requirement-convergence`、`spec-designer`
- 实施：`context-implementer`
- 质量门禁：`integrated-validator`、`artifact-purity-keeper`
- 能力演进：`skill-scout`、`skill-squadron`

## 示例

User: “把这支代码审查小队落成 Maglev Squad Kit 模板。”

AI: “我会先确认通用小队设计包，再填写 Maglev Adapter Contract，落到 Squad Kit 文件、测试、catalog 和质量声明。”
