# maglev spec-check adds non-empty docs/thinking check

> 结晶时间: 2026-08-15T14:49:42.421Z

maglev_spec_check 新增第 13 项检查 docs_thinking：docs/thinking/ 存在且至少含一个 .md 才 PASS，修复空目录假阳性；本仓库补决策记录后 13/13 全过。

# 结论

`maglev_spec_check`（host 插件 `index.ts`）新增第 13 项检查 `docs_thinking`：`docs/thinking/` 目录**存在且至少含一个 `.md` 文件**才 PASS，否则 FAIL。

## 变更明细

- `index.ts` 新增辅助函数 `dirHasMarkdown(p)`：用 `readdir(withFileTypes)` 判断是否存在 `isFile() && name.endsWith('.md')` 条目，目录缺失走 `catch`，区分「目录缺失」与「目录空/无 .md」。
- `runSpecCheck` 在 specs 骨架（4 项）+ AGENTS.md 纪律（1 项）+ 主链路技能（7 项）之后追加 `docs_thinking`（1 项），合计 13 项。
- 工具 description 同步为「…主链路技能、docs/thinking 决策记录（非空）…」。
- 补 `docs/thinking/2026-08-15-spec-check-requires-non-empty-thinking.md` 决策记录，使本仓库自身通过新检查。
- `specs/10_reality/README.md` 检查项计数 12 → 13，并同步工具描述。

## 根因

仓库定位要求「为什么」（`docs/thinking/`）与「是什么」（`specs/`）连接，但 `maglev_spec_check` 此前完全不检查 `docs/thinking/`，导致「存在但为空」的目录也能让整体检查 PASS（假阳性）。

## 验证证据

- 真实执行（Node 24 原生 TS 加载修改后的 `index.ts`，驱动 `apply` 注册的 `maglev_spec_check.execute`）：
  - 空 `docs/thinking/`：`docs_thinking` → FAIL「docs/thinking (empty or no .md)」，pass=12 fail=1（假阳性已修复）。
  - 补 `.md` 后：`docs_thinking` → PASS，pass=13 fail=0。
- 会话内调用 `maglev_spec_check` 工具返回 12 项（会话启动时已加载的旧插件实例，未热重载）；本改动需重启会话生效，真实执行测试为本改动的闭环证据。

## 已知边界

`scripts/spec_integrity_check.py` 是另一套独立校验脚本（Python），同样未检查 `docs/thinking/`；本次迭代范围限定 `index.ts` 的 `maglev_spec_check`，该脚本作为后续对齐项待办。

