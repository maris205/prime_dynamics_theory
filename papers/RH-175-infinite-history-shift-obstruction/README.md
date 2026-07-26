# RH-175: Infinite-History Shift Obstruction

The literal square completion of the normalized history cocycle contains a
weighted unilateral shift of radius `q=sqrt(eta)`.  RH-175 proves:

```text
spectrum(L) = spectrum(B) union { |z| <= q },
essential spectrum(L) = { |z| = q }.
```

No positive power is compact or Schatten, so the direct Fredholm determinant
route is unavailable.  Finite truncations have only zero shift eigenvalues,
but the audit records an interior resolvent lower bound above `10^39.9` at
length 64.

This rejects only the literal infinite weighted-history shift.  Finite cyclic
closures and scattering/relative constructions remain open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /root/math/.venv/bin/python experiments/run_shift_obstruction_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf infinite-history-shift-obstruction.pdf
```
