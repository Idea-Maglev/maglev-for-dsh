---
name: step-03-map-roles
description: 映射铁三角角色在每个需求上的参与状态
next_step: references/step-04-render-board.md
---

# Step 3: Map Roles (角色状态映射)

## 目标

基于流程阶段和人员配置，确定每个需求中 VO/TP/XG 的当前状态。

## 动作

### 1. 读取项目级配置

检查 `.maglev/team.yaml` 是否存在。

若存在，解析 YAML 中的 team 配置：

```yaml
team:
  vo: { name: "张三", title: "产品经理" }
  tp: { name: "李四", title: "前端工程师" }
  xg: { name: "王五", title: "测试工程师" }
```

若不存在，标记 `team_config = null`（后续仅展示角色代号）。

> **边界规则**：若 `team_config` 存在但 `name` 为空字符串 `""`，视同未配置，展示 `(未配置)` 而非空白。

### 2. 检查 Spec 级覆盖

对每个活跃 spec，检查是否有局部角色配置：
- `{spec_dir}/team.yaml` 文件
- 或 `{spec_dir}/00_intent.md` 中的 `## 角色` 章节

若存在，该 spec 使用局部配置覆盖项目级配置。

### 3. 阶段→角色状态映射

根据每个需求的当前阶段，应用以下规则：

| 阶段 | VO | TP | XG |
|------|----|----|-----|
| 需求收敛 | 主导中 | 待介入 | 未参与 |
| 方案设计 | 已完成 | 主导中 | 待介入 |
| 编码实施 | 已完成 | 主导中 | 待介入 |
| 综合验证 | 已完成 | 已完成 | 主导中 |
| 结晶归档 | 已完成 | 已完成 | 已完成 |

### 4. 组装输出

每个需求的 RoleMapping：

| 字段 | 说明 |
|------|------|
| vo.person | 人员名称（若配置了）或 null |
| vo.status | 主导中 / 待介入 / 已完成 / 未参与 |
| tp.person | 同上 |
| tp.status | 同上 |
| xg.person | 同上 |
| xg.status | 同上 |

## 输出

每个 ActiveItem 附加 RoleMapping，传递给 Step 4。
