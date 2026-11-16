# Roadmap

What a next version would add, in the order of how much it costs:

## 1. Status buildup numbers (paralysis, sleep, stun)

Wilds counts every status's buildup as coloured numbers at the monster. MH4U applies
those statuses **without a damage event**: the hook set this mod uses (poison ticks,
blast, mount) only sees effects that take health. Adding the rest needs finding where the
game adds buildup to a monster's status table (the `uEnemy`'s status fields), hooking
those calls the way `damage_numbers_stub.s` hooks the poison tick, and recompiling the
blocks (`tools/build/build_code_space.py`, devkitARM) into
`core/game/executable/generated/code_space.json`. The drawing side already takes five
kinds (`KIND_*`); a status kind needs a colour entry and no new renderer.

## 2. Damage readout / hunt totals

A per-monster total (and a rough per-second rate) is derivable in the existing frame hook
(sum what the hooks saw per `dmg_monster`), but drawing a readout needs either a layout
with its own panes for the totals or reusing slot panes for a persistent number. Both are
small in code and need on-device testing to place well; the number atlas is already
there to draw the digits.

## 3. Per-version JPN map

MH4G's code differs from MH4U's; a map made from a Japanese dump and the canonical one
would let the mod run on MH4G.

## 4. A web installer page

Heavenfall's installer runs in a browser (pyodide) so phones need no PC; this repository
ships the CLI path (PC or Termux) first. Porting the focused profile to a page is
straightforward but is its own piece of work.

## Known limits (not planned)

* Element breakdown per hit: MH4U folds element into the final damage before the hooks
  see it — there is nothing to split.
* Wounds / focus strikes: no such system in MH4U.
* Cluster / hunting-art damage attribution: the hit records say what made a hit; refining
  the "whose" rules beyond the current ones is possible but needs careful testing.
