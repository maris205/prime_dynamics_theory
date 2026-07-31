# RH-324: Sharp physical endpoint-to-affine leg remainder

This paper replaces the first tangent leg of RH-323 by the exact finite-noise
folded physical kernel.  For the endpoint source `x = 1 - sigma*v`, write

```text
c_(sigma,v) = alpha*v - u_c*sigma*v^2.
```

On the negative endpoint branch, the physical row differs from the full
Gaussian `phi(u+c_(sigma,v))` by the exact boundary identity

```text
2 * [normal_survival(r/sigma-c_(sigma,v))
     + normal_survival((1-r)/sigma+c_(sigma,v))].
```

The remaining curved-to-tangent error is exactly

```text
4*Phi(u_c*sigma*v^2/2) - 2.
```

After averaging against the RH-322 entrance profile and restoring its exact
finite folded seed, the physical one-leg joint law satisfies an explicit
bound of the form

```text
||P_(sigma,a) - A_d||_1
  <= |a-d| + C(a)*sigma + explicit Gaussian tails.
```

For every fixed phase `d`, the phase-matched result is sharp:

```text
lim_(sigma->0) ||P_(sigma,d)-A_d||_1 / sigma
  = sqrt(2/pi)*u_c*(d^2 + 1 + d*phi(d)/Phi(d)) > 0.
```

Thus the fold, state boundary, and exact row normalizer contribute only
exponentially small terms, while quadratic curvature gives a genuinely
linear joint remainder.  Exponential affine accuracy is false.

At the first-alias clock, `R^(-2k) = Theta(sigma^theta)` with
`theta = log(1.4)/log(lambda) = 0.6496301165... < 1`; hence the local
phase-matched `O(sigma)` scale is smaller than `R^(-2k)`.  This is only a
scale comparison, not a moving-order Duhamel or trace theorem.

The second physical leg, parity layer, neighboring shell, and joint
first-alias trace replacement remain open.  Gates A--E remain false/open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf sharp-physical-endpoint-affine-leg-remainder.pdf
```
