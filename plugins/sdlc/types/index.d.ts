// What `sdlc.py status --json` reports; null outside sdlc projects.
export type Status = {
  modules: string[]
  allModules: string[]
  gates: 'commit' | 'all' | 'none'
  quick: boolean
  phases: string[]
  item: string | null
  phase: string | null
}

declare module 'claude-code' {
  interface PluginState {
    sdlc: { status: Shaped<Status | null>; isExpanded: boolean; limits: Shaped<SessionRateLimit[]> }
  }
}
