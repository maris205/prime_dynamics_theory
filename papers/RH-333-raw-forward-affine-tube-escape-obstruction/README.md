# RH-333: Raw Forward Affine-Tube Escape Obstruction

RH-333 proves a scoped negative result for the canonical raw, mass-one,
full-line forward affine reference along the RH-17 boundary cycle.  Here
`Q_j` is the `sigma`-scaled coordinate about `x_(k,j)`; the finite statements
take `k>=2` and `sigma>0` throughout.
Two signed noisy
one-step tangents compose to mean slope `S'(x_(k,j))` and innovation variance
`1+f'(f(x_(k,j)))^2`, so this is the canonical raw two-step component
coarsening.  The component cycle has period `k`, hence physical one-step
period `2k`.  Before the final tiny closing component row, the raw affine
variables obey

```text
Q_(j+1) = a_(k,j) Q_j + beta_(k,j) Z_j,   j=0,...,k-2,
a_(k,j) = S'(x_(k,j)).
```

The slopes remain signed in the forward means.  Expanding the preclosing
coordinate shows that the first innovation has propagated standard deviation

```text
s_k = beta_(k,0) prod_(j=1)^(k-2) |a_(k,j)|
    = beta_(k,0) |M_k| / (m_(k,0) m_(k,k-1)).
```

The archived analytic laws imply

```text
s_k = C_s lambda^(2k) (1+o(1)),
C_s = C_M sqrt(1+lambda^2)
      / (8 u_c^2 lambda sqrt(C_b)) > 0.
```

Every physical folded/normalized preclosing marginal is supported in the
scaled interval

```text
I_(sigma,k) = [-x_(k,k-1)/sigma,
                (1-x_(k,k-1))/sigma],
|I_(sigma,k)| = 1/sigma.
```

A Gaussian of standard deviation `s` puts at most
`2 Phi(L/(2s))-1` mass in any interval of length `L`, uniformly in its mean
and the interval location.  Conditioning on all variables except the first
innovation and using the unhalved `L1` convention therefore gives the exact
finite lower bound

```text
||mu_phys - mu_aff||_1
  >= 4 barPhi(1/(2 sigma s_k)).
```

Marginal contraction lifts this bound to retained component-prefix path laws
and to any full retained extension that still includes the preclosing
coordinate.  On a fixed first-alias phase

```text
eta_sigma = k - log(1/sigma)/(2 log(lambda)) -> eta,
```

one has `sigma*s_k -> c_eta = C_s lambda^(2 eta)` and hence

```text
liminf ||P_phys - P_aff||_1
  >= 4 barPhi(1/(2 c_eta)) > 0.
```

Thus, on every fixed phase or family confined to one compact phase window,
`O(k*sigma)` and `o(H_k)`, with `H_k=k*R^(-2k)`, are false for this raw
full-line forward affine retained-path comparison because both proposed upper
scales tend to zero.

This does **not** prove a lower bound for the final endpoint marginal after
the omitted tiny closing row.  It does not refute a cyclic bridge, Doob
transform, physical truncated/folded affine kernel, adapted reference, or
branch-complete nonlinear closing profile; those alternatives are not yet
defined in the required physical data type.  A retained probability path is
not a cyclic trace.  No trace observation, parity/shell cancellation,
full-trace replacement, determinant gluing, Gate A--E promotion, or
Hilbert--Polya/RH conclusion is obtained.

The symbolic theorem keeps `C_b` and `C_M` analytic.  Orbit identities are
evaluated at 110 decimal working digits before JSON conversion; the phase
table uses the archived decimals and binary64 normal-tail evaluation.  Both
are deterministic reproduction checks only, not interval certificates or
asymptotic evidence.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf raw-forward-affine-tube-escape-obstruction.pdf
```
