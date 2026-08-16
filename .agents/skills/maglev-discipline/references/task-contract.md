# Task Contract（任务契约）

> 本文件是 maglev-discipline 的核心参考资料之一。
> 定义 Task Contract 四元组、proposed/verified status 协议、Sub-agent 注入规范、`[MAGLEV-DIAGNOSIS]` 与 `[MAGLEV +1]` 语法。

---

## Task Contract 四元组

对每个有一定复杂度的任务，开始前先建立契约：

```yaml
task_contract:
  intent: |
    要解决的真实问题（不是"用户要什么"而是"为什么要"）
  acceptance: |
    可观察的验收信号（必须可跑命令验证，不接受主观描述）
  forbidden: |
    明确不该做 / 不该改的事（防止越界）
  verify_commands: |
    用什么命令 / 检查项验证交付
```

### 各字段说明

#### intent（意图）

- 必须回答"为什么要做这件事"，不只是"做什么"
- 好例子：`修复登录接口在并发场景下的 race condition，防止用户 token 被覆盖`
- 坏例子：`修复登录 bug`（太模糊，不知道验收标准）

#### acceptance（验收信号）

- 必须是**可观察的**：跑什么命令？看什么输出？
- 好例子：`pytest tests/auth/ 全绿 + 并发压测脚本 10 线程跑 100 次无 500`
- 坏例子：`登录正常工作`（不可观察）

#### forbidden（禁止事项）

- 明确列出不该碰的文件 / 不该做的改动
- 好例子：`不改 database schema（本次只修应用层逻辑）`
- 坏例子：（留空 = 没约束 = 后续争议源）

#### verify_commands（验证命令）

- 交付时必须跑完的命令集
- 好例子：`npm test && npm run lint && curl -X POST localhost:3000/login -d '...' | jq .token`
- 坏例子：`测试通过`（没给具体命令）

---

## proposed / verified Status 协议

### 状态流转

```
[task start]
    ↓
[AI 执行]
    ↓
agent_proposed_status: done  ← AI 自评（可以自信，但不是终态）
    ↓
[用户 / integrated-validator 验证]
    ↓
verified_status: pass | fail | partial  ← 人类 / 验证器给出（终态）
```

### 核心规则

1. **AI 只能写 `agent_proposed_status`**
   - AI 可以自信地标"done"，但这是"提议"不是"宣判"
   - 不允许 AI 宣布"任务完成"后不等验证就收工

2. **`verified_status` 由外部给出**
   - 来源：用户显式确认 / integrated-validator 自动验证 / CI 通过
   - AI 不能自己给自己 verified

3. **禁止 AI 自评通过最终交付**
   - "我验证过了" ≠ verified_status: pass
   - 自评是 proposed，别人确认才是 verified

### 例外

- 琐碎任务（如格式化、明确的 typo 修复）：用户可授权 AI 同时给 proposed + verified
- 但这需要**用户显式授权**，不是 AI 默认行为

---

## Sub-agent 注入规范

### 必须注入的场景

使用 `task` 工具 spawn 以下类型子 agent 时，**必须**在 prompt 末尾追加注入块：

- `explore` agent
- `general-purpose` agent
- `code-review` agent

### 注入模板

```text
---
开工前用 view 工具读取以下文件，按其中的行为协议执行：
- 核心红线: .agents/skills/maglev-discipline/SKILL.md
- 惰性识别: .agents/skills/maglev-discipline/references/laziness-patterns.md
---
```

### 不注入的后果

- 子 agent 是**空白上下文**，不注入 = 没红线、没纪律
- 交回的活质量不达标是**派活人的责任**
- 这是 owner 责任失职（对应 Owner 四问 §2"还有谁会被影响"）

### 不需要注入的场景

- `task` agent 用于纯命令执行（如 `npm test`）— 无需纪律，只需结果
- 明确的信息查询（如 "grep X in Y"）— 无判断空间，不需要红线

---

## `[MAGLEV-DIAGNOSIS]` 语法

### 格式

```text
[MAGLEV-DIAGNOSIS] 问题是 ___；证据是 ___；下一步动作是 ___。
```

### 使用时机

- 改代码前
- 改配置前
- 改状态文件前
- 每个主流程 step 起始时
- AI 识别到自身可能犯惰性时

### 三要素规则

| 要素 | 要求 |
|------|------|
| 问题 | 具体到文件 / 模块 / 行号 / 接口 |
| 证据 | 标注来源：错误原文 / 源码行 / 复现实验 / 官方文档 / 历史先例 |
| 下一步 | 必须指向诊断的位置；不处理必须说明为什么 |

### 反例

```text
# BAD — 诊断和行为脱节
[MAGLEV-DIAGNOSIS] 问题是配置解析失败；证据是日志报错；下一步研究一下。
                                                          ↑ "研究一下"不是动作

# GOOD
[MAGLEV-DIAGNOSIS] 问题是 config.yaml 第 12 行 indent 错误导致解析失败；
证据是 python -c "import yaml; yaml.safe_load(open('config.yaml'))" 报
"mapping values are not allowed here, line 12"；
下一步修复第 12 行缩进并重跑验证。
```

---

## `[MAGLEV +1]` 语法

### 格式

```text
[MAGLEV +1] {一句话说明做了什么额外有价值的工作}
```

### 合法标记（真正有价值的额外工作）

- `[MAGLEV +1]` 主动加了 SQL 注入防护 — 安全红线不能碰
- `[MAGLEV +1]` 发现上游接口也有同样 bug，一起修了 — 冰山法则
- `[MAGLEV +1]` 跑完后额外 curl 了全部端点确认无回归 — 闭环验证加强
- `[MAGLEV +1]` 补了一个边界测试用例，防止未来同类回归 — 防止再发

### 非法标记（不允许）

- ❌ `[MAGLEV +1]` 写了代码 — 本职工作
- ❌ `[MAGLEV +1]` 读了文件 — 默认义务
- ❌ `[MAGLEV +1]` 思考了方案 — 默认义务
- ❌ `[MAGLEV +1]` 遵守了红线 — 底线不是超额

### 本质

`[MAGLEV +1]` 区分的是"本职工作"和"真正的 owner 意识"。不是给 AI 邀功的工具。
