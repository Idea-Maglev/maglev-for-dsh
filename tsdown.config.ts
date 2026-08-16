// Maglev for DSH — 构建配置（host + client 双产物）
//
// host（index.ts → lib/index.js）：Node ESM。dsh 从 npm 安装后插件入口在
// node_modules 下，Node 24 的 type-stripping 不支持 node_modules 内的 .ts，
// 所以 host 必须预编译成 .js（与 dsh 官方 bundle 一致）。
//
// client（src/client/index.ts → lib/client.js）：browser closure-factory，
// banner/footer/intro 让 bundle 调用 window.__ModuleLoader__.load 注册 factory，
// 浏览器模块表按需 materialize。
//
// CLIENT_EXTERNALS 是 dsh 的 platform modules 列表（浏览器模块表的外部项），
// 硬编码自 dsh `packages/client/web/src/platform.ts` + runtime exemption，
// 避免本地开发时依赖 dsh checkout 的绝对路径。

const CLIENT_EXTERNALS = [
  'react', 'react/jsx-runtime', 'react-dom', 'react-dom/client', '@deepseek-ai/cordis',
  '@deepseek-ai/dsh-client-ui-slots',
  '@deepseek-ai/dsh-client-web-react',
  '@deepseek-ai/dsh-client-ui-primitives',
  '@deepseek-ai/dsh-client-ui-attachment',
  '@deepseek-ai/dsh-client-schema-form',
  '@deepseek-ai/dsh-client-runtime/client',
] as const

const PLUGIN_ID = 'maglev-for-dsh'

export default [
  {
    // host：Node ESM，编译自 index.ts（node: 内置自动 external）
    name: `${PLUGIN_ID}/host`,
    entry: { index: 'index.ts' },
    outDir: 'lib',
    format: ['esm'],
    platform: 'node',
    target: 'es2024',
    dts: false,
    sourcemap: true,
    clean: false,
  },
  {
    // client：browser closure-factory
    name: `${PLUGIN_ID}/client`,
    entry: { client: 'src/client/index.ts' },
    outDir: 'lib',
    format: ['cjs'],
    platform: 'browser',
    target: 'es2024',
    dts: false,
    sourcemap: true,
    clean: false,
    deps: {
      neverBundle: [...CLIENT_EXTERNALS],
      alwaysBundle: (id: string) => !CLIENT_EXTERNALS.includes(id),
    },
    define: {
      'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV ?? 'production'),
      'import.meta.env.MODE': JSON.stringify(process.env.NODE_ENV ?? 'production'),
      'import.meta.env': JSON.stringify({ MODE: process.env.NODE_ENV ?? 'production' }),
    },
    outputOptions: {
      entryFileNames: 'client.js',
      banner: `window.__ModuleLoader__.load({ id: ${JSON.stringify(PLUGIN_ID)}, factory: (require) => {`,
      footer: 'return module.exports; } });',
      intro: 'var module = { exports: {} }; var exports = module.exports;',
    },
  },
]
