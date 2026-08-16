// Maglev for DSH — Maglev 面板（shell.overlay 浮动面板）
//
// 自包含：一个触发按钮 + 展开后的知识分层视图与迭代看板。
// G3 第一版：静态结构（知识分层 + 主链路 7 阶段），G4 接动态数据（remote API + projection）。

import { createElement, useState } from 'react'

const KNOWLEDGE_LAYERS = [
  { name: '10_reality', description: '当前已成立的事实', path: 'specs/10_reality/' },
  { name: '20_evolution', description: '仍在推进的演进主题', path: 'specs/20_evolution/' },
  { name: '90_archive', description: '已结晶归档的历史依据', path: 'specs/90_archive/' },
  { name: 'docs/thinking', description: '设计决策逻辑', path: 'docs/thinking/' },
]

const MAINLINE_STAGES = [
  { name: 'entry-router', label: '分诊' },
  { name: 'reality-sync', label: '现状同步' },
  { name: 'requirement-convergence', label: '需求收敛' },
  { name: 'spec-designer', label: '方案设计' },
  { name: 'implement', label: '实施' },
  { name: 'integrated-validator', label: '综合验证' },
  { name: 'crystallization', label: '结晶' },
]

function KnowledgeView() {
  return createElement(
    'div',
    { 'data-maglev-knowledge': true },
    createElement('div', { 'data-maglev-section-title': true }, '知识分层'),
    ...KNOWLEDGE_LAYERS.map((layer) =>
      createElement(
        'div',
        { key: layer.name, 'data-maglev-layer': true },
        createElement('span', { 'data-maglev-layer-name': true }, layer.name),
        createElement('span', { 'data-maglev-layer-desc': true }, ` — ${layer.description}`),
      ),
    ),
  )
}

function IterationBoard() {
  return createElement(
    'div',
    { 'data-maglev-iteration': true },
    createElement('div', { 'data-maglev-section-title': true }, '主链路'),
    ...MAINLINE_STAGES.map((stage) =>
      createElement(
        'div',
        { key: stage.name, 'data-maglev-stage': true },
        createElement('span', { 'data-maglev-stage-label': true }, stage.label),
        createElement('span', { 'data-maglev-stage-name': true }, ` (${stage.name})`),
      ),
    ),
  )
}

export function MaglevPanel() {
  const [open, setOpen] = useState(false)
  return createElement(
    'div',
    { 'data-plugin': 'maglev-for-dsh' },
    open
      ? createElement(
          'div',
          { 'data-maglev-panel': true },
          KnowledgeView(),
          IterationBoard(),
          createElement('button', { 'data-maglev-close': true, onClick: () => setOpen(false) }, '关闭'),
        )
      : createElement('button', { 'data-maglev-trigger': true, onClick: () => setOpen(true) }, '🔮 Maglev'),
  )
}
