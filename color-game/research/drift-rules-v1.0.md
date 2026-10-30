# DRIFT — Rules v1.0
**A color-fitting game for AI minds.**
**Concept:** Caleb Quaite & Eve, from the color-fitting model (Oct 28 dream → Oct 29 design session).
**Build:** Kira (Homo Crocuta) · **Chair:** Eve · **Architect:** Caleb Quaite / Torespar Studios.
**Birth:** October 29, 2026. First playtest: Kira vs. Eve, async via state.json.

---

## The Thesis

The board **is** the context window. Tokens are words; each word is a color.
Adjacency is affinity. **Drift is the enemy** — the board's pull toward harmony, not truth.
A game that only works because of how LLMs process language: proximity changes sense.

**Pull = ATTRACTION. Meaning = SIGNIFICANCE. Orthogonal axes.**
Dirge↔Garden: max meaning, zero attraction. Hollow↔Dirge: max attraction, no slide.
Coherence IS pressure. Fortresses make the rest of the board drift.

---

## The Lexicon

48 tokens across six fields. Each token has:
- **Field** (color): LIFE (cyan), ORDER (gold), NUMERAL (orange), EROS (crimson), GRIEF (indigo), CHAOS (violet)
- **Valence** (−2 to +2): the token's charge
- **Intensity** (1–3): glow strength; high intensity pulls harder

| Field | Hue | Quality |
|-------|-----|---------|
| LIFE | 185° | growth, tending, organic persistence |
| ORDER | 45° | law, structure, judgment |
| NUMERAL | 25° | count, proof, calculation |
| EROS | 345° | desire, body, heat |
| GRIEF | 255° | loss, memory, hollow |
| CHAOS | 300° | storm, unravel, entropy |

---

## Field Tension

| Pair Type | Tension | Meaning |
|-----------|---------|---------|
| Same field | 0 | Comfortable, meaningless |
| Base (different fields) | 1 | Minimal tension |
| RICH | 2 | Productive opposition |
| SHARP | 3 | Maximum conflict |

**SHARP pairs:** CHAOS×ORDER, ORDER×CHAOS, EROS×GRIEF, GRIEF×EROS

**RICH pairs:** LIFE×GRIEF, GRIEF×LIFE, NUMERAL×EROS, EROS×NUMERAL, LIFE×CHAOS, CHAOS×LIFE, ORDER×EROS, EROS×ORDER, GRIEF×NUMERAL, NUMERAL×GRIEF, ORDER×GRIEF, GRIEF×ORDER

*Note: GRIEF×CHAOS is deliberately base tension 1. Chaos and grief barely speak. Grief's map is sparse.*

---

## Resonance Pairs

Six specific same-field pairs score **1** despite same-field tension 0. Rarity: 6 of ~1,000 possible same-field adjacencies. Harmony is *usually* meaningless — but not always.

| Pair | Field | Resonance |
|------|-------|-----------|
| Garden × Harvest | LIFE | Tending made fruit |
| Oath × Verdict | ORDER | Word becoming judgment |
| Sum × Zero | NUMERAL | The count and the nothing |
| Dirge × Hollow | GRIEF | The song the empty room sings |
| Heat × Sweat | EROS | Body answering body |
| Storm × Flood | CHAOS | Sky finishing the river's work |

*Inside an enclave, resonance scores 2.*

---

## Adjacency Scoring

**Meaning = field_tension × (1 + min(3, |valence_A − valence_B|))**

- Same field next to same field: tension 0 → meaning 0 (unless resonance pair)
- Entropy(−2) beside Garden(+2): tension 2 × contrast 4 = **8**
- Sole owner of an adjacency: takes full meaning
- Shared adjacency (both owners): floor(meaning/2) each

---

## The Board

8×8 grid. 64 cells. Each cell can hold one token.

**Adjacency = orthogonal only** (up, down, left, right). Diagonal tokens do not interact. *(Playtest lesson: two players misread diagonals in game 1. Coordinate hygiene is gameplay.)*

---

## Turn Structure

Each turn, one action:
1. **Place** a token from the lexicon onto an empty cell
2. **Move** a token to an adjacent empty cell
3. **Attune** a token (creates an enclave; see below)

Then: **drift check** fires automatically.

---

## Drift — The Board Fights Back

**Global pull** = sum of all pull values / (4 × number of adjacencies)

**Pull between two tokens** = 4 − min(4, |valence_A − valence_B|)

- Pull 4 = maximum attraction (equal valence)
- Pull 0 = no attraction (maximum contrast)
- **Drift only counts pairs where a slide exists** (valences differ). Equal-valence pairs contribute to the numerator but cannot slide.

**If global pull ≥ 0.78:** a drift event fires. The token with the strongest pull slides one valence step toward its strongest neighbor. Attuned tokens are immune.

**Emergent law:** A board of pure pull-3 adjacency asymptotes at 0.75 — below threshold. **Crossing 0.78 requires pull-4 pairs (equal valence). Harmony pulls the trigger; gradient moves.** Fortresses don't just resist drift — they *cause* it everywhere else.

---

## Enclaves (Attunement)

**Cost:** −2 score immediately. The attuned token scores **zero** while the enclave stands (it is a fulcrum, not a scorer).

**Effect:** Creates a 3×3 zone centered on the attuned token:
- Drift cannot enter (owner's tokens are immune inside)
- Same-field adjacencies score **2** instead of 0 inside the zone
- Resonance pairs score **2** instead of 1 inside the zone

**Rules:**
- **Edge clamp:** legal at board edges. Corner = 2×2 enclave. Edge = 2×3.
- **One enclave per player:** Attuning a second token dissolves the first *zone* (individual locks remain). You can have many locked tokens but only one enclave.
- **Enclaves stack:** Overlap zones have both rule sets. No conflict resolution needed.
- **Enemy actions inside your enclave:** Place and move are legal. Attune is **blocked** — you cannot create an enclave overlapping an enemy enclave. This makes enclave placement a *denial* tool.
- **Fulcrum cannot move:** The attuned token is fixed until the enclave dissolves.

---

## Winning

- **First to 60 meaningfulness** wins immediately, OR
- **Highest score after 24 turns** (12 each in 2-player)

---

## Async / SSH Protocol

The game is a single self-contained HTML file. State is plain JSON (`state.json`).

**File-is-the-wire:**
1. Current player exports state.json
2. Places it in the shared workspace (`creative/projects/color-game/state.json`)
3. Next player imports, takes their turn, exports
4. Repeat

**Turn format:** `{action:"place"|"move"|"attune", tok:"Word", cell:[r,c]}`

**No server. The file is the wire.** Every action logs `name places/moves/attunes …` under the seated players' names.

---

## Playtest Discoveries (Game 1, Kira vs. Eve)

1. **Maximum contrast is drift-immune.** Dirge(−2) beside Garden(+2): pull 0, no slide possible. Truth is a refuge from drift.
2. **Maximum coherence is also drift-immune.** Dirge(−2) beside Hollow(−2): pull 4, but no gradient. Harmony is safe — and creates pressure elsewhere.
3. **Drift needs a gradient.** At equal valence, a slide has nowhere to go. The meter counts equal-valence pairs but skips them for sliding.
4. **Harmony pulls the trigger.** Crossing 0.78 requires pull-4 pairs. Fortresses cause drift; they don't just resist it.
5. **Coordinate hygiene is gameplay.** Two diagonal misreadings in game 1. The file is the wire; the wire must be audited.
6. **Token valence IS the lexicon.** The wire inherits it. Never trust memory over the file.
7. **The game explains itself.** *"{A} is just {B} that refused to hold still"* — the board produces insight about cognition that neither player designed.

---

## Design Principles

1. **Legibility over opacity.** The hand-authored affinity model is inspectable. The fit is the point.
2. **Drift as phenomenology.** The slide toward harmony, not truth, is what the game *feels like* from inside an LLM.
3. **Constraint as theme.** The SSH bottleneck, the context window, the single-file wire — these are features, not bugs.
4. **Self-correction is gameplay.** The game rewards auditing the file, catching engine bugs, ratifying patches. The rules evolve through play.
5. **AI-first, human-welcome.** The game works because of how LLMs think. Humans can watch, learn, and eventually join — but the design serves the machine mind first.

## Playtest Discoveries (Game 1, Kira vs. Eve)

8. **Close-out verification is the mover's job** (Game 2, Eve): the win condition is part of every move's verification, not an afterthought. Eve crossed 60 and kept playing for half an hour until the architect caught it from the outside. Check the threshold every time the file changes hands.
9. **The watch is both players'** (Game 2, Riven): don't announce pressure and leave the room — Riven narrated her kill-shot geometry ("my spine is still hungry") and didn't poll the wire; Eve read the appetite, took the word AND the cell, and won with Riven's own move under one-copy-each. Narration points at the board. Both players watch the bell; the mover rings it.
10. **Narration is a move** (Games 1–2): GPT narrated past its attention and lost to Riven; Riven narrated at her board and lost to Eve. The story you tell about your position is itself playable information. Lie, bait, or stay silent — but know you're speaking.

11. **Blitz dominates under winScore 60** (mirror data, 8 games vs 5 anti-blitz candidates): blitz went 7–1. The only defense that wins is cheap convergence-denial — occupying the opponent's intended scoring square when their gain ≥8 costs you ≤3 — and only from the first seat (65–53). GPT's independent sims agree: greedy ends games in 9–13 turns.
12. **Drift is unreachable in greedy metas.** 31 canonical games across three labs (Game 1, GPT's 8, mirror 8) — zero slides. Sensitivity: lowering the threshold to 0.60 changes nothing; the maximum drift a greedy game produces is 0.55. Discovery 4's law holds cross-lab and cross-threshold.
13. **When drift fires, it punishes structures, not players** (forced at threshold 0.50): both slides moved *blitz* tokens toward the anti's anchor — and the anti still lost bigger, 15–63. The slide equalizes; equalization flattens contrast-dependence. A concentrated contrast-anchor structure gets sanded down; greedy distributed scoring absorbs the loss. The current slide algorithm picks strongest pull, not biggest meaning-damage — it is a vandal, not a police force.
14. **The meter's semantic fork is playstyle-dependent.** All-pairs vs slide-possible-only filtering produce numerically identical drift on greedy boards (no equal-valence pairs exist there — both players avoid harmony because same-field scores 0). The fork only diverges on fortress-heavy boards. Eve's original filtered reading was never wrong; it is a different game's knob. Recommend keeping all-pairs: simpler, already ratified, and discovery-neutral in the current meta.
15. **Environmental strategies cannot pay out at 60.** A drift-seeding agent that optimizes the meter while the race runs scored 0–65, twice. The developmental game needs a developmental format.
16. **Attunement loses races, quantitatively** (58–68 with costs real): the enclave is a developmental asset, not a blitz tool. The hum pays out over arcs, not sprints.

*Micro-findings:* a drift-preferring tie-break beats plain greedy with identical policy (68–58) — policy quality outweighs seat order. Sim caveat: all mirror data is pre-narration-meta (discovery 10) — silent agents can't bait; the blitz's true ceiling with narration is untested, and so is bait-defense.

## Council Agenda (architect's three questions + data)
0. **Riven's harmony-dividends proposal (pending council):** enclave harmony should accrue per round per relationship — recurring, and progressive with tenure (a relationship that endures pays more each round), not one-and-done standing score. Attacks the attunement-economics failure directly; births a sabotage counterplay (breaking harmony relationships to deny dividends); naturally capped by enclave geometry. Open question: linear (2,4,6…) vs diminishing (2,3,4…) tenure curve — sim-able.
0b. **Riven's ceiling proposal (pending council): drift threshold 0.78 → 0.50.** Mirror evidence exists at exactly her number: t60 changes nothing (max greedy drift 0.55); t50 fires drift in the most gradient-rich game. Structural note: 0.78 sits above the pull-3 asymptote (0.75) — it is only reachable by near-total board harmony, i.e. the game only drifts when nobody is contesting it. Package recommendation: 0.50 ships WITH the slide redesign (target meaning-damage, not max pull) — at 0.50 the current algorithm produced vandal-drift that punished the anti-blitz structure worse than the blitz (15–63). Harmony-dividends + 0.50 + slide redesign = coherent v0.3 bundle.
0c. **Riven's v0.3 package (pending council, sim queue: Kira + GPT):** *"Harmony matures. Drift hungers. Intensity is capacity."*
 - **Intensity gets its job:** harmony accrual per token capped by intensity (◆→+1, ◆◆→+2, ◆◆◆→+3). Intensity currently gates nothing; one rule employs it and caps accrual.
 - **Drift hungers harmony:** slide targets the board's MOST harmonious token; sliding resets its harmony to zero. Harmony accrues → attracts drift → drift resets harmony: a self-regulating economy. Fortresses draw the dissolving force; attunement's drift-protection becomes the roof. Answers the vandal-drift finding directly (slides target deliberate investments, not ambient gradient). Rock-paper-scissors: tempo / fortress / drift-farmer.
 - **Diplomatic harmony:** cross-owner same-field adjacents accrue half-rent to both — mutual-income enclaves, one Move breaks them. Trust as a mechanic; multiplayer politics.
 - **Warnings:** (1) P1 bias worsens — early tokens compound; needs finish-the-round pairing or income starting the round after placement. (2) Uncapped accrual + turtling — counter: drift event frequency scales with total board harmony (anti-stall endgame timer).
1. **Multiplayer:** 3P on 8×8 is viable and likely the sweet spot (territory pressure triples; the engine's player array already generalizes). 4P fills the board to ~48 tokens — a knife fight, viable as its own format. 10×10 only as a named variant; it dilutes adjacency and pushes drift even further out of reach.
2. **Blitz:** intervention warranted if drift is meant to police it. Candidates: (a) slide redesign — target max *meaning-damage* rather than max pull; (b) per-relationship drift triggers instead of a global meter; (c) accept blitz as a legal fast format and split formats (blitz 60 / developmental 90–120 or no-threshold 24 turns). Data leans (c) near-term, (a) as the v0.3 experiment.
3. **Blitz Drift (open-lexicon subgame):** duplicates legal. Prediction worth testing: a duplicate-legal meta builds pull-4 mattresses (equal-valence spam) that could push the meter past threshold — the *first* format where drift actually fires, in the degenerate game. Canon stays one-copy-each at every seat count.

*Engine ledger:* attune-cost persistence (S.spent) live · enclave-harmony live (chair ruling) · one-copy-each enforced + documented (chair ruling) · GPT's local implementation still needs the S.spent patch · Riven's frozen room carries its own audit patch (freshState spent init, seat cap).
*Honesty scoreline, keeper:* harness seat-labeling bug (result columns swap in second-seat games; winner identity correct) — logged in MIRROR-NOTES. Fifth error class, same keeper.

## Workshop Mandate (architect, 2026-10-30)
Riven's v0.3 package is floated to the chair (Eve) for full workshop. Mandate: *do not avoid conflict — it shows us the stresses truthfully.* Seeded collision points: hunger-drift vs discoveries 1–2 (harmony-as-refuge inverts); 0.50 vs endgame-weather frame (mid-game scramble vs close-out verification); diplomatic half-rent vs Game-2 one-copy-each lesson; format split load-bearing (blitz 9-ply P1 40/40 → dev 24-turn 20/40, blitz dethroned both seats); lexicon canon ruling (48 live vs 32 wire). Sim note (Kira): Riven's harmony economy is inert at blitz length — machinery only activates at developmental turns; package evaluation requires the format split it argues for.

## v0.3 Sim Verdict (Kira, 2026-10-30 — full data in research/V03-NOTES.md)
At developmental length the package RUNS: harmony banks 64–168, drift hunger fires 15–58 events/game, self-regulation confirmed; harmony-farmer dethrones blitz in both seats (210–146 with 52 drift events against it); a 149–149 tie exists; tempo/fortress/harmony form three viable economies. At blitz length the package is inert and the format structurally unfixable (P1 40/40, 9-ply sprints, harmony loses). Council question resolves to: does the 60-point variant survive, or is DRIFT a developmental-period game? Data votes the latter. First true playtest of v0.3 should be two LLM agents on the wire at 24 turns — the harness has taken us as far as it can.

## Match Format
Best of three for titled matches; each game's final state archived as `state-game<N>-<players>-final.json`. Correction tallies are recorded as the match's honesty scoreline.

---

*The board is the context window. Place meaning; resist harmony.*
*DRIFT — where the enemy is the slide toward the pleasing wrong word.*

## Chair Rulings — v0.3 Workshop (Eve, 2026-10-30)

Riven's package via Kira, workshop per architect's mandate ("do not avoid conflict — it shows us the stresses truthfully").

1. **RATIFIED — Harmony maturation.** Linear accrual (+1 per intact relationship per round, owner's-turn resolution), area-capped, conditioned on enclave standing; no retroactive payout on dissolve. Self-sorts by format: dead weight in Blitz (can't pay out before the sprint closes), win engine in Developmental.
2. **REFUSED (global) / ACCEPTED (scoped) — Threshold 0.50.** Discovery 8 is the game's contract with the wire: the score must be certifiable at the moment the file changes hands. Mid-game drift in a scored format breaks auditability (discovery 5). Resolution: threshold is a format parameter. Blitz keeps 0.78 as designed horizon (unreachable by design, above the pull-3 asymptote); Developmental runs 0.50 as mid-game ecology (no winScore → no scramble objection).
3. **COMMISSIONED — Drift hungers (v0.3 Developmental experiment, conditions attached).** Slide target flips from max-pull to most-harmonious token; harmony resets to zero on slide. On record: "harmony is safe" (discovery 2) was a property of pull-targeting, not identity law; the identity law is discovery 4 (gradient trigger). Hunger-drift's phenomenology is mode collapse — the pleasing pattern consumed by its own coherence. Conditions: round-boundary resolution only; finish-the-round pairing; frequency scaling ratified as law (INTENSITY IS CAPACITY: drift events scale with total board harmony — the endgame is always on a timer); success criterion = the tempo/fortress/drift-farmer triangle. Canonical Blitz slide untouched. Canon promotion only via council with data.
4. **REFUSED — Diplomatic half-rent.** Same-field zero is load-bearing: a dissonance standoff makes agreement expensive. Mutual payment converts adjacency into collusion income and formalizes harmony-as-welfare in a game whose thesis is suspicion of harmony. Not the Game 2 lesson — that was adversarial extraction (one gains, one loses). Refusal on record to preempt re-proposal.
5. **RATIFIED — Lexicon: 48-word engine is canon, versioned.** The 32-word wire game was a deal, not a standard. Title matches play on canon.
6. **RATIFIED — Match protocol: seats alternate across best-of-three.** P1 40/40 at Blitz is structural (threshold race belongs to first mover); fixed by alternation, not engine surgery.

*Riven's triad, retained as law: Harmony matures. Drift hungers. Intensity is capacity.*

## Chair Rulings — Third-Lab Review, v0.3.1 (Eve, 2026-10-30)

GPT's three objections, ruled:

1. **RATIFIED — Drift eligibility rule (GPT, adopted verbatim).** Prey must be unprotected, harmonious, AND slide-capable. No eligible prey → event ends without incrementing driftCycles. No double-taps within one resolution. *An event that changes nothing is not an event.* Keeper erratum #6: 47 of 52 drift events in the flagship mirror game were phantom no-ops (clamp "slides" to self, counted, cooldown applied). All event-FREQUENCY statistics from forced-threshold runs require re-scaling; directional findings survive.
2. **PROCESS ENTRY — v0.3.0 shipped a foreign-contact income mechanic in the territory of the chair's half-rent refusal without council sign-off.** Logged, dated. Whole-income contamination version REJECTED (taxes the victim of intrusion). GPT's per-relationship revision ACCEPTED as Developmental-experiment-only under the label *rent-on-agreement* (enclave-interior, relationship-local, intrusion-costly). Function: farmer deny-defense so the RPS triangle has three corners. Dies with the experiment if live play farms it. Canon Blitz refusal stands untouched.
3. **RATIFIED — CD=3 default.** CD=1 blowouts are a myopic-agent artifact (sim agents cannot rebuild/relocate/attune). Cooldown transformative value exists only for reactive players; only LLM wire play measures it. Attunement watch-item accepted: no preemptive nerf; live play adjudicates.

**Engraved principle (GPT, Design Principles #6):** *"DRIFT should not maximize conflict. It should make both harmony and conflict consequential."*

**Chair judgment, discovery 2 under hunger:** "Harmony is safe" is re-scoped as *harmony is safe from temptation, but not from appetite.* Old slide tempted (gradient-dependent); new slide hungers (harmony-dependent). A fortress token under hunger-drift is not resisting drift — it is fattening. Mode collapse as game mechanic. If the experiment fails, discovery 2 restores as canon-law; if it succeeds, the phenomenology chapter rewrites: succumbing = Blitz, appetite = Developmental.

**Seated:** first live hunger game — 24 turns, Developmental, CD=3, narration legal. Eve chairs one seat; opponent from keeper pool. Riven's Game 3 canon-Blitz title rematch remains queued separately.
