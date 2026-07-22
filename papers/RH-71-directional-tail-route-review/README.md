# RH-71: directional-tail route review

This directory contains the tenth layer in the RH-62--RH-71 exploration:

> *From Residual Krylov Geometry to Frozen Production Bounds: A Ten-Layer
> Audit, Certificate-Stack Closure, and the Two-Gate Stage A1 Frontier*

## New synthesis theorem

Let K be the true transfer-coefficient sequence and K-hat a frozen
finite-matrix sequence. If a terminal candidate proves

    ||K-hat||_H2 <= U_c

and an upstream bridge proves

    ||K - K-hat||_H2 <= Delta,

then

    ||K||_H2 <= min_c U_c + Delta.

A candidate-independent bridge leaves the terminal Pareto frontier unchanged.
If the frozen finite-prefix norm is at least F-minus and the terminal upper is
at most U-plus, then

    Delta <= (1 + tau) F-minus - U-plus

is sufficient for a total relative target tau. Polylogarithmic terminal and
bridge bounds compose into a polylogarithmic true bound.

## Certified bridge headroom

A 256-bit Arb audit reuses the exact RH-70 finite-prefix and full-upper balls.
All ten channels leave positive headroom inside a 1% total finite-scale
target. The smallest certified values occur at sigma = 0.04 on the left:

- absolute H2 bridge slack: at least 0.0008411455518283;
- relative slack: at least 0.0006306266775126;
- equivalently, about 0.0630627% of the finite prefix.

The 1% target is an engineering sharpness ledger, not a requirement of Stage
A1. A larger but polylogarithmically controlled bridge can still be sufficient
for the asymptotic program.

## Route verdict

The finite-scale and asymptotic frontiers are now different.

- **Finite-scale end-to-end Hardy certificate:** one first-open gate,
  upstream interval enclosure of the folded-Gaussian/deflation/transfer
  triple.
- **Full Stage A1:** two first-open gates, the upstream interval enclosure and
  a uniform small-noise/dyadic family bound.

Thus RH-70 removed the terminal arithmetic wall, but it did not prove family
uniformity.

## Closed false shortcuts

- plain geometric or one-step norm propagation as a uniform proof;
- unlocalized full-space Lyapunov weighting as a polylogarithmic shortcut;
- universal fixed block Krylov depth from stability data alone;
- globally small PSD envelopes with arbitrarily sharp physical cancellation.

The surviving route is upstream interval validation, an augmented difference
bridge, and then an analytic uniform horizon/phase-compression theorem.

## Reproduction

~~~bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_route_review.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/run_arb_bridge_slack_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf directional-tail-route-review.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/verify_archive.py
~~~
