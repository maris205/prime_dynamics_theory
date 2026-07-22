# RH-77: postblock effective-rank compression

This directory contains the seventy-seventh RH-layer paper:

> *Postblock Effective-Rank Compression Reopens the Directional Route*

## Main theorem

Let `B=A^M X` be the postblock state and

    O_M = sum_{r=0}^{M-1} (A^r)^* Y^*Y A^r.

If `q=||A^M||<1`, the full observability Gramian satisfies

    ||O|| <= ||O_M||/(1-q^2).

For any rank-r approximation `B_r`, the complete future Hardy energies obey

    |T(B)-T(B_r)|
      <= sqrt(||O_M||/(1-q^2)) ||B-B_r||_F.

The truncated SVD minimizes the residual. Thus low rank after one block is a
fully nonnormal alternative to global single-arc phase compression.

## Validated five-scale result

For the exact-dyadic frozen production systems, Arb recomputes `A^M X`, the
rank candidates, their residuals, the one-block observability upper, and the
full future perturbation.

- rank 2 captures at least `99%` in all ten channels;
- rank 4 captures at least `99.9999%` in all ten channels;
- postblock participation rank never exceeds `1.868`;
- the largest rank-4 full-future Hardy perturbation is `5.35e-6`.

## Route consequence

The failure of one global phase arc is not fatal. The actual postblock state
has uniformly tiny observed effective rank, so the all-level target can be
reformulated as a singular-value decay theorem. What remains open is proving
that rank-4-style decay analytically for every dyadic level and transporting it
from frozen matrices to the analytic family.

## Reproduction

~~~bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_effective_rank_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf postblock-effective-rank-compression.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
~~~
