---
description: maglev-reverse-spec Step 4 Support - Stack Trace
---

# Step 4 Support: Stack Trace (全栈追踪)

## 目标
从 Step 2 识别的 API 入口，追踪后端调用链：`Handler -> Service -> Repository -> Core Structure`。

## 执行逻辑

### 3.1 Controller 定位
根据 API 路径 (e.g., `/api/records`)，在后端代码中查找对应的 Handler。

### 3.2 Service & Repository 追踪
递归追踪 Service 层和 Repository 层的调用。

### 3.3 数据实体定位
标记涉及到的数据结构定义位置，但详细的数据结构建模在 `step-03-data-structure-analysis.md` 中完成。

### 3.4 输出格式 (Strict YAML)
**注意**: 所有描述性文字（purpose, fields explanation）必须使用中文。

```yaml
stack_trace:
  api: GET /api/records
  controller:
    file: RecordController.java
    method: listRecords()
    lines: 25-40
  service:
    file: RecordServiceImpl.java
    method: listRecords()
  repository:
    file: RecordRepository.java
    method: findAll()
  entities:
    - name: Record
      fields: [id, ownerId, state]
      relation: "One to Many with RecordAttachment"
```

## Checkpoint 输出模板 (中文)
```
[CHECKPOINT - Step 3 Complete]

✅ 后端追踪完成: GET /api/records

🔗 调用链:
Controller: RecordController.java
    ↓
Service: RecordServiceImpl.java
    ↓
Repository: RecordRepository.findAll()

📊 数据模型:
- Record [id, ownerId, state...]

是否进入意图推测 (Intent) ? [Y/n]
```

## 复杂情况处理
- **External**: 外部调用标记为 `[外部依赖]`。
- **Async**: 消息队列标记为 `[异步事件]`。
