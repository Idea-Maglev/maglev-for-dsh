---
name: extension-evolver
description: 扩展迭代器。用于维护已存在的 Maglev Extension Pack：分析变更影响，更新 manifest 与资产，记录决策和验证证据，并准备 Registry 发布交接。
metadata:
  formal_action_name: 扩展迭代
  top_level_capability: 能力进化
  system_layer: Extension Layer
  lifecycle_chain: extension_evolution
  runtime_name_status: canonical_name_active
  distribution_scope: user_visible
  author: feiyu.gao
  last_updated: 2026-07-28
---

# Extension Evolver

用于扩展作者或 Registry 维护者对已发布的 Extension Pack 做受控迭代。它把一次变更的意图、兼容性判断、验证证据和发布信息写回扩展 source，而不是依赖会话记忆。

## 边界

负责：

- 读取 `extension.yaml`、Registry entry、已安装项目的 `.maglev/extensions.lock`，界定本次变更影响。
- 判断变更是文档澄清、资产修订、安装路径调整、Slot 契约变化还是来源/发布变化。
- 编排现有 `maglev-extension check`、`test-install` 和真实 Registry install/update/remove 验证。
- 在扩展 source 的 `maintenance/` 下记录决策、兼容性、验证命令与结果摘要。
- 准备 Registry entry、source ref 与发布交接信息。

不负责：

- 替代 `extension-manager` 的消费者安装、启用或移除动作。
- 自动把所有维护记录分发到消费者项目。
- 未经证据开放新 Slot，或把 asset pack 伪装成 Slot plugin。
- 替代发布审批、远程推送或 CI 权限。

## 记录约定

扩展 source 使用以下可选但对持续维护必需的目录，不进入 `contents` 安装清单：

```text
maintenance/
├── README.md
└── records/
    └── YYYY-MM-DD-<topic>.md
```

首次纳入维护时创建 `maintenance/README.md`。每次可发布变更新增一份 record，使用 [维护记录模板](references/maintenance-record-template.md)。记录必须包含变更意图、影响资产、兼容性结论、验证证据、Registry/source ref 和已知风险。

## 工作流

1. **确认对象与基线**：定位 extension root、manifest、Registry entry 和 source ref；若修改的是已安装扩展，读取 lock 的 resolved commit，禁止只凭 Registry 当前内容推断基线。
2. **分类影响**：列出变更资产及受影响的 skill、引用、脚本、安装路径、Slot 和消费者。安装路径、删除资产、Slot 或 compatibility 变化必须视为兼容性变更。
3. **设计最小变更**：更新资产、`extension.yaml` 和用户文档；维护记录不加入 `contents`。若 Registry 与 pack 同仓，仍将 Registry entry 与 pack 视为两个独立校验面。
4. **记录判断**：在 `maintenance/` 写入 record。不能确认兼容性时必须明确标为阻塞，不得用“可能兼容”发布。
5. **运行验证**：至少运行 `maglev-extension check` 和隔离项目 `test-install`；可从 Git source 消费时，还必须运行 `search → install → update → remove`。脚本运行时仅验证该 pack 明确声明的前置条件。
6. **发布交接**：确认 manifest version、Registry source/ref、目标发布分支或 tag 一致。未推送的本地 ref 不是发布完成；在 record 中明确记录发布状态。

## 决策规则

- 仅改说明且不改变已安装文件、行为或兼容性：记录为 patch，并说明无需迁移的依据。
- 新增安装资产或改变行为：记录为 minor，并说明已有消费者 update 后的可观察变化。
- 删除/移动安装资产、改变 skill id、Slot、默认启用或提高运行时要求：记录为 breaking，提供迁移或明确停止发布。
- `python3`、Node、网络或凭据要求属于 pack 运行时约束，必须在 README 和记录中说明；不得归因给 Extension CLI。
- 真实 Git 验证必须记录 Registry commit 与 asset source commit；branch 名称不是可复现实证。

## 交接

- 消费者接入、更新或移除：交给 `extension-manager`。
- 新扩展从零生产：先用 `extension-manager` 的 authoring 命令创建和检查，再由本 skill 建立维护记录。
- 新 Slot 论证：交给 `spec-designer`，本 skill 只保存现有 Slot 的变更证据。
