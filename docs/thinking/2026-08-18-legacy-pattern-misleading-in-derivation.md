# 反模式：派生制品被源环境的陈旧机制误导

> 记录时间: 2026-08-18
> 位段: `70_retrospective`（复盘室）— 反模式与教训沉淀
> segments_source: .agents/skills/knowledge-check/references/segments-canonical.yaml

## 一句话

**派生/迁移制品时，容易把"源环境的实现机制"误当成"目标环境的必需机制"，照搬过来反而引入陈旧包袱。** 本次案例：把 maglev-cli（Codex 时代）的 workflows/hooks 误当成 dsh 的斜杠命令机制。

## 现象与误导链

排查"为什么 `/maglev-init` 在 dsh 里看不到"时，我一度得出错误结论：

1. 看到源仓库 `packages/maglev-cli/dist/.agents/workflows/` 有 26 个 `maglev-init.md`、`standup.md`，以为"斜杠命令要靠这些 workflow 文件"
2. 看到 `.codex/hooks/`，以为"命令/流程需要 hooks"
3. 结论：插件缺 workflow 文件、缺 `commands.register`，需要补

## 真相（dsh 的原生机制）

查证 `dsh-host-apiproxy` 后确认：**dsh 里"技能即命令"**——

```ts
// api-proxy.ts：'/' 命令 popup 的数据源
const skills = (await skillRegistry.list({ cwd, scope })).filter(isUserInvocable)
```

- 技能 frontmatter/注入的 `invocation.userInvocable = true` → 技能名直接进 '/' 命令目录
- `/reality-sync`、`/maglev-bootstrapper`、`/crystallization`… 技能名就是命令名
- 之前"看不到 `/maglev-init`"，是因为 `/maglev-init` 是 Codex workflow 的名字；真正的技能命令是 `/maglev-bootstrapper`

**结论**：`.agents/workflows/*.md`、`.codex/hooks/`、`commands.register` 全都**不需要**——它们是 maglev-cli 面向 Codex 的陈旧机制，dsh 用"技能即命令"原生覆盖了同一能力。

## 治理点（建议沉淀为派生工程原则）

派生一个制品时，要区分两样东西：

| 层 | 含义 | 迁移策略 |
|---|---|---|
| **能力意图** | "用户能用命令入口触发流程" | 保留，必须迁移 |
| **机制实现** | 源环境如何实现这个意图（Codex 的 workflow md + hooks） | 不照搬，改用目标环境的原生机制（dsh 的技能 userInvocable） |

**判断方法**：迁移前先问"目标环境原生怎么实现这个能力"，而不是"源环境用了什么文件、搬过来"。本次反模式正是跳过了这一步，直接按源仓库的目录结构找"缺什么文件"。

## 影响与收口

- 补齐清单从"缺 workflows/hooks/commands/catalog 一大块"**缩小到只剩一处**：`maglev_installer.py`（骨架注入的执行物）未随插件打包 → "初始化/接入"执行时卡住。
- 这是后续要单独治理的点：执行类技能（bootstrapper/legacy-adopter）缺"注入骨架"的资产，与命令机制无关。
