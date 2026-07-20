# RH-52: intrinsic peripheral residue transfer

This directory contains the fifty-second-layer paper in the quadratic
small-noise spectral program:

> *Intrinsic Peripheral Residue Transfer from Weak Finite Factors:
> Direct Haar-Range Bounds and a Sharp Half-Power Barrier*

## Main exact result

The original A2 target asked for the intrinsic finite left-factor estimate

\[
\|\ell_d\|_2=O(h\sigma^{-1}),
\]

which would imply a fine residue action of order \(O(\sqrt{\sigma})\).
RH-52 proves that this sharp factor transfer is not required for the
RH-50 Hardy closure.

Strong/weak Ulam stability supplies finite peripheral normalizations with

\[
|\lambda_{n,-}|\ge \tfrac12,
\qquad
\|r_{n,\pm}\|_\infty+\|\ell_{n,\pm}\|_1\le C
\]

on every \(h=o(\sigma^2)\) schedule. Direct Gaussian smoothing gives

\[
\|(E_{2n}-E_n)\mathcal P_\sigma\|_{L^1\to L^2}
\le C h\sigma^{-3/2},
\]

\[
\|(E_{2n}-E_n)\mathcal K_\sigma\|_{L^\infty\to L^2}
\le C h\sigma^{-1},
\qquad
\|\mathcal P_\sigma\|_{L^1\to L^2}
\le C\sigma^{-1/2}.
\]

Together with

\[
\|B\|_{S_2},\|C\|_{S_2}
=\Theta(h\sigma^{-3/2}),
\]

these estimates imply directly

\[
\frac{\|U^*P_{f,\pm}UB\|_{S_2}}{\|B\|_{S_2}}=O(1),
\qquad
\frac{\|CP_{c,-}\|_{S_2}}{\|C\|_{S_2}}=O(1),
\]

while \(CP_{c,+}=0\) exactly.

Thus the sufficient A2 residue gate is closed without either a sharp
finite-factor detail theorem or a polylogarithmic upper for the complete
finite projector.

## Sharp barrier

The weak-information estimate is optimal:

\[
\|(E_{2n}-E_n)\mathcal P_\sigma\|_{L^1\to L^2}
=\Theta(h\sigma^{-3/2})
\]

when \(h/\sigma\) is small. Therefore uniform \(L^1\) control of the left
factor alone cannot produce \(O(h\sigma^{-1})\). Recovering the extra
\(\sqrt{\sigma}\) requires the actual postcritical spike geometry.

The stronger result remains optional for the current roadmap because the
direct \(O(1)\) range-action theorem is already sufficient.

## Five-scale audit

The floating audit uses \(N\sigma=20.48\) and reaches \(N=40960\).

| sigma | N | parity weak condition | parity detail / \(h\sigma^{-1}\) | fine parity residue | right parity residue |
|---:|---:|---:|---:|---:|---:|
| 0.0100 | 2048 | 1.0968 | 0.0553 | 0.0574 | 0.0315 |
| 0.0040 | 5120 | 1.0765 | 0.0511 | 0.0339 | 0.0130 |
| 0.0020 | 10240 | 1.0604 | 0.0489 | 0.0230 | 0.00675 |
| 0.0010 | 20480 | 1.0485 | 0.0475 | 0.0159 | 0.00356 |
| 0.0005 | 40960 | 1.0385 | 0.0465 | 0.0110 | 0.00191 |

Observed residue powers are:

~~~text
fine Perron     sigma^0.52752
fine parity     sigma^0.55003
right parity    sigma^0.93624
~~~

Hence the stored intrinsic factors exhibit the stronger sharp transfer,
even though the analytic theorem intentionally claims only \(O(1)\).

## Exact boundary

RH-52 does not prove:

- the sharp intrinsic \(O(h\sigma^{-1})\) detail law;
- the corresponding analytic \(O(\sqrt{\sigma})\) fine residue law;
- interval enclosures of the five-scale eigendata;
- the A1 growing-horizon Hardy-energy budget;
- the A3 infinite-tail and sparse-cutoff validation;
- an arithmetic trace formula, zeta-zero identity, self-adjoint
  Hilbert--Polya operator, \(T\log T\) law, the Riemann hypothesis, or a
  twin-prime theorem.

TPC remains an independent twin-prime/correlation program and is not an
assumption in this paper.

## Reproduction

~~~bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q

OPENBLAS_NUM_THREADS=16 OMP_NUM_THREADS=16 \
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/run_factor_transfer_pilot.py

PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_factor_transfer_certificate.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/verify_archive.py
~~~
