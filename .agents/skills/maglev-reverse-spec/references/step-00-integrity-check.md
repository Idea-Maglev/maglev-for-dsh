---
description: maglev-reverse-spec Step 00 - Integrity Check
---

# Step 00: Integrity Check (启动自检)

## 目标
确保逆向工程的运行环境、输出目标和分析范围都已就绪，避免在错误上下文中开始大规模扫描。

## 自检列表

### 1. 环境准备
* **Action**: 检查临时目录、输出目录和参考模板是否可用。
* **Logic**: 如果当前仓库是 Maglev 结构，优先使用 `.maglev/temp` 与 `specs/10_reality/`。

### 2. 逆向目标锁定
检查以下问题是否已有答案：
1. 逆向对象是什么
2. 入口从哪里开始
3. 输出要达到什么深度
4. 是否要生成可继续开发的规格
5. 本轮 reality 预期对应几个模块单元
6. 本轮是否严格停留在观察/建模范围内，而不进入业务修复

如果没有，先输出一个范围锁定摘要，而不是直接读取全仓库。若目标可能包含多个模块，必须在后续进入 `Module Partition`。

### 2b. 行为边界确认
* **Action**: 明确声明“本轮 reverse 默认禁止业务修复或数据变更”。
* **Reason**: 避免因为识别到问题而顺手改动现有系统，导致 reality 被 reverse 过程本身污染。

### 3. 依赖与工具检查
检查以下依赖是否存在：
1. spec pipeline 的 draft 内部模块
2. spec pipeline 的 crystallize 内部模块
3. `scripts/mri_scanner.py` 或其他快速扫描器

### 4. 状态重置
* **Action**: 清理上一次逆向的临时事实文件。
* **Reason**: 防止历史上下文污染本轮逆向。

## Checkpoint
如果上述检查通过，输出：
```
[CHECKPOINT - System Ready]
✅ 环境完整性检查通过。
- Scope: Locked
- Temp Dir: OK
- Dependencies: OK
- Clean Slate: OK
```
否则，指出缺失项并暂停。
