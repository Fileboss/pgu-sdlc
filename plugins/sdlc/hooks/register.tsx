import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { Status } from '../types'

// The band above the prompt and the commit gate. .sdlc.yml stays the source
// of truth: every read and write goes through scripts/sdlc.py.
const status = atom({ plugin: 'sdlc', key: 'status' } as const, null, { shape: 'status-1' })
const isExpanded = atom({ plugin: 'sdlc', key: 'isExpanded' } as const, false)


async function sdlc($: EngineInterface, args: string[]) {
  const root = await $.session.root()
  return $.process.run(['python3', `${$.plugin.root}/scripts/sdlc.py`, ...args], { cwd: root })
}

async function refresh($: EngineInterface) {
  const ran = await sdlc($, ['status', '--json'])
  const next: Status | null = ran.exitCode === 0 ? JSON.parse(ran.stdout) : null
  await update($, status, () => next)
}

async function change($: EngineInterface, args: string[]) {
  const ran = await sdlc($, args)
  if (ran.exitCode !== 0) $.ui.toast(ran.stderr.trim() || 'sdlc failed')
  await refresh($)
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    const started = await next(e)
    await refresh($)
    return started
  })

  // The model moves phases and edits .sdlc.yml too: re-read after each turn.
  on('turn.complete', async ($, e, next) => {
    await refresh($)
    return next(e)
  })

  // Gate: with the review module on, an item is committed only after review.
  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    if (!/\bgit\s+commit\b/.test(e.command)) return next(e)
    const s = await read($, status)
    const isGated = s?.modules.includes('review') && s.item && s.phase !== 'review' && s.phase !== 'commit'
    return isGated
      ? { deny: `sdlc: ${s!.item} is in phase ${s!.phase}; review it before committing (/sdlc:next).` }
      : next(e)
    }).catch(($, e, next) => next(e)) // a failing gate must not block work

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const s = await read($, status)
    if (s === null || e.props.hasSurvey) return next(e)
    const { Box, Button, Text } = $.ui.resolve(e)
    const expanded = await read($, isExpanded)
    const where = s.item ? `${s.item} · ${s.phase}` : 'no item'
    const toggle = (
      <Button key="toggle" plain label={expanded ? '▾' : '▸'} onPress={() => update($, isExpanded, v => !v)} />
    )
    const line = (
      <Box>
        {toggle}
        <Text dimColor> sdlc · {where} · {s.autonomy ? 'auto' : 'gates'}</Text>
      </Box>
    )
    if (!expanded) return line

    const flip = (name: string) =>
      (s.modules.includes(name) ? s.modules.filter(m => m !== name) : [...s.modules, name]).join(',')
    return (
      <Box flexDirection="column">
        {line}
        <Box flexWrap="wrap">
          {s.allModules.map(name => (
            <Button key={`m-${name}`} label={`${s.modules.includes(name) ? '●' : '○'} ${name}`}
              onPress={() => change($, ['set', 'modules', flip(name)])} />
          ))}
        </Box>
        <Box>
          <Button key="autonomy" label={s.autonomy ? 'Switch to gates' : 'Switch to auto'}
            onPress={() => change($, ['set', 'autonomy', String(!s.autonomy)])} />
          {s.item && (
            <Button key="next" variant="primary" label={`Approve ${s.phase} → next`}
              onPress={() => change($, ['next'])} />
          )}
        </Box>
      </Box>
    )
  })
}
