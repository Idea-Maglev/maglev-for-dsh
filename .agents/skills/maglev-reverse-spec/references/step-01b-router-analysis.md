---
description: maglev-reverse-spec Step 2 Support - Router Analysis
---

# Step 2 Support: Router Analysis (路由智能分析)

## 目标
当用户选择 **[S]mart** 策略时，通过解析路由配置文件，精准还原页面结构，避免全量扫描造成的干扰和浪费。

## 支持文件
优先查找以下模式的文件：
- `src/router/index.js` (Vue)
- `src/router/routes.ts` (Vue/React)
- `src/App.tsx` (React Router)
- `src/app/app-routing.module.ts` (Angular)

## 执行逻辑

1.  **Locate**: 使用 `find_by_name` 查找上述路由文件。
2.  **Parse**: 读取内容，提取路由定义对象。
    *   `path`: URL 路径
    *   `name`: 路由名称
    *   `component`: 关联的组件文件路径 (Key Signal)
3.  **Map**: 将提取出的组件路径作为 "确定的入口"，仅对这些文件进行后续分析。

## 输出
更新 Feature Map，标记 source 为 `router-inference`。

```json
{
  "features": [
    {
      "name": "PrimaryWorkspace",
      "path": "/workspace",
      "frontend": "src/views/PrimaryWorkspace.vue",
      "source": "router-inference"
    }
  ]
}
```

## 下一步
返回 Step 1 并展示生成的 Feature Map。
