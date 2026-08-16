# Step 6: Cross-Examination (交叉质询)

## 目标
对生成的 Spec 做对抗性审查，确保其与代码、测试和已知运行事实严格一致。

## 动作
1. 以“挑错优先”的视角重新审读 Spec。
2. 逐条核对 Spec 中的 Claims、Code Refs、Unknowns 和 Assumptions。
3. 输出 `Inconsistency Report`。
4. 根据审查结果修正 Spec，并保留不能消解的分歧。

## 审查清单

### 1. Hallucination Check
- Spec 声称的逻辑，代码里真的存在吗？
- 若 Spec 写了“发送了事件 / 更新了状态 / 做了鉴权”，但代码里没有对应实现，标记为 `[HALLUCINATION]`。

### 2. Omission Check
- 代码里是否处理了明显边界情况，但 Spec 没写？
- 典型遗漏包括：重试、回滚、降级、空值防御、异常分支、异步补偿。

### 3. Traceability Check
- 每一段关键逻辑后，是否都有可定位的文件引用？
- 引用是否真的指向支持该断言的代码位置？

### 4. Assumption Check
- Spec 中是否存在模糊表达，例如“应该”“可能就是”“大概”？
- 若有，必须要求降级为 `[INFERENCE]` 或 `[UNKNOWN]`。

### 5. Cross-Layer Consistency Check
- 前端、接口、后端、数据结构之间的字段与语义是否一致？
- 若存在契约漂移、同名异义、默认值不一致，标记为 `[MISMATCH]`。

## 输出格式

```markdown
## Inconsistency Report

### Critical Issues
- [HALLUCINATION] ...
- [OMISSION] ...

### Warnings
- [TRACEABILITY] ...
- [ASSUMPTION] ...
- [MISMATCH] ...

### Conclusion
- PASS / REJECT / PASS WITH DEVIATIONS
```

## 交互示例
AI: "我有异议。Spec 声称 `user_id` 为必填，但在 `UserController.java:45` 仍存在 `if (userId == null) return` 的防御逻辑。这说明当前实现至少允许空值进入 Controller，建议将该结论降级或补充边界说明。"

## 退出条件
所有 Inconsistency 都被解决，或被用户确认为 `Acceptable Deviation`。
