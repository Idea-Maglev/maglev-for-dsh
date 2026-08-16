# Rules Extension — 自定义规则扩展指南

底层规则集在本 skill 目录下的 `scripts/rules.yaml`. 用户可加自定义规则集, 不必改动核心.

## 规则文件结构

```yaml
version: 1
description: 我的项目自定义规则集

rules:
  - id: <唯一 id>
    severity: hard | soft | info
    category: <人读分类名>
    description: <规则用途>
    pattern: <Python 正则>
    exclude_paths:           # 可选, 路径正则, 命中则跳过
      - '<project-internal-path>/'

default_exclude_paths:        # 可选, 全局排除
  - 'node_modules/'

default_extensions:           # 可选, 仅扫指定扩展名
  - '.md'
  - '.txt'
```

## 添加新规则的方法

1. 复制本 skill 的 `scripts/rules.yaml` 到自定义位置 (如 `~/.config/purity-rules.yaml`)
2. 修改或新增 `rules` 段
3. 调用时指定: `python3 <skill-path>/scripts/scanner.py --rules ~/.config/purity-rules.yaml <paths>`

## 何时加新规则

- 反复发现某种污染但默认规则未覆盖
- 项目特有的术语/编号需要识别 (如 `JIRA-XXX` / `TASK-NNN`)
- 团队约定的禁用词 (如某些产品代号)

## 规则编写技巧

- **从样本反推**: 先收集 5-10 条真实污染例子, 再写覆盖它们的最简正则
- **用 exclude_paths 而非过度复杂正则**: 路径排除比正则负向断言更易维护
- **severity 选择**:
  - hard: 出现就必修, 几乎不会有合理语境
  - soft: 大部分语境下要修, 但有协议引用等合法例外
  - info: 提示性, 作者一般会自觉处理

## 反模式

- ❌ 过宽正则导致大量假阳性 (作者会忽略全部 finding)
- ❌ 一条规则覆盖多类污染 (难以解读 finding)
- ❌ 规则集与代码耦合 (失去跨场景复用价值)

## 跨项目复用

规则集是**项目级别资产**. 推荐:

- 通用规则保留在 skill 自带的 `scripts/rules.yaml` (跟扫描器一起分发)
- 项目特有规则放 `<project>/.purity-rules.yaml`, 用户调用时 `--rules` 指定
- 团队规则放共享位置, 通过环境变量或配置加载
