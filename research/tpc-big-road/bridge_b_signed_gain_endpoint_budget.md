# Bridge B: TPC-276 signed-gain margin recovery and strict endpoint budget

TPC-276 is the source-attached continuation of TPC-275.  It freezes the same
literal V59 finite physical operator, exact beta source, prime shell, masks,
deleted diagonal, rank-three Haar projection, and TPC-269 growing-cutoff
registry.  No new operator, synthetic packet family, or asymptotic arithmetic
input is introduced.

## New finite and conditional result

TPC-275 supplies four actual source-block packets (V_j), their packet
diagonal energy (D=sum_j|V_j|_2^2), and signed output energy
(G=|sum_jV_j|_2^2).  With

```text
r = D/G,
m_D^2 = |C_perp|^2/(W_perp D),
m^2 = |C_perp|^2/(W_perp G),
```

the exact identity is

```text
m^2 = r m_D^2.
```

Thus a positive signed gain (r>1) recovers actual margin that is invisible
to the diagonal proxy.  If a source-level theorem eventually proves
(D/Gge b x^gamma), then the gain enters the margin through a square root:

```text
eta_eff = max(0, eta_D-gamma/2),
endpoint saving = sigma-eta_eff,
strict target condition = sigma-eta_eff > 1/400.
```

This is a conditional compiler.  The (1/400) payment is not claimed for the
finite table.

On the six registered scale triples and (s=1,2), the exact rational transfer
contains 12 rows.  Every row has `r>1`; three rows lie above the signed quarter
threshold (m^2=1/16), and five lie above the signed eighth threshold
(m^2=1/64).  All comparisons use rational interval endpoints and no decimal
or power-law inference.

The three quarter rows are `(64,1)`, `(96,1)`, and `(96,2)`.  The five eighth
rows are `(64,1)`, `(64,2)`, `(96,1)`, `(96,2)`, and `(128,2)`.  No signed
interval crosses either threshold.

## Claim firewall

```text
TPC276_MAXIMUM_CLAIM = PROVED_CONDITIONAL_SIGNED_GAIN_STRICT_ENDPOINT_BUDGET_PLUS_FINITE_TRANSFER
TPC276_ROUTE_ADVANCE = YES_SCOPED_SIGNED_GAIN_MARGIN_RECOVERY
TPC276_SIGNED_GAIN_MARGIN_IDENTITY = PROVED_EXACT_FINITE
TPC276_CONDITIONAL_BUDGET_COMPILER = PROVED_CONDITIONAL_WITH_EFFECTIVE_LOSS_MAX_ZERO_ETA_D_MINUS_GAMMA_OVER_2
TPC276_FINITE_SIGNED_MARGIN_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS
TPC276_SIGNED_QUARTER_CROSSING = NUMERICALLY_CERTIFIED_FINITE_THREE_ROWS
TPC276_SIGNED_EIGHTH_CROSSING = NUMERICALLY_CERTIFIED_FINITE_FIVE_ROWS
TPC276_GAIN_STRICTLY_ABOVE_ONE = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS
TPC276_FINITE_POWER_PROMOTION = REFUTED_SCOPED
TPC276_FIXED_POWER_CREDIT = 0
TPC276_SOURCE_LEVEL_SIGNED_GAIN = OPEN_ASYMPTOTIC
TPC276_ARITHMETIC_ADVANCE = NO
TPC276_L2 = NONE
TPC276_FULL_GATE_B = OPEN
TPC276_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC276_TWIN_PRIME_RESULT = NONE
TPC276_STATUS = PROVED_CONDITIONAL_SIGNED_GAIN_STRICT_ENDPOINT_BUDGET_PLUS_FINITE_TRANSFER
TPC276_ROUND2_CLUE = SEEK_UNIFORM_SOURCE_LEVEL_SIGNED_GAIN_LOWER_BOUND
```

The strongest positive result is the exact bridge
`m^2=(D/G)m_D^2` together with the conditional half-exponent compiler.  The
strongest obstruction is that a finite gain table does not imply a quantified
growing lower bound, so the finite gain is not a fixed-power credit.  The next
open theorem is a uniform source-level signed-gain lower bound coupled to the
margin lane.  The arithmetic (L^2), full Gate B, and twin-prime proof remain
open or none.

TPC-275 is the frozen parent certificate; its exact signed Gram, four-point
DFT, and polarization identities are not re-proved here.  The Session-named
`propose.md` and route evaluator files are absent in this checkout.  The
project proof package, theorem ledger, exact certificate, independent replay,
hostile stress audit, and this fail-closed bridge checker are the available
local fallback authority.  This document records a finite transfer and a
conditional theorem, not an asymptotic twin-prime proof.
