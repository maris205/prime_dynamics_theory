# TPC-37 - Coordinate-face reduction at the coherent Mobius gate

> **Coordinate-Face Reduction at the Coherent Mobius Gate: Physical
> Zero-Face Absorption, Jacobi Near-Isometry, and Three-Modulus Energy
> Localization**

TPC-37 separates three effects that remained entangled after TPC-36:
physical zero residue coordinates, the nonconstant complementary-factor
weight, and the seven proper faces of a three-modulus CRT completion.

## Main results

- Physical zero-coordinate faces are absorbed at the inherited scale:
  \[
  V_{L,\mathrm{sing}}+V_{R,\mathrm{sing}}
  \ll X^{o(1)}Q^3/J.
  \]
- Punctured centering keeps the ultra coefficient zero at residue zero,
  exposes only explicit rank-one mean corrections, and annihilates every
  complete complementary residue cycle in the centered core.
- The nonprincipal Jacobi matrix satisfies
  \[
  K^*K=KK^*=(q-1)^2I-q\mathbf1\mathbf1^*,
  \]
  so its singular values are \(q-1\) and \(1\). It is near-isometric,
  not an automatic source of cancellation.
- The weighted two-character energy is an exact Hadamard product of the
  complementary interval spectrum and the punctured ultra spectrum.
  Polya-Vinogradov saves one uniform Cauchy factor in an unweighted
  character average; actual outer spectral overlap remains open.
- All eight three-modulus faces are orthogonal over one CRT period. The
  seven-face proper union has squared period mass \(\asymp J^{-1}\), and
  determinant-first grouping gives fiberwise mass \(X/J^4=o(1)\).
- On the exact equality, all proper faces close at \(Q^3/J\), while the
  full face has coefficient \(1-O(J^{-1})\) and retains the terminal
  Mobius layer.

The exact next gate is either (i) absorption of the exposed
punctured-centering mean corrections and principal outer boundary together
with an aggregate nonprincipal Mellin-overlap estimate for the actual
coefficient, or (ii) a target-coupled, coefficient-weighted shifted-fiber
Bessel theorem for the unsplit raw physical output. Neither route is
proved in this paper.

## Exact certificate

Run from this directory:

~~~text
python experiments/tpc37_certificate.py
python -O experiments/tpc37_certificate.py
~~~

The script uses deterministic exact arithmetic and regenerates the
archived JSON certificate. The paper records the hashes and digest; the
JSON records the detailed per-family counts.

## Build

~~~text
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
~~~

## Claim boundary

TPC-37 does **not** prove the full physical coefficient gate, the
principal outer-boundary estimate, outer Mellin flatness for the actual
rows, a target-coupled shifted-fiber Bessel theorem, an
affine Chowla estimate, a breach of sieve parity, a Hardy-Littlewood
prime-pair asymptotic, or infinitely many twin primes.
