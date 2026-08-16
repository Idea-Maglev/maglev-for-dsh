---
description: maglev-reverse-spec Step 8 - Verify Output
---

# Step 8: Verify Output (产出验证)

## 目标
作为 Quality Gate，验证 reality 产物是否达到 **reality 产物标准**（不只是检查文件存在），且可追溯、可交接、未越界。

## 验证逻辑

### 1. 产物标准验证（对齐共享标准）

逆向产出与结晶产出遵循**同一 reality 产物标准**。标准定义见：
`.agents/skills/crystallization/references/reality-artifact-standard.md`

运行可执行验证：

```bash
maglev-python crystallization_check.py <reality_dir>
```

或：

```bash
python3 .agents/skills/crystallization/references/scripts/crystallization_check.py <reality_dir>
```

**通过标准**：`fail=0`

检查项（详见产物标准文档）：
- `placeholder_free`：正文无 TODO/TBD/待补充占位符
- `mermaid_fence_balanced`：mermaid 围栏配对
- `internal_links_reachable`：内部链接可达
- `min_density`：最小内容密度
- `module_readme_nonempty`：多模块时每个 README 非空

> 若 fail>0，先修复产物再交接，不得以"文件已生成"代替质量达标。

### 2. 输出目标确认
- Maglev 仓库: Profile 映射确定的能力域与槽位路径
- 非 Maglev 仓库: 使用用户或项目约定的等价路径

### 3. 逆向特有验证（保留）

以下为逆向独有、产物标准未覆盖的验证维度：

- [ ] 关键断言有文件引用（证据链可追溯）
- [ ] 推断被标注为 Fact / Inference / Unknown（分层标记）
- [ ] 未知项进入 Quest / Expert Queue
- [ ] 深度增强场景：`03_rmm_scorecard.md`、`99_expert_review_queue.md` 存在
- [ ] 越界行为检查：
  - [ ] 未直接修改业务代码
  - [ ] 未新增回填/修复/迁移类脚本作为"顺手修复"
  - [ ] 未执行数据修复、契约修复等改变现状的动作
  - [ ] 修复建议已与 reality 产物明确分离

## 最终报告

### Pass (通过)
```
[SUCCESS - Quality Gate Passed]
🎉 reality 校验圆满完成！

📍 产出位置: Profile 映射确定的能力域与槽位路径
✅ 产物标准: crystallization_check.py fail=0
✅ 证据链: 可追溯
✅ 分层标记: Fact/Inference/Unknown 已标注
✅ 未知项: 已登记
✅ 执行边界: 未越界到业务修复

您可以随时开始下一个功能逆向。
```

### Fail (失败)
```
[WARNING - Quality Gate Failed]
⚠️ 检测到 reality 产物未达标！

产物标准问题（crystallization_check.py）:
- {check_name}: {detail}

逆向特有问题:
- {Missing Evidence / Unmarked Inference / Mutation Leak}

建议: 先修复产物质量再交接，不要以"文件已生成"代替质量达标。
```
