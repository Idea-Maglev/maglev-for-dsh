# 10 Reality — 当前事实

本仓库当前已成立的事实。它是"当前是什么"的权威入口，不是任务总结或历史叙事。

## 派生来源（一次性派生，非运行时依赖）

| 项 | 值 |
|---|---|
| 派生自 | [Maglev](https://github.com/Idea-Maglev/maglev)（仅作参考/原型） |
| 源版本 | v0.7.1 stable |
| 源 commit | `dba2810474cb2ad16a06aea7ca4063edb1c53738`（`dba2810`） |
| 派生方式 | 一次性固化技能资产到本仓库，之后独立演进（分叉） |
| 运行时依赖 | **零**（不引用源仓库路径、不依赖 Maglev npm 包） |

## 固化清单（29 技能 + 1 脚本 + 协议主体）

技能资产位于 `.agents/skills/`，共 **29 个技能**：

```
artifact-purity-keeper  code-execution-slot  context-implementer  crystallization
entry-router            extension-evolver    extension-manager    index-librarian
integrated-validator    knowledge-check      maglev-bootstrapper  maglev-content-sync
maglev-design-ux        maglev-discipline    maglev-legacy-adopter maglev-map-maker
maglev-reverse-spec     maglev-tutor         multica-squad-architect  multica-squad-design-method
project-board           reality-sync         requirement-convergence   review-validation-surface
skill-scout             skill-squadron       spec-audit-surface    spec-designer  test-design-surface
```

另有：`_internal/` 协议主体（spec-pipeline、ai-context-check）、`scripts/maglev-python`（受控 Python 运行时脚本）。

**主链路**（7 技能）：`entry-router → reality-sync → requirement-convergence → spec-designer → (context-implementer|code-execution-slot) → integrated-validator → crystallization`，横切 `knowledge-check`。

## 排除清单（不固化）

| 技能 | 排除原因 |
|---|---|
| `radar` | 代码依赖分析工具（独立开源，未纳入本插件） |
| `maglev-updater` / `maglev-changelog-generator` / `evolution-observatory` | `private_only`（仅 Maglev 私域维护） |
| 若干企业内部技能 | 源仓库未纳入版本控制，不属于本插件范围 |

## 验证状态（dsh 兼容性已实证）

| 验证项 | 结果 | 证据 |
|---|---|---|
| dsh skill 发现协议兼容（kebab-case + 目录束 + description） | ✅ 29/29 | `scripts/verify_skills.py` |
| dsh 真实 `FileSystemSkillProvider` 发现 | ✅ 30 技能（含 _internal） | 运行时实例验证 |
| dsh 真实会话 skill 工具加载主链路 7 技能 | ✅ 全部加载 | headless 端到端验证 |
| host 插件工具注册（maglev_spec_check + maglev_crystallize） | ✅ 2 工具 | dsh workspace 环境 mock 验证 |
| host 插件工具 execute（spec 检查 13 项 + 结晶写回） | ✅ | dsh workspace 环境执行验证 |
| dsh 真实会话加载插件并调用 maglev_spec_check | ✅ agent 成功调用 | headless + `--patch` 验证 |
| dsh plugin add 安装 + 插件层加载 | ✅ | `--dump-config` 显示 maglev 层 |
| GUI 端到端（client bundle serve + boot graph） | ✅ HTTP 200 | `curl /plugins/maglev-for-dsh/client.js` + boot graph 含 maglev |
| S1 工具读真相（maglev_reality_status 读 Spec 仓库） | ✅ | mock + 真实 headless（读出 2 演进主题/愿景已建/契约未建） |
| S1 机械门禁（crystallize 前 spec 检查 fail 则 deny） | ✅ | mock deny/allow + 真实 headless（fail=11 被拦截） |
| S2 真相卡片（reality-status 事件 → 会话节点） | ✅ | client bundle 含 RealityStatusCard |
| S3 多角色接力（Architect 设计 → Auditor 审查） | ✅ | 真实 subagent 派发，Auditor 抓出 Architect 假阳性 bug |

## 架构 v2 融合点验证进度（dogfooding 自证）

| 融合点 | 验证 | 证据 |
|---|---|---|
| 1 完整真相（Spec + 过程日志） | ✅ | S4：全新会话仅凭仓库重建"是什么/现状/下一步" |
| 2 单人闭环（+ 3 人碰撞后续） | ✅ | S3：单人叠加 subagent 帮手走受控迭代 |
| 3 机械门禁 | ✅ | S1：crystallize 被 deny（不依赖 AI 自觉） |
| 4 真相可视化 | ✅ | S2：真相卡片 + 结晶卡片 |

**四个融合点全部验证成立。** 架构 v2（意图 × dsh 能力）的核心主张——maglev-for-dsh 的护城河是"maglev 意图 × dsh 原生能力"的融合，而非"maglev 技能的移植"——已被 dogfooding 自证。

## 单角色闭环价值验证（机制存在 → 价值成立）

以"给 maglev_spec_check 加 docs_thinking 检查项"为真实小迭代，验证一个人自己闭环的三个价值信号：

| 价值信号 | 结果 | 证据 |
|---|---|---|
| 更可控（门禁兜底） | ✅ | agent 用 spec_check 做前后对照（空目录 FAIL → 补 .md PASS），并诚实披露"会话内工具是旧实例" |
| 更沉淀（知识自动积累） | ✅ | 迭代后自动沉淀结晶 + 决策记录 + README 同步 |
| 更容易接手（换会话可重建） | ✅ | 全新会话仅凭仓库准确重建"刚改了什么/为什么改/已知边界" |

**结论：单角色闭环的价值（不止机制存在）被真实迭代证实。** 当前主线"先单人拿到正反馈"成立；"3 人碰撞"作为后续扩展。

## host 插件（R1 已实现）

本仓库根 `index.ts` 是 host 插件入口（bundle main，TypeScript），注册三个模型工具 + 两个事件生产者：

- `maglev_spec_check`：spec 完整性检查（specs 分层 + AGENTS.md 纪律 + 主链路技能 + docs/thinking 决策记录，13 项）
- `maglev_crystallize`：把已验证结论结晶到 specs 知识分层，并 **append `maglev/crystallize` 会话事件**（client 结晶卡片的数据源）
- `maglev_reality_status`：读真相（Spec 仓库的"是什么"），并 **append `maglev/reality-status` 事件**（client 真相卡片的数据源）
- 机械门禁：`tools/pre-execute` 拦截 crystallize，spec 检查 fail 则 deny

`package.json` 声明 `dsh.bundle`（`cordis.patch.yml` 为 patch 层），`peerDependencies` 为 `@deepseek-ai/cordis@^4.0.1` 与 `@deepseek-ai/dsh-tools@^0.1.0-rc.6`。事件类型经 `SessionEventMap` declaration merging 声明（`declare module '@deepseek-ai/dsh-session/types'`）。

## 依赖与发布（已走通的关键事实）

- 依赖用 **最新版** `@deepseek-ai/dsh-tools@0.1.0-rc.6` + `@deepseek-ai/cordis@4.0.1`（早期曾误用 `0.0.1-rc.1` 旧版，其依赖有缺失，导致误判为"dsh 生态阻塞"）。
- `exports` 必须暴露 `./package.json`（dsh client 扫描用 `require.resolve(pkg/package.json)` 解析包元数据）。
- host 插件 main 当前指向 `index.ts`（Node 24 原生 type-stripping 可加载）；正式发布建议编译为 `lib/index.js`。

## 仓库定位

本仓库是 **dsh 插件制品** + **Maglev 机制自证样本**（dogfooding）。当前阶段：

- **R0 资产固化 ✅**：29 技能 + `_internal` + maglev-python-runtime 固化，maglev 自治理体系建立
- **R1 host 插件 ✅**：`maglev_spec_check` + `maglev_crystallize` 两个模型工具（`index.ts`）+ `maglev/crystallize` 事件生产者
- **R2 client 插件（GUI）✅**：GUI 设计已结晶（`specs/20_evolution/active/maglev-gui-design.md`）；结晶卡片（`crystallize-node.ts` + `CrystallizeCard.tsx`）；Maglev 面板（`MaglevPanel.tsx`，shell.overlay 浮动面板）；GUI 端到端验证通过（dsh plugin add → client bundle serve HTTP 200 → boot graph 含 maglev）

## client bundle 构建方式（已验证）

```bash
# 在 maglev-for-dsh 目录，用 dsh checkout 的 tsdown 构建
/path/to/deepseek-harness/node_modules/.bin/tsdown --config tsdown.config.ts
# 产出 lib/client.js（closure-factory：window.__ModuleLoader__.load 包装）
```

关键：构建只需 dsh checkout 的 tsdown + `CLIENT_EXTERNALS` 常量，**不改 dsh 仓库**。GUI 完整加载链已验证：`dsh plugin add` → client 扫描 → `lib/client.js` serve（HTTP 200）→ boot graph 注入 maglev。

---

*派生决策结晶于 2026-08-15；R1 host 插件结晶于 2026-08-15；R2 GUI 设计结晶于 2026-08-15；GUI 端到端验证结晶于 2026-08-15*
