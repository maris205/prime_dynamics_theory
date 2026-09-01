# Bridge B — TPC-323 signed profile majorization

TPC-323 keeps the literal deleted-diagonal centered prime-shell blocks from
TPC-322 and adds a trace-normalized shape coordinate to the signed coherent
operator.  It separates the total energy ratio from the ordered spectral
profile and tests four predeclared sign laws on the full 24-row panel.

```text
TPC323_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_SIGNED_PROFILE_MAJORISATION_AUDIT
TPC323_ROUTE_ADVANCE = YES_SCOPED_FINITE_SIGNED_PROFILE_READOUT
TPC323_SIGNED_PROFILE_FACTORISATION = PROVED_EXACT_FINITE
TPC323_ALL_PLUS_PROFILE_MAJORISATION = NUMERICALLY_CERTIFIED_FINITE_24_OF_24
TPC323_ALTERNATIVE_PROFILE_CENSUS = NUMERICALLY_CERTIFIED_FINITE_24_ROWS
TPC323_NAMED_LAW_SELECTION = NUMERICAL_OBSERVATION_ALL_PLUS_UNIQUE_ON_PANEL
TPC323_AMPLITUDE_SHAPE_DECOUPLING = NUMERICALLY_CERTIFIED_FINITE_ALL_PLUS_3_BELOW_21_ABOVE
TPC323_ARITHMETIC_ADVANCE = NO
TPC323_FIXED_POWER_CREDIT = 0
TPC323_FULL_GATE_B = OPEN
TPC323_TWIN_PRIME_RESULT = NONE
TPC323_STATUS = NUMERICALLY_CERTIFIED_FINITE_SIGNED_PROFILE_MAJORISATION_AUDIT
TPC323_ROUND2_CLUE = TEST_PROFILE_MAJORISATION_HOLDOUT_OR_SOURCE_NATIVE_ARITHMETIC_L2
```

## Finite evidence

For `G_direct=sum_p B_p^T B_p` and
`G_e=(sum_p e_pB_p)^T(sum_p e_pB_p)`, the exact trace/profile bookkeeping
defines `rho=tr(G_e)/tr(G_direct)` and
`pi(G)=lambda(G)/tr(G)`.  On
`X={640,1280,2560}`, `Q={24,36,54,80}`, `s={1,2}`, all-plus has a strict
signed-profile majorization label on all 24 rows.  The alternative labels are
17/7 (index alternating), 21/3 (mod-4), and 18/6 (half split), where each
pair is majorizing/mixed.

All-plus energy is below the direct energy on 3 rows and above it on 21 rows;
the three below-one rows are the `Q=24,s=1` slice.  This is the finite
amplitude/shape decoupling result.  The smallest outward all-plus interior
prefix gap is `1.651764289139947e-05`, and producer/independent metric paths
agree within the declared floating guard.

## Interpretation firewall

The four signs are finite geometric probes, not Möbius or von Mangoldt
weights.  The certificate supplies no growing signed reassembly theorem,
source-native arithmetic `L2`, fixed-power credit, strict `1/400` payment,
full Gate B, or twin-prime conclusion.  The official Session-named evaluator
files are absent from the checkout; this bridge is a local fail-closed record,
not an official Route-A/Route-B pass.
