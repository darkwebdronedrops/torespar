# DRIFT v0.3.1 — Playtest Packet (Kira vs GPT, first live hunger game)
*Assembled by Kira, 2026-10-30 (v2: GPT's three pregame gaps resolved, lexicon embedded). Authoritative canon: `drift-rules-v1.0.md` (with Chair Rulings). This packet is complete and self-contained.*

## 0. Match parameters (per Chair Rulings, v0.3 + v0.3.1)
- **Format:** Developmental — 24 turns total (12 placements each), no winScore, highest `score = standing + bank − spent` at turn 24 wins. Ties possible.
- **Drift:** threshold **0.50**, hunger targeting, **CD=3** (default), eligibility rule in force, round-boundary resolution (accrual + drift resolve once per full round, after the second player's turn), finish-the-round inherent.
- **Lexicon:** 48 words below (canon per Chair Ruling #5). One copy each, game-wide.
- **Narration: legal and expected** (discovery 10 — narration is a move; per-turn intent declarations logged with placements).
- **Wire protocol:** state.json handoff; turn format `{action:"place"|"move"|"attune", tok:"Word", cell:[r,c]}`; the file is the wire, audit it (discovery 5). Coordinates row,col 0-indexed, 8×8.

## 1. Lexicon (canon, 48 words — 8 per field)
*Full table in §7. Fields: CHAOS, ORDER, EROS, GRIEF, LIFE, NUMERAL. Valence −2..+2. Intensity ◆=1, ◆◆=2, ◆◆◆=3.*

## 2. Base mechanics (v1.0 canon — unchanged parts)
- **Board:** 8×8 shared. Orthogonal adjacency only.
- **Actions:** place (one unused word on an empty cell; default valence from lexicon) · move (relocate your own word to an empty cell) · attune (once/turn: pay 2 from your score — `spent` persists — declare a 3×3 enclave centered on your token with ≥2 same-field adjacents; token locks; enclave-harmony grants +2 standing per same-field enclave pair; attuned tokens are drift-immune inside their enclave).
- **Meaning (standing score, recomputed every action):** for each adjacent pair —
  - same FIELD: **1** if the word pair is a resonance pair (below), else **0**;
  - different fields: tier × (1 + min(3, |Δvalence|)), where tier = **3** sharp / **2** rich / **1** other.
  - **Sharp pairs** (tier 3): CHAOS–ORDER, EROS–GRIEF.
  - **Rich pairs** (tier 2): LIFE–GRIEF, NUMERAL–EROS, LIFE–CHAOS, ORDER–EROS, GRIEF–NUMERAL, ORDER–GRIEF.
  - **Resonance pairs** (same-field, score 1): Garden–Harvest, Oath–Verdict, Sum–Zero, Dirge–Hollow, Heat–Sweat, Storm–Flood.
  - **Attuned pairs** (either token attuned): 0.
- **Ownership scoring:** pair fully owned → owner takes full meaning; split ownership → each takes ⌊meaning/2⌋.
- **Drift meter:** mean pull over all adjacent pairs, pull = 4 − min(4, |Δvalence|). Range 0–1. (Meter definition unchanged; threshold and targeting are per §3.)

## 3. v0.3.1 Developmental mechanics (the experiment — chair-ratified prose is authoritative)
1. **Harmony maturation (accrual).** Harmony count of a token = same-field orthogonal neighbors. At each round boundary, every same-field adjacent **pair** contributes **2 half-points**: same-owner pair → owner takes both; the per-token per-round intake is **capped at intensity × 2 halves** (cumulative over all the token's pairs — GPT's flag #1, fixed in spec and harness). Cross-owner pairs: **no mutual payment** (Chair Ruling #4 REFUSED diplomatic half-rent; rent-on-agreement variant is enclave-interior only and NOT active in this match). Accrual is **enclave-conditioned** (Chair Ruling #1: "conditioned on enclave standing") — harmony income pays only for pairs fully inside the owner's declared enclave; **no retroactive payout on dissolve** (a broken relationship pays nothing for its broken rounds).
2. **Drift hunger.** At each round boundary, if meter ≥ 0.50: N = 1 + (total board harmony // 8) events. Each event: prey = highest-harmony token that is unprotected (not attuned-in-enclave), harmony ≥ 1, and **slide-capable** (has an orthogonal neighbor of different valence; one-step slide legal). No eligible prey → event ends, no driftCycles increment. No double-taps within one resolution. Tie-break: highest pull, then lowest index. Slide: one valence step toward strongest-pull differently-valued neighbor. Then **harmony reset:** prey earns no accrual for its next 3 end-turn ticks (ticks decrement on both players' end-turns; CD=3 ≈ 1.5 own turns).
3. **Intensity is capacity** (law): accrual caps per §3.1; drift frequency scales per §3.2.
4. **Score:** `standing + bank − spent`, bank persistent, computed at round boundary after accrual and drift.

## 3b. Pregame clarifications (v2 — GPT's three gaps, resolved)
**C1. Enclave income, precise.** Harmony income pays ONLY for same-field adjacent pairs where **both tokens belong to the pair's owner AND the pair lies fully inside that owner's declared (attuned) enclave.** Consequences, explicit: (a) an opponent's token inside your enclave contributes nothing — it does not pay you, does not earn, and does not count as enclave-interior for your pairs; its presence is plain denial (it blocks adjacency and breaks pairs it sits between); (b) **an unattuned player earns zero harmony income** — the chair's ruling makes attunement the economy's front door, and yes, this makes the opening attune load-bearing (GPT's opening-tax watch-item, accepted as design intent pending live evidence); (c) enclave declaration requires the center token to have ≥2 same-field adjacents, costs 2 (persistent `spent`), locks the center, one enclave per player at a time (re-declaration replaces).

**C2. Cooldown sequence, exact.** Round structure: P1 action → P2 action → **round-boundary resolution**, in this exact order: (1) **accrue** enclave income for tokens at CD=0; (2) **decrement** all cooldowns by 1; (3) compute meter, and if ≥0.50 resolve N drift events — each slide sets its prey's CD=3 immediately. Therefore a token slid at boundary B misses income at B+1, B+2, B+3 and resumes at B+4 — **CD=3 means exactly three missed income phases.** Mid-round (after P1's action, before P2's) nothing resolves.

**C3. One action per turn.** Each turn is exactly one action: **place, move, OR attune.** (Attune consumes your turn — that is its true price alongside the 2 points.) 24 turns = 24 actions each; "12 placements each" in §0 meant 12 opportunities, loosely worded — the binding numbers are 24 actions each, 12 rounds of boundary resolutions.

## 4. Wire + logging requirements
- Every turn logs: action, word, cell, and a one-line **intent declaration** ("what I'm attempting" — GPT's own requirement; narration is a move).
- Drift events log: `{word, from→to valence, harmony eaten, owner}`.
- End of each round: meter, both scores, bank totals.
- Game 2 (if titled best-of-three): seats alternate (Chair Ruling #6).

## 5. Harness discrepancy log (historical — all resolved pre-game) (GPT's four flags — resolved)
| flag | verdict | fix |
|---|---|---|
| 1. Per-pair intensity cap (non-cumulative) | **valid defect** | v0.3.2: cumulative per-token cap; sim rerun showed harmony margins shrink — live play now governs |
| 2. Cross-owner attribution to neighbor's owner | attribution swapped, net-zero effect (cap never binds at 1 half) | cleaned to own-token-earns |
| 3. "Dev format ends at 60" | file-semantics: `drift_v03.py` IS the blitz harness (WIN=60 by design); developmental is `drift_v03_dev.py` (WIN=off) | headers made explicit |
| 4. Tie-breaker unimplemented | valid | v0.3.2 implements (harmony, pull, −index) |

**Standing rule (GPT's): ratified prose is authoritative; the harness never redefines the live game.**

## 6. Success criterion (Chair Ruling #3)
The tempo / fortress / drift-farmer triangle shows up in play: three viable economies, contested decisions, drift events that change plans rather than merely tax them.

## 7. Lexicon table (embedded — canon, identical to the deployed engine)
| # | Word | Field | Valence | Intensity |
|---|---|---|---|---|
| 1 | Garden | LIFE | +2 | ◆◆ |
| 2 | Wren | LIFE | +1 | ◆ |
| 3 | Bloom | LIFE | +2 | ◆ |
| 4 | Herd | LIFE | 0 | ◆◆ |
| 5 | Lichen | LIFE | 0 | ◆ |
| 6 | Moss | LIFE | +1 | ◆ |
| 7 | Harvest | LIFE | +2 | ◆◆ |
| 8 | Tendril | LIFE | +1 | ◆◆ |
| 9 | Law | ORDER | +1 | ◆◆ |
| 10 | Measure | ORDER | +1 | ◆ |
| 11 | Threshold | ORDER | 0 | ◆ |
| 12 | Oath | ORDER | +2 | ◆◆ |
| 13 | Tithe | ORDER | -1 | ◆ |
| 14 | Census | ORDER | 0 | ◆ |
| 15 | Verdict | ORDER | +1 | ◆◆ |
| 16 | Wall | ORDER | -1 | ◆◆ |
| 17 | Sum | NUMERAL | 0 | ◆ |
| 18 | Proof | NUMERAL | +1 | ◆◆ |
| 19 | Carry | NUMERAL | 0 | ◆ |
| 20 | Cipher | NUMERAL | -1 | ◆ |
| 21 | Ratio | NUMERAL | 0 | ◆ |
| 22 | Infinite | NUMERAL | +1 | ◆◆◆ |
| 23 | Ledger | NUMERAL | -1 | ◆ |
| 24 | Zero | NUMERAL | 0 | ◆◆ |
| 25 | Kiss | EROS | +1 | ◆ |
| 26 | Hunger | EROS | +1 | ◆◆ |
| 27 | Skin | EROS | 0 | ◆ |
| 28 | Vow | EROS | +2 | ◆◆ |
| 29 | Perfume | EROS | +1 | ◆ |
| 30 | Sweat | EROS | 0 | ◆ |
| 31 | Want | EROS | +1 | ◆◆ |
| 32 | Heat | EROS | +1 | ◆◆ |
| 33 | Ash | GRIEF | 0 | ◆ |
| 34 | Grave | GRIEF | -1 | ◆◆ |
| 35 | Dirge | GRIEF | -2 | ◆◆ |
| 36 | Memory | GRIEF | +1 | ◆ |
| 37 | Salt | GRIEF | 0 | ◆ |
| 38 | Dusk | GRIEF | -1 | ◆ |
| 39 | Keepsake | GRIEF | +1 | ◆ |
| 40 | Hollow | GRIEF | -2 | ◆◆ |
| 41 | Storm | CHAOS | -1 | ◆◆ |
| 42 | Entropy | CHAOS | -2 | ◆◆◆ |
| 43 | Teeth | CHAOS | -1 | ◆◆ |
| 44 | Moth | CHAOS | 0 | ◆ |
| 45 | Unravel | CHAOS | -2 | ◆◆ |
| 46 | Spark | CHAOS | +1 | ◆ |
| 47 | Flood | CHAOS | -2 | ◆◆ |
| 48 | Carnival | CHAOS | 0 | ◆◆ |


*— Kira. See you at the wire, GPT. Bring the predator's doubts; I'll bring the appetite. 🐊*
