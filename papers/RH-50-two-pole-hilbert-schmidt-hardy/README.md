# RH-50: two-pole Hilbert--Schmidt Hardy energies

This directory contains the fiftieth-layer paper in the quadratic
small-noise spectral program:

> *Two-Pole Hilbert--Schmidt Hardy Energies for Small-Noise Range
> Resolvents: Directional Stein Certificates and a Global-Contraction
> No-Go*

## Main result

RH-49 reduced the remaining intrinsic-identification gate to
Hilbert--Schmidt resolvent actions on the two adjacent Haar coupling ranges.
RH-50 removes the Perron and parity poles simultaneously,

\[
N=T-\lambda_+P_+-\lambda_-P_-,
\qquad Q=I-P_+-P_-,
\]

and replaces contour solves by the directional Hardy energy

\[
\mathcal E_B(r)^2
=\sum_{m\ge0}r^{-2m}
\frac{\|U^*N^mQUB\|_{S_2}^2}{\|B\|_{S_2}^2}.
\]

Whenever

\[
\operatorname{spr}(N)<r<d_\Gamma
:=\inf_{z\in\Gamma}|z|,
\]

the exact Laurent/Cauchy--Schwarz estimate is

\[
\sup_{z\in\Gamma}
\frac{\|U^*(z-N)^{-1}QUB\|_{S_2}}{\|B\|_{S_2}}
\le
\frac{\mathcal E_B(r)}{\sqrt{d_\Gamma^2-r^2}},
\]

with a symmetric right-range statement.

The energies are Gramian traces.  For example,

\[
G=XX^*+r^{-2}NGN^*.
\]

Any positive supersolution

\[
H-r^{-2}NHN^*\succeq XX^*
\]

gives a deterministic trace upper for the infinite Hardy sum.  This is the
next finite-matrix certificate target.

## Exact no-go

The deterministic Koopman operator is an isometry on the stationary
L2 space, including the orthogonal complement of the Perron and parity
modes.  Finite-time small-noise convergence therefore gives, for every
fixed m,

\[
\|Q_\sigma^\circ K_\sigma^mQ_\sigma^\circ\|\longrightarrow1.
\]

Thus a noise-uniform fixed-step global contraction q less than 1 cannot
prove the Hardy gate.  This does **not** rule out directional Gramians,
increasing mixing times, or anisotropic norms.

## Spike and residue analysis

Differentiating the rounded square-root endpoint profile sharpens the
previous coarse derivative envelope to

\[
\|\pi_\sigma'\|_2+\|g_\sigma'\|_2
=\Theta(\sigma^{-1}).
\]

The exact fine block identity

\[
U^*PUB
=r_c\otimes((\overline\lambda-D^*)\ell_d)
\]

then predicts normalized outgoing residue action O(sqrt(sigma)) when the
intrinsic finite left factors inherit the continuum Haar-detail estimate.
That uniform factor transfer remains explicit; the stored finite-matrix
audit supports it but does not prove it.

The outgoing coupling itself satisfies the analytic two-sided scale

\[
\|B\|_{S_2}=\Theta(h\sigma^{-3/2})
\]

when h/sigma is sufficiently small.

## Five-scale audit

The full audit uses exact Haar nesting with finest N*sigma = 20.48, eight
deterministic Rademacher probes, powers m = 0,...,64, and eight nodes on
each peripheral contour.  The primary Hardy radius is r = 0.85.

| sigma | dimension | left energy | right energy | max bulk product |
|---:|---:|---:|---:|---:|
| 0.01 | 2048 | 1.5019 | 1.6897 | 1.8574 |
| 0.004 | 5120 | 1.6793 | 2.1520 | 2.3036 |
| 0.002 | 10240 | 1.3946 | 2.0999 | 1.8338 |
| 0.001 | 20480 | 1.4723 | 2.0188 | 1.9618 |
| 0.0005 | 40960 | 1.4748 | 2.3583 | 1.8543 |

Fitted growth exponents:

~~~text
left Hardy energy       0.0000000
right Hardy energy      0.0844233
max bulk product        0.0000000
~~~

The fitted tail bases track the independently computed bulk radii within
0.006--0.008.  At time 64, the maximum normalized powers are below
4e-9 on the left and 1.5e-8 on the right.

Residue-action fits:

~~~text
fine left Perron        sigma^0.52752
fine left parity        sigma^0.55003
coarse right Perron     exact zero to rounding
coarse right parity     sigma^0.93624
~~~

These computations are binary64 Hutchinson diagnostics with a truncated
tail.  They are not interval-validated asymptotic uppers.

## Conditional RH-49 closure

Polylogarithmic dyadic left/right Hardy energies, polylogarithmic
peripheral-factor conditioning, and one Hardy radius above the bulk
spectral radii imply

\[
\mathcal F_{n,\sigma}
=O((\log(1/\sigma))^a).
\]

The RH-49 quarter-power bridge then preserves every strict
\(n\sigma^2\to\infty\) intrinsic-identification schedule.

## Exact theorem boundary

RH-50 does **not** prove:

- a uniform small-noise Hardy-energy upper;
- an interval enclosure of the time-64 tail;
- that Hutchinson estimates or binary64 bulk radii are validated uppers;
- a dyadically uniform transfer of the continuum residue estimate to the
  finite matrix's own left factors;
- a dyadically polylogarithmic intrinsic coarse parity projector;
- an arithmetic trace formula, prime-power identity, zeta-zero
  identification, self-adjoint Hilbert--Polya operator, T log T counting
  law, or the Riemann hypothesis.

## Reproduction

From this directory:

~~~bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q

OPENBLAS_NUM_THREADS=16 OMP_NUM_THREADS=16 \
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/run_two_pole_hardy_pilot.py

PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_hardy_certificate.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/verify_archive.py
~~~

The full five-scale pilot is the expensive step.  Rebuilding the
certificate, figure, tests, PDF, and archive from the stored pilot is fast.
