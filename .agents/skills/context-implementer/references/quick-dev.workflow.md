---
name: quick-dev
description: '上下文实施工作流：在方案依据清楚后执行改动、自检与对抗性审查。'
# Maglev: Hardcoded Config
installed_path: 'references'
quick_spec_workflow: '.agents/skills/spec-designer/SKILL.md'
---

# 上下文实施工作流 (Maglev Edition)

**目标：** 在输入边界清楚后，受控地执行实施、自检与对抗性审查。

**Maglev 标准:**
- **Spec-Check**: 进入实施前，请先确认存在可消费的方案依据或 active spec。
- **Language**: Chinese (Simplified).

---

## 工作流架构
使用 **步骤文件架构** 进行专注执行：

### 核心原则
- **微文件设计**: 每个步骤都是一个自包含的指令文件，必须严格遵循
- **状态隔离**: 每个步骤都重新加载以对抗“迷失在中间”
- **状态持久化**: 通过 `stepsCompleted` 变量持久化进度

### 关键规则 (无例外)
- 🛑 **绝不** 同时加载多个步骤文件
- 📖 **务必** 在执行前阅读整个步骤文件
- 🚫 **绝不** 跳过步骤或优化顺序 - 哪怕步骤看起来很小
- 🎯 **务必** 遵循步骤文件中的确切说明
- ⏸️ **务必** 在菜单处停止并等待用户输入

---

## 初始化序列

### 1. 配置加载
无需加载外部 Config。使用 Maglev 标准配置：
- **Language**: Chinese (Simplified)

### 2. 第一步执行
完整阅读并遵循：`references/step-01-mode-detection.md` 以开始工作流。
