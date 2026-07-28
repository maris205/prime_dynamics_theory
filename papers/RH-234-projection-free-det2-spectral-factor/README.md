# RH-234: Projection-free `det_2` spectral factor

For a Hilbert--Schmidt operator, the regularized determinant is the canonical
product over eigenvalues with algebraic multiplicity.  A finite selected
multiset therefore gives an exact factor

    det_2(I-zA) = C_cloud(z) R_cloud(z),

where each factor uses `(1-z lambda) exp(z lambda)`.  The identity is
independent of eigenvector conditioning.

The archived RH-222 candidate clouds were split into selected and resolved
complement roots on a 192-point, four-radius grid.  All 6,144 multiplicative
checks pass; the largest absolute error is `1.83e-15`.  This bypasses the
`2.26e12` projector norm from RH-232, but it does not identify the asymptotic
cloud divisor or its complementary limit.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_spectral_factor_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf projection-free-det2-spectral-factor.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
