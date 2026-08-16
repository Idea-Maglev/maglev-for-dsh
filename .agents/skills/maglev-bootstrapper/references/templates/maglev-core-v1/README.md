# maglev-core-v1 Reality Profile

此模板为 Maglev 仓库创建固定的 Reality 知识库骨架。

初始化器必须复制 `00_profile.yaml`，再按其中的 domains、domain_entry_files 和 crosscutting_entry_files 创建所有路径。
初始化器不得自行增加能力域、槽位或 `INDEX.md` 内容；索引由 index-librarian 生成，额外事实页必须先登记到 Profile 的 `documents` 后写入。

对存量 Reality，先使用迁移清单映射已证实事实，再创建骨架并迁移；不能确认的事实保持 unknown，不把旧目录原样复制为新结构。
