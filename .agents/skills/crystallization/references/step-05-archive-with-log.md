---
name: archive-with-log
description: 当 active 判定 close 时，执行结构化归档
next_step: null
---

# Step 5: Archive with Log

## 目标

在 active close 后，将已完成的 spec 归入 90_archive，并附带结构化归档日志。

## 触发条件

仅当 Step 3 判定 `active_decision: close` 时执行此步骤。若为 `continue` 或 `split`，输出 `skipped: not a close decision` 后结束。

## 前置条件（门禁）

在执行文件搬迁前，逐项确认：

1. ✅ Step 2 的 Reality 回写已执行（10_reality 有对应更新）
2. ✅ spec 索引页已更新状态为 Archived（标准结构使用 `00_index.md`；遗留主题可使用 `README.md`）
3. ✅ 归档日志已填写到该索引页中
4. ✅ 90_archive/README.md 索引条目已准备
5. ✅ 测试证据链保留：若当前主题涉及正式测试文件（tests/），归档日志必须引用这些测试文件路径，防止归档后测试证据链断裂

**任意一项未通过 → 报告缺失项，不执行搬迁。**

## 动作

1. 在 spec 索引页中填写归档日志（按模板）
2. 更新 spec 索引页状态为 Archived
3. 准备 90_archive/README.md 索引条目
4. 执行 4 项门禁检查
5. 全部通过后执行 mv
6. 更新 20_evolution/active/README.md（移除条目）
7. 更新 90_archive/README.md（新增索引行）
8. 若步骤 5-7 全部成功，调用 `project-board` Skill 更新看板，将已归档需求从总看板中移除。若步骤 5-7 中任何一步失败，跳过看板更新并报告原因

## 跨分支归档编号冲突

当多个 feature 分支并行进入结晶阶段、都在 `90_archive/README.md` 末尾追加索引行时，**编号会冲突**（两个分支都用 master 的下一个空位编号）。

**症状**：在自己的分支执行 `git rebase master` 或在 GitLab 触发 MR merge 时，`90_archive/README.md` 报 content 冲突，两条新行都占用同一个 #N。

**解决方案（约定按完成时间序排列）**：

1. **先合者保留原编号**：先 merge 进 master 的主题继续占 #N（自然 fast-forward 或 GitLab merge commit）。
2. **后合者 rebase 让位**：后到的分支 rebase master 后，把自己的索引行编号从 #N 改为 #N+1，并把先合者的 #N 行也保留进自己的版本（即接受 master 的 #N + 追加自己的 #N+1）。
3. **commit message 中的旧编号不强求 amend**：commit message 只是历史描述，不影响 master 内容；可选择在 rebase 时 amend 修正描述，或保留原文加 commit 备注（后者更轻量）。

**触发预防**：本协议要求 Step 5 步骤 3 "准备 90_archive/README.md 索引条目" 时，**检查同主题分支是否已有未合 MR 占用相邻编号**，若有则提前用 #N+1 起步避免 rebase 工作量。

## 归档日志模板

在 spec README 的状态段落后新增：

```markdown
## 归档日志

- **结晶状态**：✅ 已完成 → [10_reality 落点链接]
- **关键结论**：[1-3 句概括写入 reality 的核心内容]
- **执行经验**：[这个需求实际执行中的经验/教训]
- **测试证据**：[若当前主题有正式测试文件 tests/*.py，列出路径；用于防止归档后证据链断裂]
- **时间线**：YYYY-MM-DD 启动 → YYYY-MM-DD 归档
```

## 输出格式

- `archive_gate_passed: yes | no`
- `gate_failures`（如有）
- `archive_log_summary`

## 输出

- 一份门禁检查结果
- 一份已填写的归档日志
- 一组执行的文件操作
