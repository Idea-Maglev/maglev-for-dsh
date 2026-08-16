# Index Schema

> 执行权威：`scripts/track_scan.py` 与 `scripts/track_verify.py`。本文件只描述现行 `tracks` v3 契约。

## 1. Track 类型

| `type` | 对象 | scan 产物 | map 产物 | 本 schema 是否适用 |
|:---|:---|:---|:---|:---|
| `dir-tree` | 任意文档、规格或知识目录树 | 相邻 `INDEX.md` 网络 + summary YAML | INDEX 网络本身 | 是 |
| `repo-entry` | 仓库或能力入口目录 | 锚点 YAML | `repo-map.md` | 否 |
| `code-tree` | 代码子树 | 锚点 YAML + 可选 radar 摘要 | `code-map.md` | 否 |

每个 registry 条目必须有 `id`、`type`、`root`。`enabled` 缺省为 `true`；设为 `false` 时不参与任何执行。`output`、`map_output`、`ignore`、`max_depth` 等字段按 type 选用。多个 track 的 `output` 与 `map_output` 必须各自唯一，完整例子见 `registry.example.*.yaml`。

`dir-tree` 可用 `skip_index_dirs` 指定不写自身 `INDEX.md` 的相对目录。`.` 表示 track 根目录；该目录仍会遍历子目录，不会排除整棵子树。`collapse_single_file_dirs` 可声明一组相对 `root` 的 glob，仅当目录没有 README、没有其他可见子项且只剩一个可索引文件时，父级 `INDEX.md` 直接记录该叶文件，叶目录自身不再保留 `INDEX.md`。

## 2. INDEX 节点

`dir-tree` 中的每个可索引目录由 `track_scan.py` 写入 `INDEX.md`。该文件是机器可消费的导航节点，包含：

```yaml
type: entity-index
scope: root|collection
entity_type: document
child_count: 3
knowledge_schema_version: 1
knowledge_records: []
```

- `child_count` 描述直接子项数。
- `scope` 由生成器根据目录层级决定。
- `knowledge_records` 记录直接子文件和可导航子目录；它们的内容与正文知识导航表必须由同一次 scan 生成。
- 命中 `collapse_single_file_dirs` 的叶目录不会成为独立目录节点；其唯一文件会直接折叠到父目录记录中。
- `knowledge_records` 服务机器消费，允许保留有限的补充 topic；当前生成器对每条记录最多保留 6 个 topic，避免把正文结构整段搬进索引。
- 正文 `知识导航` 表服务人读，只展示前 4 个 topic；超出部分以 `(+N)` 折叠，防止目录节点退化成长摘要列表。
- `INDEX.md`、summary YAML、`repo-map.md` 和 `code-map.md` 都是脚本独占产物，不能手工编辑。

## 3. 知识记录

文件记录至少包含可定位路径、摘要、主题、证据、解析状态与内容指纹：

```yaml
- id: file:docs/guides/getting-started.md
  path: docs/guides/getting-started.md
  kind: file
  summary: "帮助读者完成首次设置。"
  topics: ["getting", "started"]
  evidence: [docs/guides/getting-started.md#Getting-Started]
  parse_status: indexed
  content_fingerprint: "sha256..."
```

目录记录额外使用 `kind: directory`、`directory_index` 与 `navigation_role: route`。命中目录记录后，消费者应继续读取其 `directory_index` 或叶子证据；目录摘要不能替代叶子事实。

被 `collapse_single_file_dirs` 折叠的目录不会产出 `kind: directory` 记录。消费者直接命中其叶文件记录，证据与内容指纹也以该文件为准。

`topics` 的目标是“降低定位成本”，不是复制正文结构。当前生成器会优先保留以下类型：

- 标题中的能力名、对象名、问题名、关键边界词
- 有明确检索价值的短语，如 `接入与治理`、`最小闭环怎么跑`

当前生成器会主动过滤或压缩以下类型：

- 中文碎片切词与孤立虚词
- 低信息短语，如 `没有`、`而是`
- 文章组织句，如“先看一个真实样本”“先说一个更接近真实的场景”
- 超出密度上限的后续 heading

私密、敏感或被项目 ignore policy 排除的路径不得写入内容摘要或指纹。无法安全解析的文件必须明确以 `degraded` 或 `excluded` 表示原因。

## 4. 验证边界

`track_verify.py` 对 `dir-tree` 验证产物存在、frontmatter 的关键字段、知识记录与当前目录的指纹一致性，以及证据路径可达性。它不判断摘要是否足够贴合用户意图；该语义判断由 `task_navigate.py` 和消费者完成。

不通过时，先运行同一 track 的 scan。若问题仍存在，再修改 registry、目录内容或生成器，而不是手改产物。

## 5. 导航收据契约

`task_navigate.py` 生成的 receipt 是“知识入口判断事实”，不是“任务成功证明”。当前 receipt 至少包含：

```yaml
schema_version: 1
status: queried
task_fingerprint: "sha256..."
query:
  task_intent: "..."
  known_sources: []
  missing_questions: []
  scope: "."
sources:
  docs/path.md: "sha256..."
candidates: []
missing_categories: []
events: []
created_at: "2026-07-21T10:00:00+00:00"
```

### 5.1 `status` 枚举

导航收据的 `status` 当前定义为 5 态：

| `status` | 含义 | 是否允许直接继续下游 |
|:---|:---|:---|
| `not_needed` | 当前步骤经判断不依赖额外项目知识，或已有来源足够 | 是，但应说明为何不需要导航补充 |
| `queried` | 已返回有限、可解释候选，后续应继续读叶子证据或目录下钻 | 是 |
| `insufficient` | 首次导航不足，当前 query 没有形成足够可靠候选 | 否；必须进入升级链 |
| `escalated` | 已进入 `insufficient` 的受控升级链，正在执行补救动作 | 否；只能继续升级或回到 `queried` / `not_needed` |
| `exhausted` | 升级链已走完，当前仍无法形成足够可靠候选 | 否；必须显式保留不足，不得伪造来源充分 |

`insufficient`、`escalated`、`exhausted` 的区别必须清楚：

- `insufficient` = 第一次承认“当前导航不够”
- `escalated` = 正在补救，不允许伪装成已拿到来源
- `exhausted` = 最小补救动作已穷尽，当前只能显式暴露不足

### 5.2 升级链最小字段

当 receipt 进入 `escalated` 或 `exhausted` 时，建议最少保留以下字段，避免“已经升级”沦为形式主义：

```yaml
escalation:
  step: refine_scope|reuse_hint|ask_user_hint|controlled_deep_scan
  attempt: 1
  basis:
    scope_hint: "docs/thinking"
    known_source_hint: ".agents/skills/index-librarian/SKILL.md"
  note: "..."
```

- `step` 表示当前补救动作类别，而不是自由文本总结。
- `attempt` 表示当前已进行到第几次升级动作。
- `basis` 记录触发升级所依赖的 scope、线索或用户补充锚点。
- `note` 只用于补充不能结构化表达的最小原因，不应用来替代 `basis`。

### 5.3 收据消费边界

- `queried` 只能证明“这些来源值得先读”，不能证明“答案已被证实”。
- 命中 `kind: directory` 的 route 候选时，消费者必须继续读取其 `directory_index` 或叶子证据；目录摘要不能直接充当事实来源。
- `insufficient` / `escalated` / `exhausted` 都不得被质量层解释为成功，只能被解释为“知识入口判断的当前状态”。
- `receipt_status()` 只校验 query 与 source fingerprint 是否过期；它不判断升级链是否走得充分。
