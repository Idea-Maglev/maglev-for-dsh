---
name: step-04-ai-context-check
description: AI 上下文就绪检查
---

# Step 4: AI Context Readiness Check

## 目标

在初始化完成后，判断项目的 `AGENTS.md` 与 `llms.txt` 是否已经足以辅助 AI 理解当前项目与 Maglev 的基本操作方式。

## 执行关系

这一步的职责是把 AI context readiness check 纳入 `maglev-bootstrapper` 的初始化语义。

首轮真实执行面位于：

- `packages/maglev-cli/dist/maglev_installer.py`

也就是说：

1. `maglev-bootstrapper` 负责承接、解释与结果口径
2. installer 负责在 `init` 结束时真实运行检查
3. 不在 skill references 里再复制一套独立实现

## 参考契约

- `../../_internal/ai-context-check/contract.md`

## 动作

1. 检查根目录是否存在：
   - `AGENTS.md`
   - `llms.txt`
2. 如果存在，按统一契约判断：
   - 是否达到最小可用标准
   - 是否已经明显漂移
   - 是否混入上游私有仓库现实
3. 如果不存在或不足：
   - 不要假装已经就绪
   - 明确告诉用户缺什么
   - 给出最小补齐建议

在通过 AI 入口解释初始化结果时，应以 installer 的实际检查结果为准。

## 输出要求

输出时使用四段结构：

1. `存在性`
2. `充分性`
3. `漂移风险`
4. `最小补齐建议`

## 初始化后的判断原则

### 可判为 Ready

满足下面条件时，可判为 AI context 已达到最小可用标准：

1. `AGENTS.md` 与 `llms.txt` 至少存在其一，且另一项即使缺失也不会让 AI 严重失去方向
2. 当前项目目标、关键入口或主要目录有最小说明
3. 已说明当前项目如何使用 Maglev，或至少指出主流程 / 兼容入口

### 不可判为 Ready

出现下面情况时，不应直接说“初始化已完整就绪”：

1. 两个文件都缺失
2. 文件存在，但只包含空泛口号，无法指导 AI 理解当前项目
3. 内容仍把旧 runtime name 当成唯一现役真名
4. 内容明显照搬上游 Maglev 仓库私有现实

## 完成提示

完成初始化总结时，应额外说明：

1. AI context 是否已达到最小可用标准
2. 如果没有，还缺哪些项
3. 用户下一步最值得先补的 1-2 个点是什么
