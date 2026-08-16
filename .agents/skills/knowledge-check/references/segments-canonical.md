# 思考位段 Canonical — 方法论说明

`segments-canonical.yaml` 的人读伴生文档。本文件解释 9 段记忆宫殿的设计意图、互斥关系与实战决策树，供 `knowledge-check` 在判断"某条思考归到哪个位段"时使用。

## 设计意图

思考分类不是装饰，是**让知识可被发现**的协议。9 段位段名（"00_meta / 10_critique / ..."）按以下三维设计：

1. **抽象高度**：30_philosophy（最高，不可证伪）→ 20_architecture（中，可证伪的结构选择）→ 60_case（最低，单点案例）
2. **来源方向**：00_meta（向内，自洽元理论）/ 40_paper（向外，学术）/ 50_alignment（横向，同辈对比）/ 10_critique（反向，对抗）
3. **时间形态**：70_retrospective（事后回看）/ 90_archive（已退役）/ 其他（当前在用）

编号轨（`00_/10_/20_/.../90_`）而非时间轨的原因：时间轨会被新增条目稀释，编号轨提供稳定位段语义；编号间的 10 步留白允许未来插入新位段不破坏既有顺序。

## 实战决策树

写一篇新 thinking 文档时，按下序判定位段：

```
Step 1: 这是元理论 / 方法论本体吗？
  ├── 是 → 00_meta
  └── 否 → Step 2

Step 2: 这是不可证伪的范式宣言或第一性原理吗？
  ├── 是 → 30_philosophy
  └── 否 → Step 3

Step 3: 这是引用/转译外部学术理论吗？
  ├── 是 → 40_paper
  └── 否 → Step 4

Step 4: 这是单次迭代的复盘 / 决策回顾 / 反模式提炼吗？
  ├── 是 → 70_retrospective
  └── 否 → Step 5

Step 5: 这是对自身方案/外部范式的批判性挑战吗？
  ├── 是 → 10_critique
  └── 否 → Step 6

Step 6: 这是中立的跨范式对比 / 生态对位吗？
  ├── 是 → 50_alignment
  └── 否 → Step 7

Step 7: 这是某个具体项目/场景的落地案例吗？
  ├── 是 → 60_case
  └── 否 → Step 8

Step 8: 这是系统结构 / 分层 / 边界设计吗？
  ├── 是 → 20_architecture
  └── 否 → 模糊地带 → 默认 20_architecture（结构面），或与作者沟通是否需要新位段
```

## 互斥关系（容易混淆的成对辨析）

| 易混对 | 辨析 |
|---|---|
| `10_critique` vs `70_retrospective` | critique 是**系统性挑战**（蓝军、对抗方案）；retrospective 是**单次闭环回顾**（一次发布、一次决策） |
| `30_philosophy` vs `00_meta` | philosophy 是**第一性原理**（不可证伪根基）；meta 是**方法论本体**（可演化的思考体系自身规则） |
| `30_philosophy` vs `20_architecture` | philosophy 不可证伪；architecture 可证伪（可被替代方案挑战） |
| `40_paper` vs `50_alignment` | paper 引用**学术理论**；alignment 对比**工业产品/同辈范式** |
| `10_critique` vs `50_alignment` | critique 持**对抗立场**；alignment 持**中立比较**立场 |
| `60_case` vs `70_retrospective` | case 是**单一场景的落地实例**；retrospective 是**对实例的回看与提炼** |

## 与项目实例的关系

本 canonical 是"方法论权威源"。具体项目实例（如 `docs/thinking/INDEX.md` 的 `segments:` 字段）应：

- 以本文件为内容来源；
- 在自身文件头标注 `segments_source: .agents/skills/knowledge-check/references/segments-canonical.yaml`；
- 项目可在不冲突前提下扩展自有位段（如 `80_<custom>`），但不应修改本 canonical 已定义的 9 段语义。

## 与其他 skill 的边界

- 本 canonical 由 `knowledge-check` 持有，因为"位段判定"是知识沉淀检查的核心动作。
- `index-librarian` 是基础设施层，**不**消费本 canonical。它只规约 `segments` 字段必须有 `id / room_name / description / status` 的格式，不关心具体内容。
- 同步 INDEX.md 实例与 canonical 的工作由项目自行负责（人工 / 项目级 sync 脚本），不由任一 skill 单方承担。

## 状态语义

- `active`：位段在用，新文档可入
- `draft`：位段在试运行，未稳定
- `archived`：位段不再接受新文档，仅保留历史
