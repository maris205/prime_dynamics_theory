# RH-116: monotone memory-depth optimization

RH-116 turns finite-memory depth from a heuristic parameter into an exact
first-passage optimization problem.  If each newly included cross increment
is bounded by the corresponding decrease in the discarded-tail budget, the
Weyl lower bound for the relative fourth singular mode is monotone in depth.
The first passing depth is therefore the minimum-cost certificate, and a
search through full history is complete for this nested certificate family.

The five-scale audit uses one Gram assembly path and enumerates every
available depth on 360 threshold-labelled records.  All 322 genuinely
supported records are certified.  There are zero tail-enclosure, dominance,
monotonicity, minimality, or completeness failures.  The maximum required
depth is six; the mean recordwise cost is `0.348` of full history, and the
aggregate rank-weighted action cost falls by more than 72 percent.

Observed bounded depth is not an all-level bounded-depth theorem.  RH-117
will separate finite scale trends from asymptotic implications.
