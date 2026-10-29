I ran eight additional DRIFT simulations, testing each of your four strategies from both starting positions against an immediate-scoring opponent.

The early results expose something interesting: DRIFT's current scoring incentives are extremely hostile to long-term investment. That doesn't mean the strategies are bad. It means a greedy opponent can often reach 60 before the board develops enough for them to pay off.
Results
Exploratory automated matches · DRIFT local implementation · 60-point victory threshold
Strategy	Score playing first	Score playing second	Wins
3×3 lockout	12–64	10–66	0/2
Hidden point swing	42–66	32–60	0/2
Intentional drift	49–64	56–68	0/2
Harmony pressure	49–64	56–68	0/2

These are heuristic agents, not optimized strategic players, and eight matches are insufficient to rank the strategies reliably.

The striking result is that none of the eight games triggered a drift event, including the two where the agent deliberately tried to increase drift.
What each strategy revealed
1. The 3×3 lockout

The lockout agent did attune tokens, but it spent turns establishing territory while the opponent accumulated meaning. Its poor scores aren't surprising.

More importantly, the implementation reveals a rules issue: the stated −2 attunement cost is immediately overwritten by the scoring recalculation. The fulcrum's lost scoring is real, but the two-point payment doesn't persist.

That should be fixed before evaluating the economic value of attunement.

Also, the 3×3 enclave doesn't prohibit enemy placements inside it. Its hard territorial protection applies to overlapping enemy enclaves. So it's a fortress against competing attunement, not a complete placement lockout.

2. Hidden point swings

This performed better than lockout, but my agent kept planting isolated Gardens rather than creating genuinely diversified setups.

The key tactical idea remains promising: a single placement can connect to as many as four orthogonal neighbors. If you prepare those neighbors in advance, you can convert several previously disconnected tokens into simultaneous scoring relationships.

But the opponent can also occupy the intended convergence square. The hidden strategy therefore needs to consider which player can exploit the empty square first, not just its eventual scoring potential.

3. Intentional drift

The drift-seeking agent reached substantial pull levels, but never crossed the 0.78 threshold.

This highlights a difficulty: maximizing pull isn't equivalent to controlling what will drift. The engine chooses the strongest eligible relationship and moves a token one valence step. The strategic question is whether that movement damages the opponent's scoring more than yours.

A useful drift strategy would need to engineer the direction and ownership of the vulnerable token, rather than merely increase global pull.

4. Harmony pressure

My harmony and drift agents actually converged on identical moves in these tests.

That's a limitation of the heuristic design, and it means these simulations haven't meaningfully distinguished the two concepts.

However, the rules suggest a fascinating difference: equal-valence pairs contribute maximum pull to the global meter but cannot themselves slide. So you can potentially create a large, stable harmony structure that raises global pressure while leaving a smaller number of unequal-valence tokens exposed.

A harmony fortress could become a drift engine that destabilizes everything outside it.

That's the most interesting theoretical interaction I found in this round.
The broader finding
I think you're pointing toward four strategies that operate on different dimensions of the game:
- Lockout controls territory.
- Hidden swings control timing.
- Intentional drift controls instability.
- Harmony controls the environment in which instability occurs.
Those are potentially distinct strategic identities, rather than merely alternative ways to maximize immediate points.

The current simulations demonstrate the challenges but don't yet establish their competitive viability.
Eight complete match records

Strategy simulation source


One design observation stands out: DRIFT may have a much richer positional game than its current victory threshold allows players to discover. The greedy agent was often winning within 9–13 total turns. That leaves very little room for the kind of delayed, environmental manipulation you're proposing.