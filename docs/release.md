# Maglev for DSH — 发布操作手册

> 面向维护者。发布 = GitHub 仓库（源码/文档入口）+ npm 发布（分发）。两者都要。

## 仓库与历史

- **公开仓库**：`Idea-Maglev/maglev-for-dsh`（GitHub，Public）—— 发布权威源
- **历史策略**：公开仓库从**干净的初始提交**开始（`2c263b6`），**不继承**派生自公司私域 GitLab（`git.nevint.com`）的历史——旧历史含私域 URL，公开仓库从独立演进起点开始
- **私域仓库**（`git.nevint.com`）：不再是发布目标；仅作内部备份保留，不参与公开流程

## 前置条件

- npm 账号，且是 `@idea-maglev` 组织成员（`npm login` 已验证）
- GitHub 账号，且在 `Idea-Maglev` 组织有仓库权限
- 本地已 `pnpm install`（仓库根目录）

## 发布流程

### 1. 构建产物

```bash
pnpm build
```

产物：
- `lib/index.mjs` — host 插件（Node ESM，零外部依赖，仅 node: 内置）
- `lib/client.js` — client 插件（browser closure-factory bundle）

> host 必须编译成 `.js`：Node 24 的 type-stripping 不支持 node_modules 下的 `.ts`，而发布后插件入口位于 node_modules。

### 2. 检查发布产物

```bash
pnpm pack --pack-destination /tmp/
tar -tzf /tmp/idea-maglev-maglev-for-dsh-*.tgz   # 确认含 index.mjs / client.js / .agents/ / LICENSE
```

### 3. 提交 + 推送 + 打 tag

```bash
git add -A && git commit -m "..."               # 功能/修复提交
git push -u origin main                        # 推到 GitHub
git tag v0.1.0 && git push origin v0.1.0         # 版本 tag（GitHub Release 用它）
```

### 4. npm 发布

```bash
npm login
npm publish --access public
```

（`package.json` 已配 `publishConfig.access: public`，scope 包默认公开。）

### 5. 发布后验证（必须做）

```bash
# 在任意干净目录建一个测试 profile，从 registry 安装
dsh plugin --profile verify add @idea-maglev/maglev-for-dsh
dsh --profile verify "请调用 maglev_reality_status 工具，一句话报告结果"
# 期望：工具调用成功，exit 0
```

再验证 GUI（web）：

```bash
dsh --profile web --port 3100
# 打开页面：Maglev 面板按钮、真相卡片、结晶卡片应出现
```

## 版本管理

- 语义化版本：`0.1.0` 起
- 改动后升版本：`npm version patch|minor|major`（自动打 tag）
- 每次发版走「构建 → pack 检查 → commit/tag → push → publish → 验证」

## 常见问题

| 现象 | 处理 |
|---|---|
| `ERR_UNSUPPORTED_NODE_MODULES_TYPE_STRIPPING` | 忘了构建 host，或 main 仍指向 index.ts。确认 `main: lib/index.mjs` 且已 `pnpm build` |
| `Cannot find package 'maglev-for-dsh'` | `cordis.patch.yml` 的 `name` 必须与 `package.json` 的 `name` 一致（当前 `@idea-maglev/maglev-for-dsh`） |
| 工具调度报 `reading 'prepare'` | 用户 profile 若存在 hoisted dsh-tools 且旧版本插件直接 import dsh-tools 会分裂。本插件 host 零依赖 dsh-tools（见 `docs/thinking/2026-08-15-dsh-tools-instance-split.md`），不受影响 |
| scope 包发布 404/403 | 确认 `@idea-maglev` 组织存在且你有 publish 权限；`publishConfig.access: public` 已配 |

## 本地开发（link 模式）

```bash
# maglev-demo profile 用 link 指向本仓库（package.json dependencies 里）
dsh plugin --profile maglev-demo add /path/to/maglev-for-dsh
```

> link 模式加载的是 `lib/index.mjs`（main 指向），**改代码后需 `pnpm build` 再重启 dsh 才生效**。
