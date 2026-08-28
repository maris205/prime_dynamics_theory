# Bridge-B note: TPC-289 cross-prime Gram coherence

TPC-289 follows the TPC-288 full-rank obstruction without changing the
literal deleted-diagonal prime-component family.  It replaces rank by a
signed, normalized cross-prime coherence audit and proves an exact
conditional accumulation envelope.

On 18 declared rows there are 1,380 unordered pair comparisons.  Seventeen
rows have all-positive off-diagonal Gram entries.  The single exceptional row
`(N,H,Q,z,s)=(256,38,27,5,1)` has three exact negative pairs, including a
near-zero coherence pair.  Eight late-shell rows satisfy the finite thresholds
`Gamma>=9/25` and `d_min/d_max>=4/5`; all 18 rows have energy ratio greater
than one.

This establishes a finite sign/coherence phase diagram and refutes a tested
uniform positivity/coherence-floor shortcut.  It does not establish a
growing-shell theorem, source-uniform arithmetic `L2`, fixed-power credit,
full Gate B, or a twin-prime conclusion.

```text
TPC289_MAXIMUM_CLAIM = PROVED_EXACT_NORMALIZED_GRAM_COHERENCE_ACCUMULATION_BOUND_PLUS_NUMERICALLY_CERTIFIED_FINITE_SIGN_PHASE_DIAGRAM
TPC289_ROUTE_ADVANCE = YES_SCOPED_EXACT_COHERENCE_ENVELOPE_AND_FINITE_SIGN_PHASE_DIAGRAM
TPC289_EXACT_GRAM_COHERENCE = PROVED_EXACT_FINITE
TPC289_EXACT_ACCUMULATION_BOUND = PROVED_EXACT_CONDITIONAL
TPC289_PAIRWISE_POSITIVITY = NUMERICALLY_CERTIFIED_FINITE_17_OF_18_ROWS
TPC289_SIGN_FLIP_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_3_PAIRS_ONE_ROW
TPC289_STRONG_COHERENCE_BLOCK = NUMERICALLY_CERTIFIED_FINITE_8_ROWS
TPC289_ENERGY_AMPLIFIED = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ROWS
TPC289_TOTAL_PAIR_COMPARISONS = 1380
TPC289_CONTROL_EQUIVALENCE_GROUPS = 2
TPC289_UNIFORM_PAIRWISE_POSITIVITY = REFUTED_FINITE_DECLARED_GRID
TPC289_GROWING_COHERENCE_STABILITY = OPEN
TPC289_SOURCE_CONTROL_UNIFORMITY = OPEN
TPC289_SOURCE_NATIVE_L2 = OPEN_LITERAL_SOURCE
TPC289_FIXED_POWER_CREDIT = 0
TPC289_FULL_GATE_B = OPEN
TPC289_TWIN_PRIME_RESULT = NONE
TPC289_STATUS = PROVED_EXACT_NORMALIZED_GRAM_COHERENCE_ACCUMULATION_BOUND_PLUS_NUMERICALLY_CERTIFIED_FINITE_SIGN_PHASE_DIAGRAM
TPC289_ROUND2_CLUE = TEST_ADAPTIVE_SHELL_WEIGHTING_OR_SOURCE_RESTRICTED_COHERENCE_BEYOND_FINITE_BLOCK
```

The Session-named Route-A/Route-B evaluator files are absent.  The project
proof package, canonical certificate, independent replay, stress audit, and
the checker below form the local fail-closed fallback; no official evaluator
pass is claimed.
