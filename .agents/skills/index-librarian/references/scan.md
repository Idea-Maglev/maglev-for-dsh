---
name: step-scan
description: 索引管家扫描步骤，调用 generic track_scan.py 生成或刷新索引产物
next_step: references/verify.md
---

# Step: Scan

扫描是唯一的索引产物写入步骤。使用 registry 中的 `tracks`，不要手工编辑 `INDEX.md`、summary YAML 或地图文件。

```bash
PROTOCOL=".agents/skills/index-librarian/protocol"
./scripts/maglev-python "$PROTOCOL/scripts/track_scan.py" --track-id <id>
# 或扫描全部已启用 track
./scripts/maglev-python "$PROTOCOL/scripts/track_scan.py" --all
```

- exit `0`：产物已写入或 track 根不存在而被跳过。
- exit `1`：部分产物写入；报告输出中的失败原因。
- exit `2`：registry 或运行环境错误；先修复该错误，不要继续 verify。

scan 成功后必须进入同一范围的 verify。扫描本身不证明 INDEX 内容仍与目录同步。
