# Bridge B: TPC-279 minimal coherence-to-gain theorem

TPC-279 is the analytic continuation forced by TPC-278's finite shell/clock
sign flips.  It leaves the arithmetic source untouched and asks for the
weakest exact four-packet statement that could feed TPC-276's endpoint
compiler.

For four Hilbert-space packets define

```text
D=sum_j ||V_j||^2, G=||sum_j V_j||^2,
E=sum_(j<k) Re <V_j,V_k>,
q=G/D, Delta=(D-G)/D, r=D/G.
```

The exact theorem is

```text
0 <= q <= 4,
Delta = 1-q = -2E/D,
r >= b X^gamma  <=>  q <= b^(-1) X^(-gamma)
                 <=>  Delta >= 1-b^(-1) X^(-gamma).
```

For pairwise absolute coherence `mu`, the sharp phase-blind envelope is

```text
q <= min(4,1+3mu),
r >= max(1/4,1/(1+3mu)).
```

Equicorrelation Gram matrices attain equality for every `mu` in `[0,1]`;
orthogonal packets have `r=1`, and a scalar near-cancellation family has
unbounded gain with `mu=1`.  Hence pairwise coherence alone cannot deliver a
positive power; the missing input is an aggregate schedule-specific bound on
`G/D`.

The released TPC-278 gain intervals are transferred exactly to reciprocal
`q` and `Delta` intervals.  All 12 rows pass, with 8 positive and 4 negative
deficits, and the parent cross-sign labels agree.

```text
TPC279_MAXIMUM_CLAIM = PROVED_EXACT_MINIMAL_COHERENCE_TO_GAIN_CRITERION_PLUS_NUMERICALLY_CERTIFIED_TRANSFER
TPC279_ROUTE_ADVANCE = YES_SCOPED_EXACT_COHERENCE_TO_GAIN_CRITERION
TPC279_PAIRWISE_COHERENCE_POWER = REFUTED_EXACT_BY_ORTHOGONAL_WITNESS
TPC279_FINITE_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS
TPC279_SOURCE_LEVEL_DEFICIT = OPEN_ASYMPTOTIC
TPC279_FIXED_POWER_CREDIT = 0
TPC279_ARITHMETIC_ADVANCE = NO
TPC279_L2 = NONE
TPC279_FULL_GATE_B = OPEN
TPC279_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC279_TWIN_PRIME_RESULT = NONE
TPC279_STATUS = PROVED_EXACT_MINIMAL_COHERENCE_TO_GAIN_CRITERION_PLUS_NUMERICALLY_CERTIFIED_TRANSFER
TPC279_ROUND2_CLUE = COMPILE_COHERENCE_DEFICIT_WITH_MARGIN_AND_ARITHMETIC_L2
```

Strongest positive result: exact necessary-and-sufficient deficit criterion
and sharp coherence envelope.  Strongest obstruction: absolute coherence is
phase-blind and cannot pay a power.  Open theorem: a growing source-level
aggregate deficit estimate.  The Session-named evaluator files are absent;
the local proof, certificate, independent replay, stress audit, and checker
are the fail-closed fallback.
