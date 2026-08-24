# Derivation Package

## Target

Derive an explicit lower frame for exponential sums supported on distinct
primitive rational frequencies of height at most \(U\), measured on an
arbitrary interval of \(N\) consecutive integers.

## Status

**COHERENT AS STATED**

The requested theorem survives unchanged. No extra arithmetic hypothesis and
no weakening of the constants is needed.

## Invariant object

The invariant object is the finite-window energy

\[
E_I(z)=\sum_{n\in I}\left|\sum_{\alpha\in\mathcal F_U}
z_\alpha e(n\alpha)\right|^2,
\qquad e(t)=e^{2\pi i t},
\]

where \(\mathcal F_U\) is a finite set of distinct primitive fractions
\(\alpha=a/h\pmod 1\) with \(h\leq U\).

## Assumptions

- \(I=\{M,M+1,\ldots,M+N-1\}\) with \(N\geq1\).
- \(U\geq1\).
- Every frequency is represented by a primitive pair \((a,h)\), so
  \(\gcd(a,h)=1\).
- Distinct indices represent distinct points of \(\mathbb R/\mathbb Z\).
- The coefficient family is finitely supported.

## Notation

- \(L=\lfloor(N+1)/2\rfloor\).
- \([y]_+=\max(y,0)\).
- \(\|\theta\|=\min_{m\in\mathbb Z}|\theta-m|\).
- \(F_L(\theta)=L^{-1}|\sum_{r=0}^{L-1}e(r\theta)|^2\).
- \(\|z\|_2^2=\sum_\alpha|z_\alpha|^2\).

## Derivation strategy

Replace the hard interval by a translated triangular weight lying below its
indicator. Its Fourier transform is the nonnegative Fejér kernel. The
resulting weighted Gram matrix has diagonal \(L\). Primitive Farey spacing,
Fejér off-diagonal decay, and a circular packing estimate control every
off-diagonal row. Schur's test or Gershgorin's theorem then yields a uniform
lower eigenvalue.

## Derivation map

1. Build a triangular weight supported in \(I\).
2. Identify its transform exactly as a translated Fejér kernel.
3. Show distinct primitive frequencies are \(U^{-2}\)-separated.
4. Bound each off-diagonal Fejér entry by inverse square distance.
5. Sum inverse squares using circular packing.
6. Convert the row-sum bound into a lower frame.
7. Normalize using \(L\geq N/2\).
8. Insert the V59 scale.

## Main derivation

### Step 1: triangular window

Set \(c=M+L-1\) and

\[
w(c+k)=
\begin{cases}
1-|k|/L,& |k|<L,\\
0,& |k|\geq L.
\end{cases}
\]

The support has length \(2L-1\). If \(N\) is odd, \(2L-1=N\); if \(N\) is
even, \(2L-1=N-1\). Thus the support lies in \(I\), and \(0\leq w\leq1_I\).
The exact weight sum is

\[
\sum_nw(n)=1+2\sum_{k=1}^{L-1}\left(1-\frac{k}{L}\right)=L.
\]

### Step 2: exact Fejér transform

For every \(\theta\in\mathbb R/\mathbb Z\),

\[
\sum_n w(n)e(n\theta)
=e(c\theta)\sum_{|k|<L}\left(1-\frac{|k|}{L}\right)e(k\theta)
=e(c\theta)F_L(\theta).
\]

This is an identity. In particular, \(F_L(0)=L\).

### Step 3: weighted Gram matrix

Since \(0\leq w\leq1_I\),

\[
E_I(z)\geq \sum_nw(n)
\left|\sum_\alpha z_\alpha e(n\alpha)\right|^2
=z^\ast Gz,
\]

where

\[
G_{\alpha,\beta}=e(c(\beta-\alpha))F_L(\beta-\alpha).
\]

The phase direction is fixed by
`conjugate(z_alpha) z_beta e(n(beta-alpha))`; the opposite direction gives
the conjugate quadratic form and is not interchangeable for complex `z`.

The matrix is Hermitian and has diagonal \(L\).

### Step 4: primitive Farey spacing

If \(a/h\) and \(b/k\) are distinct modulo \(1\), choose the integer \(m\)
realizing their circular distance. Then

\[
\left\|\frac ah-\frac bk\right\|
=\left|\frac{ak-bh-mhk}{hk}\right|
\geq\frac1{hk}\geq U^{-2}.
\]

The numerator is a nonzero integer because the two frequencies are distinct.
This step is exact.

### Step 5: Fejér decay

For \(\theta\notin\mathbb Z\),

\[
F_L(\theta)
=\frac1L\left|\frac{\sin(\pi L\theta)}{\sin(\pi\theta)}\right|^2
\leq\frac1{L|\sin(\pi\theta)|^2}.
\]

For \(\|\theta\|\leq1/2\), concavity of sine on \([0,\pi/2]\) gives
\(|\sin(\pi\theta)|\geq2\|\theta\|\). Therefore

\[
F_L(\theta)\leq\frac1{4L\|\theta\|^2}.
\]

### Step 6: circular inverse-square packing

Fix one frequency. Enumerate the other points clockwise and counterclockwise
according to shortest circular distance. The \(j\)-th point in either
direction has distance at least \(j\delta\) when the set is
\(\delta\)-separated. Assign a possible antipodal point to only one direction.
Hence

\[
\sum_{\beta\ne\alpha}\frac1{\|\alpha-\beta\|^2}
\leq2\sum_{j=1}^{\infty}\frac1{(j\delta)^2}
=\frac{\pi^2}{3\delta^2}.
\]

With \(\delta=U^{-2}\), this is at most \(\pi^2U^4/3\).

### Step 7: spectral lower bound

The absolute off-diagonal row sum of \(G\) is at most

\[
D=\frac1{4L}\frac{\pi^2U^4}{3}
=\frac{\pi^2U^4}{12L}.
\]

Schur's test gives \(\|G-LI\|_{\ell^2\to\ell^2}\leq D\). Equivalently,
Gershgorin's theorem places every eigenvalue of \(G\) in
\([L-D,L+D]\). Therefore

\[
z^\ast Gz\geq(L-D)\|z\|_2^2.
\]

Combining this with nonnegativity of \(E_I\) gives

\[
E_I(z)\geq
\left[L-\frac{\pi^2U^4}{12L}\right]_+\|z\|_2^2.
\]

### Step 8: normalized simplification

Because \(L\geq N/2\),

\[
\frac LN\geq\frac12,
\qquad
\frac{\pi^2U^4}{12LN}\leq\frac{\pi^2U^4}{6N^2}.
\]

The positive-part function is monotone, so

\[
\frac{E_I(z)}N
\geq
\left[\frac12-\frac{\pi^2U^4}{6N^2}\right]_+\|z\|_2^2.
\]

### Step 9: V59 exponent

At \(U=x^{133/400}\) and \(N\asymp x\),

\[
\frac{U^4}{N^2}
=x^{4(133/400)-2+o(1)}
=x^{-67/100+o(1)}.
\]

Thus the normalized lower frame is \(1/2-o(1)\).

## Remarks and interpretation

- Translation changes the Gram matrix only by diagonal unitary conjugation.
- The theorem is uniform in the coefficient vector.
- The result identifies where a future power saving must enter: the norm of
  the coefficient vector before distinct-frequency reassembly, not the
  cross-frequency Gram geometry.

## Boundaries and non-claims

- No constant is claimed sharp.
- The theorem starts after \(q\)-collapse.
- Within-bucket cancellation remains open.
- Literal signed \(C_h\) cancellation remains open.
- Signed four-packet projection remains open.
- No arithmetic advance, Route-A gate, \(L2\) gate, full Gate B, or global
  strict \(1/400\) saving is claimed.

## Open risks

No mathematical gap is currently identified. The main research risk is
external to the theorem: a useful arithmetic bound must still lower the
collapsed coefficient energy itself.
