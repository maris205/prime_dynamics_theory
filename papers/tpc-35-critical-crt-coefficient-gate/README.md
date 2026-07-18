# TPC-35 — Orbit-scale CRT compression and coefficient-specific spectrum

This directory contains:

> **Orbit-Scale CRT Compression and Uniform Gram Obstructions:
> Product-Slope Character Spectrum, Three-Modulus Alias Reduction,
> and a Coefficient-Specific Gate**

TPC-35 audits the next routes after the orbit-sliced \(Q^3/J\) energy
gate in TPC-34. It proves exact limitations of two broad uniform
certificates, diagonalizes the coherent product-slope operator, identifies
the critical three/four-modulus CRT thresholds, and improves one physical
ultra-divisor block.

## Main results

### 1. Exact aspect-ratio Gram obstruction

For the abstract equal-row deletion model

\[
A=\mathbf1\mathbf1^*-I_n,\qquad M_j=AD_j,
\]

with \(t<n\) unit-phase observations and phase matrix \(R\), the
off-diagonal Gram matrix is exactly

\[
O=(n-2)(R^*R-tI_n).
\]

Hence

\[
\|O\|_{\rm op}\ge(n-2)\max\{t,n-t\},
\qquad
\|O\|_{\rm HS}^2\ge(n-2)^2nt(n-t).
\]

Both bounds are sharp at the Fourier tight-frame scale. A block theorem
shows that equal same-source deletion alone retains a \(Q^2\)-scale
operator obstruction. These are abstract information-class results, not
lower bounds for the actual physical masked Gram matrix.

### 2. One-modulus multiplicity saturation

For integer sets of sizes \(J_0,S_0\), the residue-multiplicity
right-hand side from the incomplete projective-Plancherel implementation
has normalized factor

\[
\mathscr R_q^2=
\frac{q\nu_{\mathcal J}^*\nu_{\mathcal S}^*}{J_0S_0}
\ge\frac1{\min\{J_0,S_0\}}.
\]

Balanced nonzero-residue sets attain this scale up to constants. This
saturates that certificate only; it is not a lower bound on the actual
correlation.

### 3. Exact coherent product-slope spectrum

For centered \(f,g:\mathbb F_q\to\mathbb C\), define

\[
R_s(a)=\sum_D f(D)g(s^{-1}(aD+h)),
\qquad
(Tb)(j,s)=\sum_\ell b(\ell)R_s(\ell j).
\]

Multiplicative characters diagonalize \(T\):

\[
\sum_{j,s}|Tb(j,s)|^2
=\frac1{q-1}\sum_\chi
|\widehat b(\bar\chi)|^2\mathcal E_\chi,
\qquad
\|T\|_{\rm op}^2=\max_\chi\mathcal E_\chi.
\]

The paper gives closed formulas for every principal and nonprincipal
\(\mathcal E_\chi\). Projective Plancherel controls their average; a
coherent coefficient vector sees their maximum. The factor \(q-1\)
between the two is sharp. This identity applies exactly to complete,
separable finite layers; a controlled decomposition of the actual
\(j\)-dependent mask into such layers remains unproved.

### 4. Critical CRT depth

If an affine determinant \(F\) satisfies \(|F|\ll X\), simultaneous
congruences modulo pairwise-coprime \(q_i\asymp J\) leave

\[
O(1+X/J^r)
\]

integer aliases. At the endpoint

\[
Q=X^{267/400+o(1)},\qquad J=X^{133/400+o(1)},
\]

three moduli leave

\[
X/J^3=X^{1/400+o(1)}=Q/J^2,
\]

exactly the allowance above the orbit diagonal; four are the first
orbit-scale moduli giving strict ambient no-wrap.

The paper also proves that CRT gain does not automatically tensorize:
data lifted from any proper coordinate block preserve the normalized rms
of that smaller CRT product.
The specified merge-then-complete route obeys the bookkeeping inequality

\[
(1+X/P)(1+P/J)\ge X/J\asymp Q.
\]

### 5. Physical same-ultra saving

After opening both divisor copies inside the actual orbit-sliced energy,
the equal-ultra block satisfies

\[
\mathcal V_{L,u=}+\mathcal V_{R,u=}
\ll X^\varepsilon Q^2J(1+Q/T).
\]

At the endpoint this is

\[
\ll X^{o(1)}Q^3J/T.
\]

It removes one orbit factor from the earlier two-time estimate and saves
the full factor \(T\), but it still misses the \(Q^3/J\) gate by
\(J^2/T\).

## Next gate

The next viable input is one of:

- a bound for the actual coefficient-weighted bad multiplicative-character
  mass, after a controlled complete separable mask decomposition;
- a genuine joint three-modulus theorem that also suppresses principal,
  singleton, and double-coordinate CRT modes;
- an equivalent signed terminal/proper-divisor dispersion estimate.

The paper does **not** prove that mask decomposition, the physical
coefficient-specific orbit gate, an affine Chowla theorem, a parity
breach, a Hardy–Littlewood asymptotic, or infinitely many twin primes.

## Exact certificate

Requires Python 3.10 or later. Run from this directory:

```text
python experiments/tpc35_certificate.py
python -O experiments/tpc35_certificate.py
```

Both modes perform 141,803 exact checks and regenerate byte-identical
JSON. The code uses integers, `Fraction`, and Gaussian rationals only.

Reproducibility values:

- Normalized source SHA-256:
  `7e08d1d29dc88e40b9653176b06336ba2ed879db33fb080e2c697e79b94e948e`
- JSON SHA-256:
  `02dea583a12f7078ee15ae8205f7e8d0787f92c5c858c80a525396534357c134`
- Certificate digest:
  `26b282b0b8a989e792524dc12ab1a6ed8215204fc36a0ef4493ab28982a7dae5`

## Files

- `main.tex` — paper entry point
- `sections/` — section sources
- `references.bib` — bibliography
- `main.pdf` — compiled paper
- `experiments/tpc35_certificate.py` — exact certificate
- `experiments/tpc35_certificate.json` — archived certificate output

## Build

```text
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
