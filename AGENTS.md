<!-- maglev:managed:discipline -->
# 🔴 会话纪律（maglev-discipline）

> 本区块为 Maglev for DSH 的会话级强制层，所有 agent 在本仓库工作时必须遵循。

## 三条不可灰度红线

1. **闭环验证**：交付前必须用证据（命令输出、文件 diff、可观察事实）说话，禁止用"已完成/已修复"代替证据
2. **事实驱动**：声明任何状态前必须有工具验证依据，禁止凭记忆/印象下结论
3. **穷尽方法**：宣告无法解决前必须走完 maglev-discipline 通用 5 步方法论

## 强制读取

进入任何主流程（`reality-sync` / `spec-designer` / `context-implementer` / `integrated-validator`）或本仓库治理任务前，必须读取 `.agents/skills/maglev-discipline/SKILL.md`，并将其红线协议作为本会话默认背景纪律。

---
<!-- /maglev:managed:discipline -->

# Maglev for DSH 仓库工作约定

## 本仓库的双重身份（dogfooding 自证）

本仓库既是**产品制品**，又是 **Maglev 机制的自证样本**：

1. **作为产品**：它是 Maglev 面向 dsh 的独立插件制品——固化 29 个技能、提供 host/client 插件（spec 工具、验证门禁、Maglev GUI），作为 dsh 插件分发。
2. **作为自证样本**：它**本身**就是通过 Maglev 机制构建和治理的——本仓库的开发也走 `entry-router → reality-sync → requirement-convergence → spec-designer → 实施 → integrated-validator → crystallization` 主链路，知识沉淀在 `specs/` 三层，决策记录在 `docs/thinking/`。

> 一句话：**Maglev 用自己构建自己，用自己治理自己。** 只有本仓库自己跑通了"迭代 → 结晶 → 知识沉淀"的闭环，才有资格论证"Maglev 作为插件真实有效"。

## 派生边界（与 Maglev 源的关系）

- 本仓库从 Maglev 私域源仓库**一次性派生**（详见 `specs/10_reality/README.md` 的派生来源记录）。
- **零运行时依赖**：本仓库不引用 Maglev 源仓库路径、不依赖 Maglev 的 npm 包。
- 技能资产在本仓库**独立演进**（派生分叉），与 Maglev 源的后续变更互不同步。

## 知识分层（本仓库自己的知识资产）

| 层 | 路径 | 回答的问题 |
|---|---|---|
| 当前事实 | `specs/10_reality/` | 本插件现在是什么（固化清单、验证状态、已成立的事实） |
| 演进主题 | `specs/20_evolution/` | 正在推进什么（host/client 插件、GUI 等） |
| 历史归档 | `specs/90_archive/` | 曾经做过什么（已结晶的历史依据） |

决策逻辑记录在 `docs/thinking/`。任何会话都能从这三层重建本仓库的上下文——这正是"降低对人和 AI 体系依赖"在本仓库身上的自证。

## 目录速查

| 目录 | 用途 |
|------|------|
| `.agents/skills/` | 29 个固化技能（产品资产 = 本仓库自治理技能）+ `_internal` 协议主体 |
| `packages/host/` | dsh host 插件（TypeScript：spec 工具、结晶事件） |
| `packages/client/` | dsh client 插件（React：Maglev 面板、结晶卡片） |
| `assets/` | preset、workflow、验证脚本等静态资产 |
| `scripts/` | maglev-python 运行时、验证工具 |

## Git 分支约定

- 默认主分支：`master`。
- 新需求必须新分支：`feat/<描述>`、`fix/<描述>`、`docs/<描述>`。
- 版本发布、紧急热修复、仓库治理类操作可直接在主分支。

## 工作原则

- **可追溯性**：把"为什么"（docs/thinking/）与"是什么"（specs/）连接，不只看 Spec 不看上下文。
- **主动维护**：发现索引报错、spec 与 issue 不同步、断链时，主动提议修复。
- **治理前置（dogfooding）**：任何新的插件能力，先以本仓库自身为样本验证，通过后再对外。
