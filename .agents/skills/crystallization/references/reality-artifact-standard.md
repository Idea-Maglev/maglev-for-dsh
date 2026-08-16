---
name: reality-artifact-standard
description: reality（10_reality）产物标准 —— 定义写回 reality 的结构要求与质量门槛，由 crystallization_check.py 可执行地表达。crystallization 与 maglev-reverse-spec 共同遵循。
---

# Reality 产物标准

> 本文档定义写回 `specs/10_reality/` 的**产物标准**（结果长什么样、达到什么质量）。
>
> 它是**结果契约**，不是生产流程。不同技能可用不同流程生产 reality：
> - crystallization：演绎（已完成主题 → 四步推导）
> - maglev-reverse-spec：归纳（存量代码 → 证据驱动切分）
>
> 但两者产出都必须满足本标准。

## 为什么需要显式标准

此前产物标准隐性地藏在 `crystallization_check.py` 的检查逻辑里，只有结晶消费。逆向的产物验证停留在"文件存在检查"，无法保证质量对齐。显式化后，任何写回 reality 的技能都有同一份可引用、可执行的契约。

## 结构要求

reality 不规定固定 schema，结构由主题决定（单一主题就地更新；多模块产出每模块一个目录）。但须满足：

- **有索引**：目录含 `INDEX.md` 或 `README.md` 作为导航入口
- **模块 README 非空**：多模块结构下，每个模块目录的 `README.md` 至少 3 行有效内容
- **结构自适应**：不存在的维度不产生结构，读者不需要的细节不写

## 质量门槛

以下门槛由 `crystallization_check.py` 可执行地检查。

### 通用检查（始终运行）

| 检查项 | 要求 | 说明 |
|--------|------|------|
| `placeholder_free` | 无占位符 | 正文（代码块外）不得含 TODO/TBD/FIXME/待补充/裸 `...` |
| `mermaid_fence_balanced` | mermaid 围栏配对 | ` ```mermaid ` 必须正确闭合 |
| `internal_links_reachable` | 内部链接可达 | 相对路径 markdown 链接指向存在的文件 |
| `min_density` | 最小密度 | 每个 `.md` 至少 5 行有效内容（低于报 WARN） |

### 结构信号检查（条件触发）

| 检查项 | 触发条件 | 要求 |
|--------|----------|------|
| `module_readme_nonempty` | 检测到多模块（≥2 个含 README 的同级目录） | 每个模块 README ≥3 行有效内容 |
| `arch_doc_nonempty` | 子目录含 architecture.md/overview.md | 该文件 ≥3 行有效内容 |
| `rtag_format_valid` | 检测到 R-标记文本 | R-标记格式 `R-XXX-XXX-N` 合法 |
| `cross_module_rtag_reachable` | 多模块 + 有 R-标记引用 | 被引用的 R-标记有定义 |

> **分层标记说明**：R-标记检查仅在产物含 R-标记时触发。这是 crystallization 的分层机制（标记引用来源）。maglev-reverse-spec 使用 Fact/Inference/Unknown 分层（标记可信度），不产生 R-标记，故 R-标记检查对逆向产物不触发。分层标记是各技能的生产特性差异，不属于统一的产物标准。

## 验证方式

```bash
maglev-python crystallization_check.py <reality_dir>
```

或在有 python 运行时的环境：

```bash
python3 .agents/skills/crystallization/references/scripts/crystallization_check.py <reality_dir>
```

**通过标准**：`fail=0`（WARN 不阻断，但应尽量消除）。

输出示例：

```
summary: pass=88 warn=0 fail=0 modules_detected=6
```

## 消费者

| 技能 | 生产流程 | 引用本标准的位置 |
|------|----------|------------------|
| crystallization | 演绎四步推导 | step-02-judge-writeback |
| maglev-reverse-spec | 证据驱动切分 | step-06-verify-output |

新增写回 reality 的技能，也应引用本标准并运行验证脚本。