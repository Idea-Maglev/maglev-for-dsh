---
description: maglev-reverse-spec Step 1 - Evidence Acquisition
---

# Step 1: Evidence Acquisition

## 目标
在不提前深读全仓库的前提下，快速建立证据地图，判断该从哪里进入，以及哪些结论可信。

## 优先抓取的证据
1. 测试文件
2. 路由、命令注册、任务注册、事件订阅
3. API Schema、DTO、类型定义
4. 数据模型、迁移、表结构
5. UI 入口、页面、状态管理
6. 配置、环境变量、feature flags
7. 可用的运行日志、样例响应、截图或录屏

## 扫描策略
1. 先做浅扫描，识别技术栈和入口类型
2. 再使用 `scripts/mri_scanner.py` 或等价脚本提取路由/API/接口线索
3. 最后人工读取关键文件，建立第一版 Evidence Log

## 输出
至少输出：
- 技术栈判断
- 入口类型判断
- 关键文件列表
- 证据等级摘要
- 推荐下一步路径
