---
name: extension-manager
description: Maglev 扩展管理器。Use when 用户要搜索、检查、安装、启用、禁用、更新、移除 Maglev Extension / Capability Pack，查看 plugin slot 候选，或把官方/自建 registry 中的扩展接入 `.agents/skills/`。不用于执行插件内部能力，例如不要用它直接执行 Superpowers 的代码流程。
metadata:
  formal_action_name: 扩展管理
  top_level_capability: 能力进化
  system_layer: Extension Layer
  lifecycle_chain: extension_management
  runtime_name_status: canonical_name_active
  distribution_scope: user_visible
  author: feiyu.gao
  last_updated: 2026-07-29
---

# Extension Manager

这是 Agent 面向的薄入口。它只调用 PATH 上已安装的 `maglev-extension`。不要手写复制、lock 更新或 registry 解析逻辑。

## 核心边界

负责：

- 配置与查看消费者项目的 Registry source（`.maglev/extensions.sources.yaml`）。
- 搜索、inspect、安装、更新、启用、禁用和移除 extension。
- 解释 CLI 的 JSON envelope、issues 和 slot 候选。
- 在 CLI 缺失时提供安装引导。

不负责：

- 执行插件内部能力；例如 Superpowers 被选中后，应读取对应 provider skill。
- 让所有已安装扩展自动进入默认上下文。
- 管理 BDD / `test-generation` 槽位；v1 只允许 `code-execution`。
- 绕过 Maglev 主流程或替代 `entry-router` / `spec-designer` / `integrated-validator`。
- 在 CLI 缺失时回退到 Python scripts；不要回退到 Python，因为这会重新引入用户运行时环境依赖。

## 前置检查

先确认命令可用：

```bash
maglev-extension --version
```

若命令不在 PATH，停止管理动作并提示用户安装 Extension CLI：

```bash
npm install --global @nio-fe/maglev-extension-cli
```

在 prerelease 或本地 tarball 验证阶段，应使用发布方提供的 package tarball 安装命令；不要改用仓库内 Python 原型作为用户入口。

## 消费命令

所有命令在目标 Maglev 项目根目录运行，并携带 `--json`。

```bash
maglev-extension sources list --json
maglev-extension sources add --id <source-id> --type local --path <registry-dir> --json
maglev-extension search --slot code-execution --json
maglev-extension inspect superpowers --json
maglev-extension install <extension-id> --json
maglev-extension update <extension-id> --json
maglev-extension enable <extension-id> --json
maglev-extension disable <extension-id> --json
maglev-extension remove <extension-id> --json
maglev-extension slot resolve code-execution --json
```

`sources add` 是消费者项目接入 Registry 的正式入口：缺少 `.maglev/extensions.sources.yaml` 时会创建该文件；local source 必须位于目标 workspace 内且已包含合法 `registry.yaml`；git source 记录 `url/ref`（默认 `master`）。`sources list` 返回当前 source 文件路径、是否存在以及已配置源。

`install` 从项目配置的 Registry source 解析 asset source；`update` 从 `.maglev/extensions.lock` 的 provenance 解析来源。安装不等于启用；只有 enable 后，asset-managed slot 才会成为候选。

`inspect` 返回 Registry metadata 和项目状态。对于 external integration，它还返回官方检测规则及最近的 detected/enabled 状态；detect、enable、disable、remove 均不修改 provider 资产。

## 结果处理

CLI 使用 versioned JSON envelope：

- `status: pass`：读取 `result`，同时提示 `issues` 中的 warning 或 suggestion。
- `status: fail`：停止当前动作，按 error code、message 和 path 向用户解释下一步。
- 不要把 `search` 结果当作已安装状态；只以 inspect 或 slot resolve 的项目 lock 状态为准。
- 没有 slot 候选时，代码任务使用 `agent-native` fallback，不要臆造 provider 已启用。

## 作者校验与本地安装

扩展作者在扩展包根目录执行：

```bash
maglev-extension init <extension-root> --profile single-skill --id <extension-id> --json
maglev-extension check . --workspace-root <target-maglev-project> --json
maglev-extension test-install . --workspace-root <target-maglev-project> --json
```

`init` 是非交互脚手架命令，支持 `single-skill`、`skill-pack`、`slot-plugin`、`asset-pack` 和 `validator-pack`。它创建 extension workspace、最小 manifest、README 和开发态 `.maglev-extension/workspace.yaml`；只有 `slot-plugin` 会生成 `code-execution` Slot 声明。

`check` 对 v1 manifest 合约执行确定性校验：必填字段、资产路径、skill frontmatter 与引用、slot 声明、entry skill、validation check 和既有安装目标。`test-install` 是作者或测试场景的本地 root 入口；它会先以严格资产模式运行同一检查器，只有没有 error 时才会写入目标项目和 lock。

`test-install` 不替代消费者的 `install <extension-id>`；真实消费安装仍必须从已配置的 Registry source 解析 extension id。

## Registry 作者命令

自建 Registry 使用与消费者相同的 `registry.yaml` 协议：

```bash
maglev-extension registry init <registry-root> --id <registry-id> --name <registry-name> --json
maglev-extension registry add <extension-root> --registry-root <registry-root> --workspace-root <consumer-project-root> --category <category> --json
```

`registry add` 会先对 extension 执行 strict `check`，再从 manifest 生成 `asset_pack` Registry entry。对于 local source，`--workspace-root` 是未来消费者解析 `source.path` 的根；extension 不在该目录内时命令会拒绝生成 entry。该命令不会发布或修改远程 Git Registry。

## 当前范围

当前 Node CLI 已覆盖消费侧 source 配置与扩展管理命令，以及作者侧的 `init`、`check`、本地 `test-install`、`registry init` 和 `registry add`。远程 Registry 发布、CI 治理与 registry entry 审核仍不在稳定用户命令范围；不要调用遗留 Python scripts 作为用户入口。

## 参考资料

- `references/extension-authoring.md`：解释 manifest 字段和作者规则。
- `references/registry-authoring.md`：解释 registry 字段和维护规则。
- `protocol/schemas/extension.schema.json`、`protocol/schemas/registry.schema.json`：字段级协议参考。
