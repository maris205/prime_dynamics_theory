# RH-63: nested Krylov residual closure

This directory contains the sixty-third RH-layer paper:

> *Nested Arnoldi Residual Closure for Directional Stein Tails: Repairing
> the One-Step Propagation Failure*

## Main result

RH-62 expanded the physical source once with Arnoldi, but propagated the
resulting residual with an ordinary norm. RH-63 expands that residual again
and adds all projected residual vectors coherently before taking a norm. Only
the terminal unexpanded remainder is bounded positively.

The resulting finite-dimensional certificate is always an upper. If the
residual chain reaches Arnoldi breakdown, it is exact.

## Pilot result

At horizon 32:

- the RH-60 two-block model improves from a one-level gain of 66.41 to
  exactly 1.0 with the nested schedule (1,1);
- the four-step nonnormal chain improves from 84.05 to 52.30, 53.48, and
  finally 1.0 at four nested levels;
- the RH-61 slow/fast surrogate was already nearly exact at one level, and
  recursive triangle splitting can make it slightly more conservative.

This is a useful route selection result: coherent recursion repairs the
two-block failure, but depth and terminal residual propagation remain to be
controlled uniformly.

## Evidence boundary

Analytic finite-dimensional results:

- coherent nested Arnoldi identity;
- positive terminal remainder bound;
- exactness at terminal breakdown.

Computer evidence:

- three finite-dimensional recursive audits;
- a 256-bit Arb two-block identity check;
- no production physical-family interval theorem.

Stage A1, Stage A4, uniform residual depth, block cross-column fusion, a
self-adjoint Hilbert--Polya operator, a prime-power trace formula, and the
Riemann hypothesis remain open.

## Reproduction

~~~bash
pytest -q -p no:cacheprovider
python experiments/run_nested_krylov_pilot.py
python experiments/run_arb_nested_audit.py
MPLBACKEND=Agg python experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf nested-krylov-residual-closure.pdf
python experiments/build_archive.py
python experiments/verify_archive.py
~~~
