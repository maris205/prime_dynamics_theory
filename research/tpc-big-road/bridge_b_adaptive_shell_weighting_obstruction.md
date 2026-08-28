# Bridge-B note: TPC-290 adaptive shell weighting obstruction

TPC-290 takes the TPC-289 physical output Gram and makes “adaptive
weighting” explicit.  For `R(w)=||sum_q w_q g_q||^2 / sum_q w_q^2 d_q`, it
proves the exact weighted identity and the following conditional rule:
nonnegative weights cannot produce `R(w)<1` when all cross-prime Gram entries
are nonnegative; under the inherited coherence floor and diagonal balance,
`R(w)>=1+eta*delta*(kappa(w)-1)` with effective support
`kappa(w)=(sum w)^2/sum w^2`.

The finite replay uses the same 18 rows as TPC-289.  Uniform,
inverse-diagonal, and linear-taper policies give 54 full-support records, all
amplified.  Every leave-one-out uniform support is also amplified.  Exactly
three equal two-prime supports are subunit, all in the exceptional early
sign-flip row; they are sparse witnesses rather than full-shell decay.

```text
TPC290_MAXIMUM_CLAIM = PROVED_EXACT_NONNEGATIVE_WEIGHTED_GRAM_NO_DECAY_BOUND_PLUS_NUMERICALLY_CERTIFIED_FINITE_ADAPTIVE_WEIGHTING_OBSTRUCTION
TPC290_ROUTE_ADVANCE = YES_SCOPED_EFFECTIVE_SUPPORT_WEIGHTED_GRAM_FIREWALL
TPC290_WEIGHTED_IDENTITY = PROVED_EXACT_FINITE
TPC290_NONNEGATIVE_NO_DECAY = PROVED_EXACT_CONDITIONAL
TPC290_DIFFUSE_ACCUMULATION_BOUND = PROVED_EXACT_CONDITIONAL
TPC290_FULL_SUPPORT_POLICY_SCAN = NUMERICALLY_CERTIFIED_FINITE_54_OF_54_AMPLIFIED
TPC290_SPARSE_SIGN_FLIP_ESCAPE = NUMERICALLY_CERTIFIED_FINITE_3_PAIRS_ONE_ROW
TPC290_DROP_ONE_SCAN = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_AMPLIFIED
TPC290_UNIFORM_NONNEGATIVE_NO_DECAY = REFUTED_FINITE_BY_SPARSE_SIGN_FLIP
TPC290_GROWING_WEIGHTED_THEOREM = OPEN
TPC290_SOURCE_NATIVE_L2 = OPEN_LITERAL_SOURCE
TPC290_FIXED_POWER_CREDIT = 0
TPC290_FULL_GATE_B = OPEN
TPC290_TWIN_PRIME_RESULT = NONE
TPC290_STATUS = PROVED_EXACT_NONNEGATIVE_WEIGHTED_GRAM_NO_DECAY_BOUND_PLUS_NUMERICALLY_CERTIFIED_FINITE_ADAPTIVE_WEIGHTING_OBSTRUCTION
TPC290_ROUND2_CLUE = TEST_SIGNED_TWO_PRIME_SCHUR_CANCELLATION_OR_SOURCE_RESTRICTED_DIFFUSE_WEIGHTS
```

The Session-named evaluator files are absent; the project proof package,
canonical certificate, reverse-order replay, stress audit, and checker below
are the local fail-closed fallback.
