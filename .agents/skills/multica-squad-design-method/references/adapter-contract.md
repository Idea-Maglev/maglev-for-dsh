# Adapter Contract

Adapter Contract 是通用小队方法与具体平台之间的承诺边界。没有 Adapter Contract 时，小队最多只能声明到 L1。

## 必填项

```yaml
adapter_contract:
  adapter_name:
  target_platform:
  file_surface:
    template_root:
    role_files:
    skill_or_prompt_files:
    user_guide:
  command_surface:
    validate:
      - ...
    test:
      - ...
    sync_or_apply:
      - ...
  identity_surface:
    managed_marker:
    lock_or_remote_id:
    display_name_policy:
  permission_surface:
    read_roles:
      - ...
    write_roles:
      - ...
    approval_roles:
      - ...
  write_gate:
    required_evidence:
      - baseline
      - allowed_scope
      - owner_approval
      - before_after_snapshot
  validation_surface:
    static_validation:
      - ...
    runtime_proof:
      - ...
```

## 规则

- Adapter 必须说明对象归属判断是否依赖展示名；如果不依赖，必须写出真实身份锚点。
- Adapter 必须说明写入外部状态前的批准和证据。
- Adapter 必须说明哪些验证只能证明 L2，哪些验证才能证明 L3。
- Adapter 不能把平台特有概念写回通用方法，除非抽象成可替换字段。
