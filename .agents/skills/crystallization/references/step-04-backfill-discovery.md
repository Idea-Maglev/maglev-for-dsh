---
name: backfill-discovery
description: 必要时触发地图与索引回填，保证新现实可被发现
next_step: references/step-05-archive-with-log.md
---

# Step 4: Backfill Discovery

## 目标

确保新现实不只被写回，还能被后续会话发现。

## 动作

1. 判断当前主题变化是否影响：
   - 项目地图
   - 索引 / 导航
2. 若影响地图，调用或转交 `maglev-map-maker`。
3. 若影响索引，调用或转交 `index-librarian`。
4. 输出当前主题是否已完成可发现性回填。

## 触发规则

- 影响 `10_reality` 结构时，优先考虑 `maglev-map-maker`
- 影响入口、目录、索引或可检索路径时，优先考虑 `index-librarian`
- 若当前主题变化不影响后续发现路径，可以显式输出"无需回填"

### 跨模块引用一致性检查

当 step-02 推导输出 `modules_detected > 1` 时，本步骤额外执行：

1. **R-标记可达性**：被引用的 R-标记（`R-{MODULE}-{DOMAIN}-{SEQ}`）必须在目标模块文件中存在定义，否则标记断链
2. **依赖声明对称**：模块 README 中的 `depends_on` 与对方 `consumed_by` 必须对称（A 声明依赖 B → B 应声明被 A 消费）

输出字段增加：`cross_module_consistency: ok | issues[]`（仅当 `modules_detected > 1` 时输出）

## 输出格式

- `discovery_backfill_required: yes | no`
- `map_backfill`
- `index_backfill`
- `downstream_actions`

## 输出

- 一份可发现性回填判断
- 一组必要的下游回填动作
