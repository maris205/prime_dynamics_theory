# RH-51: cyclic-rank obstructions and growing-horizon Stein certificates

This directory contains the fifty-first-layer paper in the quadratic
small-noise spectral program:

> *Cyclic-Rank Obstructions and Growing-Horizon Stein Certificates for
> Small-Noise Hardy Energies: Minimal Gramians, Conic No-Go Witnesses,
> and a Viable Block Route*

## Main exact result

For a stable scaled bulk matrix \(A=N/r\) and directional source \(X\), let

\[
G=\sum_{m\ge0}A^mXX^*(A^*)^m,
\qquad G-AGA^*=XX^*.
\]

Every positive Stein supersolution

\[
H-AHA^*\succeq XX^*
\]

dominates \(G\). Moreover,

\[
\operatorname{Ran}G
=\operatorname{span}\{A^m\operatorname{Ran}X:m\ge0\},
\]

and every such \(H\) has an \(A\)-invariant range containing this cyclic
subspace. Hence

\[
\operatorname{rank}H\ge \operatorname{rank}G.
\]

This rules out fixed-rank exact Lyapunov factors whenever the directional
cyclic dimension grows. It does not rule out low-rank approximations
completed by a positive background metric.

## Growing-horizon route

For

\[
S_M=\sum_{j=0}^{M-1}A^jXX^*(A^*)^j,
\]

the block inequality

\[
H-A^M H(A^*)^M\succeq S_M
\]

already implies \(H\succeq G\). If \(q_M=\|A^M\|_2<1\), the explicit
candidate

\[
H_M=S_M+\alpha_M I,
\qquad
\alpha_M=
\frac{\|A^M S_M(A^*)^M\|_2}{1-q_M^2}
\]

is a block supersolution. Thus RH-50's fixed-step global-contraction no-go
is compatible with a horizon \(M=M(\sigma,n)\) that grows.

The paper also proves:

- the necessary floor
  \(\alpha\ge\lambda_{k+1}(G)\) for \(H=ZZ^*+\alpha I\),
  \(\operatorname{rank}(Z)\le k\);
- an anisotropic residual/background completion theorem;
- positive-semidefinite and rank-one conic dual witnesses that rule out
  entire metric ansatz cones.

## Five-scale dense audit

The binary64 audit fixes \(N\sigma=5.12\), uses Hardy radius \(r=0.85\),
and solves the left and right Lyapunov equations densely.

| sigma | N | left energy | right energy | left 99% rank | right 99% rank | cyclic rank | block M |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.16 | 32 | 0.9040 | 1.0026 | 5 | 5 | 22 | 4 |
| 0.08 | 64 | 1.1626 | 1.2653 | 9 | 9 | 43 | 8 |
| 0.04 | 128 | 1.3338 | 1.4845 | 17 | 17 | 84 | 16 |
| 0.02 | 256 | 1.4096 | 1.6340 | 35 | 33 | 165 | 24 |
| 0.01 | 512 | 1.4681 | 1.7603 | 69 | 64 | 322 | 32 |

The cyclic ranks use relative singular threshold \(10^{-8}\). Their fitted
dimension power is \(0.9683\). The selected block horizons have a linear
fit against \(\log_2N\) with slope \(7.2\); this is finite evidence, not an
asymptotic theorem. At every level the block energy upper is within
\(6.3\times10^{-4}\) relative of the dense exact-Gramian energy.

The scalar identity cone has a rank-one dual obstruction at the four
finest levels. Simply taking the diagonal of the exact Gramian fails the
Stein inequality at all five levels. These failures do not rule out all
diagonal, banded, localized, hierarchical, or multilevel metrics.

## Exact boundary

RH-51 does **not** prove:

- an analytic divergence theorem for the physical cyclic rank;
- a dyadically uniform small-noise block horizon or trace budget;
- an interval validation of the dense Lyapunov solves;
- Stage A1 of the post-RH-50 roadmap;
- small-noise intrinsic Riesz identification or a renormalized determinant;
- an arithmetic trace formula, zeta-zero identity, self-adjoint
  Hilbert--Polya operator, \(T\log T\) law, the Riemann hypothesis, or a
  twin-prime theorem.

TPC remains an independent twin-prime/correlation program. Its methods may
be cited, but it is not an assumption in this paper.

## Reproduction

From this directory:

~~~bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q

OPENBLAS_NUM_THREADS=16 OMP_NUM_THREADS=16 \
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/run_structured_stein_pilot.py

PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_stein_certificate.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/verify_archive.py
~~~

The full five-scale pilot takes only a few seconds on the archived server.
