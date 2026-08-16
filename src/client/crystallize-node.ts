// Maglev for DSH — 结晶卡片的 ConversationNodeDefinition
//
// 消费 host 产生的 maglev/crystallize 会话事件（单事件），折叠成一张会话内卡片。
// 参考 dsh adding-a-conversation-node.md 的 review-job 示例。

import type { ConversationNodeContext, ConversationNodeDefinition } from '@deepseek-ai/dsh-client-runtime/client'
// 触发 host index.ts 的 SessionEventMap merge（让 event.type 收窄包含 'maglev/crystallize'）
import type {} from '../../index.ts'

/** 结晶卡片展示数据（与 host 的 maglev/crystallize 事件数据一致）。 */
export interface CrystallizeCardData {
  title: string
  summary: string
  written: string
  target?: string
}

declare module '@deepseek-ai/dsh-client-ui-conversation/client' {
  interface ChatNodeDataMap {
    'maglev-crystallize': CrystallizeCardData
  }
}

declare module '@deepseek-ai/dsh-client-runtime/client' {
  interface ConversationStepDataMap {
    'maglev-crystallize': CrystallizeCardData
  }
}

function locationOf(context: ConversationNodeContext<CrystallizeCardData>) {
  return context.start?.location ?? context.matches[0]?.location ?? { kind: 'unresolved' as const }
}

export const crystallizeDefinition: ConversationNodeDefinition<CrystallizeCardData> = {
  kind: 'maglev-crystallize',
  target: 'chat',
  match: (event) => {
    if (event.type === 'maglev/crystallize') {
      return { id: String(event.seq), role: 'start' as const }
    }
    return null
  },
  start: (_context, match) => {
    const data = match.event.data
    return {
      title: data.title,
      summary: data.summary,
      written: data.written,
      ...(data.target !== undefined ? { target: data.target } : {}),
    }
  },
  update: (context) => context.state,
  publication: () => 'immediate' as const,
  buildViewNode: (context) => {
    if (context.state === undefined) return null
    return {
      key: context.key,
      kind: 'maglev-crystallize',
      id: context.id,
      target: 'chat',
      anchorSeq: context.start?.event.seq ?? context.matches[0]?.event.seq ?? 0,
      location: locationOf(context),
      visibility: 'visible' as const,
      data: context.state,
    }
  },
}
