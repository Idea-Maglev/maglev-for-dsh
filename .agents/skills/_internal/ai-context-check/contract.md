# AI Context Check Contract

## 目标

统一 `AGENTS.md` 与 `llms.txt` 的最小检查口径，避免不同技能各自给出不一致判断。

这份契约不负责自动重写文件。
它只负责判断：

1. 文件是否存在
2. 内容是否达到最小可用标准
3. 内容是否已经和当前 Maglev 结构漂移
4. 应该给出哪些最小补齐建议

## 检查对象

1. `AGENTS.md`
2. `llms.txt`

## 当前 Maglev 最小对齐事实

检查时应以当前运行面事实为准：

<!-- maglev:managed:mainline -->
当前主链路（由治理注册表生成）：

- `entry-router`
- `reality-sync`
- `requirement-convergence`
- `spec-designer`
- 执行分支：`context-implementer` | `code-execution-slot`
- `integrated-validator`
- `crystallization`
- 横切能力：`knowledge-check`
<!-- /maglev:managed:mainline -->

<!-- maglev:managed:compatibility -->
兼容 workflow 入口（由治理注册表生成）：

- `/standup` → `reality-sync`
- `/create-spec` → `spec-designer`
- `/quick-dev` → `context-implementer`
- `/validate-all` → `integrated-validator`
<!-- /maglev:managed:compatibility -->

补充说明：`workflow filename / slash entry` 与 `skill runtime name` 允许不同层命名，不应混为一谈。

## 统一检查维度

### 1. 存在性

1. `AGENTS.md` 是否存在
2. `llms.txt` 是否存在

输出状态：

- `present`
- `missing`

### 2. 充分性

至少判断是否覆盖下面这些最小信息：

1. 项目目标、关键目录或主要任务入口
2. AI 在当前项目中的基本行为约束
3. Maglev 主流程或关键操作入口
4. 当前项目是否已经接入 Maglev 的基本事实

输出状态：

- `sufficient`
- `insufficient`

### 3. 对齐 / 漂移

至少检查：

1. 是否仍把旧主流程 runtime name 当现役真名
2. 是否缺少对兼容 workflow 入口的说明
3. 是否混淆 workflow 入口名与 skill runtime name
4. 是否还在引用已失效的结构事实
5. 是否缺少会话纪律（maglev-discipline）引用

输出状态：

- `aligned`
- `drifted`

### 4. 上游私有污染

至少检查是否混入明显只属于上游 Maglev 源仓库、而不属于用户项目的内容，例如：

1. 把上游仓库的当前 active 主题、issues 或路径事实当成当前项目事实
2. 直接照搬只适用于上游仓库的仓库说明
3. 指向当前用户项目不存在的私有技能或目录现实

输出状态：

- `clean`
- `contaminated`

## Bootstrapper 口径

`maglev-bootstrapper` 关注 `readiness`：

1. 新项目初始化后，这两个文件是否已经存在
2. 如果不存在或不足，AI 是否还能给出明确补齐建议
3. 检查结果应帮助用户把项目带到“最小可用 AI 上下文”状态

## Updater 口径

`maglev-updater` 关注 `drift`：

1. 现有项目的这两个文件是否仍与当前 Maglev 结构一致
2. 是否仍停留在旧 skill runtime name
3. 是否遗漏对兼容 workflow 入口和 update 机制的说明

## 统一输出结构

输出时优先保持下面四段：

1. `存在性`
2. `充分性`
3. `漂移风险`
4. `最小补齐建议`

## 首轮边界

首轮不要求：

1. 自动 merge
2. 自动重写
3. release / manifest / installer 直接下发这两个文件

## 最小草稿参考

当检查结果需要给出补齐建议时，可优先引导用户参考：

1. `templates/AGENTS.minimal.md`
2. `templates/llms.minimal.txt`

这些模板只提供最小结构，不代表应原样复制上游项目私有内容。
