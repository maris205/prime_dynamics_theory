# RH-200: Conjugate-Pair Parity and Edge-Quartet Selection

The physical matrices are real, so nonreal spectral modes occur in conjugate
pairs.  At each of the three audited scales and on both left/right channels,
the four largest-modulus eigenvalues form two conjugate pairs, are all
source-observable, and are separated from the fifth modulus by at least
`0.05949`.

This gives a principled finite selection rule:

```text
select the four source-observable modes at the outer spectral edge.
```

It explains why an odd length-three packet cannot represent the full real
edge object when the edge consists of two nonreal pairs.  The RH-185 length-
three candidates indeed have zero two-sided passes at all audited scales,
while the finest length-four branch has 12 passes.

The result is not an all-level edge-gap theorem and does not identify these
conjugate pairs with prime pairs or any zeta arithmetic.  It is a finite
canonicity improvement: the quartet can be selected by an edge rule rather
than by matching after the fact.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_edge_quartet_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf conjugate-pair-edge-quartet-selection.pdf
```
