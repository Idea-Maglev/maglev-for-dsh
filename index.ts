// Maglev for DSH — host 插件入口（TypeScript）
//
// 注册 Maglev 的 host 能力：
//   - maglev_spec_check：spec 完整性检查（机械验证门禁）
//   - maglev_reality_status：读项目真相（供真相卡片渲染）
//   - maglev_crystallize：记录结晶结果（写回 specs + 产生 maglev/crystallize 会话事件）
//
// 设计约束：本插件**不直接 import @deepseek-ai/dsh-tools**。
// 工具定义手动构造 ToolDefinition 对象传给 ctx.tools.register，
// 避免 dsh-tools 多物理实例导致的 TOOL_RUNTIME_SCHEDULER unique symbol 分裂
// （根因与证据见 docs/thinking/2026-08-15-dsh-tools-instance-split.md）。
// 这样插件在任意 dsh 环境安装都不会与内置插件实例分裂。

import { access, mkdir, readFile, readdir, writeFile } from 'node:fs/promises'
import { constants } from 'node:fs'
import { join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import type { Context } from '@deepseek-ai/cordis'

// 声明 maglev/crystallize 会话事件（供 client 渲染结晶卡片）
declare module '@deepseek-ai/dsh-session/types' {
  interface SessionEventMap {
    /** 一次结晶：把已验证结论写回 specs 知识分层的记录。 */
    'maglev/crystallize': {
      /** 结晶标题 */
      title: string
      /** 一句话结论 */
      summary: string
      /** 写入的文件路径 */
      written: string
      /** 目标层（10_reality / 20_evolution/active / 90_archive） */
      target?: string
    }
    /** 一次真相读取：maglev_reality_status 读到的项目现状结构。 */
    'maglev/reality-status': {
      /** 能力域清单 */
      domains: string[]
      /** 进行中的演进主题 */
      activeTopics: string[]
      /** 是否已建立愿景 */
      hasVision: boolean
      /** 是否已建立真相契约（profile） */
      hasProfile: boolean
    }
  }
}

export const name = 'maglev-host'
export const inject = ['tools', 'skills']

// 技能资产目录：本插件包内的 .agents/skills（host 编译产物在 lib/，技能在上一级）。
// 通过 ctx.skills.registerProvider 注入，让 npm 安装后任何项目（无需本地 .agents/skills）
// 都能发现 maglev 技能——解决"dsh 技能发现只扫项目根"的发布缺口。
const PKG_SKILLS_DIR = fileURLToPath(new URL('../.agents/skills', import.meta.url))
// dsh-skill 的 bundled 标准 rank（项目技能 rank 100-500，bundled 600 最不优先，项目优先）
const BUNDLED_SKILL_RANK = 600

// Maglev 知识分层骨架（相对项目根）
const SPECS_SKELETON_DIRS = [
  'specs/00_vision',
  'specs/10_reality',
  'specs/20_evolution/active',
  'specs/90_archive',
]

const MAINLINE_SKILLS = [
  'entry-router',
  'reality-sync',
  'requirement-convergence',
  'spec-designer',
  'integrated-validator',
  'crystallization',
  'maglev-discipline',
]

const DISCIPLINE_MARKER = '<!-- maglev:managed:discipline -->'

interface SpecCheckResult {
  pass: number
  fail: number
  results: { level: 'PASS' | 'FAIL'; check: string; detail: string }[]
}

interface CrystallizeInput {
  title: string
  summary: string
  target?: string
  content?: string
}

function projectRootOf(exec: { agent?: { session?: { header?: { cwd?: string } } } }): string {
  const header = exec?.agent?.session?.header
  if (header?.cwd) return resolve(header.cwd)
  return resolve(process.cwd())
}

async function pathExists(p: string): Promise<boolean> {
  try {
    await access(p, constants.F_OK)
    return true
  } catch {
    return false
  }
}

// 检查目录存在且至少含一个 .md 文件（避免"空目录也 PASS"的假阳性）
async function dirHasMarkdown(p: string): Promise<{ ok: boolean; reason: string }> {
  try {
    const entries = await readdir(p, { withFileTypes: true })
    const ok = entries.some((e) => e.isFile() && e.name.endsWith('.md'))
    return ok ? { ok, reason: '' } : { ok, reason: ' (empty or no .md)' }
  } catch {
    return { ok: false, reason: ' (missing)' }
  }
}

async function runSpecCheck(root: string): Promise<SpecCheckResult> {
  const results: SpecCheckResult['results'] = []
  for (const rel of SPECS_SKELETON_DIRS) {
    const ok = await pathExists(join(root, rel))
    results.push({ level: ok ? 'PASS' : 'FAIL', check: 'specs_skeleton', detail: rel })
  }
  const agentsMd = join(root, 'AGENTS.md')
  if (await pathExists(agentsMd)) {
    const text = await readFile(agentsMd, 'utf8')
    results.push({
      level: text.includes(DISCIPLINE_MARKER) ? 'PASS' : 'FAIL',
      check: 'discipline_block',
      detail: 'AGENTS.md',
    })
  } else {
    results.push({ level: 'FAIL', check: 'discipline_block', detail: 'AGENTS.md (missing)' })
  }
  const skillsDir = join(root, '.agents', 'skills')
  for (const skill of MAINLINE_SKILLS) {
    const ok = await pathExists(join(skillsDir, skill, 'SKILL.md'))
    results.push({ level: ok ? 'PASS' : 'FAIL', check: 'mainline_skills', detail: skill })
  }
  const thinking = await dirHasMarkdown(join(root, 'docs', 'thinking'))
  results.push({
    level: thinking.ok ? 'PASS' : 'FAIL',
    check: 'docs_thinking',
    detail: 'docs/thinking' + thinking.reason,
  })
  const fail = results.filter((r) => r.level === 'FAIL').length
  return { pass: results.length - fail, fail, results }
}

async function runCrystallize(root: string, input: CrystallizeInput) {
  const target = input.target ?? '10_reality'
  const realityDir = join(root, 'specs', target)
  await mkdir(realityDir, { recursive: true })
  const stamp = new Date().toISOString().slice(0, 10)
  // 纯非 ASCII 标题（如中文）会 slug 成空串，回退到带短随机后缀的稳定文件名
  let slug = input.title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '')
  if (!slug) slug = `crystal-${Math.random().toString(36).slice(2, 7)}`
  const file = join(realityDir, `${stamp}-${slug}.md`)
  const body = `# ${input.title}\n\n> 结晶时间: ${new Date().toISOString()}\n\n${input.summary}\n\n${input.content ?? ''}\n`
  await writeFile(file, body, 'utf8')
  return { written: file, title: input.title, summary: input.summary, target }
}

interface RealityStatus {
  domains: string[]
  activeTopics: string[]
  hasVision: boolean
  hasProfile: boolean
}

async function runRealityStatus(root: string): Promise<RealityStatus> {
  // 读真相（Spec 仓库的"是什么"）：domain 清单 + active 主题 + 愿景/契约存在性
  const domains: string[] = []
  const realityDir = join(root, 'specs', '10_reality')
  try {
    for (const entry of await readdir(realityDir, { withFileTypes: true })) {
      if (entry.isDirectory()) domains.push(entry.name)
    }
  } catch {
    // 10_reality 不存在 → 空 domains
  }
  const activeTopics: string[] = []
  const activeDir = join(root, 'specs', '20_evolution', 'active')
  try {
    for (const entry of await readdir(activeDir, { withFileTypes: true })) {
      if (entry.isFile() && entry.name.endsWith('.md')) activeTopics.push(entry.name)
    }
  } catch {
    // active 不存在 → 空 topics
  }
  const hasVision = await pathExists(join(root, 'specs', '00_vision'))
  const hasProfile = await pathExists(join(root, 'specs', '10_reality', '00_profile.yaml'))
  return { domains, activeTopics, hasVision, hasProfile }
}

/** 简单参数校验：缺必填参数时给出与 dsh INVALID_ARGS 一致的失败体验。 */
function requireParams(args: Record<string, unknown>, required: readonly string[]): void {
  const missing = required.filter((k) => typeof (args as Record<string, unknown>)[k] !== 'string' || (args as Record<string, unknown>)[k] === '')
  if (missing.length > 0) {
    throw new Error(`invalid arguments: missing required parameter(s): ${missing.join(', ')}`)
  }
}

// ---- 技能注入（让 npm 包内的 .agents/skills 对任意项目可用） ----

/** 从 SKILL.md 解析 frontmatter 的 name/description 与正文（零依赖正则解析）。 */
function parseSkillFile(text: string): { name?: string; description?: string; body: string } {
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/)
  if (!m) return { body: text }
  let name: string | undefined
  let description: string | undefined
  for (const line of m[1].split(/\r?\n/)) {
    const kv = line.match(/^name:\s*(.+)$/)
    if (kv) name = kv[1].trim().replace(/^['"]|['"]$/g, '')
    const dv = line.match(/^description:\s*(.+)$/)
    if (dv) description = dv[1].trim().replace(/^['"]|['"]$/g, '')
  }
  return { name, description, body: text.slice(m[0].length) }
}

interface BundledSkillLocator { dir: string }
interface BundledSkillCandidate {
  name: string
  description: string
  invocation: { modelInvocable: boolean; userInvocable: boolean }
  source: string
  provider: string
  rank: number
  locator: BundledSkillLocator
  path: string
  resourceBase: { kind: 'directory'; path: string }
}

/** 列出本包内全部技能候选（跳过 `_` 开头的内部目录）。 */
async function listBundledSkills(): Promise<readonly BundledSkillCandidate[]> {
  let entries
  try {
    entries = await readdir(PKG_SKILLS_DIR, { withFileTypes: true })
  } catch {
    return []
  }
  const candidates: BundledSkillCandidate[] = []
  for (const entry of entries) {
    if (!entry.isDirectory() || entry.name.startsWith('_')) continue
    const dir = join(PKG_SKILLS_DIR, entry.name)
    const skillFile = join(dir, 'SKILL.md')
    let text: string
    try {
      text = await readFile(skillFile, 'utf8')
    } catch {
      continue
    }
    const { name, description } = parseSkillFile(text)
    if (!name || !description) continue
    candidates.push({
      name,
      description,
      invocation: { modelInvocable: true, userInvocable: true },
      source: 'bundled',
      provider: 'maglev-bundled',
      rank: BUNDLED_SKILL_RANK,
      locator: { dir },
      path: skillFile,
      resourceBase: { kind: 'directory', path: dir },
    })
  }
  return candidates
}

/** 加载一个技能候选的完整正文（去掉 frontmatter），返回完整 SkillDefinition。 */
async function getBundledSkill(candidate: {
  name?: string
  description?: string
  invocation?: unknown
  source?: string
  provider?: string
  resourceBase?: unknown
  path?: string
  locator?: BundledSkillLocator
}): Promise<unknown> {
  const dir = candidate?.locator?.dir
  if (!dir || typeof candidate.name !== 'string' || typeof candidate.description !== 'string') return undefined
  try {
    const text = await readFile(join(dir, 'SKILL.md'), 'utf8')
    const { body } = parseSkillFile(text)
    return {
      name: candidate.name,
      description: candidate.description,
      invocation: candidate.invocation ?? { modelInvocable: true, userInvocable: true },
      source: candidate.source ?? 'bundled',
      provider: candidate.provider ?? 'maglev-bundled',
      resourceBase: candidate.resourceBase,
      content: body,
      path: candidate.path,
    }
  } catch {
    return undefined
  }
}

export function apply(ctx: Context): void {
  // 技能注入：任何项目（无需本地 .agents/skills）都能发现 maglev 技能。
  // ctx.skills 由 dsh-skill 服务提供；结构按 dsh 的 SkillProvider 接口。
  try {
    const skills = (ctx as unknown as { skills?: { registerProvider(p: unknown): unknown } }).skills
    skills?.registerProvider(() => ({
      name: 'maglev-bundled',
      list: listBundledSkills,
      get: getBundledSkill,
    }))
  } catch {
    // 技能注册失败不阻断工具能力（降级：仅工具可用）
  }

  ctx.tools.register({
    name: 'maglev_spec_check',
    description: '检查 Maglev 项目的 spec 完整性：specs 知识分层骨架、AGENTS.md 会话纪律区块、主链路技能、docs/thinking 决策记录（非空）是否齐全。交付前调用它作为机械验证门禁。',
    parameters: { type: 'object', properties: {} },
    output: {
      schema: { type: 'object', additionalProperties: true },
      render: (_args, value: SpecCheckResult) => {
        const lines = value.results.map((r) => `[${r.level}] ${r.check}  ${r.detail}`)
        const summary = `spec 完整性检查：pass=${value.pass} fail=${value.fail}`
        return [{ type: 'text', text: summary + '\n' + lines.join('\n') }]
      },
    },
    async execute(_args, exec) {
      const root = projectRootOf(exec)
      return runSpecCheck(root)
    },
  })

  ctx.tools.register({
    name: 'maglev_reality_status',
    description: '读项目的真相（Spec 仓库的"是什么"）：列出 specs 的能力域、进行中的演进主题、是否已建立愿景与真相契约。让 AI/接手者快速知道项目现状结构。',
    parameters: { type: 'object', properties: {} },
    output: {
      schema: { type: 'object', additionalProperties: true },
      render: (_args, value: RealityStatus) => {
        const lines = [
          `能力域（${value.domains.length}）：${value.domains.join(', ') || '无'}`,
          `进行中主题（${value.activeTopics.length}）：${value.activeTopics.join(', ') || '无'}`,
          `愿景：${value.hasVision ? '有' : '无'}；真相契约(profile)：${value.hasProfile ? '有' : '无'}`,
        ]
        return [{ type: 'text', text: lines.join('\n') }]
      },
    },
    async execute(_args, exec) {
      const root = projectRootOf(exec)
      const status = await runRealityStatus(root)
      // 记录真相读取（强化融合点 1：AI 读真相的动作也进 session log）
      exec.agent?.session?.append('maglev/reality-status', status)
      return status
    },
  })

  ctx.tools.register({
    name: 'maglev_crystallize',
    description: '把已验证的结论结晶到项目的 specs 知识分层。title=结晶标题，summary=一句话结论，target=目标层（默认 10_reality，可选 20_evolution/active 或 90_archive），content=完整结论正文（markdown）。',
    parameters: {
      type: 'object',
      properties: {
        title: { type: 'string', description: '结晶标题' },
        summary: { type: 'string', description: '一句话结论' },
        target: { type: 'string', description: '目标层：10_reality（默认）/ 20_evolution/active / 90_archive' },
        content: { type: 'string', description: '完整结论正文（markdown）' },
      },
      required: ['title', 'summary'],
    },
    output: {
      schema: { type: 'object', additionalProperties: true },
      render: (_args, value) => [
        { type: 'text', text: `已结晶：${value.title}\n写入：${value.written}\n结论：${value.summary}` },
      ],
    },
    async execute(args: CrystallizeInput, exec) {
      requireParams(args as Record<string, unknown>, ['title', 'summary'])
      const root = projectRootOf(exec)
      const result = await runCrystallize(root, args)
      // 产生 maglev/crystallize 会话事件（client 结晶卡片的数据源）
      exec.agent?.session?.append('maglev/crystallize', {
        title: result.title,
        summary: result.summary,
        written: result.written,
        target: result.target,
      })
      return result
    },
  })

  // 机械门禁（融合点 3）：结晶前强制 spec 完整性检查，fail 则拒绝。
  // 不依赖 AI 自觉——tools/pre-execute 在工具执行前拦截，deny 即阻断。
  ctx.on('tools/pre-execute', async (exec, next) => {
    if (exec.name !== 'maglev_crystallize') return next()
    const root = projectRootOf(exec.agent ? { agent: exec.agent } : {})
    const check = await runSpecCheck(root)
    if (check.fail > 0) {
      return {
        kind: 'deny',
        reason: `结晶门禁拦截：spec 完整性检查未通过（fail=${check.fail}），先修复真相层再结晶`,
      }
    }
    return next()
  })
}
