# 反模式：文档写命令不验证可执行性（dsh 无全局命令）

> 记录时间: 2026-08-18
> 位段: `70_retrospective`（复盘室）— 反模式与教训沉淀
> segments_source: .agents/skills/knowledge-check/references/segments-canonical.yaml

## 一句话

**写文档时假设了一个"不存在的命令"，导致用户按文档操作处处碰壁。** 本次案例：文档里写 `dsh plugin add ...`，但 dsh 是 developer preview，**没有全局 `dsh` 命令**，实际是 `pnpm dsh ...`（在 dsh checkout 目录下）。

## 现象与误导链

整轮"怎么用起来"的对话中，我反复给用户流程，用户始终走不通。最终用户自己点破：**"dsh 实际是 pnpm dsh 这个命令，并没有注册到全局"**。

查证后确认：
- dsh 没有全局命令（`command -v dsh` 为空）
- 真实入口是 `pnpm dsh`（= `node --import tsx/esm apps/cli/src/bin.ts`，在 dsh checkout 目录下）
- 我一直写 `dsh plugin add`、`dsh --profile web`，全是错的

## 根因（两层）

1. **写文档/给流程时，没有先验证命令是否真的存在、能否执行**——凭"惯例"假设了 `dsh` 命令，没查 `command -v dsh`。
2. 更深的：我在开发/验证时一直用 `node $DSH/apps/cli/lib/bin.js`（编译产物）或 `pnpm dsh`（源码），但给用户的文档里却写成了不存在的 `dsh`——**我自己验证用的命令，和文档里写的命令，不一致，且没发现**。

## 治理点（沉淀为文档原则）

- **文档里的任何命令，必须先实际执行验证过，再写进去**（不是"应该能跑"，是"我跑过"）。
- **给用户的命令，必须和"我自己实际用的命令"完全一致**。如果我用的是 `node bin.js` 而文档写 `dsh`，这个不一致本身就是 bug。
- 对 developer preview 类工具，明确标注"无全局命令，需在 checkout 下用 pnpm/源码入口"，而不是默认用户有命令。

## 影响与收口

- README / usage.md 已全部修正为 `pnpm dsh ...`（见 0.1.5 待发）。
- 与 `2026-08-18-legacy-pattern-misleading-in-derivation.md`（被源环境陈旧模式误导）同类：都是"假设了不存在的机制/命令"。两者可合并为一条元规则：**写任何"用户怎么做"的指引前，先亲自走通一遍**。
