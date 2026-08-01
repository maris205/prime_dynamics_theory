# RH-332: Sharp Physical Repelling-Return Affine-Leg Remainder

RH-332 proves the sharp remainder for the second physical row after the
actual RH-324 endpoint-to-repelling prefix.  In repelling coordinates

```text
x = r + sigma*u,
y = r + sigma*w,
d_sigma(u) = lambda*u + u_c*sigma*u^2,
```

the Jacobian-scaled physical row is exactly

```text
L_sigma(u,w)
  = [phi(w+d_sigma(u))
     + phi(w+2*r/sigma-d_sigma(u))]
    / Z_sigma(r+sigma*u) * 1_(I_sigma)(w).
```

Its distance to the full curved Gaussian is exactly two state-boundary
tails, and the curved-to-tangent distance is

```text
4*Phi(u_c*sigma*u^2/2) - 2.
```

The actual first-leg marginal `mu_(sigma,a)` has a uniform fourth moment on
compact phase sets.  Consequently, for either repelling orientation and
`a_sigma -> d`, the exact second hybrid Duhamel row term satisfies

```text
D_(sigma,a_sigma)^(+/-) / sigma
  -> sqrt(2/pi)*u_c * integral_(+/- u > 0) u^2 p_d(u) du > 0.
```

The two coefficients sum to

```text
sqrt(2/pi)*u_c
  * [1 + alpha^2*(d^2 + 1 + d*phi(d)/Phi(d))].
```

Thus exponential and `o(sigma)` accuracy are false for this precisely typed
hybrid row term.  The row coefficient is zero at `u=0`, and the moving
source `u=(b-r)/sigma` gives an order-one obstruction to a global uniform
`O(sigma)` row bound.

Both hybrids use the same actual physical first-leg prefix and retain `u`.
The theorem is not an equality between the fully physical and fully affine
two-leg laws, and the `W` marginal receives only an `L1` contraction bound.
The signs `U<0` and `U>0` are orientations around the repelling point `r`,
not the RH-19 critical siblings around `b`.

No all-cycle transport, cyclic trace control, parity/shell cancellation,
full-trace replacement, determinant gluing, or Gate A--E promotion is
obtained.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf sharp-physical-repelling-return-affine-leg-remainder.pdf
```
