# RH-121: optimal Gram-gauge pairing

RH-121 solves the exact-Gram gauge problem left by RH-120.  Write the
ordered generalized tail spectra as

```text
alpha_1 <= ... <= alpha_4,      beta_1 <= ... <= beta_4.
```

Among every invertible `S` satisfying `S* G S = G'`, the smallest `b` for
which `D' <= b S* D S` is

```text
b_opt = max_i beta_i / alpha_i.
```

An optimizer aligns the ordered generalized eigenframes.  The result is
global over all exact-Gram gauges, not merely over permutations.

The five-scale audit contains 96 phase-matched adjacent-scale pairs.  All
theorem checks pass, but the finite data do not support a uniform `b`:
only 25 pairs are contractive, the median `b_opt` is `27.6936`, and the
maximum is about `9.88e290` after an explicit `1e-12` conditioning floor.
The huge values identify weak-direction mismatch; they are not used as an
asymptotic extrapolation or a support certificate.

