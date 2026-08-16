# Step 2: Bootstrap (基础设施注入)

## 目标
补全 Maglev 运行所需的最小环境。

## 逻辑
1.  **If .maglev missing**:
    - 提示用户: "检测到缺少 Maglev 核心配置。建议运行 `maglev-bootstrapper` 或手动复制 Starter Kit。"
    - *Auto-Fix*: 如果用户同意，且你具备 `maglev-bootstrapper` 能力，尝试调用它。否则，提供复制指令。
2.  **If specs/ missing**:
    - 创建 `specs/00_planning`, `specs/10_reality`, `specs/20_evolution`, `specs/90_archive`。
3.  **If issues/ missing**:
    - 创建 `issues/active`, `issues/closed`。
