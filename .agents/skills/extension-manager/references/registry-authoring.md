# Registry Authoring Guide

本文说明 `registry.yaml` 的 v1 写法。Registry 是扩展索引源，只负责发现和定位扩展，不展开完整安装规则。安装前，Maglev 必须读取扩展来源中的 `extension.yaml` 并再次校验。

## 最小结构

```yaml
schema_version: 1
registry:
  id: team-extensions
  name: Team Extensions
  description: Internal extension index.

extensions:
  - id: my-extension
    name: My Extension
    summary: Short capability summary.
    category: execution
    maturity: team_internal
    provides_slots:
      - code-execution
    source:
      type: git
      url: git@example.com:team/my-extension.git
      ref: master
    manifest_path: extension.yaml
```

## 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `schema_version` | 是 | 当前固定为 `1`。 |
| `registry.id` | 是 | 索引源唯一 id。 |
| `registry.name` | 是 | 人类可读名称。 |
| `registry.description` | 否 | 索引源说明。 |
| `extensions` | 是 | 扩展条目列表。 |

## Extension 条目

| 字段 | 必填 | 说明 |
|------|------|------|
| `id` | 是 | 扩展 id，应与 `extension.yaml` 中的 `id` 一致。 |
| `name` | 是 | 扩展名称。 |
| `summary` | 是 | 一句话摘要，用于搜索结果。 |
| `category` | 是 | 分类：`execution`、`testing`、`review`、`release`、`knowledge`、`other`。 |
| `maturity` | 是 | 成熟度：`official_recommended`、`experimental`、`team_internal`。 |
| `provides_slots` | 否 | 扩展提供的 slot。仅 Slot 扩展需要声明；v1 只允许 `code-execution`。 |
| `source` | 是 | 扩展来源。v1 支持 `git` 与 `local`。 |
| `manifest_path` | 是 | 扩展来源中的 manifest 相对路径，通常是 `extension.yaml`。 |

## 官方源与自建源

Maglev 可以提供官方默认 registry，但项目可以添加自建 registry。自建 registry 只需要满足：

1. 根目录存在 `registry.yaml`。
2. `registry.yaml` 通过 `registry.schema.json` 校验。
3. 每个条目的 `source` 可被当前项目访问。
4. 每个条目的 `manifest_path` 指向合法 `extension.yaml`。

## CLI 脚手架

```bash
maglev-extension registry init <registry-root> --id <registry-id> --name <registry-name> --json
maglev-extension registry add <extension-root> --registry-root <registry-root> --workspace-root <consumer-project-root> --category execution --json
```

`registry init` 创建空的 `registry.yaml` 和 README。`registry add` 先运行严格的 extension check，再从 manifest 写入一个 `asset_pack` 条目。它只生成本地 source；`source.path` 相对于 `--workspace-root`，因此 extension 必须位于该项目根内。远程 Git Registry 的提交和审核由 Registry 自身的协作流程负责。

## Registry 不负责什么

- 不托管完整扩展内容。
- 不替代 `extension.yaml`。
- 不决定扩展是否默认启用。
- 不声明 Maglev core 不开放的能力边界，例如 `entry-routing` 或 `governance-discipline`。
