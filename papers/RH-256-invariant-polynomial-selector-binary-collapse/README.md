# RH-256: Invariant Polynomial-Selector Binary Collapse

This paper proves a structural firewall for the proposed signed/complex route.
If a selector is an idempotent polynomial in a finite operator, then on each
generalized root space it is either zero or the identity.  Signed or complex
monomial coefficients are merely coordinates for a binary spectral mask; they
do not create fractional spectral multiplicities.

Consequently the RH-255 expanded box obstruction already excludes every real,
conjugate-closed idempotent polynomial selector supported on that resolved
window.  A 6-shell interpolation diagnostic confirms that complex polynomial
coordinates reproduce binary nodal values, with residual at most `7.31e-14`.

The result does not exclude non-idempotent signed quotient grouping or an
operator outside the resolved finite spectral algebra.

Gates A--E remain false/open.  No Hilbert--Polya operator, zeta-divisor
equality, Riemann-zero identification, or RH implication is claimed.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_polynomial_selector_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf invariant-polynomial-selector-binary-collapse.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
