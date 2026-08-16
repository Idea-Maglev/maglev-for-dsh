# Index Protocol

内部的通用 track 索引协议。它按 `registry.yaml` 的 `tracks` 声明为目录树、仓库入口和代码树生成可定位的索引产物。

## 契约

- `registry.yaml` 是项目实例配置；第一阶段当前实现由 `maglev init` 生成，后续由项目自己维护，`maglev update` 不静默覆写。
- `dir-tree` 生成相邻 `INDEX.md` 网络和 summary YAML。
- `repo-entry` 生成入口锚点和人读地图；`map_output` 可显式指定地图路径，未指定时由 `output` 派生为 `<output-stem>-map.md`。
- `code-tree` 生成代码锚点；可选 `radar_summary` 失败时降级，不阻断索引。
- `.maglev/config.json` 的 `indexing` 是项目级目录忽略策略；track `ignore` 仅补充该 track 的规则。
- `enabled` 默认为 `true`。禁用的 track 不接受单 track 调用，也不会被 `--all` 处理。
- 所有索引产物由 `track_scan.py` / `track_map.py` 独占写入，AI 不得手工编辑；共享目录中的多个 track 必须使用不同的 `map_output`。

## 入口

```bash
PROTOCOL=".agents/skills/index-librarian/protocol"

./scripts/maglev-python "$PROTOCOL/scripts/track_scan.py" --track-id <id>
./scripts/maglev-python "$PROTOCOL/scripts/track_verify.py" --track-id <id>
./scripts/maglev-python "$PROTOCOL/scripts/track_map.py" --track-id <id>

./scripts/maglev-python "$PROTOCOL/scripts/track_scan.py" --all
./scripts/maglev-python "$PROTOCOL/scripts/track_verify.py" --all
./scripts/maglev-python "$PROTOCOL/scripts/track_map.py" --all
```

运行顺序是 scan → verify → map（按需）。`task_navigate.py` 只负责返回来源选择收据，不能代替 scan 或 verify。

## 参考

- `index-schema.md`：`dir-tree` 的 `INDEX.md` 与知识记录规则。
- `registry.example.{dir-tree,repo-entry,code-tree}.yaml`：新增 track 模板。
- `../references/track-extension.md`：在项目中追加 track 的操作说明。
