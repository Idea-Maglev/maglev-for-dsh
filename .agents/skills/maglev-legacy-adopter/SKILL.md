---
name: maglev-legacy-adopter
description: 存量项目接入器。负责环境诊断、基础设施注入，并编排逆向工程与索引构建。
metadata:
  formal_action_name: 存量接入
  top_level_capability: 整体接入
  system_layer: Infrastructure Layer
  lifecycle_chain: system_enablement
  runtime_name_status: active_legacy_name
  distribution_scope: runtime_internal
---

# 存量接入器 (Legacy Adopter)

> 结构动作名：`存量接入`
> 运行面名称：`maglev-legacy-adopter`
> 这不等于已经完成正式物理改名。

## 核心规则

1. 接入过程不得破坏现有代码逻辑。
2. 不要求项目先有完整文档，而是允许根据代码和已有产物重建结构理解。
3. 存量接入不是终点，接入后应继续完成逆向、审计和索引回填，确保产物可持续维护。

## 何时使用

- 需要把一个已有仓库纳入 Maglev 结构时。
- 项目已存在代码与运行现实，但缺少可直接进入 Maglev 主流程的基础承接时。
- 需要为后续逆向、索引和治理建立最小接入环境时。

## 处理流程

### Phase 1: 环境诊断

**目标**：评估项目现状，确定接入策略。

- 扫描项目根目录。
- 检查关键特征：`pom.xml` / `package.json`、`README.md`、`specs/` 等。
- 若发现关键目录结构缺失，应明确提示当前接入风险和最小补齐建议。

### Phase 2: 基础设施注入

**目标**：建立 Maglev 运作所需的最小环境。

- 确认 `.maglev` 配置（Rules/Protocols）是否存在。
- 确认 `.agents` 技能库是否完整。
- 若缺失，引导进入 `maglev-bootstrapper` 或补齐最小基础设施。

### Phase 3: 逆向工程准备

**目标**：建立第一个可持续依赖的现实锚点。

- 询问本项目中最核心、或近期准备修改的功能范围。
- 先读取或创建 `specs/10_reality/00_profile.yaml` 与固定骨架。
- 调用 `maglev-reverse-spec` 建立第一个现实锚点，并将结果映射到 Profile 的主域和槽位。
- 无法映射的事实保持 unknown 或提出版本化扩展，不按主题新建目录。

### Phase 4: 输入质量审计

**目标**：确保逆向结果达到可继续协作的质量门槛。

- 调用 `spec-audit-surface`
- 审查刚生成的逆向结果是否具备可追踪性、结构完整性和继续使用的稳定性。

### Phase 5: 索引登记

**目标**：将新接入结果纳入可发现性体系。

- 调用 `index-librarian`
- 更新对应索引，使后续会话可以发现接入结果。

## 必需的参考资料

- 工作流入口: `references/legacy-adopter.workflow.md`
- 诊断步骤: `references/step-01-mri-scan.md`
- 引导步骤: `references/step-02-bootstrap.md`
