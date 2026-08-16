---
description: maglev-reverse-spec Step 3 - Data Structure Analysis
---

# Step 3: Data Structure Analysis

## 目标
把项目中的“数据承载体”系统化还原出来，让用户和 AI 能看清系统到底在操作什么对象，而不是只看到调用链。

## 必须覆盖的结构类型
1. 持久化结构: Table / Entity / Document / Migration
2. 接口结构: DTO / Request / Response / Schema
3. 前端结构: ViewModel / Store State / Form Model
4. 运行时结构: Cache Object / Session Payload / Event Payload
5. 派生结构: Aggregation / Projection / Mapper Output

## 解析维度
每个关键结构至少回答：
- 名称与角色
- 定义位置
- 核心字段
- 字段约束: required / optional / enum / default / nullable
- 结构关系: one-to-one / one-to-many / nested / derived
- 生命周期: create / update / persist / expire / archive
- 跨层映射: API -> Service -> DB / Store -> View

## 输出格式
```yaml
data_structures:
  - name: Record
    kind: entity
    defined_in: backend/models/record.py
    fields:
      - name: id
        type: string
        required: true
      - name: state
        type: enum
        required: true
    relations:
      - target: RecordAttachment
        type: one-to-many
    lifecycle:
      - create: create_record()
      - update: update_record_state()
    mappings:
      - api_request: CreateRecordRequest
      - api_response: RecordDetailResponse
```

## 关键规则
- 不只列字段名，要解释字段在业务中的作用
- 不只看数据库，也要看前端状态和事件载荷
- 发现“同名异义”或“多结构映射同一概念”时，必须显式标注
- 对不确定字段语义，标记为 `[UNKNOWN]` 或进入 `Quest`
