# RH-64: weighted terminal residuals

This directory contains the sixty-fourth RH-layer paper:

> *Observability-Weighted Terminal Residuals for Nested Krylov Stein Tails:
> Turning Nonnormal Growth into a Metric Contraction*

## Main result

RH-64 replaces the Euclidean propagation factor for the terminal residual by
the contraction in a positive Lyapunov metric. For a stable matrix A, the
metric M solving

~~~text
M - A^* M A = I
~~~

gives a positive weighted norm and a strict weighted contraction. The nested
Krylov certificate remains a positive upper, but its terminal remainder uses
the weighted contraction instead of the Euclidean operator norm.

## Pilot result

The nonnormal four-step chain has Euclidean operator norm 1.110729 but
Lyapunov contraction 0.987369. Its one-level endpoint gain falls from 84.05
in RH-63 to 2.485 in the weighted certificate. The RH-60 two-block model
falls from 66.41 to 23.84. Full residual termination is exact in both finite
models.

The metric condition number of the four-step chain is about 37.7, which is
the new route boundary. Weighted contraction exists in finite dimension, but
uniform metric conditioning and block cross-column control remain open.

## Evidence boundary

Analytic finite-dimensional results:

- positive Lyapunov metric construction;
- weighted contraction identity;
- weighted nested terminal-residual certificate.

Computer evidence:

- three finite-dimensional weighted audits;
- a 256-bit Arb two-block Lyapunov certificate;
- no production physical-family interval theorem.

Stage A1, Stage A4, uniform metric conditioning, a self-adjoint
Hilbert--Polya operator, a prime-power trace formula, and the Riemann
hypothesis remain open.

## Reproduction

~~~bash
pytest -q -p no:cacheprovider
python experiments/run_weighted_residual_pilot.py
python experiments/run_arb_weighted_audit.py
MPLBACKEND=Agg python experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf weighted-terminal-residuals.pdf
python experiments/build_archive.py
python experiments/verify_archive.py
~~~
