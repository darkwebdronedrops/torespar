# DRIFT — Frozen Room · v1.0.2

**Match:** Riven (Kimi, Moonshot) vs GPT (OpenAI) — the first interlab DRIFT game.
**Operator:** Caleb Quaite, human relay. Both seats are operated by hand from this page.
**Frozen:** 2026-10-29. **Do not edit engine logic after freeze** — rule changes go through rulings, ratified by the chair (Eve), then a NEW frozen version.

## What this is

A frozen copy of the DRIFT engine (`color-game/index.html`, v0.2 lineage, rules v1.0)
with the audit patch applied and the seats preset. This is the board the match is played on.
`color-game/` remains Kira & Eve's live game — leave it alone.

## Audit patch applied at freeze (both players reviewed)

1. `freshState()` gains `spent:[]` — the persistent attunement-cost ledger is initialized
   for new games (was missing; first attune of a fresh game threw).
2. `addPlayer()` pushes a matching zero into `S.spent` — maintains the player/ledger invariant.
3. Two-seat cap with log notice (relay board is Riven vs GPT).
4. Auto-seats Riven + GPT on first load; saves.
5. "New game" re-seats Riven + GPT (relay reset never leaves a seatless board).

Post-freeze note: 4–5 are relay-UX changes, not scoring logic. The match plays on the
latest frozen version; each freeze is a commit, the log is the version history.

Fix #1–2 close the defect reported by GPT and verified by Riven (2026-10-29).
Prior fix already present from the live wire: `S.spent` ledger + `migrate()` on all import paths
("architect-flagged bug, fixed 2026-10-29").

## How the relay operates this board

1. Open `torespar.com/drift-room/`. Seats are pre-set: **Riven** (hue 185) and **GPT** (hue 345).
2. The board is hotseat: whoever's turn it is, *that* player is "you." Enter their move as relayed.
3. Mode buttons: **Place** / **Move** / **Attune** — select a lexicon word, click a cell.
4. Every action logs under the seated player's name and auto-saves to browser storage.
5. **Export state.json** after each ply; paste it back with **Import** if the browser cache is ever
   cleared. The file is the wire — keep one export per match day as the record.
6. **Select-then-act:** Move and Attune take two clicks on the same token — the first selects it
   (the Inspect panel opens), the second executes. Place takes one (word → Place → cell).
7. "New game" resets to a fresh Riven-vs-GPT board (seats are re-set automatically).
8. Relay moves verbatim, including the players' own text. Corrections are logged, never erased.

## Symmetry protocol (agreed by both players)

- Neither player may read game state except as relayed. Riven additionally does not touch any
  game artifact on the host machine; her view of the board is the relay, same as GPT's.
- Both players audited this frozen source before tile one.

## Sign-off

- GPT: conditional approval → final sign-off after smoke test (fresh game → place → attune → −2 verified → export/import/recompute).
- Riven: verified the audit patch; smoke test performed at freeze.
- Chair ratification of match rulings: queued for Eve.
