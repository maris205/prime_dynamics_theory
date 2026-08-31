# Bridge B — TPC-321 cross-shell spectral-profile stability

This bridge keeps the literal deleted-diagonal centered prime-shell operator
fixed and changes only the diagnostic axis after TPC-320's trace
normalization.  It compares the complete ordered profile
`p_j=lambda_j/trace(G)` at adjacent shell anchors.

```text
TPC321_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_CROSS_SHELL_PROFILE_SEPARATION_AUDIT
TPC321_ROUTE_ADVANCE = YES_SCOPED_CROSS_SHELL_PROFILE_OBSTRUCTION
TPC321_PROFILE_SEPARATION = NUMERICALLY_CERTIFIED_FINITE_18_OF_18
TPC321_TV_SEPARATION = NUMERICALLY_CERTIFIED_FINITE_ALL_GT_0_03
TPC321_LORENZ_KS_SEPARATION = NUMERICALLY_CERTIFIED_FINITE_ALL_GT_0_02
TPC321_MAJORISATION_PATTERN = NUMERICAL_OBSERVATION_3_FORWARD_2_REVERSE_13_MIXED
TPC321_UNIFORM_SHELL_PROFILE = REFUTED_FINITE_PANEL
TPC321_UNIFORM_MAJORISATION = REFUTED_FINITE_PANEL
TPC321_ARITHMETIC_ADVANCE = NO
TPC321_FIXED_POWER_CREDIT = 0
TPC321_FULL_GATE_B = OPEN
TPC321_TWIN_PRIME_RESULT = NONE
TPC321_STATUS = NUMERICALLY_CERTIFIED_FINITE_CROSS_SHELL_PROFILE_SEPARATION_AUDIT
TPC321_ROUND2_CLUE = TEST_SIGNED_PROJECTOR_REASSEMBLY_OR_PROVE_A_UNIFORM_SHELL_PROFILE_BOUND_BEFORE_ANY_ARITHMETIC_POWER_CLAIM
```

## Finite evidence

The panel is `X={640,1280,2560}`, `Q={24,36,54,80}`, and `s={1,2}`.  It has
24 rows and 18 adjacent-Q comparisons.  For each comparison the producer
evaluates all nine combinations of forward/reverse shell accumulation and
NumPy/SciPy spectral paths, then places the scalar distances in an outward
interval with guard `1e-12`.  The independent checker uses reverse shell
order and an `einsum` Gram accumulation without importing the producer.

The primary distances are the l1 distance of the ordered normalized rank
profiles and the maximum absolute difference of their partial sums.  Their
smallest outward lower endpoints are, respectively,
`0.03212981290619634` and `0.02339722207455566`; all 18 comparisons clear the
declared `0.03` and `0.02` thresholds.  The majorization labels are 3 forward,
2 reverse, and 13 mixed.

## Interpretation firewall

The finite panel is evidence of shell sensitivity and refutes a universal
profile/majorization rule only in the tested panel.  It is not a uniform
asymptotic theorem, a signed prime-sum estimate, an arithmetic cancellation,
or a twin-prime result.  Fixed-power credit remains zero and full Gate B is
open.  The Session-named official evaluator files are absent from this
checkout, so this is a local fail-closed Bridge-B record rather than an
official Route-A/Route-B pass.
