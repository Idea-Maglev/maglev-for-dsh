# 发布缺口：dsh 技能发现只扫项目根 → 技能随插件注入

> 记录时间: 2026-08-16（0.1.1 发布前）

## 现象

端到端测试（模拟新用户从公域 npm 安装）发现：**干净项目（无 `.agents/skills`）里，dsh 的 skill 工具找不到 npm 包内的 maglev 技能**（"技能不可用"）。

## 根因

dsh 的 skill-filesystem 原生扫描 `<projectRoot>/.agents/skills`（`skill-filesystem/src/index.ts:247`），技能发现**绑定项目根**。npm 包内的 `.agents/skills` 只存在于 `node_modules/@idea-maglev/maglev-for-dsh/.agents/skills`，不在用户项目根，因此永远不会被扫描到。

之前"29 技能被 dsh 真实发现"的验证都是在仓库**自己**（项目根有 .agents/skills）做的，掩盖了发布后的缺口。

## 解决方案：bundled skill provider 注入

dsh-skill 提供 `ctx.skills.registerProvider()`（`skill/src/index.ts:423`），接受**工厂函数** `(control) => SkillProvider`（`create(control)` 模式，第一个参数不是 provider 对象！）。

maglev host 插件（apply 时）注册 `maglev-bundled` provider：

- `list()`：读包内 `.agents/skills/<skill>/SKILL.md`（跳过 `_` 开头目录），正则解析 frontmatter 的 name/description，返回候选（`rank: 600` = `BUNDLED_SKILL_RANK`，**低于项目技能 rank 100-500，项目优先**）
- `get()`：读 SKILL.md 全文，**返回完整 SkillDefinition**（name/description/invocation/source/provider/content/path——漏字段会报 `loaded skill name must be a string`）

## 关键实现细节

1. **定位包内技能目录**：`fileURLToPath(new URL('../.agents/skills', import.meta.url))`（host 编译产物在 `lib/`，技能在上一级）
2. **零依赖**：frontmatter 用正则解析（不引入 yaml 库）
3. **provider 是工厂函数**：`registerProvider(() => ({name, list, get}))`，不是对象
4. **容错**：技能注册失败不阻断工具能力（try-catch 降级）

## 验证证据（0.1.1）

- 干净项目（仅 README.md）+ 公域 npm 安装的 0.1.1 tarball
- skill 工具加载 `reality-sync` / `maglev-discipline` 成功，内容完整
- `maglev_reality_status` 工具正常
- 无调试残留，exit 0

## 版本

- 0.1.0：缺技能注入（发布后才发现）
- 0.1.1：技能随插件注入（本记录）
