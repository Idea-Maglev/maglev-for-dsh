---
name: reality-sync
description: 会话启动器 (Session Bootstrapper)。快速同步主线、风险与下一步动作，让 AI 进入正确工作模式。
metadata:
  formal_action_name: 现状同步
  top_level_capability: 现状同步
  system_layer: Core Flow Layer
  lifecycle_chain: main_flow
  runtime_name_status: canonical_name_active
  distribution_scope: user_visible
  author: feiyu.gao
  last_updated: 2026-03-30
---

# Reality Sync (会话启动器)

## 概览 (Overview)

`现状同步（reality-sync）` 是面向项目贡献者与维护者的会话启动器，负责在每次会话开始时快速建立对当前仓库真实状态的可操作认知。

调用入口：

- 结构动作名：`现状同步`
- 运行面名称：`reality-sync`
- 兼容 workflow 入口：`/standup`

## 为什么需要它？

仅靠记忆或过时的文件约定，AI 容易在会话起点：

- 误判当前主线
- 忽略结构性风险
- 给出错误的下一步建议

reality-sync 通过 Reality / Risk / Action / Mode 四类同步，把会话起点对齐到当前仓库的真实状态。

## 核心能力 (Capabilities)
1. **Reality Sync**: 识别当前主 Spec、主实现、关键发行物和历史资产。
2. **Risk Sync**: 识别当前最重要的结构风险、试用反馈和未闭环项。
3. **Action Sync**: 基于 active specs / issues / 计划文档生成下一步建议。
4. **Mode Sync**: 判断当前更适合进入 `Analyze`、`Implement`、`Verify` 还是 `Release` 模式。

## 生命周期提醒 (Lifecycle Reminder)

当会话涉及“收口 / 结晶 / 归档 / 迁移”时，必须先做最小分层提醒：

- `10_reality` = 当前已经成立的事实
- `20_evolution` = 仍在推进的主题
- `90_archive` = 历史依据与过程保留

若用户目标属于收口类任务，不得默认把“归档”理解成可直接写进 Reality，或把演进目录当历史存储层。

## 何时使用 (When to use)
- 每天第一次打开会话时。
- 仓库刚经历一轮大改、试用反馈或 spec 收口之后。
- 感觉 AI “失忆”、抓错主线、或不知道下一步该先做什么时。
- 在开始测试、发版或较大重构之前。

## 交互模式 (Interaction)

- **背景纪律**：本 skill 执行期间持续遵循 `maglev-discipline` 红线（闭环验证 / 事实驱动 / 穷尽方法），每个 step 起始前先做 `[MAGLEV-DIAGNOSIS]` 自检
- **启动期漂移哨兵**：reality-sync 启动时先跑 `./scripts/maglev-python --doctor` 进行运行时 preflight，再跑 `./scripts/maglev-python .agents/skills/index-librarian/protocol/scripts/track_verify.py --track-id skills`；若 preflight 失败，必须 surface `env_failed` 并给出安装 `uv` 或 Python>=3.11 的修复动作；若 verify exit ≠ 0，再 surface track 状态（`partial` / `failed`）并提示用户运行对应 `track_scan --track-id skills` 重建
- **索引健康**：只检查入口索引是否可验证和新鲜，不自动发起任务级检索；任务级导航仍由后续受控阶段消费收据。

## 交互示例
User: "Standup."

AI:
```
[Space]
当前主线是 `maglev_distribution`，主执行核心位于发行构建沙箱 `.maglev_build/` 与包内镜像 `packages/maglev-cli/dist/`，Npx 包装层在 `packages/maglev-cli/`。

[Mind]
最近已确认 `version_sync_tool` 已被吸收，旧同步实现已移除，当前进入试用反馈驱动的分发治理阶段。

[Risk]
当前重要风险是发行物仍可能暴露过多底层实现，以及 AI 操作层尚未补齐更新入口。

[Action]
建议先修复当前试用暴露的问题，再跑一次更新链路验证，而不是先做发版。

[Mode]
Implement
```

## 输出要求 (Output Contract)
输出必须包含以下 5 段：

1. `Space`
2. `Mind`
3. `Risk`
4. `Action`
5. `Mode`

其中：

- `Action` 应只给出 1-3 个最优先动作
- `Mode` 必须是单个推荐模式
- 允许简洁，但不允许泛化、空泛或仍停留在过时上下文
- 不把当前结构动作名误解为已完成运行面重命名
