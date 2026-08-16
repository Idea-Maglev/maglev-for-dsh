---
name: step-01-empathy
description: 深度用户画像访谈与情感目标定义 (Deep Mode v2.0)
next_step: references/step-02-journey.md
---

# Step 1: Empathy (同理心) - Deep Mode

## 目标
通过 **深度访谈** 理解**谁**在使用功能，以及他们想要**什么感觉**。
**拒绝假设**: 不接受"一般用户"或"目标用户"这种模糊定义。

## 动作

### 1. Scan (扫描)
读取 `01_requirements.md`，提取初始的用户信息。

### 2. Challenge (挑战)
**主动质疑用户假设**，避免设计偏离真实用户：

> **[EMPATHY CHECKPOINT]**
>
> 在开始设计之前，我想和你确认几个关于用户的问题：
>
> 1. "这个功能的用户具体是谁？能描述一个真实的人吗？"
>    - (不接受: "企业用户"、"C端用户" 这种抽象标签)
>
> 2. "这个用户在使用我们产品之前/之中/之后，分别是什么情绪？"
>    - Before: 焦虑？期待？
>    - During: 困惑？专注？
>    - After: 满足？释然？
>
> 3. "如果这个设计失败了，用户会有什么感受？"
>    - (这能帮助我们理解 stakes)

### 3. Define (定义)
基于访谈结果，提炼 1-2 个 **核心 Persona**。

## 模板 (Persona - Enhanced)
```markdown
### 👤 Persona: {Real Name or Archetype}
- **Who**: {具体描述，不是标签} (e.g., "35岁的产品经理，每天开6个会")
- **Context**: {使用场景} (e.g., "在地铁上用手机快速查看")
- **Pain Point**: {当前痛点} (e.g., "找不到上次看的订单")
- **Need**: {核心需求} (e.g., "3秒内找到需要的信息")
- **Emotional Journey**:
    - **Before**: {使用前情绪} (e.g., 焦虑)
    - **During**: {使用中情绪} (e.g., 专注)
    - **After**: {使用后情绪} (e.g., 满足)
```

## 退出条件
当满足以下条件时，可进入 Step 2 (Journey)：
- [ ] Persona 是具体的人，不是抽象标签
- [ ] 情绪曲线 (Before/During/After) 已定义
- [ ] 已识别至少一个"失败体验"场景
- [ ] 上下文已更新到 `./00_context.md`

---

## 上下文交接 (Context Handoff)

### 读取已有上下文
技能启动时，先检查 `./00_context.md` 是否存在：
```
IF ./00_context.md 存在 AND 包含 Persona THEN
    展示: "根据已有上下文，用户是 [Persona]。是否需要修改？[Y/n]"
    IF 用户确认 THEN 跳过 Persona 问题
```

### 写入情绪曲线
将本步骤的产出 **Append** 到共享上下文：

```markdown
## 情绪曲线 (Emotional Journey)
<!-- design-ux 填充 -->
- **Before**: {使用前情绪}
- **During**: {使用中情绪}
- **After**: {使用后情绪}

## 失败体验 (Failure Scenario)
<!-- design-ux 填充 -->
- {识别的失败场景}
```

> **注意**: 使用相对路径 `./00_context.md`，不要暴露本地绝对路径。
