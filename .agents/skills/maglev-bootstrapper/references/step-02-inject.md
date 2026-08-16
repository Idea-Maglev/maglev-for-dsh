---
name: step-02-inject
description: 骨架注入
next_step: references/step-03-config.md
---

# Step 2: Structure Injection (骨架注入)

## 目标
物理创建 Maglev 标准目录结构。

## 动作
1.  **Inject Core**:
    *   Copy `.agents/` -> Root.
    *   Copy `.maglev/` -> Root.
    *   Create `specs/`, `docs/`, `issues/`, `tests/`.
2.  **Handle Mode**:
    *   **Greenfield**: Create `code_storages/` directory.
    *   **Adoption**:
        *   Ask user: "Should I move existing `src` to `code_storages/` (Recommended) or keep it in Root (Legacy Mode)?"
        *   If Legacy Mode, note this for config step.

## 关键指令
- 使用 `mkdir -p` 创建目录。
- 确保不要覆盖用户已有的重要文件 (如 `.gitignore`)。

## AI 引导摘要生成

注册新仓库后，自动生成 AI 引导摘要：

1. **扫描项目文件生成摘要**：
   - 产品上下文: README.md 前 3 段 + package.json description
   - 技术约定: package.json dependencies + tsconfig + .eslintrc + Makefile
   - 代码结构: src/ 或 lib/ 目录（2 层深度）

2. **展示给用户确认**（不直接写入）

3. **用户确认后**追加到 `crosscutting/repository-map/repositories.md` 的 AI 引导摘要区

摘要写入 `specs/10_reality/crosscutting/repository-map/repositories.md`。每个仓库摘要控制在 20 行以内。

## 交互示例
AI: "Injecting Maglev core structures..."
AI: "Done. `specs/`, `.agents/` created."
