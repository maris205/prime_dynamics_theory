# Bridge-B: TPC-331 control-average / centered response decomposition

## Parent and scope

TPC-331 is the direct structural continuation of TPC-330.  It keeps the same
two held-out origins `28001,36001`, scales `4096,8192`, four shell anchors,
two kernel exponents, four sign laws, five coordinate bijections, and locked
V59 declared source model.  The TPC-330 producer and certificate are parent
locked.

## New exact structure

For `w_j=P_j v`, `v_bar=mean_j w_j`, and `z_j=w_j-v_bar`,
`sum_j z_j=0`.  For each finite quadratic form `q`,

```text
mean_j q(w_j) = q(v_bar) + mean_j q(z_j).
```

Applied to the signed-Gram energy `E`, coordinate diagonal `D`, and
off-diagonal `O=E-D`, this gives the exact three-component decomposition:

```text
mean E = E_coherent + E_centered
mean D = D_coherent + D_centered
mean O = O_coherent + O_centered
```

No ratio is averaged in this identity.

## Finite certificate

The certificate has 32 rows and 128 law-level decompositions.  Negative/positive
off-diagonal census:

| law | average | coherent | centered |
|---|---:|---:|---:|
| all-plus | 0/32 | 1/31 | 0/32 |
| alternating index | 23/9 | 23/9 | 23/9 |
| mod-4 character | 32/0 | 32/0 | 32/0 |
| half split | 32/0 | 32/0 | 32/0 |

For all-plus, the ratio ranges are:

```text
average  [1.0291358503710915, 2.6078747190560239]
coherent [0.99496392236342945, 4.7216117506002702]
centered [1.0059897276060032, 2.7607585737280149]
```

The largest float64 identity residuals are `4.76837158203125e-6` for energy,
`2.6226043701171875e-6` for the diagonal, and `5.9604644775390625e-6` for
the off-diagonal.  The exact rational anchor is on `[36001,36016]`, `Q=4`,
shell `{5,7}`, `s=1`.

## Claim firewall

```text
TPC331_EXACT_MEAN_CENTERED_DECOMPOSITION = PROVED_EXACT_FINITE
TPC331_SOURCE_NATIVE_VECTOR = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC331_CONTROL_AVERAGE_CENSUS = NUMERICALLY_CERTIFIED_FINITE_32_OF_32
TPC331_CENTERED_POSITION_CENSUS = NUMERICALLY_CERTIFIED_FINITE_32_OF_32
TPC331_COHERENT_CENSUS = NUMERICALLY_CERTIFIED_FINITE_31_OF_32
TPC331_NUMERIC_IDENTITY = NUMERICALLY_CERTIFIED_FINITE
TPC331_ARITHMETIC_ADVANCE = NO
TPC331_FIXED_POWER_CREDIT = 0
TPC331_GROWING_SOURCE_NATIVE_L2 = OPEN
TPC331_FULL_GATE_B = OPEN
TPC331_TWIN_PRIME_RESULT = NONE
```

The local checker is a fail-closed Bridge-B fallback.  Session-named official
Route-A/Route-B evaluator files are absent, so this bridge does not claim an
official route pass.
