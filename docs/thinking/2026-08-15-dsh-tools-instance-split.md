# dsh 插件依赖 dsh-tools 的实例分裂坑（完整根因）

> 记录时间: 2026-08-15（第二轮排查后重写，第一轮结论部分修正）

## 现象

在 3099 web（maglev-demo profile）跑真实会话时，agent 调用**任意工具**（含 dsh 内置的 `skill`）报错：

```
Cannot read properties of undefined (reading 'prepare')
```

错误码 `UNKNOWN`，报错点 `packages/core/agent-loop/src/tool-calls.ts:169`（`ctx.tools[TOOL_RUNTIME_SCHEDULER].prepare(...)` 中 scheduler 是 undefined）。

## 根因（最终确认）

dsh-tools 用 **unique symbol** 作工具调度器通信键（`Symbol('@deepseek-ai/dsh-tools.scheduler')`），**每个模块物理实例的 symbol 都不同**。

dsh 的 loader 加载插件时，用 `ctx.baseUrl`（= profile 目录）作为 bare specifier 的解析基础（`vendor/loader/lib/index.js:264`）。因此：

| 场景 | profile/node_modules 里有无 hoisted dsh-tools | loader 把 `@deepseek-ai/dsh-tools` 插件解析到 | 结果 |
|------|-----------------------------------------------|---------------------------------------------|------|
| headless（官方） | 无（@deepseek-ai 树外包 0 个） | checkout 的 D1 | 统一，正常 |
| 官方 web profile | 无（dependencies 为空，dsh-web-app 是内置包） | checkout 的 D1 | 统一，正常 |
| **maglev-demo（报错）** | **有**（91 个树外包，dsh-tools 是 npm 装的 D2） | **profile 的 D2** | **分裂，报错** |

**关键机制**：`- id: tools, name: '@deepseek-ai/dsh-tools'`（dsh-base patch 里的 tools 服务行）由 loader 加载。当 profile/node_modules 里存在 hoisted dsh-tools（D2，来自 `dsh plugin add dsh-web-app` 时作为树外包安装的传递依赖）时，loader 用 **D2** 创建 ToolRuntime（tools 服务）；而 agent-loop 等其他内置插件从 dsh 安装目录（checkout）解析 **D1**。D1 与 D2 的 `TOOL_RUNTIME_SCHEDULER` 是不同 Symbol → agent-loop 访问 `ctx.tools[D1.symbol]` 是 undefined → `.prepare` 报错。

## 决定性调试证据

在 maglev-demo profile 注入调试插件（wrap `agents.create`）后：

```
[agent] agent.ctx.tools: ToolRuntime
[agent] tools[checkoutSym]: UNDEF ⚠️   ← agent-loop 用 checkout(D1) symbol 访问 → 找不到
[agent] tools[maglevSym]:   OK          ← tools 服务实际用 profile(D2) symbol 挂 scheduler
```

headless 对照组（同款调试插件）：

```
[agent] tools[checkoutSym]: OK          ← headless 的 tools 用 D1，与 agent-loop 一致
```

## 修复（已验证）

让 maglev-demo **像官方 profile 一样不把 dsh-web-app 装成树外包**：

1. `maglev-demo/package.json` 的 `dependencies` 只保留 `maglev-for-dsh`（link），**移除 `@deepseek-ai/dsh-web-app`**（bundles 里保留它，作为内置包从 dsh 安装目录解析）。
2. `pnpm install` 清理 222 个树外包 → profile/node_modules 里不再有 hoisted dsh-tools（D2）。
3. 验证：`require.resolve('@deepseek-ai/dsh-tools')` 从 profile 解析到 checkout D1；调试 probe 显示 `tools[checkoutSym]: OK`。

同时，**maglev-for-dsh 仓库的 node_modules 里 `@deepseek-ai/dsh-tools` 必须 symlink 到 dsh checkout 的 `packages/core/tools`**（D1），让 `index.ts` 的 `defineTool` 与内置包用同一实例（本地 link 开发阶段的依赖解析问题：Node 从仓库向上找 node_modules，找不到 checkout）。

## 关键认知

1. **报错与 maglev 代码无关**：根因是 profile 里存在 hoisted dsh-tools（D2）导致 dsh 的 tools 服务与内置插件分裂。任何 `dsh plugin add` 装成树外包的包（传递依赖含 dsh-tools）都可能触发。
2. **dsh 内置包与树外包的 dsh-tools 是不同实例**：内置包从 dsh 安装目录解析（D1），树外包从 profile 解析（D2）。dsh 官方 profile 的设计是"不把 @deepseek-ai/* 装进 dependencies"来规避。
3. **本地 link 开发**：maglev-for-dsh 的 dsh-tools 必须 symlink 到 checkout D1（与内置包一致）。

## 发布时的待办

- 发布 README 应提示：`dsh plugin add maglev-for-dsh` 后，若用户 profile 已有 hoisted dsh-tools（如曾用 `dsh plugin add @deepseek-ai/dsh-web-app` 装成树外包），可能触发同样分裂；应让 dsh-web-app 作为内置包（不进 dependencies）。
- 更稳健的长期方案：让 maglev 的 `index.ts` **不直接 import dsh-tools**，手动构造 `ToolDefinition` 对象传给 `ctx.tools.register`（彻底解耦 dsh-tools 实例），待评估。
