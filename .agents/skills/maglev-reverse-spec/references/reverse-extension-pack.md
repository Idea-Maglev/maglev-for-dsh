---
description: maglev-reverse-spec Optional Extension Pack
---

# Reverse Extension Pack

## 目标
让逆向结果既能足够完整，又不会因为一次性塞入太多内容而失焦。

## 使用规则
先完成核心层，再判断是否启用扩展层。

如果用户已经在 Step 00b 选择了输出档位，则按以下映射执行：
- `Lean` -> Core Layer
- `Standard` -> Core Layer + Recommended Layer
- `Deep` -> Core Layer + Recommended Layer + 按证据启用 Extended Layer

### Core Layer
每次逆向都应包含：
- Feature Map
- Evidence Log
- Data Structure Map
- Main Flow / State Trace
- Unknowns / Quests

### Recommended Layer
在以下情况默认启用：
- 逆向结果将指导开发、重构或补测试
- 目标模块存在明显状态流或多结构映射
- 用户要求“严谨”“完整”“可交接”

建议启用：
- Domain Model
- Dependency Topology
- State Machine
- Test Mapping
- Change Risk

### Extended Layer
只有在高复杂度或高风险场景启用：
- Security Surface
- Error Taxonomy
- Runtime Behavior
- Configuration Matrix
- Observability Map

## 冗余识别规则
如果出现以下情况，应提示用户可裁剪：

1. 结构重复
同一信息已经在 Data Dictionary、API Schema、State Machine 中重复出现。

2. 低收益扩展
例如纯静态页面仍生成大量 Security/Runtime 内容。

3. 证据不足
当前只有命名或少量注释，不足以稳定产出该维度。

4. 与目标不匹配
用户只是想了解模块用途，却生成了过多工程治理内容。

## 推荐的启用交互
逆向开始后，先给出一个扩展建议摘要：

```markdown
[Extension Suggestion]
- 必选: Core Layer
- 推荐: Domain Model, State Machine, Test Mapping
- 可选: Security Surface, Observability Map

当前判断:
- 项目复杂度: High
- 证据完整度: Medium
- 目标用途: 计划用于后续重构

建议选择:
- `Lean`: 仅 Core
- `Standard`: Core + Recommended
- `Deep`: Core + Recommended + 部分 Extended
```

## 各扩展维度说明

### 1. Domain Model
适合有明确业务概念、术语不统一、对象关系复杂的系统。
输出：
- 核心业务对象
- 术语对齐
- 聚合与边界

### 2. Dependency Topology
适合服务多、基础设施重、外部依赖复杂的系统。
输出：
- 上下游依赖图
- 同步/异步边界
- 外部依赖风险

### 3. State Machine
适合存在显式状态字段、审批流、任务流、会话流的系统。
输出：
- 状态集合
- 转移条件
- 非法状态与保护逻辑

### 4. Runtime Behavior
适合异步、并发、缓存、流式输出、后台任务场景。
输出：
- 并发模型
- 缓存策略
- 重试/补偿机制
- 定时与后台任务

### 5. Security Surface
适合有租户、权限、数据隔离、审计要求的系统。
输出：
- 身份认证
- 权限检查点
- 敏感数据流向
- 审计日志

### 6. Error Taxonomy
适合异常复杂、降级链路重要的系统。
输出：
- 错误类型
- 用户可见错误
- 系统内部异常传播
- 回滚与补偿

### 7. Configuration Matrix
适合环境差异大、配置驱动强的系统。
输出：
- 配置项
- 生效范围
- 默认值
- 环境差异

### 8. Observability Map
适合线上诊断成本高的系统。
输出：
- 日志点
- 指标点
- Trace 锚点
- 告警建议

### 9. Test Mapping
适合需要补测试或做验证闭环的系统。
输出：
- 代码到测试映射
- AC 到测试映射
- 空白覆盖区

### 10. Change Risk
适合准备重构或要交接给别人改的系统。
输出：
- 热点文件
- 脆弱边界
- 改动半径
- 高风险入口
