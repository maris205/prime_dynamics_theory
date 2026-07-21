# RH-62: Krylov residual Stein tails

This directory contains the sixty-second RH-layer paper:

> *Krylov Residual Certificates for Directional Stein Tails: A First
> Arnoldi Replacement for the Norm Envelope*

## Main result

For an Arnoldi relation

~~~text
A V = V H + g e_m^*,
~~~

and a source in the Krylov range, the power has the exact decomposition

~~~text
A^L z = V H^L beta
        + sum_j A^(L-1-j) g e_m^* H^j beta.
~~~

Bounding only the residual propagation gives a directional certificate that
depends on the actual Krylov coefficients. It is always a valid upper for
the power norm and becomes exact at Arnoldi breakdown.

## Pilot result

The deterministic models include a surrogate calibrated to the RH-61 left
endpoint gap. At L=32, its ordinary norm envelope is about 2000 times the
exact power norm, while the one-vector Krylov certificate is essentially
exact. The nonnormal four-step stress model improves the ordinary gain from
about 220 to 84 with one vector and becomes exact at full Krylov dimension.
The RH-60 two-block Arb model shows the limitation: a crude one-vector
residual propagation can still be worse than the ordinary norm bound, while
the full two-dimensional certificate terminates exactly.

Thus Krylov structure is a viable direction, but the residual propagator must
itself become directional or weighted before it can close a physical-family
bound.

## Evidence boundary

Analytic finite-dimensional results:

- Arnoldi residual identity;
- directional power upper;
- exact termination at Krylov breakdown;
- Stein-factor multiplication.

Computer evidence:

- three finite-dimensional model audits;
- a 256-bit Arb two-block identity check;
- no production folded-Gaussian interval audit and no continuum theorem.

Stage A1, Stage A4, a physical-family tail theorem, a self-adjoint
Hilbert--Polya operator, a T log T law, a prime-power trace formula, a
zeta-zero identity, and the Riemann hypothesis remain open.

## Reproduction

~~~bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_krylov_tail_pilot.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_arb_krylov_audit.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf krylov-residual-stein-tails.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
~~~
