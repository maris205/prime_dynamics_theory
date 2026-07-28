# RH-229: Nonnormal Frobenius Tail-Budget Barrier

Schur triangularization gives

```text
sum |lambda_j|^2 <= ||A||_F^2.
```

After subtracting the Perron, parity, and selected-cloud eigenvalue masses,
this yields a valid whole-matrix upper bound for the remaining `det_2`
logarithmic tail.

The certificate is far too loose. On the unit disk its upper bound grows from
`5.15135` to `169.27116`; no endpoint passes the gate `<1`. The fitted
growth exponents are `1.025` and `1.033` in `sigma^{-alpha}`, and the
whole-matrix bound can be 5,563 times the resolved-shell bound.

This rejects the raw Frobenius certificate, not the determinant. A reducing
complement, singular-direction removal, or two-step trace-class bound may be
much sharper.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_frobenius_tail_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf nonnormal-frobenius-tail-budget-barrier.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
