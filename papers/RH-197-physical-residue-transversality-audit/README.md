# RH-197: Physical Residue and Transversality Audit

The two physical edge quartets are source-observable and transverse, but not
well conditioned.  Their canonical minimum cross singular values are about
`5.21e-3` on the left and `1.05e-3` on the right, giving optimal
biorthogonal norm products `192.05` and `950.26`.  The minimum transfer
residue modulus is `1.107e-2`.

The late temporal packets converge not only in subspace angle but also in
conditioning: at the latest accepted windows their oblique condition numbers
differ from the canonical optima by less than two percent.  Thus the large
condition is mostly physical source--observation geometry, not a removable
choice of temporal basis.

This is a finite positive transversality result and a quantitative warning.
There is no uniform lower bound as `sigma -> 0`, so Gate A remains open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_physical_transversality_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf physical-residue-transversality-audit.pdf
```
