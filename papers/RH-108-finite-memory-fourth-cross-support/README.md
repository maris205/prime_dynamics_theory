# RH-108: finite-memory fourth-cross support

This directory contains the one-hundred-and-eighth RH-layer paper:

> *Finite-Memory Fourth-Cross Support: A Weyl Certificate, Reduced Moments,
> and a Normalized-Memory Barrier*

## Main result

For the full projected cross `K_t` and its depth-`m` recent-memory version
`Khat`, RH-101 gives a positive tail bound `delta`.  Weyl's inequality then
gives

```text
s4(K_t) / s1(K_t) >= max(0, s4(Khat)-delta) / (s1(Khat)+delta).
```

RH-95 identifies the recent squared singular values with the eigenvalues of
`M2 - A^2`.  Thus the support gate is reduced to a small exact moment test,
although direct thin actions are numerically safer than binary64 moment
subtraction in weak branches.

## Five-scale result

With `eta=1/512` and depth five:

- all 360 threshold-update records obey the selector implication;
- all 78 physical updates on `sigma=0.02` and `0.01` are certified for
  `tau=1e-8,1e-6,1e-4`;
- the minimum fine certified ratio is `7.3604523e-4`;
- the minimum fine support margin is `7.36045` at `tau=1e-4`;
- the largest moment/direct-cross discrepancy is `0.7272`, exposing weak-mode
  cancellation rather than an algebraic identity failure.

## Exact boundary

The normalized-memory family in `src/fourth_cross_support/bounds.py` has fixed
trace clock and fixed packet/complement diagonal blocks, while
`s4/s1 = epsilon/4` tends to zero.  Therefore an all-level lower bound needs
physical transversality or volume information beyond generic positivity and
finite-memory decay.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_support_certificate_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_support_certificate_audit.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf finite-memory-fourth-cross-support.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
