// Maglev for DSH — 真相卡片的 ConversationNodeDefinition
//
// 消费 maglev/reality-status 事件（maglev_reality_status 工具读真相时产生），
// 把"项目现状结构"渲染成会话内卡片——让"AI 看到的真相"对人可见（融合点 4）。

import type { ConversationNodeContext, ConversationNodeDefinition } from '@deepseek-ai/dsh-client-runtime/client'
import type {} from '../../index.ts'

export interface RealityStatusCardData {
  domains: string[]
  activeTopics: string[]
  hasVision: boolean
  hasProfile: boolean
}

declare module '@deepseek-ai/dsh-client-ui-conversation/client' {
  interface ChatNodeDataMap {
    'maglev-reality-status': RealityStatusCardData
  }
}

declare module '@deepseek-ai/dsh-client-runtime/client' {
  interface ConversationStepDataMap {
    'maglev-reality-status': RealityStatusCardData
  }
}

function locationOf(context: ConversationNodeContext<RealityStatusCardData>) {
  return context.start?.location ?? context.matches[0]?.location ?? { kind: 'unresolved' as const }
}

export const realityStatusDefinition: ConversationNodeDefinition<RealityStatusCardData> = {
  kind: 'maglev-reality-status',
  target: 'chat',
  match: (event) => {
    if (event.type === 'maglev/reality-status') {
      return { id: String(event.seq), role: 'start' as const }
    }
    return null
  },
  start: (_context, match) => {
    const data = match.event.data
    return {
      domains: data.domains,
      activeTopics: data.activeTopics,
      hasVision: data.hasVision,
      hasProfile: data.hasProfile,
    }
  },
  update: (context) => context.state,
  publication: () => 'immediate' as const,
  buildViewNode: (context) => {
    if (context.state === undefined) return null
    return {
      key: context.key,
      kind: 'maglev-reality-status',
      id: context.id,
      target: 'chat',
      anchorSeq: context.start?.event.seq ?? context.matches[0]?.event.seq ?? 0,
      location: locationOf(context),
      visibility: 'visible' as const,
      data: context.state,
    }
  },
}
