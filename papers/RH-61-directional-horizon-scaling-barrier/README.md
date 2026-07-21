# RH-61: directional horizon scaling for phase-aware Stein tails

This directory contains the sixty-first RH-layer paper:

> *Directional Horizon Scaling for Phase-Aware Stein Tails: A Geometric
> Envelope Barrier and the Need for Residual Certificates*

## Main result

For a packetwise normalized Stein tail

~~~text
t_j(L) = sqrt(kappa_j) ||S_j^L z_j||_HS,
q_j = ||S_j|| < 1,
~~~

the exact finite-dimensional envelope is

~~~text
t_j(L) <= t_j(0) q_j^L.
~~~

If a reducing slow mode has contraction q and tail amplitude a, then any
certificate with tolerance epsilon requires

~~~text
L >= ceil(log(a / epsilon) / (-log(q))).
~~~

Thus a power contraction gap 1-q_sigma = O(sigma^beta) can force a
sigma^(-beta) log(1/sigma) horizon. This is a barrier for the norm-based
tail certificate, not a lower bound on the exact phase-fused Hardy energy.

## Archived five-scale result

RH-61 reanalyzes the RH-59/RH-60 binary64 archives without reoptimization.
At sigma=0.01 and L=32:

- phase-aware completion ratios are 1.004695 (left) and 1.002169 (right);
- directional tail sums are 0.006892 and 0.003819;
- packetwise geometric envelopes are 13.149 and 5.617;
- a 5% geometric tail target requires horizons 850 and 228;
- the first stored phase horizons are both 32.

The endpoint gap shows that the physical source leaves the worst-case norm
direction quickly, even though the maximum packet contraction approaches one.
The next viable theorem is a directional residual/Krylov tail estimate.

## Evidence boundary

Analytic finite-dimensional results:

- packetwise geometric Stein-tail envelope;
- exact integer horizon search for that envelope;
- reducing slow-mode lower bound;
- power-gap horizon obstruction.

Computer evidence:

- five archived finite-matrix rows and their log-log fits;
- 256-bit Arb equality-case audit for the scalar horizon algebra;
- no production interval audit and no continuum uniformity.

Stage A1, unconditional Stage A4, a physical-family directional tail theorem,
a self-adjoint Hilbert--Polya operator, a T log T counting law, a
prime-power trace formula, a zeta-zero identity, and the Riemann hypothesis
remain open.

## Reproduction

~~~bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_horizon_scaling_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_arb_horizon_audit.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf directional-horizon-scaling-barrier.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
~~~
