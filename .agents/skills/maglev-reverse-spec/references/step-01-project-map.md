---
description: maglev-reverse-spec Step 2 Support - Project Map
---

# Step 2 Support: Project Map (项目地图)

## 目标
在 Step 1 Evidence Acquisition 已完成的前提下，把已识别的入口线索整理成用户可理解的 `Feature Map`，为后续模块选择和入口分析服务。

## 前置条件
- 已完成 `step-01-evidence-acquisition.md`
- 已有初版技术栈判断、入口类型判断和关键文件列表
- 已明确当前项目更适合 `UI / API / Event / Data / CLI` 哪种入口

## 执行逻辑

### 1.1 汇总入口证据
把 Step 1 中拿到的入口信号归并为可读列表，例如：
- 页面 / 路由
- API / Handler / Contract
- Event Producer / Consumer
- Schema / Model / Migration
- Command / Job / Script

### 1.2 生成 Feature Map
每个入口至少包含：
- `name`: 功能或入口名称
- `entry_type`: `ui / api / event / data / cli`
- `path_or_signal`: 路径、路由、事件名或结构线索
- `source`: `router-inference / code-scan / schema-scan / test-evidence / runtime-artifact`
- `confidence`: `high / medium / low`

### 1.3 入口收敛
根据项目形态做最小收敛：
- 如果是 UI 明显主导项目，优先保留用户可见功能入口
- 如果是纯服务项目，优先保留 API / Event / Data 入口
- 如果入口很多，先标出核心入口和边缘入口，不要求一步穷尽

### 1.4 进入下一步
- 在进入具体分析前，先执行 `references/step-02b-module-partition.md`
- UI 型入口可继续使用 `references/step-01b-router-analysis.md` 或 `references/step-02-page-analysis.md`
- API / Event / Data 型入口可直接进入 `step-03-stack-trace.md` 或数据结构分析

## 输出示例

```json
{
  "features": [
    {
      "name": "PrimaryWorkspace",
      "entry_type": "ui",
      "path_or_signal": "/workspace",
      "source": "router-inference",
      "confidence": "high"
    },
    {
      "name": "RecordQueryAPI",
      "entry_type": "api",
      "path_or_signal": "GET /api/records",
      "source": "code-scan",
      "confidence": "medium"
    }
  ]
}
```

## 失败处理
- 若入口太分散，先输出“候选入口列表”，不要强行合并成单一主线
- 若证据不足以命名功能，允许先用技术性名称占位，并标记为 `[INFERENCE]`
