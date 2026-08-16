// Maglev for DSH — 结晶卡片 React 组件
//
// 渲染在会话流中的一张卡片：标题 + 一句话结论 + 写入路径 + 目标层。

import { createElement } from 'react'
import type { ChatNodeViewProps } from '@deepseek-ai/dsh-client-ui-conversation/client'

export function CrystallizeCard({ node }: ChatNodeViewProps<'maglev-crystallize'>) {
  const d = node.data
  return createElement(
    'div',
    { 'data-plugin': 'maglev-for-dsh', 'data-crystallize-card': true },
    createElement('div', { 'data-crystallize-title': true }, `🔮 ${d.title}`),
    createElement('div', { 'data-crystallize-summary': true }, d.summary),
    createElement('div', { 'data-crystallize-written': true }, `写入：${d.written}`),
    d.target !== undefined
      ? createElement('div', { 'data-crystallize-target': true }, `目标层：${d.target}`)
      : null,
  )
}
