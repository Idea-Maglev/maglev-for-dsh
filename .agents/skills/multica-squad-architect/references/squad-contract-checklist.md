# Maglev Squad Adapter Checklist

本清单用于 Maglev Adapter 落地。通用协同设计先由 `multica-squad-design-method` 负责，本清单只检查 Maglev Squad Kit、治理资产、测试和 Workspace 同步边界。

## Intent

- [ ] 小队名称让技术和非技术读者都能理解。
- [ ] In Scope / Out of Scope 明确。
- [ ] 明确是否支持未初始化仓库。
- [ ] 明确不是完整交付小队时，不承担业务实现、bug 修复或重构。
- [ ] 已引用或整理通用小队设计包。
- [ ] 已声明目标 `squad_quality`。

## Topology

- [ ] 存在唯一默认 Coordinator。
- [ ] Coordinator 不承担成员角色的主体结论。
- [ ] 每个成员有 `member_role_description`。
- [ ] 每个成员有准入、输入、执行、输出、阻塞与禁止事项。
- [ ] 审计角色不审计自己主持的流程。

## Collaboration

- [ ] 使用精确 mention markdown。
- [ ] 明确必须新建评论触发。
- [ ] 禁止裸 `@name`。
- [ ] 成员默认交回 Coordinator。
- [ ] 禁止横向委派。
- [ ] 有一次性只读并行审查例外条件。
- [ ] 有标准 Handoff。
- [ ] 有自动接力失败排查顺序。

## Write Gate

- [ ] 写入任务要求 Work Graph。
- [ ] 写入任务要求 lease。
- [ ] 写入任务要求基线提交。
- [ ] 写入任务要求允许文件范围。
- [ ] 写入任务要求项目负责人批准。
- [ ] 写入后要求 Git 前后快照。

## Template Assets

- [ ] `manifest.yaml` 角色集合完整。
- [ ] `squad.json` 写小队级协议。
- [ ] Agent JSON 与 manifest 角色一致。
- [ ] Bridge Skill 明确 entry-router 双路径。
- [ ] `说明.md` 面向使用者，不混入维护者过程叙事。
- [ ] catalog 注册模板。
- [ ] README / 配置指南说明选择条件和升级 drift。

## Validation

- [ ] 模板 validate 通过。
- [ ] `maglev-complete` 回归 validate 通过。
- [ ] 单测覆盖模板可发现、可实例化和协议关键句。
- [ ] `git diff --check` 通过。
- [ ] 对外文档洁净度扫描通过。
- [ ] 如存在远端 dev config，`plan` 输出已解释。
- [ ] 未完成真实 Workspace 接力验证时，`allowed_claim` 不包含 `runtime_verified`。
