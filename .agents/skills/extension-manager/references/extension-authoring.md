# Extension Authoring Guide

本文说明 `extension.yaml` 的 v1 写法。`extension.yaml` 是 Extension Pack 的入口文件，用来告诉 Maglev：这个扩展包含哪些能力资产、应安装到哪里、提供哪个 Plugin Slot，以及安装前应做哪些检查。

## 最小结构

```yaml
schema_version: 1
id: my-extension
name: My Extension
version: "0.1.0"
summary: Short capability summary.
kind: capability_pack

contents:
  skills:
    - id: my-extension-entry
      source: skills/entry/SKILL.md
      install_to: .agents/skills/my-extension-entry/SKILL.md
      exposure: enabled

plugin_slots:
  - slot: code-execution
    entry_skill: my-extension-entry
    priority: 50
    selection_hint: Use when code implementation needs this extension's execution discipline.
    fallback: maglev-default
```

## 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `schema_version` | 是 | 当前固定为 `1`。 |
| `id` | 是 | 扩展唯一 id，使用小写字母、数字和连字符。 |
| `name` | 是 | 人类可读名称。 |
| `version` | 是 | 扩展版本或上游版本。 |
| `summary` | 是 | 一句话说明这个扩展提供什么能力。 |
| `kind` | 是 | 当前固定为 `capability_pack`。 |
| `maturity` | 否 | `official_recommended`、`experimental` 或 `team_internal`。 |
| `compatibility` | 否 | Maglev 版本约束，例如 `maglev_min_version`。 |
| `source` | 否 | 扩展内容来源；registry 安装时也会提供 source。 |
| `contents` | 是 | 可安装资产清单。可包含 skill、template、validator、doc、reference 或 script。 |
| `plugin_slots` | 否 | 声明后扩展才参与插槽选择；v1 只允许 `code-execution`。 |
| `activation` | 否 | 默认启用策略。建议默认 `default_enabled: false`。 |
| `validation` | 否 | 期望自检项，例如 schema、引用、冲突、可消费性。 |

## 资产声明

### Skill

```yaml
contents:
  skills:
    - id: my-extension-entry
      source: skills/entry/SKILL.md
      install_to: .agents/skills/my-extension-entry/SKILL.md
      exposure: enabled
      description: Entry skill for this extension.
```

规则：

- `source` 必须是扩展包内相对路径，不能是绝对路径或 URL。
- `install_to` 必须是项目内相对路径；v1 推荐 `.agents/skills/<skill-name>/SKILL.md`。
- `id` 应与安装后的 skill runtime name 对齐，方便 `plugin_slots[].entry_skill` 引用。

### Docs / Templates / Validators / References / Scripts

这些资产使用通用结构：

```yaml
contents:
  docs:
    - source: README.md
      install_to: docs/extensions/my-extension/README.md
      description: User-facing extension guide.
```

如果省略 `install_to`，表示该资产只作为扩展包内部说明或引用，不进入项目安装路径。

`scripts` 只描述需要随扩展分发的辅助脚本，不表示 Extension CLI 可以执行它们。脚本的运行时、依赖与权限仍由对应 skill 明确声明和负责。

若 skill frontmatter 中声明了 `attached-scripts`，每个路径必须同时满足：

1. 相对于该 `SKILL.md` 的源文件存在；
2. 在 `contents.scripts` 中有同一 source 的资产声明；
3. 脚本的 `install_to` 保持相对 `SKILL.md` 的相同路径，确保安装后 skill 内的相对调用仍可用。

```yaml
contents:
  skills:
    - id: my-extension
      source: SKILL.md
      install_to: .agents/skills/my-extension/SKILL.md
  scripts:
    - source: scripts/helper.sh
      install_to: .agents/skills/my-extension/scripts/helper.sh
      description: Helper invoked by the installed skill.
```

## Plugin Slot 声明

只有需要参与 Maglev 主流程插槽时才声明 `plugin_slots`。普通 single-skill、asset pack 和 validator pack 不应为了安装而伪造 Slot。

```yaml
plugin_slots:
  - slot: code-execution
    entry_skill: my-extension-entry
    priority: 50
    selection_hint: Use for code delivery tasks that need this extension.
    fallback: maglev-default
```

字段含义：

| 字段 | 必填 | 说明 |
|------|------|------|
| `slot` | 是 | v1 只允许 `code-execution`。 |
| `entry_skill` | 是 | 插槽被选中后 Agent 应读取的 skill id，必须存在于 `contents.skills[].id`。 |
| `priority` | 否 | 候选排序提示，0-100；不是强制选择。 |
| `selection_hint` | 是 | 给 Agent 的自然语言选择依据。 |
| `fallback` | 否 | 当前只允许 `maglev-default`。 |

## 不允许的声明

- 不要声明 `entry-routing` 或 `governance-discipline`。它们是 Maglev core 边界，不是可扩展插槽。
- 不要把安装等同于默认启用；默认应让用户显式 enable。
- 不要在 manifest 中写多 Agent 适配矩阵；v1 follow Maglev 的适配机制。
- 不要使用绝对路径、`file://`、`http://` 或 `https://` 作为资产路径。

## 自检建议

扩展作者提交前至少检查：

1. `extension.yaml` 符合 `extension.schema.json`。
2. `contents.*[].source` 在扩展包内存在。
3. `plugin_slots[].entry_skill` 能在 `contents.skills[].id` 中找到。
4. skill 的 `description` 和正文能让 Agent 判断何时使用、何时不使用。
5. 安装目标不会覆盖项目已有用户文件。
6. `attached-scripts` 中的脚本已在 `contents.scripts` 声明，并保持安装后的相对路径。
