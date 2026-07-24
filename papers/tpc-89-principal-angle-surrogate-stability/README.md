# TPC-89: Principal-angle surrogate stability

This paper rewrites determinant flatness as an exact principal-angle
quantity on the literal post-bin support.

For a nonzero coefficient `a` on a prescribed support of size `S`,
write

```text
Z = <a, 1>,
D = ||a||_2^2,
rho(a) = |Z| / sqrt(S D),
F(a) = |Z|^2 / D.
```

Then

```text
D = |Z|^2 / S + D_perp,
F(a) = S rho(a)^2.
```

## Sharp perturbation theorem

If

```text
||a - b||_2 <= delta ||b||_2,    0 <= delta < 1,
```

and `r = rho(b)`, then the exact sharp envelope is

```text
L(r,delta) <= rho(a) <= U(r,delta),
```

where, with `alpha = arccos(r)` and `gamma = arcsin(delta)`,

```text
L = cos(min(pi/2, alpha + gamma)),
U = cos(max(0, alpha - gamma)).
```

Both endpoints are attained in dimension two. In particular,

```text
|rho(a) - rho(b)| <= delta,
```

with optimal constant `1`.

The elementary estimate

```text
rho(a) <= (rho(b) + delta) / (1 - delta)
```

is valid but nonsharp. The denominator comes from separately
estimating the numerator and norm; the projective-angle proof removes
it.

## Critical surrogate barrier

To transfer an upper target

```text
rho(b_J) = O(1/J)
```

uniformly, relative `l2` accuracy

```text
delta_J = O(1/J)
```

is sufficient and necessary in order. Merely `delta_J = o(1)` is
not enough. A sharp two-dimensional tangent example has

```text
rho(b_J) = 0,
relative error = delta_J,
rho(a_J) = delta_J.
```

Taking `delta_J = J^(-1/2)` gives an `o(1)` approximation that misses
the required angle by a factor `J^(1/2)`.

To preserve a two-sided statement `rho ~ 1/J` uniformly from the
norm hypothesis alone, the error constant must also be strictly
smaller than the surrogate's lower signal constant. An error exactly
equal to that signal can erase it.

## Literal TPC-32 crosswalk

Let `A_X` be the already aggregated fixed-`h0` TPC-32 determinant
coefficient on its actual support `Omega_X`, with

```text
S_X << X^o(1) Q_X.
```

A same-frame surrogate satisfying

```text
rho(b_X) <= X^o(1) / J_X,
||A_X - b_X||_2 / ||b_X||_2 <= X^o(1) / J_X
```

would certify

```text
F(A_X) <= X^(1/400 + o(1))
```

at

```text
Q_X = X^(267/400 + o(1)),
J_X = X^(133/400 + o(1)).
```

This is an exact L1 stability certificate. The paper does not
construct such a surrogate and proves no new L2 arithmetic estimate.

## Normalization and claim boundary

- `rho` must be computed on the actual literal support. Zero padding
  changes `rho`, even though it leaves `F` unchanged.
- The determinant ledger `lambda_D <= 2 eta_Z` is separate from the
  physical-loss rule `Lambda_phys < 1/400`.
- Surrogate accuracy is a third interface and cannot be spent as an
  arithmetic saving without a proved crosswalk.
- The paper does not specialize `h0` to `2`, breach sieve parity,
  prove a prime-pair lower bound, or prove the twin-prime conjecture.

## Build

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

```text
principal-angle-surrogate-stability.pdf
```
