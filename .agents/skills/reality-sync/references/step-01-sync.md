---
name: step-01-sync
description: 同步上下文
---

# Step 1: Sync (现实同步)

## 目标
读取当前真实有效的主线文件，向用户输出一份可操作的会话启动简报。

## 动作
1. **Read Core Reality**: 优先读取以下内容：
   - `specs/20_evolution/active/` 中的活跃主线 Spec
   - `issues/active/` 中的活跃任务
   - `specs/10_reality/crosscutting/repository-map/overview.md`
   - `specs/10_reality/glossary.md`（若存在且非空，加载已确认术语到会话上下文）
   - `specs/20_evolution/board.md`（若存在，读取看板摘要：活跃需求数、各阶段分布、主导角色。不触发看板更新，仅展示缓存数据。若 `最后更新` 时间戳距今超过 7 天，追加提示 `⚠️ 看板数据已过期，建议运行 /board 刷新`）

2. **Read Recent Decisions**:
   - `docs/thinking/README.md`
   - 最近新增或最近修改的决议文档

3. **Read Execution Reality**:
   - 必要时读取 `git status --short`
   - 必要时读取关键实现或发行物文件，确认当前正式实现与历史实现的边界

4. **Synthesize**: 输出 **"Maglev Session Brief"**，必须包含以下部分：
   - `Space`: 当前主线、主实现、关键发行物
   - `Mind`: 最近决议、当前阶段判断
   - `Risk`: 当前最重要的结构风险或试用暴露问题
   - `Action`: 当前最优先的 1-3 个动作
   - `Mode`: 推荐进入的工作模式，只能选一个

5. **Ready**:
   - 结束语应为动作导向，而不是空泛问候
   - 例如：`System aligned. Recommended mode: Implement.`

## 示例输出
```text
# Maglev Session Brief

[Space]
- 主线: `maglev_distribution`
- 主实现: `.maglev_build/maglev_installer.py`, `scripts/maglev_release.py`
- 包装层: `packages/maglev-cli/`

[Mind]
- `version_sync_tool` 已被吸收
- 当前处于试用反馈驱动的分发治理阶段

[Risk]
- 根目录下发安装器脚本会污染目标项目
- AI 操作层尚未补齐更新入口

[Action]
- 1. 先修正试用中暴露的下发行为
- 2. 再验证更新链路

[Mode]
- Implement

System aligned. Recommended mode: Implement.
```
