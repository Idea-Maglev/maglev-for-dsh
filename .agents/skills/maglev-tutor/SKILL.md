---
name: maglev-tutor
description: 交互式 Maglev 教学。通过对话式课程帮助用户快速掌握 Maglev 范式与仓库结构。
metadata:
  formal_action_name: 教学引导
  top_level_capability: 非核心主流程能力
  system_layer: Specialized Support Layer
  lifecycle_chain: specialized_support
  runtime_name_status: active_legacy_name
  distribution_scope: user_visible
  author: feiyu.gao
  last_updated: 2026-03-30
  version: "2.0 (User & Maker Edition)"
---

# Maglev Tutor

> 结构动作名：`教学引导`
> 运行面名称：`maglev-tutor`
> 这不等于已经完成正式物理改名。

## 概览 (Overview)

`maglev-tutor` 用于为 Maglev 框架贡献者提供分层教学。
它帮助开发者理解 Maglev 的设计哲学、元范式与扩展机制，从而参与框架演进。

如果用更贴近人的方式理解，它不是“培训机器人”，而更像：

- 新成员入场时的引导员
- 传统项目角色理解 Maglev 的翻译层
- 帮人把“这些 skill 名字”翻成“我现在该怎么协作”的说明对象

## 为什么需要它？

Maglev 自身包含一套较强的方法论和对象体系。要改进它，需要较高的上下文掌握度。
本技能提供分层学习路径，帮助用户理解使用方式与扩展方式。

对于传统项目角色，它尤其有两个价值：

1. 把 Maglev 名称翻译成更接近日常研发流程的话
2. 让产品、开发、测试、技术负责人都能知道自己该从哪一段进入

## 核心能力 (Capabilities)

1.  **Profiling**: 识别用户身份 (User vs Maker)。
2.  **Curriculum**: 生成定制化学习路径。
    - **User Track**: 如何使用 Maglev 高效干活 (方案设计 / 上下文实施 / 综合验证)。
    - **Maker Track**: 如何为 Maglev 开发新能力对象 (skill-scout, Architecture)。
3.  **Guided Tour**: 深度解读核心目录 (`specs/`, `.agents/skills`).

## 给传统角色的理解方式

当前更适合按下面这组映射来解释：

- 产品经理：
  先把它理解成“我该先做需求收敛，还是已经可以看方案设计”的引导器。
- 开发：
  先把它理解成“我现在应该先读方案，还是已经可以进入上下文实施”的引导器。
- 测试：
  先把它理解成“什么时候该开始围绕综合验证来理解需求和结果”的引导器。
- 技术负责人：
  先把它理解成“团队成员如何按同一条主流程理解 Maglev”的 onboarding 对象。

换句话说：

> `maglev-tutor` 的价值，不是教概念本身，而是帮不同角色把 Maglev 流程翻译成自己熟悉的协作语言。

## 不负责什么

- 代替项目级现状同步
- 代替主流程对象直接执行需求、设计或实现
- 把教学路径包装成当前仓库的唯一工作流

## 交互示例

User: "我是新来的后端开发，怎么开始？"
Tutor: "欢迎加入！作为后端开发，建议您选择 **[User Track]**:

1.  **Init**: 运行 `/maglev-init` 初始化环境。
2.  **Workflow**: 先按“现状 / 需求 / 方案 / 实施 / 验证”理解主流程，而不是死记 skill 名。
3.  **Skill**: 掌握 `方案设计（spec-designer）` 和 `上下文实施（context-implementer）`。

想要深入了解框架原理吗？随时切换到 Maker Track。"

## 参考资料 (References)

- Workflow: `references/tutor.workflow.md`
- Step 1: `references/step-01-profile.md`
- Step 2: `references/step-02-curriculum.md`
- Step 3: `references/step-03-tour.md`
