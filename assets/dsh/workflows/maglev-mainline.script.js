// Maglev 主链路 workflow（参考脚本）
//
// 这是给 dsh workflow 工具使用的参考编排：把 Maglev 的"收敛 → 设计 → 验证 → 结晶"
// 主链路编排成 dsh 的多代理 fan-out。模型可以在实际会话中据此生成更贴合上下文的
// workflow，也可以直接复用这个骨架。
//
// 约定：
//   - `args.request`：用户的需求描述（由调用方传入）
//   - 每个阶段启动一个 subagent，subagent 在 prompt 里被要求先用 skill 工具加载
//     对应的 Maglev 技能（requirement-convergence / spec-designer /
//     integrated-validator / crystallization）
//   - 每个阶段把产出通过 `args` 传给下一阶段，形成可追溯的链条

const request = args?.request ?? '（未提供需求描述）'

phase('收敛')
log(`开始收敛需求：${request}`)
const converged = await agent(
  `你是需求收敛器。请先用 skill 工具加载 requirement-convergence 技能，然后严格按该技能收敛下面的需求边界，输出稳定的需求描述与 Ready Gate 结论。\n\n需求：\n${request}`,
  { label: '需求收敛' },
)

phase('设计')
log('需求已收敛，进入方案设计')
const spec = await agent(
  `你是方案设计器。请先用 skill 工具加载 spec-designer 技能，然后基于下面已收敛的需求，形成可执行的方案（含验收标准与验证依据）。\n\n已收敛需求：\n${converged}`,
  { label: '方案设计' },
)

phase('验证')
log('方案已形成，进入综合验证')
const verified = await agent(
  `你是综合验证器。请先用 skill 工具加载 integrated-validator 技能，然后对下面的方案做 requirements ↔ spec ↔ code ↔ tests 交叉验证，输出验证结论与风险清单。\n\n方案：\n${spec}`,
  { label: '综合验证' },
)

phase('结晶')
log('验证完成，进入结晶回写')
const crystallized = await agent(
  `你是现实结晶器。请先用 skill 工具加载 crystallization 技能，然后基于下面的验证结论，判断哪些结果应写回 specs/10_reality、哪些收口到 active、哪些归档。\n\n验证结论：\n${verified}`,
  { label: '结晶回写' },
)

return {
  request,
  converged,
  spec,
  verified,
  crystallized,
}
