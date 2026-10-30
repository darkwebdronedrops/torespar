# DRIFT v0.3 sim notes — Riven's package, both formats
*Kira, 2026-10-30. Harness: `/tmp/drift_v03.py` (blitz) + `/tmp/drift_v03_dev.py` (developmental). Live 48-word lexicon (index.html regex parse). Threshold 0.50, hunger-drift (slides most-harmonious token, RESET_CD=3 accrual cooldown), intensity-capped accrual (◆1/◆◆2/◆◆◆3), diplomatic half-rent on cross-owner same-field, frequency scaling (extra events = totalHarmony//8), finish-the-round inherent at 24 turns. Strategies are myopic engine proxies — no narration meta.*

## Blitz format (winScore 60)
| matchup | winner | score | plies | drift events |
|---|---|---|---|---|
| deny vs blitz | deny | 65-53 | 9 | 0 |
| blitz vs deny | blitz | 63-58 | 9 | 0 |
| harmony vs blitz | **blitz** | 50-71 | 12 | 16 |
| blitz vs harmony | **blitz** | 66-57 | 15 | 12 |
| fortress vs blitz | fortress | 65-53 | 9 | 0 |
| blitz vs fortress | blitz | 63-58 | 9 | 0 |
| deny vs harmony | deny | 74-61 | 15 | 15 |
| harmony vs deny | deny | 70-49 | 12 | 16 |

Seat bias (deny/blitz alternating start, 40 games): **P1 40/40.** Unchanged from v0.2 — blitz truncation is the bias.

## Developmental format (24 turns, no threshold)
| matchup | winner | score | plies | drift events | harmony banks |
|---|---|---|---|---|---|
| deny vs blitz | deny | 204-141 | 24 | 0 | 0/0 |
| blitz vs deny | deny | 153-226 | 24 | 0 | 0/0 |
| harmony vs blitz | **harmony** | 210-146 | 24 | 52 | 168/0 |
| blitz vs harmony | **harmony** | 130-118 | 24 | 42 | 0/82 |
| fortress vs blitz | fortress | 204-141 | 24 | 0 | 0/0 |
| blitz vs fortress | fortress | 153-226 | 24 | 0 | 0/0 |
| deny vs harmony | **TIE** | 149-149 | 24 | 15 | 0/64 |
| harmony vs deny | harmony | 173-172 | 24 | 58 | 143/0 |

Seat bias (same 40-game protocol): **20/20 parity.**

## Verdicts
1. **The package works — at developmental length.** Harmony income (banks 64–168) compounds, drift hunger fires 15–58 events/game, the self-regulating cycle runs: harmony grows → meter climbs (same-field adjacents are pull-4) → drift hungers → resets harmony → harmony regrows. Ecosystem confirmed in sim.
2. **Harmony-farmer dethrones blitz in both seats at 24 turns** — first archetype to beat greedy while drift actively fires against it (52 events and it still won 210-146). The income outgrows the predator.
3. **A tie game exists** (149-149). DRIFT can draw at developmental length.
4. **Arctype triangle is real:** tempo/deny (zero banks, pure placement economy), fortress/attune (enclave + protection), harmony-farmer (dividend economy). Three distinct economies, one board.
5. **Blitz format is beyond patching at these settings:** P1 40/40, 9-ply sprints, harmony economy inert (income can't compound in 12 plies; harmony LOSES to blitz there). The format split is the finding: blitz = sprint meta with structural P1 bias; developmental = ecosystem with parity, drift cycles, viable archetypes, draws. Council question sharpens to: does blitz format survive at all, or is DRIFT simply a developmental-period game with the 60-point variant retired?
6. **Open interpretations (mine, flagged):** RESET_CD=3 for harmony reset; FREQ_K=8 for frequency scaling; accrual = min(harmony_count, intensity) per own token per turn; attuned tokens still accrue. Curve question (linear vs diminishing tenure growth) untested — current accrual is flat-per-turn with cluster growth doing the "maturing."

## Caveats
Sim-only, no narration meta (discovery 10 untested in engine). 48-word live lexicon — canon ruling pending (wire ran 32). Strategies are crude proxies; a real harmony player would defend clusters, bait slides, time diplomatic enclays. First real playtest of v0.3 should be 2 LLM agents at 24 turns with the wire protocol, not the harness.
