# RH-330: Joint-cancellation full-trace transfer criterion

RH-330 proves an exact but inactive transfer criterion for the moving
first-alias coefficient and its contribution to a weighted full-trace
prefix.  It does not prove that the actual noisy operator satisfies the
criterion.

On a fixed-phase clock, let `H_k = k R^(-2k)` and choose a weighted prefix
containing order `2k` but no second alias.  Its nonnegative error splits
exactly as

```text
E_prefix = E_off + |e_actual,k|/(2 H_k).
```

Therefore the prefix vanishes exactly when the off-alias background vanishes
and `e_actual,k = o(H_k)`.  RH-330 does not supply the off-alias hypothesis.

For the observable packet use the five slots

```text
e = B + S + R + P - A.
```

If hats denote a frozen model and `Delta` denotes actual minus model, define

```text
Theta = Delta_B + Delta_S + Delta_R + Delta_P - Delta_A.
```

Then

```text
e_actual = e_model + Theta
```

exactly.  Hence a closing model transfers if and only if `Theta=o(H_k)`.  A
modular auditable sufficient condition keeps the critical signed aggregate
small and controls the already aggregated far slot separately:

```text
Delta_B + Delta_S + Delta_P - Delta_A = o(H_k),
Delta_R = o(H_k).
```

The separate far condition is sufficient, not logically necessary; it
prevents an uncontrolled far contribution from being used as an accidental
repair.

The exchange/observation split is not intrinsic.  The transformation

```text
X -> X+t,       E_obs -> E_obs-t
```

leaves the observable shell `S=X+E_obs` unchanged.  Unless a physical
identification map is frozen in advance, transfer must therefore compare
`S`, not claim separate smallness for `X` and `E_obs`.

For two length-`2k` critical product channels, the criterion retains every
one of the `4k` Duhamel hybrid terms before grouping.  Coupled signed group
enclosures give a sharp residual interval.  Singleton absolute majorants are
a safe fallback, but they are not necessary: defects `(+A_k,-A_k)` cancel
exactly even though their absolute budget is `2A_k >> H_k`; the same unsigned
bounds with `(+A_k,+A_k)` give a defect `2A_k`.

Applied to RH-329, with

```text
e_model/A_k -> -(1-C_*C_M),      A_k/H_k -> infinity,
```

actual closure requires the exact repair law

```text
Theta_k = -e_model,k + o(H_k).
```

The synthetic choice `Theta_k=-e_model,k+H_k/k` closes to `H_k/k`.  Thus an
isolated-model no-go cannot be promoted to actual divergence without a
replacement theorem.  Conversely, `Theta_k=o(A_k)` would transfer the
negative divergence, but no such actual bound is known.

The result ledger contains six exact-arithmetic reproduction rows and 344
synthetic signed Duhamel terms.  These examples are not physical data.

No actual identification map, off-alias budget, physical two-channel
Duhamel enclosure, signed far-remainder theorem, full-trace replacement,
full-trace divergence, determinant gluing, Gate A--E closure,
Hilbert--Polya operator, Riemann-zero identification, zeta-divisor equality,
or RH conclusion is obtained.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf joint-cancellation-full-trace-transfer-criterion.pdf
```
