---
name: content-sync
description: 内容写作前同步流程
---

# Content Sync Workflow

## Goal
在开始内容写作前，完成当前版本 Maglev 定义、边界与表达规则的同步。

## Process

### 1. Load Current Facts
- Read these canonical Reality sources first:
  - `specs/10_reality/positioning.md`
  - `specs/10_reality/glossary.md`
  - `specs/10_reality/reality-knowledge/operations/agent-context.md`
- Treat them as the only current fact sources for positioning, boundaries, terminology and runtime context.

### 2. Load Editorial Guides
- Read:
  - `docs/marketing/strategy/maglev_current_definition.md`
  - `docs/marketing/strategy/message_house.md`
  - `docs/marketing/strategy/audience_map.md`
  - `docs/marketing/strategy/content_style_guide.md`
  - `docs/marketing/registry/lifecycle.md`
  - `docs/marketing/registry/context_injection_protocol.md`
- Use these files for audience, tone, lifecycle and writing constraints only.

### 3. Load Task Sources
- Read the task `brief.md`.
- Read only the `source_of_truth` paths explicitly listed by the brief.
- Reject `docs/marketing/assets/`, `welcome.md`, `start_here.md` and generated publishing packages as current fact sources.

### 4. Synthesize
- Output a short `Content Sync Brief` including:
  - What Maglev is in the current version
  - What Maglev is not
  - What problem domain this writing should stay within
  - What drift risks to avoid

### 5. Ready
- End with:
  - `Definition synced. Ready for brief injection.`
