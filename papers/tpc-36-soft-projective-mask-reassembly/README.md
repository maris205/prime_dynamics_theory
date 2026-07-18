# TPC-36 - Soft projective mask reassembly

> **Soft Projective Reassembly of the Physical Row Mask: Orthogonal GCD
> Compression, Optimal Ferrers Separation, and Coherent Product-Slope
> Spectra**

TPC-36 resolves the static reassembly issue left open by TPC-35. It proves
that the actual row mask has only \(X^{o(1)}\) bounded-projective cost,
then identifies the genuinely remaining obstacles: product-phase
separation, incomplete/aliased completion, and the coherent \(s\)-spectrum
of the actual Möbius coefficients.

## Main results

### 1. Global actual-mask reassembly

For

\[
\mathfrak m_{\rm act}(\alpha,\gamma)
=\mathbf1_{\ell_\alpha\ne\ell_\gamma}
 \mathbf1_{|m_\alpha-m_\gamma|>\Delta}
 \mathbf1_{(d_\alpha,d_\gamma)\le G},
\]

the paper proves

\[
\pi_\infty(\mathfrak m_{\rm act})
\ll \log(2Q)(3+2\sqrt2)^{\omega_*}=X^{o(1)}.
\]

The three components are handled by source orthogonality, finite interval
Fourier inversion, and a new global orthogonal compression of the exact
gcd projector.

### 2. Fixed-column product-ready form

After fixing the opposite row and one of the \(O_h(1)\) fixed orbit
residue cells, the physical multiplier has an exact decomposition into

\[
b_\rho(\ell)f_\rho(d)\eta_\rho(j)
\]

with \(O(D)\) formal discrete layers but only \(X^{o(1)}\) total signed
projective and orbit-seminorm mass. In particular, \(b_\rho(\ell)\) is
independent of \(j\) and of the reflected complementary factor \(s\).

This solves the **static half** of the complete product-slope reassembly
requested in TPC-35. It does not solve integer-to-modular completion or
alias reassembly.

### 3. Optimal Ferrers separation

For the triangular Ferrers matrix \(T_n=(\mathbf1_{k\le r})\),

\[
\pi_\infty(T_n)=\Theta(\log n),
\qquad
\pi_+(T_n)=n.
\]

Thus signed Fourier layers are optimally logarithmic, while nonnegative or
raw column-by-column rectangle splitting is polynomially expensive.

### 4. Absolute additive-frequency separation is costly

For \(A_r(x,y)=e_q(rxy)\), \(r\ne0\), on
\(\mathbb F_q^\times\),

\[
\pi_\infty(A_r)
=\frac{(q-2)\sqrt q+1}{q-1}\asymp\sqrt q.
\]

By contrast, the multiplication kernel
\(\mathbf1_{xy=a}\) has projective cost exactly \(1\). Expanding it by
additive delta frequencies and reassembling term by term manufactures a
\(\sqrt q\) amplitude loss. At \(q\asymp J\), this is one full \(J\) in
energy. This is a sharp obstruction for that absolute-reassembly route;
the cost-one multiplicative-character reconstruction avoids it.

### 5. Coherent complementary-factor spectrum

For an arbitrary \(s\)-weight \(w\),

\[
\sum_j\left|\sum_s w(s)(Tb)(j,s)\right|^2
=\frac1{q-1}\sum_\chi
|\widehat b(\bar\chi)|^2
\left|\sum_s w(s)\widehat R_s(\chi)\right|^2.
\]

For the complete weight \(w=1\), additive centering gives

\[
\sum_sR_s(a)=qg(0)f(-h/a).
\]

However, the paper also gives centered nonprincipal data for which the
Cauchy factor \(q-1\) in the coherent \(s\)-sum is attained exactly.
Therefore a physical gain must use the actual Möbius-derived weights or a
new joint-alias theorem.

### 6. Reciprocal dyadic localization and the alias ledger

Before modular completion, the divisor range is partitioned into
\(O(\log X)\) dyadic blocks \(u\asymp U\), each paired with its exact
complementary support \(s\asymp X/U\). On every resulting Cartesian
block, \(su=O(X)\). Consequently a prime \(q\asymp X\) gives an exact
no-alias realization, while the analytically useful scale \(q\asymp J\)
has \(O(X/q)=O(Q)\) one-modulus aliases. Three orbit-scale moduli leave
the critical ledger \(X/J^3=Q/J^2=X^{1/400+o(1)}\); proving their
coherent reassembly remains open.

## Exact certificate

Run from this directory:

```text
python experiments/tpc36_certificate.py
python -O experiments/tpc36_certificate.py
```

Both modes perform 137,083 deterministic exact checks and regenerate
byte-identical JSON.

- Certificate digest:
  `4718f7216d8e67a87e84e3ebf6c550afca725c27c7980070f11ca6025ce7ff85`
- Normalized source SHA-256:
  `ed669550fbf29aecdc31062f98fc6446367871505f46d6a4bf0e20d7625a7151`
- JSON SHA-256:
  `9fbbc133d77ca53ed978e75461900917b188bfdb9abf3bd436c1df5e4cfd09b6`

The certificate uses the Python standard library, integers, `Fraction`,
and symbolic finite-group orthogonality. It uses no floating point,
random input, true division, or Python `assert` statements.

## Build

```text
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Claim boundary

TPC-36 does **not** prove the physical coefficient gate, a three-modulus
alias estimate, an affine Chowla theorem, a parity breach, a
Hardy-Littlewood asymptotic, or infinitely many twin primes.

The next exact target is the aggregate weighted coherent functional

\[
\frac1{q-1}\sum_\chi
|\widehat b(\bar\chi)|^2
\left|\sum_s w(s)\widehat R_s(\chi)\right|^2
\]

after the actual incomplete ranges and CRT aliases are restored.
