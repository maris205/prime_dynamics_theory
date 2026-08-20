# TPC-215 Paper Plan

## Title

Short-Quotient Mobius Tails and a No-Power-Loss Majorant for the Physical Cluster Gram

## Research question

Once TPC-214 has identified the literal cluster coefficient `C_h`, how large
can the complete-period physical cluster Gram be relative to the divisor
direct-sum energy on the actual V46 band `Y0<d<=U`?

## Main theorem

The integer reciprocal cutoff forces every emitter-active reduced denominator
into `h>=H/q_max>=2Y0`.  Consequently `h` itself occurs in the full squarefree
divisor band and the quotient in `d=hk` is bounded by

```text
k <= U q_max/H <= 2x^(23/2400+o(1)).
```

The `k=1` term anchors the diagonal mass, while the remaining terms admit a
harmonic majorant.  Combined with the exact reduced-denominator row
decomposition, this gives a complete-period cluster/direct comparison with
factor `O((log x)^2)=x^(o(1))`.

## Sharp scoped obstruction

For active `h` in the top shell `U/2<h<=U`, the only band multiple is `d=h`.
Hence the rowwise cluster/direct ratio is exactly one.  Cluster algebra alone
cannot provide a uniform fixed-power saving; any saving must use arithmetic
control of the direct-sum energy or additional coupling outside this algebra.

## Evidence package

1. Source-locked rational exponent ledger.
2. Exact activation, quotient, and row-decomposition proofs.
3. Exact rational finite emitter rows and independent reconstruction.
4. Exhaustive finite checks of the harmonic majorant and top-shell equality.
5. Fail-closed release checker and claim registry.

## Claim ceiling

```text
PROVED = ACTIVATION_FLOOR_SHORT_QUOTIENT_NORMAL_FORM_AND_ROW_DECOMPOSITION
PROVED_ASYMPTOTIC_STRUCTURAL = O_LOG_X_SQUARED_CLUSTER_TO_DIRECT_MAJORANT
REFUTED_SCOPED = UNIFORM_ROWWISE_FIXED_POWER_CLUSTER_SAVING
NUMERICAL_OBSERVATION = FINITE_TAIL_AND_GLOBAL_ENERGY_RATIOS
OPEN = DIRECT_SUM_ARITHMETIC_ENERGY_FINITE_WINDOW_GRAM_AND_PRIME_SHELL_REASSEMBLY
ARITHMETIC_ADVANCE = NO
```

## Sections

1. Literal V46 source lock.
2. Activation floor and short-quotient tail.
3. Exact row decomposition.
4. No-power-loss majorant.
5. Top-shell obstruction and finite certificate.
6. Route evaluation and next theorem.
