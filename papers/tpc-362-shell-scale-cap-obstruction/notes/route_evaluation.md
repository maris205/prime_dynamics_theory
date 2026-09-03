# TPC-362 route evaluation and proof package

## Object and scope

We use the literal finite prime-shell block

\[
 B_p(u,t)=p\frac{66^{2s}}{(66^2+(u-t)^2)^s}
 (1_{p\mid u-t}-(p-1)^{-1})1_{u\ne t}1_{p\nmid u}1_{p\nmid t},
\]

with the TPC-355 unsigned mask-energy congruence
`G_u=sum_{p,t}B_p(u,t)^2` and the symmetric normalization
`D_G^{-1/2} A D_G^{-1/2}`.  This is a finite operator audit on the frozen
TPC-361 origins.  It does not use the source response or perform arithmetic
reassembly.

## Established finite facts

* **PROVED_EXACT_FINITE:** the Schur row-sum and Frobenius inequalities bound
  the operator norm for every finite matrix in the declared model.
* **NUMERICALLY_CERTIFIED_FINITE:** a complete four-law replay covers 384
  rows, with a reverse-shell implementation and a 15-mutation stress test.
  The rational `Q=4` anchor on `[313060,313073]` is symmetric and has positive
  geometry.
* **NUMERICALLY_CERTIFIED_FINITE_SCOPED:** the low-shell range
  `Q={12,24,36,54,80}` retains Schur maximum `0.80830232610282304` and
  spectral maximum `0.62690716242733457`; these stay below the working caps
  `0.83` and `0.64`.
* **NUMERICALLY_CERTIFIED_FINITE_SCOPED:** the full ladder reaches Schur
  maximum `1.7172665118910415` and spectral maximum `1.6398895499394266`.
  The first cap failure is at `Q=128`; there are 33 Schur and 30 spectral
  violations across the 384 rows.

## Strongest obstruction

The finite cap is not shell-uniform.  The Q-transition census has 200
increases and 136 decreases among 336 adjacent transitions, with no flat
transition under guard `1e-8`.  Thus the `Q<=80` behavior cannot be silently
extended to `Q>=128`, and a growing masked-operator estimate remains open.
The winner census (78 all-plus, 4 alternating-index, 14 mod-4, 0 half-split)
also shows that the high-Q effect is not logically reducible to a single
universal sign law.

## Claim firewall

```text
TPC362_SHELL_SCALE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_384_ROWS
TPC362_FINITE_SCHUR_ENVELOPE = PROVED_EXACT_FINITE
TPC362_FINITE_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE
TPC362_LOW_Q_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC362_HIGH_Q_CAP_EXTENSION = REFUTED_SCOPED_ON_DECLARED_Q_LADDER
TPC362_LAW_WINNER_CENSUS = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC362_GROWING_OPERATOR_BOUND = OPEN
TPC362_SOURCE_UNIFORM_L2 = OPEN
TPC362_ARITHMETIC_ADVANCE = NO
TPC362_FIXED_POWER_CREDIT = 0
TPC362_FULL_GATE_B = OPEN
TPC362_TWIN_PRIME_RESULT = NONE
```

The official Session-named evaluator files are absent.  Consequently neither
official Route A nor Route B is declared passed; local Bridge-B is only a
fail-closed reproducibility control.  The high-Q negative result is scoped to
the declared finite ladder and does not refute an appropriately renormalized
future theorem.

## Reusable structure and next clue

```text
frozen high-origin panel
  -> low/high shell-scale partition
  -> all-law normalized envelope and spectrum replay
  -> Q-transition and winner census
  -> reverse-shell replay + mutation stress + exact anchor
  -> finite cap extension refutation
```

`ROUND2_CLUE = LOCALIZE_HIGH_Q_OBSTRUCTION_BY_LAW_AND_ROW_GEOMETRY`.
The next defensible question is which law and which row-level geometry cause
the first `Q=128` violation, while keeping any proposed repair finite and
explicitly conditional.
