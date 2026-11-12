import { expect, test } from 'claude-code/testing'

const BAND = { plugin: 'sdlc', component: 'AbovePrompt', props: {} } as const

function project(on: any, status: object | null) {
  // Hooks here stand for the engine: sdlc.py answers through process.run.
  on('session.root', () => ({ value: '/p' }))
  on('process.run', () => ({
    value: status
      ? { exitCode: 0, stdout: JSON.stringify(status), stderr: '' }
      : { exitCode: 1, stdout: '', stderr: 'sdlc: no .sdlc.yml here' },
  }))
  on('session.start', (_: unknown, e: any) => ({ cwd: e.cwd }))
  on('tool.call', () => ({ result: {} }))
}

const implementing = {
  modules: ['spec', 'review'],
  allModules: ['spec', 'review', 'tdd'],
  autonomy: false,
  phases: ['spec', 'implement', 'review', 'commit'],
  item: 'session-cookie',
  phase: 'implement',
}

test('the band shows the item and phase, on every surface', async ($, on) => {
  project(on, implementing)
  await $.session.start({ cwd: '/p', surface: 'desktop', isInteractive: true })
  for (const surface of ['terminal', 'desktop'] as const) {
    const ui = await $.ui.mount({ ...BAND, surface })
    expect((await ui.find({ type: 'Text', text: /sdlc/ }))?.text).toBe(' sdlc · session-cookie · implement · gates')
    await ui.unmount()
  }
})

test('a commit before review is denied; other git commands pass', async ($, on) => {
  project(on, implementing)
  await $.session.start({ cwd: '/p', surface: 'desktop', isInteractive: true })
  const denied: any = await $.tool.call({ tool: 'Bash', command: 'git commit -m "Auth: add cookie"' })
  expect(denied.deny).toMatch(/session-cookie is in phase implement/)
  const listed: any = await $.tool.call({ tool: 'Bash', command: 'git status' })
  expect(listed.deny).toBe(undefined)
})

test('outside an sdlc project the mod draws nothing and gates nothing', async ($, on) => {
  project(on, null)
  on('ui.render', ($: any, e: any) => {
    const { Text } = $.ui.resolve(e)
    return <Text>engine</Text>
  })
  await $.session.start({ cwd: '/p', surface: 'desktop', isInteractive: true })
  const ran: any = await $.tool.call({ tool: 'Bash', command: 'git commit -m x' })
  expect(ran.deny).toBe(undefined)
  const ui = await $.ui.mount({ ...BAND, surface: 'terminal' })
  expect(await ui.find({ type: 'Text', text: /sdlc/ })).toBe(undefined)
  await ui.unmount()
})
