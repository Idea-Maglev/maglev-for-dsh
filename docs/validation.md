# maglev-for-dsh 验证记录

本文档记录 maglev-for-dsh 插件制品的四层验证证据与端到端验证方法，供复现与追溯。验证对象是本仓库固化的技能资产（`.agents/skills/`，29 个技能）。

## 验证目标

证明：从 Maglev 派生的 dsh 适配体系，在 dsh 运行时中**真实可被发现、可被加载、可被用于工作**。

## 四层验证证据（由浅入深）

### 第 1 层：源码级确认

确认 dsh 的 skill 发现机制与 Maglev 技能目录结构匹配：

- dsh `skill-filesystem/src/index.ts:247` 原生扫描 `<projectRoot>/.agents/skills`（rank 200）
- dsh `discoverRoot`（`skill-filesystem/src/index.ts:719-747`）支持 `<name>/SKILL.md` 目录束 + 扁平 `.md`
- dsh `isSkillName`（`skill/skill/lib/index.js:17`）= `/^[a-z0-9]+(?:-[a-z0-9]+)*$/`
- Maglev 30 个派生技能：name 全部 kebab-case、与目录名一致、全部含 description

### 第 2 层：复刻级验证

用 dsh 真实模块（`@deepseek-ai/dsh-skill` 的 `isSkillName` + `yaml` 的 `parse`）复刻 `parseSkillFile` 校验逻辑，对 30 个 SKILL.md 逐一验证：

```
=== dsh parseSkillFile 复刻验证 ===
通过: 30 个技能
失败: 0 个
结论: ✓ 30 个派生技能全部通过 dsh 真实解析校验
```

（对应 `scripts/verify_skills.py`，可独立复现）

### 第 3 层：真实 FileSystemSkillProvider 发现

用 dsh 真实的 `FileSystemSkillProvider` 类（非复刻）完整走 `roots → discoverRoot → parseSkillFile` 链路：

```
=== dsh FileSystemSkillProvider 真实发现 ===
发现技能数: 30
主链路技能缺失: 无（全部发现）
结论: ✓ dsh 运行时真实发现 Maglev 派生技能（30 个，主链路齐全）
```

### 第 4 层：真实 dsh 会话端到端（决定性）

在 test 仓库（`maglev-for-dsh-test`）作为 workspace 启动 dsh headless 会话，让 agent 通过 `skill` 工具（非读磁盘）确认能发现并加载 Maglev 技能：

```
已通过 skill 工具逐一加载确认（未读取磁盘文件），本会话的 skill 工具能发现并加载
.agents/skills 下的 Maglev 技能。

给定集合中全部 7 个技能均可发现并成功加载：
- entry-router ✅  reality-sync ✅  requirement-convergence ✅
- spec-designer ✅  integrated-validator ✅  crystallization ✅
- maglev-discipline ✅

一句话结论：我可以通过 skill 工具逐一加载这 7 个技能（每次调用都成功返回了
对应 SKILL.md 的完整指令内容，其 base directory 均指向本仓库 .agents/skills/<技能名>）。
```

同时 agent 正确回答了 Maglev 的知识分层（`10_reality` 当前事实 / `20_evolution` 演进主题 / `90_archive` 历史归档）与主链路技能——证明**不仅技能可被发现，agent 还能用它们理解项目现状**。

## 端到端验证方法（可复现）

```bash
# 前置：dsh 仓库已 build（pnpm run build），API key 已配置（~/.dsh/.credentials.yaml）

# 在 test 仓库目录运行 dsh headless（用构建后的 bin.js，脱离源码模式 cwd 绑定）
cd /path/to/maglev-for-dsh-test
node /path/to/deepseek-harness/apps/cli/lib/bin.js --profile headless "你的任务"

# 关键：cwd 必须是目标项目（headless 的 workspace = process.cwd()）
# 注意：不要用 pnpm --dir 方式（会让 cwd 变成 dsh checkout，导致发现不到项目技能）
```

## 已知限制与发现

1. **dsh headless 源码模式绑定 checkout cwd**：`pnpm dsh --profile headless`（tsx 源码模式）必须在 dsh checkout 内运行，脱离后因 tsconfig paths 失效而报错。生产验证用构建后的 `apps/cli/lib/bin.js`。
2. **headless workspace = process.cwd()**：无显式 workspace 参数（`bundle/headless/src/index.ts:113`）。GUI 用户通过 Choose workspace 选择，等价于指定 cwd。
3. **真实 GUI 验证**：本记录用 headless 验证（等价于 GUI 的 workspace 选择 + 会话）。GUI 端到端体验（界面操作）未单独录证，但底层 skill 发现机制与 headless 完全一致。

## 第 5 层验证：真实前端 GUI 会话（2026-08-16）

在 3099 web（maglev-demo profile）真实浏览器会话中，用户手动走完演示脚本核心步骤，session log 导出至 `~/Downloads/session.jsonl`：

- **maglev_reality_status**：调用成功，返回项目现状（能力域/进行中主题/愿景/契约状态）。
- **maglev_crystallize**：调用成功，先写 `docs/thinking/` 决策记录满足 docs_thinking 检查 → 门禁放行 → 写回 `specs/20_evolution/active/2026-08-16-crystal-j5yyb.md`，并**真实产生 `maglev/crystallize` 会话事件**（前端结晶卡片的数据源）。
- **文件名**：中文标题正确回退为 `crystal-<随机>`（空 slug 修复生效，见 `docs/thinking/2026-08-15-dsh-tools-instance-split.md`）。
- **门禁复验**：agent 结晶后运行 `spec_integrity_check.py` 全 PASS。

结论：**浏览器演示核心链路（真相卡片 + 结晶卡片 + 事件卡片渲染数据）在真实前端会话中验证通过**。

## 验证日期

- 2026-08-15：R0 固化 29 技能 + 四层验证 + 端到端会话验证完成
- 2026-08-16：真实前端 GUI 会话验证（第 5 层）+ 修复 dsh-tools 实例分裂导致工具调度失败的排查闭环
