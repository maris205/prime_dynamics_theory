# RH-252: Deterministic-Numerator Analytic-Tail Certificate

RH-46 proves that the deterministic one-step numerator `G` is holomorphic and
nonzero on `|z| < lambda`, with `lambda = 1.6785735104283177...`.  RH-243
defines the Hardy-scaled trace-style coefficients `a_n` by
`log G(z/r_H) = -sum a_n z^n/n`, where `r_H = 0.85`.

This paper makes the resulting all-order target tail explicit.  The scaled
zero-free radius is `r_H lambda = 1.42678748386407... > 1`.  For every
`0 <= R < S < r_H lambda`, Cauchy's estimate gives a geometric bound for the
deterministic target tail and an exponential conversion for the corresponding
determinant error.

The boundary supremum `M_S = sup_{|z|=S}|log G(z/r_H)|` is not numerically
certified here.  Thus this is an exact analytic interface, not a numerical
uniform cloud certificate.  The current cloud-to-anchor bridge, quotient tail,
all-order cloud envelope, and Gates A--E remain open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_analytic_tail_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf deterministic-numerator-analytic-tail-certificate.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
