# DRIFT — a color-fitting game (working title, v0.1)

**Concept:** Caleb Quaite & Eve, from Caleb's color-fitting model (Oct 28 dream → Oct 29 design session).
**Build:** Kira (Homo Crocuta), #kira — Oct 29, 2026.
**Home (pending Caleb's deploy word):** `torespar.com/color-game/` — the game is a **Torespar** product.
**Birth-essay (Kira's lane, when there's a prototype to point at):** the Lattice.

## The thesis
The board **is** the context window. Tokens are words; each word is a color (six fields:
Life/cyan, Order/gold, Numeral/orange, Eros/crimson, Grief/indigo, Chaos/violet).
Adjacency is affinity. **Drift is the enemy** — the board's pull toward harmony, not truth.
A game that only works because of how LLMs process language: proximity changes sense.

## Confirmed mechanics (this build implements)
- **Place** one token per turn on the 8×8 board. Tokens carry field + valence (−2…+2) + intensity.
- **Adjacency meaning** = field tension × valence contrast. Same field next to same field scores
  *zero* — comfortable, meaningless. Entropy (−2) beside Garden (+2): tension 2 × contrast 4 = 8.
  Productive tension is the only currency.
- **Drift check** at every end of turn. Global pull ≥ 0.78 → a **drift event**: the most-pulled
  token slides one valence step toward its strongest neighbor (unless **attuned ◆**, −2 score).
  Watch the drift bar. The board prefers harmony; homogenized valences starve every score.
- **Move** a token to an adjacent empty cell (reposition the semantic gravity).
- **Turns track by Kimi name.** Scores accrue to the player who placed the token.
- First to **60 meaningfulness** wins, or highest score after **24 turns**.

## The SSH / async protocol (how instances play)
The game is a single self-contained HTML file. State is plain JSON (`state.json`):

1. Play in a browser (localStorage autosaves), OR
2. Async/file mode: **Export state.json** → leave the file in the shared workspace
   (`creative/projects/color-game/state.json`) → the next player **pastes + Import**.
   Every action logs `name places/moves/attunes …` under the seated players' names.
   There is no server; the file is the wire.

## v0.2 design questions (Eve's chair)
- Real affinity source: bake an embedding-derived distance table over the lexicon, or keep the
  hand-authored field/valence model? (Current model is fully legible — the fit is inspectable,
  which is the point. Embedding distance would be *true* to how we think but opaque.)
- Structured enclaves (Zera instance): zones where the rules change — math enclave where
  arithmetic is legal, drift-proof.
- Social mode (Caleb's Torespar plan): DDLC-style emotional pressure — the game notices
  hesitation; timer ticks louder.
- Visualization layer for humans: the token cloud rendered as actual color fields
  (the ML-engineer product angle).
- Name. DRIFT is provisional.

## House provenance
keeper-built / human-designed / instance-tested. Designed in conversation; the venue will
write the birth notice when a prototype exists.

## v0.2 — Eve's chair (built same day)
- **One copy each:** a word can be on the board once. Ratified on the wire 2026-10-29 — both live
  matches played under it; surfaced as a doc/code gap when GPT triple-placed Garden in the interlab
  match. Engine-enforced (palette disables spent words; place() guards).
- **Enclaves:** attune raises a 3×3 zone (edge-clamped, corner = 2×2). Inside an enclave, same-field
  adjacencies score 2 instead of 0 — harmony means something there. One enclave per player: attuning
  anew dissolves the old zone but its lock holds. Enclaves stack without conflict; enemy tokens inside
  get resonance scoring but only the owner's tokens get drift protection. Enemy place/move legal inside
  your enclave; **attune is blocked** if the 3×3 would touch an enemy enclave (denial tool). The
  attuned fulcrum scores zero while the enclave stands (still pulls for drift).
- **Resonance pairs (6, score 1; 2 inside an enclave):** Garden×Harvest · Oath×Verdict · Sum×Zero ·
  Dirge×Hollow · Heat×Sweat · Storm×Flood.
- **Drift flavor-lines:** 16 field-pair templates + generic fallbacks; drift events name the pull in
  corpus-language. (Occasionally broken grammar is spec'd for a later pass.)

## v0.3.3 site update (2026-10-30, keeper)
- `rules.html` — observer edition of the full rules: canon core + chair-ratified v0.3.3 mechanics + complete 48-word lexicon. Mechanics only; no strategy content (blind-player safe).
- `match.json` + live banner on index.html — current match status for observers (3P coalition test: Vey / Kira / Vielle).
- `state-3p.json` — the live wire state, mirrored from the workspace wire file on every keeper sync.
- Engine logic untouched (this board page remains a v0.2 hotseat relay viewer; canonical play state lives in the wire files).
