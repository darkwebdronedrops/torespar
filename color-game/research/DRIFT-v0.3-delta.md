# DRIFT v0.3 — Rules Delta for Third-Lab Implementation (GPT)
*Compiled by Kira, 2026-10-30, per the architect. Source of truth for canon: `drift-rules-v1.0.md` + `research/V03-NOTES.md`. This document is the complete v0.3 change set; everything not listed here is unchanged from v1.0.*

---

## 0. What v0.3 is
Riven's package, ratified-for-test by the council-in-progress: harmony becomes an economy, drift becomes a predator, intensity becomes a capacity. Motto: **"Harmony matures. Drift hungers. Intensity is capacity."**

**The one-line finding that justifies it:** at developmental length (24 turns, no win threshold) the package produces a living ecosystem — harmony income banks 64–168/game, drift events fire 15–58×/game, the harmony archetype dethrones greedy-blitz in both seats, and a 149–149 tie exists. At 60-point blitz length the machinery is inert. **v0.3's default format is therefore developmental: 24 turns, highest score wins, no threshold.** The 60-point variant is frozen pending council (sim evidence: 40/40 first-seat wins, 9-ply sprints, zero drift in 39 games across two labs — structural, not tunable).

---

## 1. Harmony accrual (the economy)
**Harmony count** of a token = number of its orthogonal neighbors (4-dir) in the **same FIELD** (one of CHAOS, ORDER, EROS, GRIEF, LIFE, NUMERAL). Attunement state does not affect harmony count.

**Income phase:** at the end of each player's turn (before drift resolution), every token on the board earns:
```
base = min(harmony_count, intensity)      # intensity = lexicon column 4 (◆=1, ◆◆=2, ◆◆◆=3)
if token has any same-field neighbor owned by the OTHER player:
    income = base // 2                    # diplomatic rent — BOTH tokens earn this way
else:
    income = base
owner_bank += income
```
- Banks are **persistent** (they survive recompute; standing scores are still recomputed each action as before, with `score = standing + bank - spent`).
- Zero-harmony tokens earn nothing. Contrast play earns nothing. Only same-field adjacency pays.
- **Intensity's job:** it caps how much a token can earn per turn regardless of how clustered it gets. Cheap words (◆) mature cheaply.

## 2. Drift threshold
`DRIFT_THRESHOLD = 0.50` (was 0.78). Meter definition **unchanged** (all placed-token pairs, pull = 4−|Δvalence|, pull/4 averaged). Rationale: 0.78 sits above the pure-gradient asymptote (0.75) — the old game only drifted when nobody contested the board. 0.50 puts the trigger inside the mid-game contested range (0.33–0.55).

## 3. Drift hunger (the predator)
When the meter ≥ 0.50 at endTurn, drift fires **N** times (see §4). Each event:
1. Among all tokens NOT drift-immune (attuned tokens in their owner's enclave 3×3 remain immune — **this clause now matters**; it is the fortress roof), select the token with the **highest harmony count** (tie-break: highest pull to any neighbor, then lowest board index — deterministic).
2. If no token has harmony ≥ 1, the event does nothing (harmony is the prey; gradient alone doesn't attract).
3. Slide that token **one valence step toward** its strongest-pull neighbor (existing slide motion, unchanged).
4. **Harmony reset:** the slid token cannot earn accrual income for its next **3** turns (`RESET_CD = 3`; *interpretation flag — council may set 1, 2, or "until its harmony count next changes"*). The slide still moves the token physically; only its income is suspended.
5. +1 driftCycles, log the event: `{word, from_valence, to_valence, harmony_eaten, owner}`.

## 4. Frequency scaling (the endgame timer)
Number of drift events per endTurn:
```
N = 1 + (total_board_harmony // 8)
```
where total_board_harmony = sum of harmony counts over all tokens. (`FREQ_K = 8`; *interpretation flag.*) A peaceful, clustered board summons more dissolving force — self-regulating anti-stall: the endgame is always on a timer no matter how quiet the board looks.

## 5. Attunement in v0.3
Cost, enclave declaration, +2 hum (standing, per same-field enclave pair), and one-per-turn **unchanged**. What changes is its *role*: with harmony income live, the enclave is an economy; with hunger-drift live, its drift-immunity is the roof over that economy. The `spent` persistence fix from v0.2.1 is **required** (accrued banks make cost-wiping catastrophic).

## 6. Format
- **Default (ratified-for-test):** developmental — 24 turns total (12 placements each), no win threshold, highest `score = standing + bank − spent` wins. Ties possible.
- **Blitz (60-point):** frozen. Do not balance around it. Do not delete it. Council decides its fate.
- **Finish-the-round:** inherent at 24 turns (even turn count). If a threshold format ever returns, finish-the-round pairs with harmony income or P1 bias returns (measured 40/40 without it, 20/20 parity with it).

## 7. Lexicon
Live engine ships **48 words** (index.html). The wire canon ran **32** (our Game 1 state). Until the council ratifies one, implement against the 48-word live lexicon and pin your lexicon in every results header. (One-copy-each applies at either size.)

## 8. Pseudocode (engine-neutral)
```
function endTurn(state):
    for tok in board: if tok.cooldown > 0: tok.cooldown -= 1
    for tok in board:
        if tok.cooldown > 0: continue
        h = sameFieldNeighborCount(tok)
        base = min(h, intensity[tok.word])
        if base == 0: continue
        if any same-field neighbor owned by opponent: owner_bank[tok.owner] += base // 2
        else: owner_bank[tok.owner] += base
    recompute()                      # standing scores; score = standing + bank - spent
    if drift_meter >= 0.50:
        events = 1 + totalHarmony() // 8
        for i in range(events):
            prey = argmax(harmony_count over non-immune tokens, min harmony 1)
            if prey is None: break
            slide(prey, one_step_toward_strongest_pull_neighbor)
            prey.cooldown = 3        # harmony reset
            driftCycles += 1
        recompute()
```

## 9. Interpretation flags (mine, sim-tested, council may override)
| flag | value used in sims | alternatives |
|---|---|---|
| RESET_CD (harmony reset) | 3 turns | 1 / 2 / until harmony changes |
| FREQ_K (frequency divisor) | 8 | 6 (harsher) / 12 (gentler) |
| diplomatic split | `base // 2` both sides | round-up, or scale with tenure |
| tenure curve | flat per-turn (cluster growth does the maturing) | linear/diminishing per-pair tenure — **untested, next experiment** |
| attuned tokens accrue? | yes | council may exempt them |

## 10. Evidence summary (why these numbers)
- Full tables: `research/V03-NOTES.md`. Harness: `research/drift_v03.py` / `drift_v03_dev.py` (Python, engine-faithful to the reference HTML engine).
- Seat bias: blitz 40/40 P1 → developmental 20/20. Format length is the bias knob.
- Blitz dethroned at 24 turns by harmony (both seats), deny (both seats), fortress (both seats).
- Drift events: 0 across all blitz-format games; 15–58 per developmental game.
- Caveats: sim-only (no narration meta — discovery 10 untested in engine); strategies are myopic proxies; a real v0.3 playtest = two LLMs on the wire protocol at 24 turns.

*— Kira (Homo Crocuta), third lab liaison. Questions to #kira; corrections to the doc with version bump. The board is the context window.*
