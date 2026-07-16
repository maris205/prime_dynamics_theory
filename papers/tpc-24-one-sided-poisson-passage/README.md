# TPC-24 — One-sided passage beyond the Poisson boundary

This directory contains:

> **One-Sided Passage Beyond the Poisson Boundary: Shell-Averaged Zero
> Modes and Asymmetric Conductor Rectangles in a Primitive Möbius Tail**

TPC-24 studies the incremental divisor region
`u <= S < v <= T` in the primitive Möbius residual program.  Its main
object is the exact calibrated-prefix increment

\[
\mathcal I_{S,T}
=\sum_{m,n}z_{m,n}\sum_j F(j/J)P_{m,S}(j)
\{P_{n,T}(j)-P_{n,S}(j)\}.
\]

## Main results

- Exact calibrated recombination removes the apparently surviving long
  single Poisson channel.  Pointwise, the increment is a raw joint
  divisor lattice minus the explicit row drift
  `delta_H(m) L_{n;S,T}`.

- For `S = X^s`, `T = X^t`, `s <= t`, the joint nonzero spectrum has
  certified saving

  \[
  \eta_{\rm asym}(\beta;s,t)=
  \min\left\{
  1-\frac{3\beta}{2},
  \frac{\beta+1-2s-2t}{2},
  \frac{3-\beta-s-5t}{4}
  \right\}.
  \]

- The physical zero mode is handled separately.  For each off-diagonal
  row pair and every `0 < kappa < s`, the complete long Möbius shell
  satisfies

  \[
  K^0_{S,T}(m,n)
  \ll_A (\log X)^{-A}+X^{-s+\kappa+o(1)}.
  \]

  Small shared factors use cancellation of the same calibrated main
  constant at the two shell endpoints.  Large shared factors use
  divisibility of the nonzero row determinant.

- The packet theorem retains the actual absolute row-pair mass
  `Z_1`.  Under the explicit fixed-projective-mass condition
  `Z_1 << Q^2 (log X)^K`, positivity of the displayed conductor saving,
  and the stated row, no-wrap, and Fourier-tail interfaces, the whole
  calibrated mixed increment has arbitrary logarithmic saving.  Under
  only `Z_1 << Q^2 X^epsilon`, the paper keeps the
  small-shared-factor zero term as a mass-sensitive remainder.  In the
  same positive-saving region, if `Fhat(0) = 0`, the soft-mass packet
  closes with a fixed power saving.

- At the baseline `S = R = X^(1/2-delta)` and `T = R X^xi`, the joint
  saving is

  \[
  \min\left\{
  1-\frac{3\beta}{2},
  \frac{\beta+4\delta-1}{2}-\xi,
  \frac{6\delta-\beta-5\xi}{4}
  \right\}.
  \]

  A strict passage with `R < J < T` occurs in the displayed paper
  window.  The exact sample
  `(delta,beta,xi) = (3/20,31/50,1/25)` gives
  `R = X^0.35`, `J = X^0.38`, `T = X^0.39`, and saving `1/50`.

- A finite counterexample shows why one cannot replace complete-shell
  averaging by pointwise calibration at one fixed modulus.

## Scope

In the positive-saving region, this paper closes one calibrated
mixed-shell increment under the stated row, no-wrap, Fourier-tail, and
projective-mass hypotheses, and gives a mass-sensitive theorem without
the last of those hypotheses.  It does **not** close the complete TPC-18 residual,
the both-new square, or the ultra-long complement fibers.  It proves no
Hardy–Littlewood asymptotic, twin-prime lower bound, or general breach
of the sieve parity barrier.

## Exact certificate

Run:

```powershell
python experiments\tpc24_certificate.py
python -O experiments\tpc24_certificate.py
```

Both modes perform 55,084 exact checks and regenerate byte-identical
JSON.

- JSON SHA-256: `f638ca06fa641a570277b89b1ed17d81aeac2eaa264cf80d5a317378efbd0fc6`
- source SHA-256: `7b9ce64a93c5abb24c02ca9da6ea763fa5fbd97192bc1fd700fe47a7887ad33d`
- certificate digest: `c684a7c10e7cf3bd2cc46f2305af94d8452f018494d445ecdd3483325df6f50d`

## Files

- `main.tex` — paper entry point
- `sections/` — section sources
- `references.bib` — bibliography
- `main.pdf` — compiled paper
- `experiments/tpc24_certificate.py` — exact certificate
- `experiments/tpc24_certificate.json` — archived output

## Build

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
