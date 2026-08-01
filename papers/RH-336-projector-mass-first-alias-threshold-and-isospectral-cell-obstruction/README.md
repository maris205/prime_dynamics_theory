# RH-336: Projector-Mass First-Alias Threshold and Isospectral Cell Obstruction

RH-336 isolates the moving-order scale of the RH-335 projector-density parity
gauge.  For a measurable cell `J`, put

```text
G_sigma,k(J)
  = r_H^(-2k) [1-lambda_minus(sigma)^(2k)] pi_sigma(J),
H_k = k R^(-2k),
eta_sigma = k-log(1/sigma)/(2 log(lambda)).
```

On every bounded-phase first-alias sequence with `k=k_sigma in N`, `k>=2`,

```text
G_sigma,k(J)/H_k
  = 2 C_* lambda^(eta_sigma) (beta R)^(2k)
      pi_sigma(J) [1+o(1)],
beta = 1/(r_H sqrt(lambda)).
```

The projector-mass exponent is

```text
kappa_proj
  = log(beta R)/log(lambda)
  = log(28/17)/log(lambda)-1/2
  = 0.463406944517002...       (ordinary decimal diagnostic).
```

It is distinct from the RH-325 Duhamel stability threshold
`gamma_*=0.3503698834605293...`.  The separation is exact: RH-334 gives
`lambda^3+4 lambda^2-16=0`, whose positive root satisfies
`lambda<17/10`, while

```text
(196/85)^2-(17/10)^3 = 116783/289000 > 0.
```

Therefore `196/85>lambda^(3/2)` and
`kappa_proj-gamma_*>0`.  The displayed decimals remain diagnostics only.
Exact phase conversion gives

```text
(beta R)^(-2k)
  = sigma^(kappa_proj) (beta R)^(-2 eta_sigma).
```

Consequently,

```text
G_sigma,k(J)=o(H_k)
iff
pi_sigma(J)=o((beta R)^(-2k)).
```

If `(beta R)^(2k) pi_sigma(J) -> p` and `eta_sigma -> eta`, then

```text
G_sigma,k(J)/H_k -> 2 C_* lambda^eta p.
```

For a fixed `N`-cell partition, `sum_i pi_sigma(J_i)=1`, so
`max_i pi_sigma(J_i)>=1/N`.  Since `beta R>1`, the maximum normalized parity
cell diverges.  Its maximizing index may depend on `sigma`; pigeonhole gives
only a subsequence on which one fixed cell recurs.  This cell is not
identified with physical `B+S`.  Raw localized defects, the remaining cells,
and the subtracted alias packet may still cancel it.

The second result is an exact finite algebraic obstruction.  Reuse the
RH-335 positive row-stochastic matrix `K` and parity projector `E_minus`, and
put

```text
S_t = [[1-t,t,0],[0,1,0],[0,0,1]],
K_t = S_t^(-1) K S_t.
```

For the convenient sufficient interval

```text
-5/174 < t < 1/2,
```

`K_t` is strictly positive and row-stochastic.  This interval is not claimed
maximal; the maximal connected positivity interval containing zero is

```text
(-5/174,(-19+sqrt(781))/12).
```

Similarity preserves the spectrum `{1,-2/5,1/5}` and, for every `m>=1`,

```text
Tr(K_t^m) = 1+(-2/5)^m+(1/5)^m.
```

Yet `E_minus(t)=S_t^(-1) E_minus S_t` has singleton masses

```text
pi(t) = ((10-8t)/17,(-4+24t)/51,25/51),
pi(t)-pi(0) = (8t/17)(-1,1,0).
```

In the fixed-order RH-335 fixture `n=2`, `r_H=17/20`, with deterministic
singleton slots zero,

```text
C(t) = ((6800-5760t)/4913,
        (400+5760t)/4913,
        6672/4913),
sum C(t) = 48/17.
```

The drift is `(5760t/4913)(-1,1,0)`.  At `t=1/100` it is exactly
`(-288/24565,288/24565,0)`.

This family is nonphysical finite algebra, and `n=2` is not a `k=1`
first-alias counterloop.  RH-210 already supplied an explicit fixed-divisor
similarity example with moving projectors.  RH-336 adds only the narrow
combination of strict
positivity, row-stochasticity, all power traces, and corrected singleton-cell
motion.

The intended physical `Delta_B+Delta_S` signed Duhamel cancellation remains
`NOT_TESTABLE`; no physical nonzero normalized obstruction is proved.  No
moving full-trace replacement, `o(H_k)` cancellation verdict, determinant
closure, Gate A--E progress, Hilbert--Polya construction, Riemann-zero
identification, von Mangoldt trace formula, completed-zeta equality, or RH
conclusion is obtained.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf projector-mass-first-alias-threshold-and-isospectral-cell-obstruction.pdf
```
