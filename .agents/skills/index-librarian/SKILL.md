---
name: index-librarian
description: 项目索引管家 — 编排确定性脚本完成相邻 INDEX.md 知识记录、任务导航收据和目录树、仓库入口、代码树三类索引产物的扫描、验证与地图生成。当需要降低定位权威文件的成本或确认索引数据准确性时，使用这个技能。
metadata:
  formal_action_name: 项目索引维护
  top_level_capability: 项目索引维护
  system_layer: Foundation Layer
  lifecycle_chain: governance_loop
  runtime_name_status: canonical_name_active
  distribution_scope: runtime_internal
  author: feiyu.gao
  last_updated: "2026-07-22"
  version: "3.3.2"
---

# Index Librarian (项目索引管家)

## 概览

按 `index-librarian/protocol/registry.yaml` 中 `tracks:` 段的声明，编排 `index-librarian/protocol/scripts/track_*.py` 与 `task_navigate.py`，为仓库提供相邻知识索引、任务导航收据及三类索引/地图产物：

| Track 类型 | 适用对象 | 主要产物 |
|:---|:---|:---|
| `dir-tree` | 任意目录树 (specs/, docs/, 自定义) | 各级 `INDEX.md`（entity-index 网络）+ summary YAML |
| `repo-entry` | 仓库根目录 | `repo-entry.yaml`（锚点）+ `repo-map.md`（人读地图） |
| `code-tree` | `packages/` / `src/` 等代码子树 | `code-tree.yaml`（锚点 + radar 摘要两段式） |

`dir-tree` 生成的每个 `INDEX.md` 同时包含人读的知识导航表与机读的 `knowledge_records`。叶子文件记录在直接父目录的 INDEX 中；索引记录路径与证据均相对仓库根。索引不在 `.maglev/` 下创建摘要目录或知识缓存。

第一阶段当前实现里，这份 `registry.yaml` 虽然位于 `.agents/skills/index-librarian/protocol/`，但语义上属于**项目实例配置**：

- `maglev init` 负责生成最小实例
- 用户按项目需要显式增删 tracks
- `maglev update` 不静默覆写这份文件

当前协议对 `INDEX.md` 明确区分两层密度：

- `knowledge_records` 面向机器消费，保留有限 topic 与证据，帮助导航与收据校验
- `知识导航` 表面向人读，只展示前 4 个 topic，并用 `(+N)` 折叠余量，避免索引退化成正文摘抄

任务导航先遍历这些相邻 INDEX 记录，返回有限、可解释的候选与导航收据。收据只能证明上下文判断和来源选择，不能证明任务成功。

当前导航收据状态分为两层：

- 基础状态：`not_needed`、`queried`、`insufficient`
- 升级状态：`escalated`、`exhausted`

其中 `insufficient` 表示首次导航不足；`escalated` 表示已进入受控补救链；`exhausted` 表示补救链走完仍不足，主流程必须显式保留信息缺口，不能伪造来源充分。

Reality Profile 根目录（存在 `00_profile.yaml` 的目录）由 Profile 声明管理：scan 不为这类受控槽位根强制生成 `INDEX.md`，verify 接受 Profile 边界，不把固定骨架目录误判成缺索引。

> **已移除**: `spec-tree` / `docs-tree` 已统一为 `dir-tree` (protocol v3.0)

**核心原则**：凡是确定性逻辑能完成的，不让 AI 做。AI 只负责编排、解读 JSON/YAML 输出、按固定模板呈现报告、协调人工判断部分。

## 何时使用

- 用户对 `docs/` / `specs/` 索引数据没有信心时。
- 批量 `git mv` / 重组 / 跨模块迁移后需确认一致性时。
- `reality-sync` 发现索引异常时。
- `integrated-validator` 编排调用时。
- 新模块接入索引协议时；用户在 `registry.yaml` 新增 track 后。
- 想要快速产出仓库地图（repo-entry）或代码子树锚点（code-tree）时。

## 触发条件

- `"检查索引"` / `"索引巡检"` / `"verify index"` / `"索引状态"` / `"index status"`
- `"扫描模块"` / `"scan modules"` / `"scan track"`
- `"修复索引"` / `"刷新索引"` / `"repair index"`
- `"生成仓库地图"` / `"repo map"` / `"代码地图"` / `"code map"`

## 交互模式

- **Role**：你是项目索引管家。执行操作前必须按 track 调用脚本，不要凭自己判断索引数据。
- **Protocol**：按 `track 选择 → scan → verify → map（按需）` 顺序执行，每步引用脚本退出码与产物路径。
- **Script First**：所有数值判断（计数、比对、链接检查、anchors / radar 摘要）必须由脚本完成。AI 只负责：
  1. 解读脚本 JSON / YAML 输出；
  2. 按下方"运行时报告契约"模板向用户呈现；
  3. 执行脚本不能完成的语义判断（如 body table 内容是否合理）；
  4. 协调修复流程。

## 脚本路径

```
PROTOCOL=".agents/skills/index-librarian/protocol"

# Generic（v3.0 的唯一入口；按 --track-id 或 --all 路由）
./scripts/maglev-python ${PROTOCOL}/scripts/track_scan.py             --track-id <id>
./scripts/maglev-python ${PROTOCOL}/scripts/track_verify.py           --track-id <id>
./scripts/maglev-python ${PROTOCOL}/scripts/track_map.py              --track-id <id>
./scripts/maglev-python ${PROTOCOL}/scripts/_track_resolver.py        # 列出注册的 tracks
./scripts/maglev-python ${PROTOCOL}/scripts/task_navigate.py --root . --intent "<任务意图>"
```

## 委派 radar 的边界

**本能力只做目录索引、锚点提取与地图渲染**。仓库代码层面的依赖分析（impact / cycles / unused / hotspot / path / functions）请使用独立的 `radar` skill。

`code-tree` track 的 `radar_summary` 段是 generic 脚本通过 `subprocess` 调 `radar` 子命令产生的"统计摘要"，仅供 INDEX 上下文使用——并非 radar 能力的替代。需要完整依赖图、影响面、调用链时，**直接使用 `radar` skill**，不要试图从本 skill 的 yaml 产物里反推。

`code-tree` 的 `radar_summary` 失败时（binary 不在 PATH / 超时 / 子命令报错）会降级为 `{skipped: true, reason: ...}`，不阻断主流程；这是预期行为，不要因此重试或报错。

## 运行时报告契约

向用户呈现 track 输出时，AI 必须按以下两条纪律生成报告，避免上下文爆炸、保证输出可预期。

### A. `radar_summary` 报告纪律

呈现 `code-tree` 的 `radar_summary` 时：

1. **只展示统计行 + Top 3 hotspot 名称**，禁止展开依赖列表、引用列表、文件路径全列表。
2. 超出 Top 3 的内容必须以 `(+N more)` 引导用户改用 `radar` skill 直接查询。
3. 单 track 报告**不超过 5 行**。
4. 当 `skipped: true` 时，单行展示：`radar_summary: skipped ({reason})`。

### B. 多 track 状态报告模板

涉及多个 track 的总览报告（如 `--all` 或 `index status`）时，每个 track 用固定模板**单行**呈现：

```
{track-id}: {status} ({summary})
```

`status` 仅可使用下列 5 态：`ok`、`partial`、`skipped`、`env_failed`、`failed`。

## Exit Code 约定（generic 脚本）

| 脚本 | 0 | 1 | 2 |
|:---|:---|:---|:---|
| `track_scan.py` | 完成或 root 不存在而跳过 | 部分 track 失败但产物已写 | 资源/契约错误 |
| `track_verify.py` | 全部通过 | 有 error | 脚本错误 |
| `track_map.py` | 完成 | 部分失败 | 脚本错误 |

## 必需的参考资料

- 工作流：`references/index-librarian.workflow.md`
- 扫描步骤：`references/scan.md`
- 验证步骤：`references/verify.md`
- 加新 track：`references/track-extension.md`
- 协议规则：
  - `index-librarian/protocol/registry.yaml`
  - `index-librarian/protocol/index-schema.md`
  - 模板：`index-librarian/protocol/registry.example.{dir-tree,repo-entry,code-tree}.yaml`

## 快速参考

- **Pattern**：Entry → Workflow → Track-Scoped Micro-Steps
- **Isolation**：`INDEX.md` / `repo-map.md` / `code-tree.yaml` 由脚本独占写权，任何技能（含本 skill 的 AI 部分）不得直接编辑产物。
- **导航门禁**：受控阶段先消费或校验导航收据；无充分候选时保留 `insufficient`，不得以目录列表替代来源判断。
- **Reality 边界**：存在 `00_profile.yaml` 的受控 Reality 根由 Profile 固定骨架管理，索引器应跳过根级 INDEX 生成但继续处理其子目录与文件记录。
- **验证闭环**：每次 scan 后必须运行同一 track 的 verify；verify 不通过时先重新 scan，仍不通过再定位生成器或内容问题。
