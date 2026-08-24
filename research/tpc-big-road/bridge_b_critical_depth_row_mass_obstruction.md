# Bridge B V86: critical-depth row-mass comparability obstruction

TPC-232 transfers sparse collision incidence to sparse incident mass only under a
fixed row-mass comparability constant.  That condition is not automatic in the
modeled dilated clock.

For

\[
P_L=\prod_{\ell\le L,\ \ell\ {m prime}}\ell,
\qquad
Q_L=2^{j_L}P_L,
\qquad
\log Q_L=L\log L+O(1),
\]

we have `L~log Q_L/loglog Q_L` and every prime divisor of `Q_L` is at most `L`.
The classical PNT error term places primes `p_L,r_L` in the shell with cutoffs
`L` and `2L-1`.  For the raw uniform-atom support,

\[
N_{p_L}=2,
\qquad
N_{r_L}=2\{1+\pi(2L-1)-\pi(L)\}.
\]

Therefore

\[
\kappa_{\rm raw}(Q_L,L)
\ge1+\pi(2L-1)-\pi(L)
\sim L/\log L\to\infty.
\]

The universal upper bound is `kappa_raw<=2L-1`.  Thus fixed raw comparability is
refuted as a consequence of clock geometry; row normalization remains a possible
repair but must be audited before any V59 attachment.

```text
TPC233_ROUTE_ADVANCE = YES
TPC233_CRITICAL_PRIMORIAL_CLOCK = PROVED_EXACT
TPC233_CRITICAL_SCALE_RELATION = PROVED_ASYMPTOTIC
TPC233_LOW_HIGH_PRIME_ROWS = PROVED_SOURCE_BACKED
TPC233_LOW_ROW_ATOMS = PROVED_EXACT_2
TPC233_HIGH_ROW_ATOMS = PROVED_EXACT_PRIME_INTERVAL_COUNT
TPC233_RAW_COMPARABILITY_DIVERGES = PROVED_ASYMPTOTIC
TPC233_UNIVERSAL_KAPPA_UPPER_BOUND = PROVED_EXACT_2L_MINUS_1
TPC233_FIXED_COMPARABILITY_FROM_GEOMETRY = REFUTED_SCOPED
TPC233_ROW_NORMALIZATION_REPAIR = OPEN
TPC233_ACTUAL_V59_ROW_WEIGHTS = OPEN
TPC233_ARITHMETIC_ADVANCE = NO
TPC233_ARITHMETIC_OBSTRUCTION = PROVED_SOURCE_BACKED
TPC233_FIXED_ATOM_CREDIT = 0
TPC233_L2 = NONE
TPC233_FULL_GATE_B = OPEN
TPC233_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC233_STATUS = PROVED_ARITHMETIC_OBSTRUCTION_L1
TPC233_ROUND2_CLUE = NORMALIZE_ROWS_THEN_TEST_COLLISION_OPERATOR_BEFORE_V59_ATTACHMENT
```

Strongest positive result: an exact critical clock with explicit low/high row masses.
Strongest obstruction: fixed raw row comparability diverges.  Open theorem:
source-valid normalization and normalized collision conditioning.  Reusable structure:
primorial saturation plus shrinking-window shell placement.

The finite certificate uses four signed-64-bit clocks and two independent deterministic
primality implementations.  It is reproduction only.  No collision lower bound,
actual source mass, signed saving, `L2`, or Gate-B theorem is claimed.
