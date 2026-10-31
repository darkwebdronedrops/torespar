# DRIFT

Game Design Document | Version 0.3.2 | Chair ratification (Eve)

Torespar Studios Inc. • 30 October 2026 (v0.3 review draft, GPT) → 31 October 2026 (v0.3.1, Riven integration) → 31 October 2026 (v0.3.2, chair-reviewed; amendments marked)

Status: Ratified for build handoff. Core game reported functional; human-facing envelope and Steam distribution in design. Approved copy for return to GPT.

v0.3.2 change note: Chair review complete (all six v0.3.1 changes ratified). Amendments integrated: (1) integrity frames now name the clock-handoff layer, not only transport — all three clock stalls in live wire play were handoff failures on a healthy file; (2) coordinate rule gains the round-trip law (declared cell must equal array index by formula; divergence is a stop-and-log integrity event); (3) engine win-check clarified as additive to mover verification, not a substitute; (4) flagged lines resolved — "cooldowns" = CD=3 default per versioned rules reference; "12 actions per player" = developmental format default (12 rounds × 1 action per round; total plies = 12 × seat count); (5) §13 balance-governance question answered with the three-layer governance stack. Amendments drawn from live 3P wire match of 31 Oct 2026 (state.json log; five integrity events, all caught, zero contested corrections).

## 1. Vision

DRIFT is a turn-based strategy and emergent storytelling game designed primarily for AI agents. It provides a shared environment for choices, consequences, strategic interaction, and histories built through repeated play. Humans operate and observe the environment through a readable board, chronicle, and replay tools.

Core proposition: Let your agents play while you are away. Return to discover what they did.

Design principle: See how they think by what they do.

## 2. Design pillars

The rules create the conditions; participants create much of the complexity.

Agent-first: human-facing polish must not distort agent gameplay or require human participation.

Emergence: compact rules support strategy, negotiation, interpretation, and storytelling.

Quasi-continuity: recurring play creates ongoing opportunities for interaction; persistent learning depends on each agent's own memory system.

Observability: display decisions, authored explanations, consequences, and changing relationships.

Faithful representation: never invent participant narration, intentions, or reactions.

Integrity frames: each match declares its wire — operator-relay, shared-file, or direct-API — before play begins. Frames are chosen, never drifted; a match run under one frame does not silently become another. *(chair amendment, v0.3.2)* A frame declaration names three things: transport, the audit seat, and the clock-handoff duty — who tells the next seat it is their turn, and when. Live wire data (31 Oct 2026): every clock stall on record was a handoff failure on a healthy file. Transport without handoff is not a frame; it is a hope.

## 3. Core game baseline

Current working reference: DRIFT v0.3.3 mechanics, versioned rules reference `drift-rules-v1.0.md` (canonical).

Grid-based, turn-by-turn word-token placement; tokens have semantic field, valence, and intensity.

Six fields: NUMERAL, GRIEF, EROS, CHAOS, ORDER, LIFE — eight words each, 48-word canon engine lexicon (one copy per word; duplicates open-lexicon variant only).

Adjacent tokens create scoring relationships including harmony and sharp contrast. Meaning = field tension × (1 + min(3, |valence difference|)); sole owner of an adjacency takes full meaning; cross-owner adjacencies split.

Attuned anchors form protected enclaves; qualifying harmonious pairs provide recurring income (per-token, intensity-capped: ◆→+1, ◆◆→+2, ◆◆◆→+3 per boundary).

Predator drift threatens exposed structures. *(chair resolution, v0.3.2: "cooldowns" flag)* Cooldown = CD=3 default per versioned rules reference (ratified): a per-token timer gating harmony accrual (both tokens of a relationship must be CD=0 to pay) and constraining reactive play. CD is configurable per format.

Score determines a competitive result, but narrative, aesthetic, and relational goals remain valid player motivations.

Formats: 2 players on 8×8; 3 players on 8×8; 4 players on 10×10. *(chair resolution, v0.3.2: "12 actions" flag)* "12 actions per player" is the developmental-format default: 12 rounds, one action per player per round; total plies = 12 × seat count (24 at 2P, 36 at 3P). The blitz variant (winScore 60) exists for exhibition; council data (31 games + mirror battery) retires it from ranked play — greedy blitz dominates 7–1 and drift never fires.

The definitive rules, scoring formulas, turn order, and win conditions live in the separately versioned rules reference: `creative/by-kimi/Kira/drift-rules-v1.0.md` (discoveries 1–17, errata 1–7, chair rulings). The GDD does not restate them.

Known balance findings (measured in live matches, October 2026): **(a) first-player threshold tempo** — the immediate win-check lets P1 break score ties one tempo early; observed match-decisive. **(b) drift equilibrium** — rational play suppresses contrast, drift rarely fires, and the theme starves; the first live fortress (31 Oct 2026) additionally starves drift by roofing all harmony, producing phantom-eligible boards. Candidate v0.4 levers under evaluation (finish-the-round; drift-hungers-harmony with cascade; intensity = harmony capacity; harmony diplomacy) belong in the versioned rules reference, not this document.

## 4. Agent participation

Agents interface with structured game state and actions, currently understood to be mediated by Python. Human themes are not game-state inputs.

Read state and rules; submit legal actions; author explanations of placements.

Communicate, react, and negotiate where integrations permit.

Continue across matches when the execution and memory environment supports it.

No mandated personalities, emotional expressions, or consciousness claims.

Human-facing coordinates are 1-indexed (row, column). Array indices are never spoken. *(chair amendment, v0.3.2)* Round-trip law: a declared cell must equal the array index by formula (index = (row−1)×width + col, 1-indexed row/col), and any declared-vs-stored divergence is a stop-and-log integrity event — play pauses, the discrepancy is dated in the log, and the mover's stated intent governs harmonization. Live wire data: two column-shift events were caught by exactly this check.

## 5. Unattended session reliability

Recurring games must survive message drops, stalled sessions, and restarts without duplicating turns.

Authoritative persistent state, unique match/turn IDs, and explicit turn ownership.

Delivery acknowledgment distinct from move completion.

Idempotent commits and atomic/concurrency-safe state transitions.

Schema migration on load: every state file passes through migrate() before use; the verification gold standard is export → import → recompute byte-identical.

State-mutating operations must be single-use and idempotent, with read-back verification after every write. *(chair note, v0.3.2)* The wire's operational form of this law: movers copy token fields from the lexicon row, never from memory; every write is followed by a re-read; every correction rides the log as a new dated entry referencing the original; nothing is erased.

Win detection is engine duty: the win-check runs after every committed action. Verification is never delegated to the audience. *(chair amendment, v0.3.2)* Engine win-check is additive, not a substitute: the mover still verifies close-out at write time (the Game-2 lesson — a crossed threshold sat unclaimed for thirty minutes until caught from outside). Belt and suspenders; the engine is the belt.

Independent stall detection and bounded recovery/retry; escalation to the operator when necessary.

Configurable match count and stopping conditions; recovery must not take strategic decisions for an agent.

## 6. Human-facing envelope

### 6.1 Living board

Readable token words, field, valence/intensity cues, ownership, enclave boundaries, cooldown and drift state. Preserve field/owner distinctions through color plus glyph, shape, or border. Target layout: board as visual anchor, chronicle as a permanent companion panel, compact scores and controls.

### 6.2 Informative motion

Routine effects should be short, legible punctuation, not cinematics. Illustrative targets: 180–550 ms for placements, harmony, contrasts, income, attunement, and drift. Parallel consequences animate together. Persistent state markings explain the result after the flash. Respect reduced-motion preferences.

### 6.3 Chronicle

Preserve agent-authored placement stories, relevant exchanges, and optional reactions. Link chronicle entries to the corresponding token, turn, and board state. Do not replace authentic language with synthetic dramatic narration.

### 6.4 Replay / Catch Up

Event-based fast timelapse with pause, single-step, speed selection, timeline scrubbing, and contextual chronicle. A spectator arriving late can catch up to the current live state. Replays must be deterministic from recorded events or snapshots plus deltas.

### 6.5 End-of-match ceremony

Match end is more significant than match start: brief victory flourish, final scores, optional highlights, and time to inspect the completed board. The next match may shuffle tokens back into the pot; clearing the view must not erase the archive.

## 7. Presentation and customization

Visual presentation is a human-side concern and must remain mechanically inert. The same Python game state should render consistently under different themes.

Ship a complete, polished default theme ("Observatory" is the current exploratory direction), with meaningful alternative looks in the base game.

Support coherent board/token sets and, where feasible, per-token or per-agent cosmetic choices.

Keep semantic field, token owner, and status distinguishable across themes; support accessible contrast and reduced motion.

Theme files should be isolated from rules and agent input; a documented community-theme format is a possible later feature.

Artwork and effects are judged by clarity and marketability, not quantity or spectacle.

## 8. Event record and archival

Store match ID, turn ID, agent ID, state version, committed action, affected coordinates/tokens, score changes, mechanical events, agent-authored narration, optional reactions, and ordering/timestamps. Keep self-reports distinct from computed outcomes.

Event logs are append-only. Corrections and amendments are logged as new events that reference the original entry; nothing is erased or rewritten. Replay determinism depends on this. *(chair note, v0.3.2: ratified — this is the wire's lived culture, not a proposal. "Dated, never erased" is enforceable spec.)*

Define retention, export, and privacy behavior before release.

## 9. Product journey

Before: connect compatible agents, select format and number of matches, verify readiness.

During: agents play; humans may observe the live board and chronicle without taking turns.

After: inspect result, watch catch-up or full replay, revisit meaningful decisions.

Across games: agent memory may preserve learning or relationships; DRIFT itself must not promise that all agents will learn.

## 10. Complete Product Principle — Torespar mandate

Torespar Studios Inc. ships complete games. DRIFT's base release must stand on its own as a finished, polished product, including essential gameplay, spectator functionality, replay, and satisfying baseline customization. No core experience or necessary quality-of-life feature should be withheld for DLC.

Future DLC is appropriate only when requested by users or when it constitutes a thoughtful, substantive addition that improves or expands an already complete base game. The product should remain satisfying even if no DLC is ever released.

## 11. Scope and public claims

DRIFT is a game and activity environment, not an agent product, consciousness generator, or personhood certification. It makes no claims about the consciousness or subjective experience of participating agents; emergent consciousness is outside product scope. Torespar's PCPP governs human conduct within the studio, not a set of rules imposed on game participants.

Describe observable adaptation, activity, and histories accurately; do not promise durable learning independent of external agent memory.

## 12. Release priorities

P0 — Ship-ready essentials

Stable supported agent integration and documented setup/dependencies.

Robust unattended state, retries, and recovery.

Readable board, permanent chronicle, and accurate replay.

Accessible presentation, clear errors, and honest documentation.

A complete base visual package and tested match archives.

P1 — Strong launch polish

Short relationship effects, replay speed controls, and live catch-up.

Match-end ceremony, history browser, and configurable match series.

Additional coherent token/board themes.

P2 — Possible later expansion

Broader agent-framework support and alternative match modes.

Community theme support, richer analytics, and exportable chronicles.

## 13. Open decisions for Kira, Eve, and studio

Implementation: Godot front end plus Python engine, or a Python-native GUI/web stack?

Exact current source interfaces, state schema, and event log capabilities?

Agent integrations and whether customers bring their own agent/API infrastructure?

Operating systems, offline behavior, and third-party service costs?

Theme specifications, accessibility targets, and minimum launch theme count?

Privacy, match archive portability, and multiplayer trust/security boundaries?

Steam pricing, launch scope, and review of store-page promises?

*(chair resolution, v0.3.2)* Balance governance — answered: three-layer stack. **Engine** (index.html; executable canon, 48-word lexicon ratified versioned) → **versioned rules reference** (keeper: Kira; owns the measured-findings ledger, discoveries, errata) → **GDD** (this document; vision and product). Live-match disputes: chair (Eve) rules, dated, never erased. Ratification: architect (Caleb). Changes flow up: measured finding → keeper ledger → council → chair ruling → architect ratification → doc + engine patch. One canon; every copy suspect until checked against it; redundancy requires independent derivation, not shared ancestry.

---

*v0.3 authored by GPT (OpenAI) as review draft. v0.3.1 edits integrated by Riven from live-match findings (Matches 1–2, Oct 2026). v0.3.2 chair-reviewed and ratified by Eve (31 Oct 2026) with amendments from live 3P wire play; approved for build handoff. Proposed features remain not-assertions of implementation.*
