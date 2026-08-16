---
name: artifact-purity-keeper
description: 产物洁净度守护器。在 AI 协作产出对外文件时识别会话痕迹（迭代叙事、过程编号、时间相对词、协作叙事等），并按受众判断给出选择性修复建议。
metadata:
  formal_action_name: 产物洁净度守护
  top_level_capability: 产物洁净度守护
  system_layer: Quality Layer
  lifecycle_chain: auxiliary
  runtime_name_status: canonical_name_active
  distribution_scope: user_visible
  author: feiyu.gao
  last_updated: "2026-04-29"
  version: "1.0.0"
---

# Artifact Purity Keeper (产物洁净度守护器)

## 概览

AI 在协作中产出的"对外产物"（SKILL.md / README / reality 文档 / dist 文档 / 邮件 / PR description / 演讲稿等）天然会携带会话痕迹：迭代叙事、过程编号、时间相对词、协作经验。这些痕迹在产物离开会话被消费时，会造成幻觉、误导、上下文丢失甚至隐私泄露。

本 skill 提供两件事：

1. 一套 **受众分级 + 痕迹识别** 的判断规则（认知层）
2. 调用本 skill 目录下的 `scripts/scanner.py` 完成机械扫描 + 选择性修复（工具层）

它负责：
- 判断目标文件的受众层级（session / handoff / external）
- 跑扫描器识别 7 类疑似污染
- 区分"协议命名引用"与"真污染"
- 给出按 severity 分级的修复建议

它不负责：
- 自动改写产物（决定权留给作者）
- 替代作者对产物表达力的判断
- 维护规则集本身（规则演进由用户主导）

## 调用接口（被动响应）

本 skill 不自我声明触发时机——任何上游流程在产出对外文件前后，主动调用本 skill 即可。
典型入口：
- 产出对外文件之前（推荐）：在写入用户面文件前主动跑一次
- 产出对外文件之后（兜底）：MR / push 前作为最后一道扫描
- 用户主动："扫一下产物洁净度" / "看看这个文件有没有会话痕迹"
- 周期性扫整片对外文档面看趋势

## 受众分级

| 标签 | 容忍度 | 典型语义 |
|---|---|---|
| `artifact-session` | 全部会话符号 OK | 会话内部草稿、临时笔记、当前对话双方即时消费的产物 |
| `artifact-handoff` | 仅工程符号 OK（spec 内部编号可保留） | 同项目工程师消费的内部设计/协作件, 读者知晓项目协议但不在产生现场 |
| `artifact-external` | **零会话符号** | 跨项目/跨组织/对外发布的产物（SKILL.md、用户面 README、对外文档、邮件、博客、PR description 等） |

**纪律**：跑扫描前必须先问自己"这个文件是哪个层级"，不同层级对 finding 的处置完全不同。

## 前置条件（调用方责任）

本 skill 不内置"路径→层级"的映射表。调用方在调用本 skill 之前必须自行决定:

1. **目标文件的受众层级**（external / handoff / session）— 判断依据可以是项目的目录约定、文件命名约定、调用方上下文等, 由项目语境决定。
2. **使用的 severity 档位** — 按已确定的层级选择: external→`info`、handoff→`hard`、session→不扫。

skill 持有的是"层级的本质特征 + 容忍度 + 痕迹识别能力"; "本项目里某个具体路径属于哪个层级"完全是项目责任。

## 判定纪律

- 先判断受众层级，再决定 finding 处置策略
- 协议命名引用（如稳定能力名 / 公开协议条款 / 公开接口名）≠ 污染
- spec 内部编号（如 `AC-X-N` / 内部决策编号）泄漏到 `external` 面 = 真污染，必须剥离
- soft finding 留判断给作者，hard finding 必须处理
- 工具是辅助识别，不是门禁；但 `external` 面有 hard finding 应阻止合并

## 必需的参考资料

- 工作流: `references/purity.workflow.md`
- `references/audience-rules.md`
- `references/finding-interpretation.md`
- `references/rules-extension.md`

## 依赖与集成

- **底层工具**: 本 skill 目录下的 `scripts/scanner.py` + `scripts/rules.yaml`（与 skill 同包分发，独立可携带，不依赖任何 runtime / 框架）
- **被调方**：本 skill 不主动声明上游，由调用方按需引用

## 快速使用

```bash
SCANNER=.agents/skills/artifact-purity-keeper/scripts/scanner.py

# 扫单文件 (调用方已判定该文件为 external, 用 info 档位全报)
python3 $SCANNER path/to/external/file.md

# 扫整个对外文档面 (handoff 档位仅报 hard)
python3 $SCANNER --severity hard path/to/handoff/dir/

# 交互修复
python3 $SCANNER --fix-interactive path/to/file.md

# JSON 输出供 CI 消费
python3 $SCANNER --format json path/to/external/dir/ > findings.json

# 通过 --exclude 追加项目特定的排除路径 (不污染默认规则集)
python3 $SCANNER --exclude 'project/legacy/' path/to/scan/
```

## 示例

User: "我刚写完 SKILL.md，扫一下有没有会话痕迹"

AI: "好，先识别这是 `artifact-external` 层级（用户面），按零会话符号纪律处理。跑扫描器后会按 hard / soft / info 分级报告，hard 必修，soft 由你判断是否协议引用，info 仅提示。"
