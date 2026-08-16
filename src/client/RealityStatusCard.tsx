// Maglev for DSH — 真相卡片 React 组件
//
// 展示 AI 读到的项目现状结构：能力域、进行中主题、愿景/契约状态。

import { createElement } from 'react'
import type { ChatNodeViewProps } from '@deepseek-ai/dsh-client-ui-conversation/client'

export function RealityStatusCard({ node }: ChatNodeViewProps<'maglev-reality-status'>) {
  const d = node.data
  return createElement(
    'div',
    { 'data-plugin': 'maglev-for-dsh', 'data-reality-status-card': true },
    createElement('div', { 'data-reality-title': true }, '📋 项目现状'),
    createElement('div', {}, `能力域（${d.domains.length}）：${d.domains.join(', ') || '无'}`),
    createElement('div', {}, `进行中主题（${d.activeTopics.length}）：${d.activeTopics.join(', ') || '无'}`),
    createElement('div', {}, `愿景：${d.hasVision ? '已建立' : '未建立'}；真相契约：${d.hasProfile ? '已建立' : '未建立'}`),
  )
}
