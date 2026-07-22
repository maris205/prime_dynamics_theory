# RH-96: gap-weighted weak-mode quotient

This directory contains the ninety-sixth RH-layer paper:

> *Gap-Weighted Weak-Mode Quotients for Adaptive Ritz Enrichment*

## Main theorem

For a positive block matrix

    H = [[A, C], [C*, D]],

let `Phi_r` denote the sum of the largest `r` eigenvalues. If the retained
Ritz cutoff satisfies `lambda_r(A) >= alpha`, the omitted block satisfies
`D <= beta I`, and `alpha > beta`, then

    0 <= Phi_r(H) - Phi_r(A) <= ||C||_F^2 / (alpha - beta).

This converts omitted weak directions into a certified energy loss. A
gap-free companion bound is `2 ||C||_* + trace(D)`.

## 384-bit result

Across the 120 RH-94 updates:

- relative cutoff `1e-8` omits the fourth mode in exactly five updates;
- all five omitted losses satisfy the gap-weighted certificate;
- the adaptive chain uses width 3 five times and width 4 115 times;
- all ten endpoint gates remain green, with worst ratio 1.00117232;
- the largest adaptive/full one-step tail ratio is 1.00000465.

More aggressive cutoffs fail cumulatively: `1e-6` reaches endpoint ratio
1.02492120 and `1e-4` reaches 1.01409153, even though every local omitted loss
is certified. The next layer must compose local quotient losses into a horizon
budget.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_weak_mode_quotient_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_weak_mode_quotient_audit.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf gap-weighted-weak-mode-quotient.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
