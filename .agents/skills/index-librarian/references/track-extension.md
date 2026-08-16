# 加新 Track —— 用户最小操作清单

> 引用：`SKILL.md` "必需的参考资料"；`02_design.md` §3.6.4 "用户加 track 的体验"。
> 适用：你的项目已经接入 `index-librarian` skill，并且 `index-librarian/protocol/registry.yaml` 已存在。

## 1. 你能加的 Track 类型

| `type` | 用途 | 输出 |
|:---|:---|:---|
| `dir-tree` | 任意文档、规格或知识目录树 | 各级 `INDEX.md` |
| `repo-entry` | 仓库根目录 | `repo-entry.yaml` + `repo-map.md` |
| `code-tree` | `packages/` / `src/` 等代码子树 | `code-tree.yaml`（含 radar 摘要） |

## 2. 三步加 Track

### Step 1 — 复制对应的 example 模板

模板位置：`.agents/skills/index-librarian/protocol/registry.example.<type>.yaml`。

目录忽略策略不写在这里：它属于项目的 `.maglev/config.json`。初始化默认生成：

```json
{
  "indexing": {
    "ignore_dirs": [".agent", ".claude", ".codex", ".github"],
    "ignore_hidden_dirs": true,
    "inherit_gitignore": true
  }
}
```

`ignore_dirs` 对所有索引 track 生效；`inherit_gitignore` 让目录忽略遵循 Git 的 `.gitignore` 语义。track 中的 `ignore` 只用于该 track 的额外目录名。

把模板里的 `tracks:` 段（或单条 track 条目）复制到你的 `registry.yaml` 的 `tracks:` 段末尾。

### Step 2 — 改 4 个最小字段

每条 track 至少改这 4 个字段：

```yaml
- id: <my-unique-id>          # 全仓库唯一，建议 kebab-case
  type: <dir-tree|repo-entry|code-tree>
  root: <path/to/dir/>        # 相对仓库根
  output: <path/to/output>    # 默认产物路径，可保留模板默认
  map_output: <path/to/map.md> # repo-entry / code-tree 可选；共享输出目录时必须唯一
```

`dir-tree` 可选 `skip_index_dirs`，列出相对 `root` 且只跳过自身 `INDEX.md` 的目录路径；`.` 表示跳过根目录，但其子目录仍会被索引。`collapse_single_file_dirs` 只用于显式声明的叶目录模式：当某目录没有 README、没有其他可见子项且仅包含一个内容文件时，父级 `INDEX.md` 会直接记录该文件并删除该叶目录旧的 `INDEX.md`。`enabled` 默认为 `true`；设为 `false` 时该 track 不会被解析或包含在 `--all` 中。其余字段（`depth_limit` / `radar_summary` 等）按类型选择。

### Step 3 — 跑一次 scan + verify 验证

```bash
PROTOCOL=".agents/skills/index-librarian/protocol"
./scripts/maglev-python $PROTOCOL/scripts/_track_resolver.py                  # 确认新 track 已识别
./scripts/maglev-python $PROTOCOL/scripts/track_scan.py   --track-id <my-id>  # 生成产物
./scripts/maglev-python $PROTOCOL/scripts/track_verify.py --track-id <my-id>  # 校验
```

或者直接让 `index-librarian` skill 跑全套：跟它说 "扫描 track `<my-id>`" 即可。

## 3. 常见错误与提示

| 现象 | 原因 | 修复 |
|:---|:---|:---|
| `track not found` | `id` 拼错 / `enabled: false` | 校对 id；改 `enabled: true` |
| `unknown track type` | `type` 不在三枚举内 | 改成上表中的 `type` |
| `root does not exist` | 路径写错或相对位置不对 | `root` 必须相对仓库根 |
| `code-tree` `radar_summary: skipped` | 你环境没装 `radar` binary | 这是预期降级；产物 yaml 仍可用，需要完整依赖图请装 radar |
| 地图文件被覆盖 | 多个 track 使用同一个 `map_output` | 为每个 track 指定不同的 `map_output`；未指定时会从 `output` 派生唯一名称 |
| 单文件叶目录出现重复导航 | 目录和其唯一文件都各自有入口 | 仅对明确模式配置 `collapse_single_file_dirs`，让父级直接记录叶文件 |

## 4. 不要做的事

- ❌ 不要手编 `INDEX.md` / `repo-map.md` / `code-tree.yaml` —— 产物由脚本独占写权。
- ❌ 不要用 `code-tree` 的 `radar_summary` 当 radar 替代品 —— 真要分析依赖请直接调 `radar` skill。
- ❌ 不要把同一 `root` 挂多个相同 `type` 的 track —— 后写的会覆盖前者的产物。

## 5. 进阶：自定义字段

`dir-tree` 支持继承 `index-schema.md` 第 §1-§6 全部 frontmatter / stats 规则；`repo-entry` / `code-tree` 由对应脚本契约约束（不走 entity-index frontmatter）。详见 `index-schema.md` §0。

需要更深定制（如自定义 `entity_type` / 多语种 anchor 文件名）时：

- 改 `index-librarian/protocol/scripts/_code_tree_helpers.py` 的 `DEFAULT_ANCHOR_FILES` / `DEFAULT_IGNORE_DIRS` 是仓库级影响，慎用。
- 单 track 级覆盖建议放进该 track 的 registry 条目（如 `anchor_files: [...]` / `ignore: [...]`）。
