// Maglev for DSH — client 插件入口（浏览器 half）
//
// 注册 Maglev 的 GUI：
// - 结晶卡片（maglev/crystallize 事件 → 会话节点）
// - 真相卡片（maglev/reality-status 事件 → 会话节点）
// - Maglev 面板（shell.overlay 浮动面板，知识分层 + 迭代看板）

import type { ClientContext } from '@deepseek-ai/dsh-client-runtime/client'
import { crystallizeDefinition } from './crystallize-node.ts'
import { CrystallizeCard } from './CrystallizeCard.tsx'
import { realityStatusDefinition } from './reality-status-node.ts'
import { RealityStatusCard } from './RealityStatusCard.tsx'
import { MaglevPanel } from './MaglevPanel.tsx'

export const inject: readonly string[] = ['conversationEvents', 'slots']

export function apply(ctx: ClientContext): void {
  ctx.conversationEvents.register(crystallizeDefinition)
  ctx.conversationEvents.register(realityStatusDefinition)
  ctx.slots.inject('conversation.chat.node', () => ctx.slots.register({
    name: 'conversation.chat.node',
    key: 'maglev-crystallize',
  }, CrystallizeCard))
  ctx.slots.inject('conversation.chat.node', () => ctx.slots.register({
    name: 'conversation.chat.node',
    key: 'maglev-reality-status',
  }, RealityStatusCard))
  ctx.slots.inject('shell.overlay', () => ctx.slots.register({
    name: 'shell.overlay',
    id: 'maglev-panel',
  }, MaglevPanel))
}
