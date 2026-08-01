# RH-335: Projector-Localized Parity Ledger and Cellwise Extension Nonuniqueness

RH-335 gives a finite-order exact localization of the scalar parity correction
after the physical basepoint observation was repaired in RH-334.  Let
`E_minus_sigma` be the rank-one Riesz projector of the real simple noisy
parity eigenvalue `lambda_minus(sigma)`.  The projector itself, not
`lambda_minus*E_minus`, defines

```text
pi_sigma(J) = Tr(M_J E_minus_sigma).
```

If right and left eigenfunctions are `v,w`, then

```text
d pi_sigma = v*w / <w,v> * dm.
```

Thus `pi_sigma` is a real finite signed measure, is invariant under independent
nonzero rescalings of `v` and `w`, and has total mass one.  It need not be a
probability measure.

For a frozen measurable cell `J` and `n>=2`, define

```text
C_sigma,n(J)
  = r_H^(-n) [
      L_sigma,n(J) - P_n^abs(J)
      + ((-1)^n-lambda_minus(sigma)^n) pi_sigma(J)
    ].
```

For every frozen finite partition `P`, exact additivity gives

```text
sum_(J in P) C_sigma,n(J) = c^H_sigma,n - c^H_n.
```

At the first alias `n=2k`, `k>=2`, the Hardy full-trace constituent is

```text
q_FT = sum_(J in P) C_sigma,2k(J) - A_k,2k.
```

The counterloop alias packet is subtracted; omitting `-A_k,2k` is incorrect.
Allocating the deterministic scalar `(-1)^n` with the *noisy* density
`pi_sigma` is a frozen gauge.  It is not a canonical physical localization,
a physical local parity density, or transport of a deterministic projector.

The Perron scalars cancel in the global difference, but that cancellation
does not imply local projector deflation commutes with windows.  An exact
positive rational row-stochastic fixture has spectrum `{1,-2/5,1/5}` and
strictly satisfies

```text
[M_2, E_0 + (-2/5)^2 E_minus] != 0,
Tr([M_2, E_0 + (-2/5)^2 E_minus]) = 0.
```

The zero commutator trace is therefore irrelevant to commutation.

For the same nonphysical algebraic fixture, with `r_H=17/20`, `n=2`, and
all deterministic singleton slots set to zero, exact arithmetic gives

```text
pi = (10/17, -4/51, 25/51),
C  = (400/289, 400/4913, 6672/4913),
sum C = 48/17.
```

The negative middle projector mass proves directly that these masses are not
probabilities.  The `n=2` row is only a fixed-order ledger check; it is not a
`k=1` first-alias counterloop claim.

RH-335 also proves a scoped nonuniqueness theorem.  A global parity scalar
does not determine its local signed allocation: adding any finite signed
measure of total mass zero changes cell values while preserving the aggregate
over every finite partition.  The projector-density allocation is one frozen
extension among infinitely many.  No claim is made that the particular
RH-334 gauge interval has nonzero corrected projector mass.

The planned adapted-norm physical upper-exponent route remains
`STOP_SCOPED/NOT_TESTABLE`.  RH-325 still lacks:

1. uniform physical `delta_j=O(sigma)` for all legs;
2. physical trace-observation and prefix/suffix norm upper bounds; and
3. `max_j W_j=O(sigma^(-gamma))` for some
   `gamma<0.3503698834605293...`.

RH-18 proves only the lower bound
`cond(D_G)>=sigma^(-1/4+o(1))`; it cannot replace any required upper bound.
No moving-order or `o(H_k)` estimate, signed Duhamel cancellation, physical
projector transport, determinant closure, Gate A--E progress, or
Hilbert--Polya/Riemann-zero/RH conclusion is obtained.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf projector-localized-parity-ledger-and-cellwise-extension-nonuniqueness.pdf
```
