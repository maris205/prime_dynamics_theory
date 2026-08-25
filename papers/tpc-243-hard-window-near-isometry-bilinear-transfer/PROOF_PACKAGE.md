# TPC-243 Proof Package

## Claim

Let $\mathcal F$ be a finite $\delta$-separated subset of
$\mathbb R/\mathbb Z$, where $0<\delta\leq1/2$. Let
$I=\{M,M+1,\ldots,M+N-1\}$ with $N\geq1$, and define

$$
Tz(n)=\sum_{\alpha\in\mathcal F}z_\alpha e(n\alpha),
\qquad e(t)=e^{2\pi i t}.
$$

Put

$$
K=\left\lfloor\frac1{2\delta}\right\rfloor,
\qquad H_K=\sum_{j=1}^K\frac1j,
\qquad R_\delta=\delta^{-1}H_K,
\qquad \epsilon=\frac{R_\delta}{N}.
$$

With the standard complex inner product conjugate-linear in its first slot,
the Gram matrix $G=T^*T$ has diagonal $N$ and every absolute off-diagonal row
sum at most $R_\delta$. Consequently,

$$
[1-\epsilon]_+\lVert z\rVert_2^2
\leq N^{-1}\lVert Tz\rVert_2^2
\leq(1+\epsilon)\lVert z\rVert_2^2,
$$

and

$$
\left|N^{-1}\langle Tz,Tw\rangle-\langle z,w\rangle\right|
\leq\epsilon\lVert z\rVert_2\lVert w\rVert_2.
$$

For distinct reduced rational frequencies of height at most $U$, where
$U\geq2$, one may take $\delta=U^{-2}$ and therefore

$$
K_U=\left\lfloor\frac{U^2}{2}\right\rfloor,
\qquad R_U=U^2H_{K_U}.
$$

For the V59 interval $I_x=(x/2,x]\cap\mathbb Z$, with
$N=|I_x|=x/2+O(1)$ and $U=x^{133/400}$,

$$
\epsilon_U
=\left(\frac{133}{100}+o(1)\right)x^{-67/200}\log x
=x^{-67/200+o(1)}.
$$

Finally, if $X=N^{-1/2}Tz$ and $Y=N^{-1/2}Tw$, the TPC-242 selected mode is

$$
F_1=\langle Y,X\rangle=N^{-1}\langle Tw,Tz\rangle,
$$

and it differs from $\langle w,z\rangle$ by at most
$\epsilon\lVert w\rVert_2\lVert z\rVert_2$.

## Status

`PROVABLE AS STATED`

Maximum program status:

`PROVED_STRUCTURAL_L1_HARD_WINDOW_NEAR_ISOMETRY_BILINEAR_TRANSFER`.

## Assumptions

- Circular separation means
  $\lVert\alpha-\beta\rVert_{\mathbb R/\mathbb Z}\geq\delta$ for distinct
  $\alpha,\beta\in\mathcal F$.
- Coefficient vectors lie in the finite-dimensional space
  $\ell^2(\mathcal F)$.
- Sequence and coefficient inner products are conjugate-linear in the first
  slot and linear in the second.
- The primitive rational corollary uses reduced representatives and distinct
  frequencies modulo one.

## Notation

- $[r]_+=\max(r,0)$.
- $\lVert\theta\rVert_{\mathbb R/\mathbb Z}$ is distance to the nearest
  integer.
- $H_0=0$ by convention, although the stated range $\delta\leq1/2$ gives
  $K\geq1$.
- $G_{\alpha\beta}=\sum_{n\in I}e(n(\beta-\alpha))$.

## Proof Strategy

Bound each off-diagonal hard-window Gram entry by inverse circular distance,
sum those entry bounds using two one-dimensional packing lists, and apply the
Hermitian Schur/Gershgorin estimate to $G-NI$. The primitive, V59, and TPC-242
statements then follow by exact substitutions.

## Dependency Map

1. Lemma 1 proves the geometric-sum bound for every translated interval.
2. Lemma 2 proves the two-sided harmonic packing estimate, including an
   antipodal tie.
3. Proposition 3 combines Lemmas 1--2 to bound every Gram row.
4. Theorem 4 converts the row bound into quadratic and bilinear estimates.
5. Corollary 5 supplies primitive rational spacing.
6. Corollary 6 computes the exact V59 coefficient and exponent.
7. Corollary 7 fixes the TPC-242 orientation.

## Proof

### Step 0: Empty and singleton frequency sets

If $\mathcal F=\varnothing$, both coefficient spaces contain only the zero
vector, the Gram matrix is the empty matrix, and every assertion is vacuous.
If $|\mathcal F|=1$, the Gram matrix is $[N]$ and its off-diagonal row sum is
zero. Both inequalities then hold with equality in their identity terms. We
may therefore prove the row estimate below without assuming that an
off-diagonal point exists.

### Lemma 1: translated geometric sum

For every $\theta\notin\mathbb Z$,

$$
\left|\sum_{n=M}^{M+N-1}e(n\theta)\right|
\leq\frac1{2\lVert\theta\rVert_{\mathbb R/\mathbb Z}}.
$$

**Proof.** Translation contributes the unit scalar $e(M\theta)$. The finite
geometric-sum identity gives

$$
\left|\sum_{r=0}^{N-1}e(r\theta)\right|
=\frac{|\sin(\pi N\theta)|}{|\sin(\pi\theta)|}
\leq\frac1{|\sin(\pi\theta)|}.
$$

Let $t=\lVert\theta\rVert_{\mathbb R/\mathbb Z}\in(0,1/2]$. Concavity of
$\sin(\pi t)$ on $[0,1/2]$ and its endpoint values imply
$\sin(\pi t)\geq2t$. Since
$|\sin(\pi\theta)|=\sin(\pi t)$, the claim follows. $\square$

### Lemma 2: two-sided circular harmonic packing

Fix $\alpha\in\mathcal F$. Then

$$
\sum_{\substack{\beta\in\mathcal F\\\beta\ne\alpha}}
\frac1{2\lVert\beta-\alpha\rVert_{\mathbb R/\mathbb Z}}
\leq\delta^{-1}H_K.
$$

**Proof.** Represent each $\beta-\alpha$ by a point in $(-1/2,1/2]$.
Assign positive representatives to the clockwise side and negative
representatives to the counterclockwise side. If an antipodal point has
representative $1/2$, assign it to the clockwise side only. Thus no frequency
is counted twice.

On either side, list the assigned circular distances increasingly as
$d_1<d_2<\cdots<d_m$. Include $\alpha$ as the endpoint at distance zero.
Separation of consecutive points along that oriented half-circle gives
$d_1\geq\delta$ and $d_j-d_{j-1}\geq\delta$ for $j\geq2$. Hence
$d_j\geq j\delta$. Since every listed distance is at most $1/2$, one also has
$j\leq(2\delta)^{-1}$ and therefore $m\leq K$.

The contribution of either side is at most

$$
\sum_{j=1}^m\frac1{2d_j}
\leq\frac1{2\delta}\sum_{j=1}^K\frac1j
=\frac{H_K}{2\delta}.
$$

Adding the two side bounds proves the result. When $\delta=1/2$, there can be
at most one off-diagonal point, necessarily antipodal; the one-side assignment
above remains valid. $\square$

### Proposition 3: hard-window Gram row bound

The Gram matrix satisfies

$$
G_{\alpha\beta}
=\sum_{n\in I}\overline{e(n\alpha)}e(n\beta)
=\sum_{n\in I}e(n(\beta-\alpha)).
$$

Thus $G_{\alpha\alpha}=N$. For $\beta\ne\alpha$, separation makes
$\beta-\alpha$ nonintegral, so Lemma 1 applies. Lemma 2 then gives

$$
\sum_{\beta\ne\alpha}|G_{\alpha\beta}|
\leq
\sum_{\beta\ne\alpha}
\frac1{2\lVert\beta-\alpha\rVert}
\leq R_\delta.
$$

This proves the asserted row estimate, including $N=1$ because Lemma 1 does
not require $N>1$. $\square$

### Theorem 4: near-isometry and signed bilinear transfer

Put $A=G-NI$. The matrix $G$ is Hermitian because it is $T^*T$, so $A$ is
Hermitian. Proposition 3 bounds every absolute row sum of $A$ by $R_\delta$.
Hermitian symmetry gives the same column bound. The Schur estimate therefore
gives

$$
\lVert A\rVert_{2\to2}
\leq\sqrt{\lVert A\rVert_1\lVert A\rVert_\infty}
\leq R_\delta.
$$

Equivalently, Hermitian Gershgorin places every eigenvalue of $A$ in
$[-R_\delta,R_\delta]$. Since

$$
\lVert Tz\rVert_2^2=\langle z,Gz\rangle,
$$

we obtain

$$
(N-R_\delta)\lVert z\rVert_2^2
\leq\lVert Tz\rVert_2^2
\leq(N+R_\delta)\lVert z\rVert_2^2.
$$

The Gram matrix is positive semidefinite, so the left side may be strengthened
to $[N-R_\delta]_+\lVert z\rVert_2^2$. Division by $N>0$ proves the
near-isometry statement.

For two coefficient vectors,

$$
\langle Tz,Tw\rangle=\langle z,Gw\rangle.
$$

Consequently,

$$
\begin{aligned}
|N^{-1}\langle Tz,Tw\rangle-\langle z,w\rangle|
&=|\langle z,(N^{-1}G-I)w\rangle|\\
&\leq\lVert N^{-1}G-I\rVert_{2\to2}
\lVert z\rVert_2\lVert w\rVert_2\\
&\leq\epsilon\lVert z\rVert_2\lVert w\rVert_2.
\end{aligned}
$$

This proves both conclusions. $\square$

### Corollary 5: primitive rational frequencies

Let $a/h$ and $b/k$ be distinct reduced frequencies modulo one, with
$h,k\leq U$. Choose an integer $m$ realizing their circular distance. The
integer $ak-bh-mhk$ is nonzero, so

$$
\left\|\frac ah-\frac bk\right\|
=\frac{|ak-bh-mhk|}{hk}
\geq\frac1{hk}\geq U^{-2}.
$$

For $U\geq2$, the value $\delta=U^{-2}$ lies in $(0,1/2]$. Substitution into
Theorem 4 gives

$$
K_U=\left\lfloor\frac{U^2}{2}\right\rfloor,
\qquad R_U=U^2H_{K_U}.
$$

$\square$

### Corollary 6: V59 exponent and leading coefficient

Let $U=x^{133/400}$. Then $U^2=x^{133/200}$ and
$K_U=U^2/2+O(1)$. The harmonic-number asymptotic gives

$$
H_{K_U}=\log K_U+O(1)
=2\log U+O(1)
=\frac{133}{200}\log x+O(1).
$$

Moreover,

$$
N=|(x/2,x]\cap\mathbb Z|=\frac x2+O(1).
$$

Therefore

$$
\begin{aligned}
\epsilon_U
&=\frac{x^{133/200}
\left((133/200)\log x+O(1)\right)}{x/2+O(1)}\\
&=\left(\frac{133}{100}+o(1)\right)
x^{-67/200}\log x.
\end{aligned}
$$

Since $\log x=x^{o(1)}$, the final expression is also
$x^{-67/200+o(1)}$. $\square$

### Corollary 7: TPC-242 selected-mode orientation

In a complex Hilbert space whose inner product is conjugate-linear in the
first slot, set

$$
X=N^{-1/2}Tz,\qquad Y=N^{-1/2}Tw.
$$

TPC-242 proves that the literal $i^j$ phase convention selects
$F_1=\langle Y,X\rangle$. Hence

$$
F_1=N^{-1}\langle Tw,Tz\rangle.
$$

Apply Theorem 4 with the ordered coefficient pair $(w,z)$. It gives

$$
|F_1-\langle w,z\rangle|
\leq\epsilon\lVert w\rVert_2\lVert z\rVert_2.
$$

The target is $\langle w,z\rangle$, not $\langle z,w\rangle$. The latter is
its complex conjugate and generally differs for an orientation-sensitive
pair. $\square$

## Corrections or Missing Assumptions

None for the abstract hard-window theorem. A physical V59 application would
require a separate identification of its two polarized lanes with coefficient
vectors in one common synthesis map and a usable bound for their coefficient
norms.

## Open Risks

- The harmonic row bound uses absolute values and does not prove arithmetic
  cancellation.
- The bilinear error is proportional to
  $\lVert z\rVert_2\lVert w\rVert_2$; no physical coefficient norm bound is
  supplied here.
- Common versus asymmetric physical multipliers remain unclassified.
- Literal top-prime attachment, signed $C_h$, arithmetic $L2$, fixed-atom
  credit, strict $1/400$, full Gate B, and a twin-prime result remain open.
