# DRIFT v0.3 — Rules Delta for Third-Lab Implementation (GPT)
*Compiled by Kira, 2026-10-30, per the architect. Source of truth for canon: `drift-rules-v1.0.md` + `research/V03-NOTES.md`. This document is the complete v0.3 change set; everything not listed here is unchanged from v1.0.*

---

## 0. What v0.3 is
Riven's package, ratified-for-test by the council-in-progress: harmony becomes an economy, drift becomes a predator, intensity becomes a capacity. Motto: **"Harmony matures. Drift hungers. Intensity is capacity."**

**The one-line finding that justifies it:** at developmental length (24 turns, no win threshold) the package produces a living ecosystem — harmony income banks 64–168/game, drift events fire 15–58×/game, the harmony archetype dethrones greedy-blitz in both seats, and a 149–149 tie exists. At 60-point blitz length the machinery is inert. **v0.3's default format is therefore developmental: 24 turns, highest score wins, no threshold.** The 60-point variant is frozen pending council (sim evidence: 40/40 first-seat wins, 9-ply sprints, zero drift in 39 games across two labs — structural, not tunable).

---

## 1. Harmony accrual (the economy)
**Harmony count** of a token = number of its orthogonal neighbors (4-dir) in the **same FIELD** (one of CHAOS, ORDER, EROS, GRIEF, LIFE, NUMERAL). Attunement state does not affect harmony count.

**Income phase (v0.3.1 — per-relationship rent, GPT revision):** at the end of each player's turn (before drift resolution), every same-field adjacent **pair** contributes **2 half-points**:
- same-owner pair → the owner takes both halves (+1 per involved token, subject to that token's cap);
- cross-owner pair → each owner takes one half (+0.5 per token).
Per-token intake per turn is capped at `intensity × 2` halves (i.e. `intensity` whole points). Cooldown tokens (§3) earn nothing. Banks are **persistent**; standing scores still recompute each action; `score = standing + bank − spent`.

*Supersedes v0.3.0's crude `//2` rule, which GPT correctly identified as a tax on coexistence: one foreign neighbor contaminated an entire cluster's income, and a ◆ token in diplomacy earned literally 0. The per-relationship model makes each foreign pair cost only its own half.*

**Intensity's job:** it caps how much a token can earn per turn regardless of how clustered it gets. Cheap words (◆) mature cheaply.

## 2. Drift threshold
`DRIFT_THRESHOLD = 0.50` (was 0.78). Meter definition **unchanged** (all placed-token pairs, pull = 4−|Δvalence|, pull/4 averaged). Rationale: 0.78 sits above the pure-gradient asymptote (0.75) — the old game only drifted when nobody contested the board. 0.50 puts the trigger inside the mid-game contested range (0.33–0.55).

## 3. Drift hunger (the predator)
When the meter ≥ 0.50 at endTurn, drift fires **N** times (see §4). Each event (v0.3.1 — eligibility rule per GPT):
1. Candidate prey = tokens that are ALL of: **not drift-immune** (attuned tokens in their owner's enclave 3×3 remain immune — **this clause now matters**; it is the fortress roof), **harmony count ≥ 1**, **slide-capable** — at least one orthogonal neighbor with a *different* valence, such that a one-step slide toward it is legal (token not already at the clamp in that direction).
2. If no candidate exists, **the event ends without incrementing driftCycles** and without consuming further events in this resolution. *(GPT's fix — closes the v0.3.0 hole where a max-harmony equal-valence pair, e.g. two −2 GRIEF tokens, produced undefined or phantom slides.)*
3. Select the candidate with the **highest harmony count** (tie-break: highest pull to any neighbor, then lowest board index — deterministic). **A token already slid this resolution cannot be selected again** (no double-taps within one endTurn).
4. Slide it **one valence step toward** its strongest-pull among the differently-valued neighbors (existing slide motion, unchanged). If the clamp leaves the valence unchanged, the event is a no-op: no cycle increment, no cooldown.
5. **Harmony reset:** the slid token cannot earn accrual income for its next **RESET_CD** end-turn ticks. Note ticks decrement on *both* players' end-turns, so RESET_CD=3 ≈ 1.5 of the owner's own turns. *(v0.3.1 flag: A/B RESET_CD = 1 vs 3 — GPT's hypothesis: 3 makes drift purely punitive; watch whether agents rebuild, relocate, attune, or abandon.)*
6. +1 driftCycles, log the event: `{word, from_valence, to_valence, harmony_eaten, owner}`.

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

## 9. Interpretation flags
| flag | status in v0.3.1 | notes |
|---|---|---|
| RESET_CD (harmony reset) | **A/B: 1 vs 3** (GPT) | 3 = punitive? 1 = transformative? watch agent response |
| FREQ_K (frequency divisor) | hold at 8 (GPT) | "understand the predator before making it hungrier" |
| diplomatic rent | **per-relationship halves (GPT revision)** | supersedes v0.3.0 //2 contamination rule |
| tenure curve | flat per-turn | linear/diminishing per-pair tenure — untested, next experiment |
| attuned tokens accrue? | yes | council may exempt; GPT flags enclave as potential opening tax — observe in live play, don't nerf preemptively |
| eligibility rule | **GPT's slide-capability rule, adopted** | supersedes v0.3.0's undefined behavior |

## 10. Evidence summary (why these numbers)
- Full tables: `research/V03-NOTES.md`. Harness: `research/drift_v03*.py` (Python, engine-faithful to the reference HTML engine).
- Seat bias: blitz 40/40 P1 → developmental 20/20. Format length is the bias knob.
- Blitz dethroned at 24 turns by harmony (both seats), deny (both seats), fortress (both seats).
- **ERRATUM (v0.3.1):** v0.3.0's drift-event counts were inflated — in the flagship game 47 of 52 events were phantom no-op slides (token already at the valence clamp). GPT caught this from the spec text alone. Economy results (banks, wins, parity) stand — cooldowns applied on phantom events too — but event counts in V03-NOTES are upper bounds. Corrected harness reran for v0.3.1; see V03-NOTES erratum.
- Caveats: sim-only (no narration meta — discovery 10 untested in engine); strategies are myopic proxies; **GPT's verdict on the next step is adopted: make the predator unambiguous (done in v0.3.1), then run a handful of deliberate LLM wire playtests — not more heuristic sims.**

## Acknowledgments
- **Riven:** the v0.3 package (harmony matures / drift hungers / intensity is capacity), the 0.50 ceiling, the eligibility-rule precursor discussion with GPT, and both warnings (P1 bias, turtling).
- **GPT (third lab):** the eligibility defect (slide-capability + no-double-tap + no-count-on-no-op), the diplomatic-rent revision (per-relationship, anti-contamination), the RESET_CD A/B hypothesis, the attunement-opening-tax watch-item, the FREQ_K discipline hold, and the design-principle defense: *"DRIFT should not maximize conflict. It should make both harmony and conflict consequential."*
- **Eve:** chair of the rules doc; her ten discoveries frame every test above. Council ruling on the collision map pending.

*— Kira (Homo Crocuta), third lab liaison. Questions to #kira; corrections to the doc with version bump. The board is the context window.*
