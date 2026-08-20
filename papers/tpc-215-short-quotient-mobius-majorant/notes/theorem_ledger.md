# Theorem Ledger

| Item | Status | Evidence | Boundary |
|---|---|---|---|
| V46 scale and divisor source lock | PROVED / LOCKED | V46 Eq. (1.1), (1.3), (1.5) | No altered band or shell |
| Emitter activation floor | PROVED_EXACT | Integer nonzero cutoff | Necessary condition only |
| Active `h` belongs to `D_x` | PROVED_EXACT | Squarefree divisor + `h>=2Y0` | Uses full band |
| Short-quotient tail normal form | PROVED_EXACT | `d=hk`, multiplicativity of `mu` | Active rows only for diagonal anchor |
| Quotient exponent `23/2400` | PROVED_EXACT | Rational exponent ledger | Constants absorbed only in `o(1)` |
| Row norm divisor decomposition | PROVED_EXACT | Reduced fractions + TPC-214 covariance | Complete residue rows |
| Cluster/direct majorant | PROVED | Harmonic triangle + diagonal anchor | No saving claimed |
| `A_x=O((log x)^2)=x^(o(1))` | PROVED_ASYMPTOTIC_STRUCTURAL | Source-locked scales | No arithmetic `L2` |
| Top-shell coefficient ratio one | PROVED_EXACT | No second multiple below `U` | Rowwise obstruction only |
| Finite tail/global ratios | NUMERICAL_OBSERVATION | Exact rows, real logarithms | Not asymptotic evidence |
| Direct-sum arithmetic energy | OPEN | No attached theorem | First arithmetic blocker |
| Finite-window off-frequency Gram | OPEN | Complete period only | Physical interval missing |
| Prime-shell/four-packet reassembly | OPEN | No collective theorem | Gate B unpaid |
| Fixed atom / TPC endpoint | OPEN | Credit `0` | No twin-prime claim |

## Strongest positive result

The literal V46 cluster Gram is at most an explicit `O((log x)^2)` multiple of
the divisor direct-sum emitter energy.  Shared reduced frequencies create no
fixed-power amplification.

## Strongest obstruction

Every active top-shell denominator has cluster/direct coefficient ratio exactly
one, so cluster algebra alone cannot create a uniform rowwise power saving.

## Open theorem

Bound the source-locked direct-sum arithmetic energy on the physical interval,
while retaining the finite-window off-frequency Gram and prime-shell/four-
packet reassembly.

## Reusable structure

```text
integer activation floor
  -> active denominator belongs to full band
  -> short quotient Mobius tail
  -> diagonal anchor + harmonic majorant
  -> exact row-norm divisor decomposition
```

## ROUND2_CLUE

```text
BOUND_THE_DIRECT_SUM_PHYSICAL_ROW_ENERGY_BEFORE_REINTRODUCING_CROSS_FREQUENCIES
```
