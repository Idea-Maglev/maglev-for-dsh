---
name: step-verify
description: 索引管家验证步骤，调用 generic track_verify.py 校验索引产物
next_step: null
---

# Step: Verify

验证确认 scan 产物存在、frontmatter 可解析、知识记录与直接子项一致。它不替代人工对摘要语义的判断。

```bash
PROTOCOL=".agents/skills/index-librarian/protocol"
./scripts/maglev-python "$PROTOCOL/scripts/track_verify.py" --track-id <id>
# 或验证全部已启用 track
./scripts/maglev-python "$PROTOCOL/scripts/track_verify.py" --all
```

- exit `0`：该范围通过验证。
- exit `1`：存在索引不一致；先重新运行对应的 scan。若仍失败，检查目录内容、registry 配置或生成器。
- exit `2`：脚本或运行环境错误；展示错误原文并停止。

需要人读地图时，只能在 scan + verify 通过后调用 `track_map.py`。需要任务上下文时，使用 `task_navigate.py`，其 receipt 不能代替 verify 结果。
