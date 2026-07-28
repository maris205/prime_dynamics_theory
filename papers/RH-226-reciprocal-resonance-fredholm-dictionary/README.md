# RH-226: Reciprocal Resonance--Fredholm Dictionary

For a finite resonance multiset `Lambda`,

```text
det(I-zA) = product(1-z lambda)
          = z^n p(1/z),
```

where `p(w)=product(w-lambda)`. The Fredholm and regularized Fredholm zeros
are therefore `1/lambda`, not `lambda`.

The finite identity is verified on 3,072 grid evaluations with maximum error
`9.16e-15`. Reciprocal moduli range from `1.15129` to `13.54281`, and
the scale-free zero-factor residual is below `2.29e-16`.

RH-7 already proves the fixed-positive-noise Hilbert--Schmidt `det_2`. This
paper supplies the exact dictionary from the new rank-growing atlas to that
object; it does not claim a small-noise determinant limit. Direct product
evaluation at outer zeros is deliberately reported as numerically unstable.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_fredholm_dictionary_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf reciprocal-resonance-fredholm-dictionary.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
