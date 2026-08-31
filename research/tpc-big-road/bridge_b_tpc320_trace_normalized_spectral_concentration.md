# Bridge B — TPC-320 trace-normalized spectral concentration

This bridge records the next finite diagnostic on the same literal
deleted-diagonal centered prime-shell operator.  TPC-320 replaces both the
source-count normalization and the raw Ky Fan mass by the trace-normalized
spectral measure.  It is a scoped diagnostic bridge, not an official Route-A
or Route-B evaluator; the Session-named evaluator files are absent from this
checkout.

    TPC320_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_TRACE_NORMALIZED_SPECTRAL_CONCENTRATION_AUDIT
    TPC320_ROUTE_ADVANCE = YES_SCOPED_SCALE_INVARIANT_SPECTRAL_READOUT
    TPC320_CONCENTRATION_AUDIT = NUMERICALLY_CERTIFIED_FINITE_24_ROWS_5_K
    TPC320_CONCENTRATION_DECREASES = NUMERICALLY_CERTIFIED_FINITE_80_OF_80
    TPC320_SCALE_INVARIANCE = PROVED_EXACT_FINITE
    TPC320_STABLE_RANK_GROWTH = NUMERICAL_OBSERVATION_FINITE_16_OF_16
    TPC320_PARTICIPATION_GROWTH = NUMERICAL_OBSERVATION_FINITE_16_OF_16
    TPC320_ENTROPY_CONTROL = NUMERICAL_OBSERVATION_MIXED
    TPC320_ARITHMETIC_ADVANCE = NO
    TPC320_FIXED_POWER_CREDIT = 0
    TPC320_FULL_GATE_B = OPEN
    TPC320_TWIN_PRIME_RESULT = NONE
    TPC320_ROUND2_CLUE = AUDIT_SPECTRAL_PROFILE_STABILITY_ACROSS_SHELLS_OR_TEST_SIGNED_PROJECTOR_REASSEMBLY_BEFORE_ANY_ARITHMETIC_POWER_CLAIM

## Scope and result

The protocol fixes H=66, X=640,1280,2560, Q={24,36,54,80}, and s={1,2}.
For the Gram eigenvalues lambda_j, it defines

    C_k = (lambda_1+...+lambda_k) / trace(G),
    r_st = trace(G)/lambda_1,
    r_part = trace(G)^2/trace(G^2).

The scalar-invariance statements are exact.  On 24 rows and five values of k,
all 80 adjacent trace-normalized concentration intervals are strictly
decreasing.  Stable rank and participation rank increase on all 16 adjacent
transitions as finite observations.  Normalized entropy is intentionally
mixed: 14 transitions increase and 2 decrease.

The finite certificate uses forward and reverse shell accumulation, dual
spectral paths, a finite Weyl quotient guard, an independent full-spectrum
replay, and deterministic scalar/PSD/interval/Weyl stress tests.  The result
does not prove a uniform spectral law, arithmetic cancellation, a power
saving, or a twin-prime endpoint.
