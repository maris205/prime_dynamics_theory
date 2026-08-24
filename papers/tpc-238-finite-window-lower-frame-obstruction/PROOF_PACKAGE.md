# Proof Package

## Claim

Let \(I\) contain \(N\geq1\) consecutive integers and put
\(L=\lfloor(N+1)/2\rfloor\). Let \(U\geq1\), and let
\(\mathcal F\subset\mathbb R/\mathbb Z\) be a finite set of distinct primitive
fractions \(a/h\) with \(h\leq U\). For complex coefficients
\((z_\alpha)_{\alpha\in\mathcal F}\), define

\[
E_I(z)=\sum_{n\in I}\left|\sum_{\alpha\in\mathcal F}
z_\alpha e(n\alpha)\right|^2.
\]

Then

\[
E_I(z)\geq
\left[L-\frac{\pi^2U^4}{12L}\right]_+
\sum_{\alpha\in\mathcal F}|z_\alpha|^2.
\]

Consequently,

\[
\frac{E_I(z)}N\geq
\left[\frac12-\frac{\pi^2U^4}{6N^2}\right]_+
\sum_{\alpha\in\mathcal F}|z_\alpha|^2.
\]

## Status

**PROVABLE AS STATED**

## Assumptions

- \(N\geq1\) and \(U\geq1\).
- Fractions are primitive and distinct modulo \(1\).
- The coefficient family is finite.

## Notation

- \(e(t)=\exp(2\pi i t)\).
- \(\|\theta\|\) denotes distance to the nearest integer.
- \([y]_+=\max(y,0)\).
- \(F_L(\theta)=L^{-1}|\sum_{r=0}^{L-1}e(r\theta)|^2\).

## Proof strategy

Minorize the hard interval by a triangular window. Its Gram matrix has Fejér
entries. Bound the off-diagonal operator norm by combining primitive Farey
spacing, inverse-square Fejér decay, and circular packing.

## Dependency map

1. The main claim depends on the weighted Gram lower bound.
2. The weighted Gram lower bound depends on its diagonal and off-diagonal row sum.
3. The row sum depends on Lemmas 2--4 below.
4. The normalized statement uses only \(L\geq N/2\).

## Proof

### Lemma 1: translated triangular window

Write \(I=\{M,\ldots,M+N-1\}\), let \(c=M+L-1\), and define

\[
w(c+k)=
\begin{cases}
1-|k|/L,& |k|<L,\\
0,& |k|\geq L.
\end{cases}
\]

Then \(0\leq w(n)\leq1_I(n)\), and

\[
\sum_nw(n)e(n\theta)=e(c\theta)F_L(\theta).
\]

**Proof.**
The support is \(\{c-L+1,\ldots,c+L-1\}\). Its left endpoint is \(M\).
Its right endpoint is \(M+2L-2\), which is at most \(M+N-1\) because
\(2L-1\leq N\). Hence \(w\) is supported in \(I\), and its definition gives
\(0\leq w\leq1\).

The identity

\[
\frac1L\left|\sum_{r=0}^{L-1}e(r\theta)\right|^2
=\sum_{|k|<L}\left(1-\frac{|k|}{L}\right)e(k\theta)
\]

follows by grouping the \(L^2\) pairs \((r,s)\) according to \(k=r-s\).
Translation by \(c\) supplies the factor \(e(c\theta)\). This proves the
lemma. \(\square\)

### Lemma 2: primitive rational spacing

Distinct primitive fractions \(a/h,b/k\pmod1\), with \(h,k\leq U\), satisfy

\[
\left\|\frac ah-\frac bk\right\|\geq U^{-2}.
\]

**Proof.**
Choose \(m\in\mathbb Z\) such that the left side equals
\(|a/h-b/k-m|\). The integer \(ak-bh-mhk\) is nonzero because the two
fractions are distinct modulo \(1\). Therefore

\[
\left|\frac ah-\frac bk-m\right|
=\frac{|ak-bh-mhk|}{hk}\geq\frac1{hk}\geq U^{-2}.
\]

The primitivity assumption ensures that the chosen denominators are the
reduced heights used in the bound. \(\square\)

### Lemma 3: Fejér off-diagonal decay

For \(\theta\notin\mathbb Z\),

\[
F_L(\theta)\leq\frac1{4L\|\theta\|^2}.
\]

**Proof.**
The geometric-sum identity gives

\[
F_L(\theta)
=\frac1L\left|\frac{\sin(\pi L\theta)}{\sin(\pi\theta)}\right|^2
\leq\frac1{L|\sin(\pi\theta)|^2}.
\]

Let \(t=\|\theta\|\in(0,1/2]\). Concavity of \(\sin(\pi t)\) on
\([0,1/2]\), together with its endpoint values \(0\) and \(1\), gives
\(\sin(\pi t)\geq2t\). The claimed inequality follows. \(\square\)

### Lemma 4: circular inverse-square packing

Let \(\mathcal X\subset\mathbb R/\mathbb Z\) be finite and
\(\delta\)-separated in circular distance. For each \(x\in\mathcal X\),

\[
\sum_{\substack{y\in\mathcal X\\y\ne x}}
\frac1{\|x-y\|^2}\leq\frac{\pi^2}{3\delta^2}.
\]

**Proof.**
Fix \(x\). Assign every \(y\ne x\) to the clockwise or counterclockwise
shortest arc from \(x\) to \(y\); assign an antipodal tie to one side only.
On either side, list the assigned distances increasingly as
\(d_1<d_2<\cdots\). Separation implies \(d_j\geq j\delta\): otherwise
the arc from \(x\) to the \(j\)-th point, of length less than \(j\delta\),
would contain \(j+1\) points including \(x\), forcing two consecutive points
to be less than \(\delta\) apart. Hence

\[
\sum_{y\ne x}\frac1{\|x-y\|^2}
\leq2\sum_{j=1}^{\infty}\frac1{(j\delta)^2}
=\frac2{\delta^2}\frac{\pi^2}{6}
=\frac{\pi^2}{3\delta^2}.
\]

This proves the lemma. \(\square\)

### Theorem proof

If \(\mathcal F\) is empty, the claim is immediate. If \(1\leq U<2\), the
only possible primitive frequency is \(0/1\); the weighted Gram matrix below
has no off-diagonal entries, and the claimed weaker bound follows. We now
treat the general case uniformly.

By Lemma 1 and \(0\leq w\leq1_I\),

\[
E_I(z)\geq
\sum_nw(n)\left|\sum_{\alpha\in\mathcal F}z_\alpha e(n\alpha)\right|^2
=z^\ast Gz,
\]

where

\[
G_{\alpha,\beta}
=e(c(\beta-\alpha))F_L(\beta-\alpha).
\]

The `beta-alpha` direction follows from the coefficient
`conjugate(z_alpha) z_beta e(n(beta-alpha))`; it must not be reversed for
complex coefficient vectors.

The matrix \(G\) is Hermitian, and \(G_{\alpha,\alpha}=F_L(0)=L\).
By Lemmas 2--4, every off-diagonal row obeys

\[
\begin{aligned}
\sum_{\beta\ne\alpha}|G_{\alpha,\beta}|
&=\sum_{\beta\ne\alpha}F_L(\alpha-\beta)\\
&\leq\frac1{4L}
\sum_{\beta\ne\alpha}\frac1{\|\alpha-\beta\|^2}\\
&\leq\frac1{4L}\frac{\pi^2U^4}{3}
=\frac{\pi^2U^4}{12L}.
\end{aligned}
\]

Gershgorin's theorem for the Hermitian matrix \(G\) therefore gives

\[
z^\ast Gz\geq
\left(L-\frac{\pi^2U^4}{12L}\right)\|z\|_2^2.
\]

Independently, \(E_I(z)\geq0\). Selecting the stronger of these two lower
bounds yields

\[
E_I(z)\geq
\left[L-\frac{\pi^2U^4}{12L}\right]_+\|z\|_2^2.
\]

This proves the first claim.

For the normalized claim, \(L=\lfloor(N+1)/2\rfloor\geq N/2\), so

\[
\frac LN-\frac{\pi^2U^4}{12LN}
\geq\frac12-\frac{\pi^2U^4}{6N^2}.
\]

Division by \(N>0\) commutes with positive part, and positive part is
monotone. The second claim follows. \(\square\)

## Corrections or missing assumptions

None. The primitive and distinct-frequency hypotheses are essential to the
stated \(U^{-2}\) spacing argument and are explicit.

## Open risks

- The constants are not asserted to be sharp.
- The theorem does not control how small a collapsed coefficient can become
  through arithmetic cancellation inside its defining \(q\)-bucket.
- The result does not address the signed four-packet projection.
