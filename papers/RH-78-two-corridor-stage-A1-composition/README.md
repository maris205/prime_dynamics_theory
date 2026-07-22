# RH-78: two-corridor conditional Stage A1 composition

This directory contains the seventy-eighth RH-layer paper:

> *Two Corridors to Stage A1 and the Conditional Closure of Intrinsic Identification*

## Main theorem

There are now two sufficient all-level routes:

1. the RH-75 full-block law, giving polylogarithmic left/right Hardy energies;
2. the RH-77 postblock effective-rank law, giving a polylogarithmic reduced
   future plus a polylogarithmic truncation error.

Either route yields

    E_B, E_C = polylog(1/sigma),

so the Hardy sigma-power is zero. RH-54 then gives

    ||I_(n,sigma)||_S2
      <= n^(-2) sigma^(-13/4) polylog(1/sigma).

For every strict mesh schedule `n sigma^2 -> infinity`, this tends to zero.
Thus proving either all-level corridor closes Stage A1 and activates the
already rigorous RH-54/RH-55 identification composition.

## Five-anchor composition

The RH-75 common envelope gives per-channel Hardy uppers from `1.079` to
`1.836`, and all frozen products lie inside it. The Hardy power is `0`, safely
below the `1/4` threshold. On the stress schedule

    n = sigma^(-2) log_2(sigma_0/sigma + 2),

the identification envelope decreases from `0.07355` to `0.002961` across the
five anchors. Rank-four future errors from RH-77 remain below `5.35e-6`.

## Boundary

This is a conditional closure theorem and a validated finite-anchor
composition. Neither corridor has yet been proved for all dyadic levels, so
Stage A1 and unconditional Stage A4 remain open.

## Reproduction

~~~bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_stage_composition_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf two-corridor-stage-A1-composition.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
~~~
