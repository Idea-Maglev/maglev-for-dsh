# maglev_spec_check 新增 docs/thinking 非空检查

> 决策时间: 2026-08-15

## 决策

`maglev_spec_check` 的 `runSpecCheck` 新增一项检查 `docs_thinking`：`docs/thinking/` 目录**存在且至少含一个 `.md` 文件**才 PASS，否则 FAIL（区分「目录缺失」与「目录空/无 .md」两种情况）。

## 为什么（根因）

- 本仓库的定位是「可追溯性」：把「为什么」（`docs/thinking/`）与「是什么」（`specs/`）连接。
- 但 `maglev_spec_check` 此前只检查 specs 分层骨架、AGENTS.md 纪律区块、主链路技能，**完全没有检查 `docs/thinking/`**。
- 更糟的是，一个「存在但为空」的 `docs/thinking/` 也能让整个检查 PASS —— 这是假阳性：决策记录缺失不会被门禁发现。

## 修复方式

- 新增 `dirHasMarkdown(p)` 辅助函数：`readdir` 后判断是否存在 `isFile() && name.endsWith('.md')` 的条目，目录缺失走 `catch`。
- `runSpecCheck` 末尾追加 `docs_thinking` 检查项（原 12 项 → 13 项）。
- 工具 description 同步补充「docs/thinking 决策记录（非空）」。

## 验证证据

- 空 `docs/thinking/`：`docs_thinking` → FAIL（`docs/thinking (empty or no .md)`），修复了假阳性。
- 补入本决策记录后：`docs_thinking` → PASS，13 项全过。
