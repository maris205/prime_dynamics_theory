# TPC-34 - Orbit-sliced Gram energy

This directory contains:

> **Orbit-Sliced Gram Energy at the \(Q^3\) Gate: Gram-Copy Diagonal
> Closure, Collision Savings, and the Terminal Möbius Boundary**

TPC-34 takes the physical column-energy gate isolated in TPC-33 and
performs its exact \(TT^*\) expansion. It closes the complete Gram-copy
diagonal, proves collision and two-time orbit-content estimates, and
reduces the remaining problem to a same-time orbit-sliced row energy.

## Main unconditional results

### Exact physical Gram expansion

After opening the ultra divisor \(u\) and the actual row-gcd projector
divisor \(v\), the left energy has the exact form

\[
E_L=\sum_{\xi_1,\xi_2}
\overline{z_L(\xi_1)}z_L(\xi_2)
\mathcal G_L(\xi_1,\xi_2),
\qquad
\mathcal G_L=T_L^*T_L.
\]

If \(v_1,v_2\) are the two projector divisors, then

\[
|\mathcal G_L(\xi_1,\xi_2)|
\ll X^\varepsilon
\left(L+\frac{Q}{[v_1,v_2]}\right).
\]

The principal layer \(v_1=v_2=1\) receives no incidence gain.

### Gram-copy diagonal closure

The diagonal between the two duplicated input-row indices satisfies

\[
E_{L,\Delta}+E_{R,\Delta}
\ll X^\varepsilon Q^2J^2.
\]

This is not the physical pair diagonal \(\alpha=\gamma\), which the
actual mask already deletes. At

\[
Q=X^{267/400+o(1)},\qquad J=X^{133/400+o(1)},
\]

the bound is

\[
Q^2J^2=Q^3X^{-1/400+o(1)}.
\]

Thus the complete Gram-copy diagonal crosses the TPC-33 \(Q^3\) gate
unconditionally with a strict power margin.

### Collision and two-time estimates

The exact equal-target collision layer satisfies

\[
\mathcal M_{\mathrm{tar}}\ll X^\varepsilon Q^2J.
\]

For a common ultra divisor \(u_1=u_2>T\),

\[
\mathcal M_{u=}
\ll X^\varepsilon Q^2J
\min\left\{
Q\left(1+\frac JT\right),
J\left(1+\frac QT\right)
\right\}.
\]

At the endpoint this is

\[
\mathcal M_{u=}\ll X^{o(1)}\frac{Q^3J^2}{T}.
\]

It saves the full factor \(T\) from the absolute baseline but still
exceeds the \(Q^3\) gate by

\[
\frac{J^2}{T}=X^{279/1000+o(1)}.
\]

For one row at two orbit times,

\[
(mj+h,mj'+h)=(mj+h,j'-j).
\]

Consequently, on an interval of length \(J_0\),

\[
\#\{(j,j'):j\ne j',\ (mj+h,mj'+h)>Z\}
\ll \frac{J_0^2}{Z}+J_0\log(2J_0).
\]

### Orbit-sliced reduction

Define

\[
Y_{\gamma,j}^L
=\sum_\alpha\gamma_\alpha^{(1)}
\mathfrak A_{\alpha,\gamma}^{\rm act}(j)C_{m_\alpha}(j),
\qquad
V_L=\sum_{\gamma,j}|Y_{\gamma,j}^L|^2,
\]

and define \(V_R\) symmetrically. Then

\[
E_L+E_R\ll X^\varepsilon J(V_L+V_R).
\]

Therefore

\[
V_L+V_R\ll X^\varepsilon\frac{Q^3}{J}
\]

is sufficient for the TPC-33 energy gate. Its orbit-sliced Gram-copy
diagonal is only \(O(X^\varepsilon Q^2J)\), smaller than the allowed scale by
\(X^{1/400+o(1)}\).

The stronger diagonal-scale target

\[
V_L+V_R\ll X^\varepsilon Q^2J
\]

would return

\[
E_L+E_R\ll X^\varepsilon Q^2J^2
\ll X^{2+\varepsilon}
=X^{\varepsilon+o(1)}Q^3X^{-1/400}.
\]

Neither orbit-sliced estimate is proved here.

### Terminal Möbius boundary

On the high-beta endpoint packet, the divisor range in every ultra
increment contains the terminal value

\[
u=mj+h,
\]

whose coefficient is zero when \(\mu(mj+h)=0\).

On the principal terminal layer the row and target signs fuse as

\[
\mu(d)\mu(\ell dj+h).
\]

The same-time energy therefore contains an averaged four-Möbius row
correlation. A coherent zero-pair-diagonal finite model attains the full
sign-blind scale \(Q^3J^2\). This is an envelope-only method obstruction,
not a lower bound or counterexample for the physical Möbius kernel.

## Exact certificate

Requires Python 3.10 or later. Run from this directory:

    python experiments/tpc34_certificate.py
    python -O experiments/tpc34_certificate.py

Both modes perform 213,976 exact checks and regenerate byte-identical
JSON. The checks use integers, Fraction, and Gaussian rationals only.

Reproducibility values:

- Normalized source SHA-256:
  92db9e309593faa815b1806cc4a656bfc02b4ffab5eb1eb4f61c7b973a24168f
- JSON SHA-256:
  50e7d0aefc9dd74f549831c8f70072fb34be4788ae9d193e7acfac79753d8c34
- Certificate digest:
  da2a05161550265582a881a0b7017a3b0be540c62df3cab187c58dbeaab9d9be

The certificate checks finite identities and rational ledgers only. It
does not prove the orbit-sliced off-diagonal bound, the \(Q^3\) physical
energy gate, affine Chowla cancellation, zero-frequency flatness,
positivity, a Hardy-Littlewood asymptotic, twin primes, or a breach of
sieve parity.

## Files

- main.tex - paper entry point
- sections/ - section sources
- references.bib - bibliography
- main.pdf - compiled paper
- experiments/tpc34_certificate.py - exact certificate
- experiments/tpc34_certificate.json - archived certificate output

## Build

    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    bibtex main
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
