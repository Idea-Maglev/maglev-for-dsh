---
description: maglev-reverse-spec Step 2 Gate - Module Partition
---

# Step 2 Gate: Module Partition (模块切分)

## 目标
在生成 reality 产物前，先把当前分析对象切分成稳定的模块单元，避免多个模块被写入同一个 reality 目录。

## 核心规则

### 1. 一次只生成一个模块目录
- `module_slug` 只标识逆向分析分区，不对应 Reality 目录
- 每条事实必须在写回前映射到 Profile 的一个主域和槽位
- 禁止以多个功能、多个子域或多个入口为理由绕过 Profile 新建目录

### 2. 目录按模块现实组织，不按任务组织
- 正确：`specs/10_reality/{primary_domain}/{owner_slot}/...`
- 错误：把 module_slug 直接作为 Reality 同级目录
- 错误：按 task 或 project slug 创建同级目录

### 3. 模块边界优先来自现实结构
优先按以下信号切分模块：
- 独立页面或独立用户任务
- 独立 API 资源或独立业务对象
- 独立状态机
- 独立事件主题或消费链路
- 独立配置域
- 独立知识/资产子域

## 执行逻辑

### 1. 列出候选模块
基于 Feature Map、入口信号、数据结构和调用链，先列出候选模块列表。

### 2. 给每个候选模块生成 4 个字段
- `module_name`
- `module_slug`
- `boundary_reason`
- `primary_entry`

### 3. 判断是否需要拆分
若满足以下任一条件，应拆成多个模块：
- 主对象不同
- 主流程不同
- 状态机不同
- 用户任务不同
- 运行时链路差异明显

### 4. 锁定本轮写入目标
在真正生成 reality 文档前，必须先明确：
- 本轮只写哪个 `module_slug`
- 其他模块进入待处理列表

## 输出格式

```yaml
module_partition:
  selected_module:
    module_name: Record Query
    module_slug: record_query
    boundary_reason: 独立查询入口、独立返回结构、独立列表交互
    primary_entry: GET /api/records
  pending_modules:
    - module_name: Record Archive
      module_slug: record_archive
      boundary_reason: 独立状态流和写操作链路
      primary_entry: POST /api/records/{id}/archive
```

## module_slug 规则
- 使用稳定、可维护、面向现实对象的名称
- 优先用模块名，而不是任务批次名
- 避免使用 `reverse_`、`analysis_`、`task_`、`tmp_` 这类过程性前缀
- 避免把整个项目名直接当成模块名，除非本轮 reality 的确只对应一个单体模块

## 失败处理
- 如果暂时无法切分清楚，先输出候选模块列表，不允许直接落盘
- 如果多个入口共用同一主对象但流程不同，可先落到父模块，再在目录内按子模块章节拆分
- 如果模块边界明显不清，应将边界问题写入 `Unknowns / Quests`

## 产物标准意识

本步骤的切分是逆向**自有的结构生产流程**（证据驱动归纳，适配上下文缺失场景），与结晶的四步推导（演绎）不同，各自保留。

但切分产出的结构，最终需满足统一的 **reality 产物标准**（见 `.agents/skills/crystallization/references/reality-artifact-standard.md`）：
- 多模块时每个模块目录需有非空 README
- 结构自适应，不塞不存在的维度

产物是否达标，由 step-06 的 `crystallization_check.py` 验证。
