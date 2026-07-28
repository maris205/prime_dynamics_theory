# RH-232: Biorthogonal Riesz-cloud projection

This paper constructs floating finite-dimensional left/right spectral
projector candidates for the 32 shell-complete endpoints of RH-222.

For right and left eigenvector matrices `R` and `L`, with
`G=L^*R` invertible, the candidate is

    P = R G^{-1} L^*.

The algebraic formula is exact for a finite invariant subspace.  Numerically,
however, the overlap becomes severely ill-conditioned: the largest candidate
projector norm is about `2.26e12`, and 17 of 32 endpoints exceed `1e6`.
Eigenpair residuals remain below `2.2e-12`, so the obstruction is conditioning,
not failure to resolve the listed eigenvalues.

The result identifies a real wall for a direct operator-level Riesz proof.
It does not invalidate the finite spectral cloud or prove that an interval
Riesz contour cannot exist.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_riesz_projection_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf biorthogonal-riesz-cloud-projection.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
