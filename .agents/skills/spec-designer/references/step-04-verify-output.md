---
description: spec-designer Step 04 - Verify Output
---

# Step 04: Verify Output (产出验证)

## 目标
作为 Quality Gate (质量门禁)，在任务结束前验证 Spec 文件簇的完整性和归档状态，并获得用户明确确认后才交接给实施。

## 验证逻辑

### 1. 全局路径确认
根据上下文中的 `slug`，构建预期路径：
`Target: specs/20_evolution/active/{slug}/`

### 2. 核心文件检查 (Existence Check)
检查以下文件是否存在：
- [ ] `00_index.md` (索引)
- [ ] `01_requirements.md` (核心需求)
- [ ] `02_design.md` (设计)
- [ ] `03_plan.md` (计划)

### 3. 交互文档检查（含 UI 项目时）
如果需求中包含 I 系 AC 或 in_scope 涉及 UI/前端：
- [ ] `01_requirements_interaction.md`（交互需求，可选）
- [ ] `02_design_interaction.md`（交互设计，可选）

缺失时标记为 WARNING（不阻塞），但需告知用户。

### 4. Layout-to-API Binding Gate 检查（UI + API 项目时）
如果需求同时包含 UI/前端和后端/API/数据提供方依赖：
- [ ] `02_design_fe_be_contract.md`（页面锚点、请求编排、逐字段契约）

缺失时标记为 WARNING（不阻塞），但必须告知用户：当前方案缺少前后端页面契约，进入实施会增加接口与联调返工风险。

### 5. 归档检查 (Context Archival)
检查 Facts 是否已成功归档到 Spec 上下文目录：
- [ ] `context/input_facts.md`

### 6. 进入实施审批

在结构检查全部通过后，展示 spec 产出概要并等待用户确认：

1. **展示概要**：
   - 需求数量：F 系 {N} 个 + I 系 {M} 个（如有）
   - AC 总数：{total} 个
   - 设计文档：{列出所有设计文件}
   - 任务数量：{N} 个
   - 审计评分：{score}/100（如果已运行 spec-audit-surface）

2. **询问**："Spec 已通过结构检查，是否可以进入实施？"

3. **等待明确确认**：只接受明确肯定信号。

4. **记录审批**：
   ```yaml
   approval_log:
     - checkpoint: spec_final
       result: approved | rejected
       artifacts_reviewed:
         - 00_index.md
         - 01_requirements.md
         - 02_design.md
         - 03_plan.md
         - 01_requirements_interaction.md  # 如存在
         - 02_design_interaction.md         # 如存在
         - 02_design_fe_be_contract.md      # UI + API 项目如存在
       summary: "{产出概要摘要}"
       timestamp: "{ISO 8601}"
   ```

## 最终报告

### Pass (通过)
如果所有文件存在且用户确认进入实施：
```
[SUCCESS - Quality Gate Passed]
🎉 Spec 生成圆满完成！

📍 产出位置: specs/20_evolution/active/{slug}/
✅ 核心文件: 完整 (00-03)
✅ 上下文归档: 完整 (input_facts.md)
✅ 用户审批: 已确认进入实施

您可以运行 `/spec-audit-surface` 进行深度输入审计，或直接开始开发。
```

### Fail (失败)
如果有文件缺失：
```
[WARNING - Incomplete Generation]
⚠️ 检测到部分文件丢失！

缺失项:
- {Missing File Name}

建议: 请检查 spec pipeline 的 crystallize 内部模块是否执行成功。
```
