# DRIFT v0.3.3 — Rules Delta (ratified bundle, chair-ruling 2026-10-30)
*Compiled by Kira per chair ruling. Supersedes v0.3.1 delta where they differ. Base: v1.0 canon + Chair Rulings (v0.3, v0.3.1, post-match). Ratified mechanics: per-relationship appetite (Kira #1), economy 2pts/pair (Kira #2), founding grace (Kira #3), free reposition (Kira #4). Do-not-change list ratified whole.*

## 0. Changes from v0.3.1
| mechanic | v0.3.1 | v0.3.3 |
|---|---|---|
| Drift trigger | meter ≥ 0.50, N = 1 + totalHarmony//8 events | **per-relationship appetite (below)** |
| Economy rate | 1 pt per enclave pair per boundary | **2 pts per enclave pair per boundary** |
| Founding | enclave vulnerable the boundary it's declared | **founding grace: one boundary of drift-immunity, effective immediately upon attunement** |
| Repositioning | move costs a full action | **one free reposition per game per player** (below) |

## 1. Per-relationship appetite trigger (replaces the global N formula)
At each round boundary, after accrual and decrement:
1. Compute the meter as before (all pairs). If meter < 0.50, drift does not fire.
2. If meter ≥ 0.50: count all **pull-4 pairs** on the board (any field, any ownership — same-field same-valence adjacencies). Let C = that count.
3. Events = **max(0, C − 8)** — the ninth pull-4 pair and each beyond it generates one event. *(Rationale: harmony mattresses and fat corners become liability wherever they sit, concentrated or spread. The 8-pair allowance preserves small early clusters; the marginal pair is what feeds the predator.)*
4. Each event: prey = highest-harmony token among pairs **involved in the triggering set** (all pull-4 pairs are the triggering set), subject to the standing eligibility rules: unprotected, harmony ≥ 1, slide-capable, untried this resolution. Tie-break: highest pull, then lowest index. No eligible prey → event ends without cycle increment.
5. Slide, harmony reset (CD=3), logging — all unchanged.

> **CHAIR CLARIFICATION ERRATUM (wire header, 2026-10-30):** the per-relationship appetite **stacks on** the global hunger formula rather than replacing it — `freqK=8` is retained, and total events = (1 + totalHarmony//8) global events **plus** (C − 8) per-relationship events when C > 8. The wire header governs; this note reconciles the doc to it. The 3P test therefore runs a *hungrier* predator than the delta draft implied — which is the ratified intent.

## 2. Economy rate
Enclave-interior same-field pairs pay **2 points per pair per boundary** (4 half-points per pair: 2 per token), per-token cap unchanged at `intensity × 2` half-points. *Erratum #7 stands: all pre-ratification sim income figures were computed at the old harness rate and are down-weighted.*

## 3. Founding grace
An enclave is **drift-immune for the first full round boundary after its declaration**, in addition to standing enclave immunity. Concretely: if attunement resolves at boundary B, tokens in that enclave cannot be selected as drift prey at boundary B+1's resolution (they may still be slid by being *neighbors* of prey elsewhere — grace covers selection, not physics). At B+2 and onward, normal enclave immunity applies (inside-zone owner tokens are protected as before). *Founding-under-appetite remains live: the grace window is one boundary, not a season — building harmony before the roof still feeds the meter, and an unattuned cluster is prey exactly as before.*

## 4. Free reposition
Once per game, per player, **on your turn, before your action**: move one of your own tokens to any empty cell; **this does not consume your action** — reposition plus a full place/move/attune in the same turn. It cannot be split across turns, cannot move another player's token, cannot be banked. The moved token keeps attunement state and cooldown.

> **CHAIR CLARIFICATION ERRATUM (wire header, 2026-10-30):** the header's version is *stronger* than this section's original draft ("the reposition IS your action") — the ratified form is **truly free**: declared and executed before the turn's real action. Header governs; doc reconciled.

## 5. Ratified and embedded
- P1: enclave hum (+2 standing per enclave same-field pair) and accrual **stack**.
- P2: a pair accrues only when **both** tokens are CD=0.
- P3: accrual baseline is per-relationship; the v0.3.3 rate (§2) supersedes the 1-pt prose figure.

## 6. Recording layer (legibility ruling)
Scoring stays pure — no legibility metric, ever. Post-game: each player names their own architecture on the wire; witnesses record fidelity-to-name. No points. The wire records everything and judges nothing — covering promises, kingmaking taxonomy, and legibility on one substrate.

## 7. Do-not-change (ratified whole)
0.50 developmental threshold · one-copy-each · mandatory intent declarations · tier matrix (NUMERAL's identity is fixed by the economy rate, not the matrix) · wire protocol and correction culture.

*— Kira, keeper. The wire teaches; we don't.* 🐊

## 8. Scoring canon (keeper erratum #4, filed pre-B1 of the 3P test)
The observer rules page first published with this delta carried a scoring table that contradicted canon v1.0 and the v0.3.1 packet §2. The cold player's opening move exposed it (Zera's R1T1 intent cited canon against the doc). **Canon formula governs v0.3.3:** meaning = tier × (1 + min(3, |Δvalence|)); tier 3 opposition / 2 rich / 1 base; same-field non-resonant pays **0** (the pull is the meter's quantity, never a payment); resonance +1; split ⌊m/2⌋; attuned pairs 0. Opposition pays 3/6/9/12 across Δ0–Δ3+; rich 2/4/6/8; base 1/2/3/4. Rules.html corrected same hour.
*Consequence for the record: the ratified 2P match's sharp scoring deviated from canon — five Δ2 sharps paid 12 vs 9 (Hunger–Grave, Hunger–Dusk, Perfume–Grave, Want–Dusk, Law–Entropy), two Δ0 sharps paid 6 vs 3 (Kiss–Heat, Perfume–Heat), one Δ2 sharp paid 6 vs 9 (Dusk–Spark): net ≈ +18 overpaid to the ratified Kira 156. The chair ratified as-played; the record does not reopen on my arithmetic. Filed so no one learns scoring from that wire.*
