# Bridge B: TPC-274 projected output Frobenius envelope

TPC-274 is the controlled continuation of TPC-273.  It freezes the literal
V59 finite physical operator, exact beta source, prime shell, masks, deleted
diagonal, four-block Haar projection, and the TPC-269 growing-cutoff registry.
The question is whether a cancellation-free norm estimate can control the
projected output lane well enough to pay the margin interface.

## New finite result

For a finite matrix `A`, the projected operator and output are

```text
A_perp=(I-P_3)A,
g_perp=A_perp beta,
G_perp=||g_perp||_2^2.
```

Rowwise Cauchy--Schwarz proves the exact envelope

```text
G_perp <= G_F := ||A_perp||_F^2 ||beta||_2^2.
```

On the six registered scale triples

```text
(N,H,Q)=(64,15,4),(96,20,5),(128,24,5),
        (192,32,6),(256,38,6),(384,50,7)
```

with the registered growing cutoffs and `s in {1,2}`, exact rational matrix
construction gives 12 rows.  The envelope-to-actual output-energy ratio has
lower endpoint above 50 on every row, and the conservative proxy

```text
m_F^2 = |C_perp|^2/(W_perp G_F)
```

has upper endpoint below `1/64` on every row.  The phase census is 11
`NEGATIVE_REAL_AXIS`, one `POSITIVE_REAL_AXIS`, and zero crossings.  The exact
certificate, independent reconstruction, and five-mutation stress audit all
pass in normal and optimized modes.

The gap is a method diagnostic: it says that this cancellation-free envelope is
too loose for the registered finite source.  It is not an upper bound on the
actual margin, an asymptotic sequence, or a counterexample to signed output
reassembly.

## Claim firewall

```text
TPC274_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_PROJECTED_FROBENIUS_ENVELOPE_GAP
TPC274_ROUTE_ADVANCE = YES_SCOPED_PROJECTED_FROBENIUS_ENVELOPE_GAP
TPC274_PROJECTED_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE_INEQUALITY
TPC274_FINITE_GAP = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS
TPC274_CANCELLATION_FREE_ROUTE = INSUFFICIENT_SCOPED
TPC274_ENVELOPE_MARGIN = NOT_AN_ACTUAL_MARGIN_UPPER_BOUND
TPC274_SOURCE_LEVEL_OUTPUT_BOUND = OPEN_ASYMPTOTIC
TPC274_SIGNED_OUTPUT_REASSEMBLY = OPEN
TPC274_FIXED_POWER_CREDIT = 0
TPC274_ARITHMETIC_ADVANCE = NO
TPC274_L2 = NONE
TPC274_FULL_GATE_B = OPEN
TPC274_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC274_TWIN_PRIME_RESULT = NONE
TPC274_STATUS = NUMERICALLY_CERTIFIED_FINITE_PROJECTED_FROBENIUS_ENVELOPE_GAP
TPC274_ROUND2_CLUE = TEST_SIGNED_OUTPUT_REASSEMBLY_BEYOND_CANCELLATION_FREE_ENVELOPES
```

The strongest positive result is the exact projected Frobenius inequality with
an exact matrix replay.  The strongest obstruction is the certified factor-50
method gap and the resulting envelope margin below `1/8` on all rows.  The
open theorem is a source-level signed output reassembly with an effective
saving.  A finite envelope gap does not grant fixed-power credit.  The
Session-named `propose.md` and route evaluator files are absent in this
checkout; the project proof package, theorem ledger, certificate, independent
replay, stress audit, bridge checker, and `AGENTS.md` are the fail-closed local
fallback.
