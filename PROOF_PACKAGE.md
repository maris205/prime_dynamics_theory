# TPC working proof: a long-window local-energy operator envelope

Unnumbered research draft, 2026-09-09. This is not a publication or a physical-gate verdict.

## Claim

Let $\mathcal P$ be a finite nonempty set of odd primes, let $a_p>0$, and let
$H\in\mathbb N$ satisfy $H\ge\max\mathcal P$. Set $N=4H$ and
$I_o=\{o,\ldots,o+N-1\}$ for any $o\in\mathbb Z$.
Define real symmetric, zero-diagonal matrices

$$
K_p(u,v)=a_p\frac{H^2}{H^2+(u-v)^2}
\big((p-1)\mathbf1_{p\mid u-v}-1\big)
\mathbf1_{u\ne v}\mathbf1_{p\nmid u}\mathbf1_{p\nmid v}.
$$

For arbitrary real coefficients $|\varepsilon_p|\le1$, put

$$
M=\sum_{p\in\mathcal P}\varepsilon_pK_p,\quad
G(u)=\sum_{p\in\mathcal P}\sum_{v\in I_o}K_p(u,v)^2,\quad
D=\operatorname{diag}(G(u)),\quad \mu=\min_{p\in\mathcal P}a_pp.
$$

Use zero on the zero-energy coordinates in the diagonal inverse square root.
Then, uniformly in all the declared parameters,

$$
\boxed{\left\|D^{-1/2}MD^{-1/2}\right\|_2
\le\frac{144\pi}{\mu}<\frac{576}{\mu}.}
$$

## Status

VERIFIED_SCOPED_CANDIDATE: the parent proof below passed an independent read-only
adversarial proof/source audit on 2026-09-09. See the
[audit report](research/tpc-big-road/research-rounds/2026-09-09-multi-agent-recon/agent-reports/recon-longwindow-proof-audit.md).
The audited mathematical statement is unchanged; the empty-family wording below
has been clarified after that review. This is not publication GO, and novelty is unestablished.
This status concerns only the displayed full-kernel, row-energy-normalized model.
It is not an arithmetic $L^2$ theorem or a closure of image Bridge A / repository Gate B.

## Assumptions and Source Contract

The full C1 kernel is the one printed before the short-window simplification in
[TPC401 main.tex](papers/tpc-401-c1-diagonal-deletion-decomposition/paper/main.tex).
Its shell amplitude is $a_p=p^3/[Q_p^2(p-1)]$. The present proposition allows
general positive amplitudes but retains $a_p$ in the bound through $\mu$.
All diagonal and nonunit masks remain literal. The long-window assumption
$H\ge p$ is used explicitly below and is not inherited from TPC417/418.

No meaning is assigned to $\varepsilon_p$ beyond real model coefficients of
absolute value at most one. No physical $h_0$, actual outer packet weights,
exceptional set, or arithmetic source sequence is assumed or supplied.

## Notation

For a fixed row $u$ write

$$
W_p(u)=\sum_v|K_p(u,v)|,\qquad
G_p(u)=\sum_vK_p(u,v)^2,\qquad
T(d)=\frac{H^2}{H^2+d^2}.
$$

Thus $G(u)=\sum_pG_p(u)$. The norm is the Euclidean operator norm on
the finite coordinate space indexed by $I_o$.

## Proof Strategy and Dependency Map

1. Same-residue points within distance $H$ give $G_p(u)\ge a_p^2pH/72$ on every active row.
2. An integral comparison gives $W_p(u)\le2\pi a_pH$.
3. Summation over primes gives $\sum_v|M(u,v)|\le(144\pi/\mu)G(u)$.
4. Symmetry and a weighted quadratic-form estimate give the operator bound, including zero-energy rows.

No prime-counting, CRT-origin, randomness, or arithmetic cancellation estimate is used.

## Proof

### 1. Inactive rows and same-residue neighbors

If $p\mid u$, all entries of the row of $K_p$ vanish, so $W_p(u)=G_p(u)=0$.
Now suppose $p\nmid u$. Among the two sides of $u$ inside a window of length
$4H$, at least one contains all distances $1,\ldots,H$.
Consequently that side contains the distinct points
$u\pm p,\ldots,u\pm\lfloor H/p\rfloor p$, with the same choice of sign.
They remain in the same nonzero residue class modulo $p$.

Since $H/p\ge1$, we have $\lfloor H/p\rfloor\ge H/(2p)$.
Each such point has $T(d)^2\ge1/4$, and its kernel multiplier is $p-2$.
It follows that

$$
G_p(u)\ge\frac{a_p^2(p-2)^2}{4}\left\lfloor\frac Hp\right\rfloor
\ge\frac{a_p^2(p-2)^2H}{8p}
\ge\frac{a_p^2pH}{72}.
$$

The last step uses $p-2\ge p/3$, valid for every $p\ge3$.

### 2. Absolute row sum

The positive function $T(x)$ decreases for $x\ge0$. For any positive integer $b$,
comparing each term to the integral over the preceding interval of length $b$ yields

$$
\sum_{k\ge1}T(kb)\le\frac1b\int_0^\infty T(x)\,dx
=\frac{\pi H}{2b}.
$$

On an active row, a same-residue off-diagonal entry has absolute multiplier
$p-2$, and every other unit entry has absolute multiplier $1$. Therefore

$$
\begin{aligned}
W_p(u)
&=a_p\left[
\sum_{\substack{v\ne u\\p\nmid v}}T(u-v)
+(p-3)\sum_{\substack{v\ne u\\p\mid u-v}}T(u-v)\right]\\
&\le a_p\left[2\sum_{k\ge1}T(k)
+2(p-3)\sum_{k\ge1}T(kp)\right]\\
&\le a_p\left[\pi H+(p-3)\frac{\pi H}{p}\right]
\le2\pi a_pH.
\end{aligned}
$$

The nonnegative coefficient $p-3$ includes the boundary case $p=3$.
Combining this with Step 1 gives, on active and inactive rows alike,

$$
W_p(u)\le\frac{144\pi}{a_pp}G_p(u)
\le\frac{144\pi}{\mu}G_p(u).
$$

### 3. Combined row sum

The triangle inequality and $|\varepsilon_p|\le1$ imply

$$
\sum_v|M(u,v)|\le\sum_pW_p(u)
\le cG(u),\qquad c=\frac{144\pi}{\mu}.
$$

If $G(u)=0$, every summand $K_p(u,v)^2$ is zero; hence the entire row and,
by symmetry, column of $M$ vanish. The stated zero-inverse convention is consistent.

### 4. Weighted quadratic form

Let $x$ be a real vector and let $y=D^{-1/2}x$, with $y(u)=0$ at zero-energy
coordinates. Symmetry and $2|y(u)y(v)|\le y(u)^2+y(v)^2$ give

$$
\begin{aligned}
|x^TD^{-1/2}MD^{-1/2}x|
&\le\sum_{u,v}|M(u,v)|\,|y(u)y(v)|\\
&\le\sum_u y(u)^2\sum_v|M(u,v)|\\
&\le c\sum_uG(u)y(u)^2
\le c\|x\|_2^2.
\end{aligned}
$$

The normalized matrix is real symmetric, so its Euclidean operator norm equals
the supremum of the absolute Rayleigh quotient. The desired inequality follows;
$\pi<4$ gives the displayed weaker rational constant. $\square$

## Corollary: uniform growing shell families

For a finite nonempty set of integer shell scales $Q_j\ge2$, take any disjoint prime shells
$Q_j<p\le2Q_j$, amplitudes $a_p=p^3/[Q_j^2(p-1)]$, and
$H\ge2\max_jQ_j$. Write $Q_{\min}=\min_jQ_j$.
Since $a_p>p^2/Q_j^2>1$ and $p>Q_{\min}$, the theorem gives

$$
\|Z\|_2<\frac{576}{Q_{\min}},
$$

uniformly in the origin, number of shells, shell cardinalities, and all real
model sign laws. If the prime family is empty but the scale family remains
specified, define the zero operator and the same conclusion holds without
forming $\mu$. If the scale index set itself is empty, state only $Z=0$;
$Q_{\min}$ and the maximum scale are then undefined.
Thus $Q_{\min}\to\infty$ gives a uniform model norm limit in this long-window regime.
No restriction on the size of $o$ and no CRT sign realization are needed.

For comparison only, $Q=\lfloor X^{1/3}\rfloor$ and
$H=\lceil X^{21/32}\rceil$ meet the long-window size condition for all sufficiently
large $X$. This parameter comparison is not an identification with the physical TPC problem.

## Corrections or Missing Assumptions

The bound is not asserted when some $p>H$: Step 1 then supplies no same-residue
neighbors. The full kernel and its full row energy must both be used; the
short-window denominator cannot be substituted. General subwindow restrictions
with a newly defined denominator require a separate argument.

## Open Risks and Claim Ceiling

- Independent scoped proof/source audit passed; publication novelty and physical usefulness remain unestablished.
- This is an unsigned row-sum/energy comparison for a signed model sum, not exploitation of arithmetic signs.
- The physical input/output attachment and the resulting weighted vector norms are unknown here.
- No bound for the actual centered scalar $\mathfrak C_X$, no strict $1/400$ physical saving,
  and no twin-prime statement follows from the displayed normalized estimate alone.
- The existing route ledger must not be changed merely because this unnumbered draft exists.

## Exact readout cost, conditional on a future physical attachment

For arbitrary real vectors $b,w$ on this model window, the zero-energy convention gives

$$
\langle w,Mb\rangle
=\langle D^{1/2}w,ZD^{1/2}b\rangle,
\qquad
|\langle w,Mb\rangle|
\le\frac{144\pi}{\mu}
\left(\sum_uG(u)|w(u)|^2\right)^{1/2}
\left(\sum_uG(u)|b(u)|^2\right)^{1/2}.
$$

This follows by substitution and Cauchy--Schwarz; it does not identify $M$ with
the physical source operator. If such an identification with $\mu\asymp Q=x^{1/3}$
were supplied, using this inequality to reach $x^{5/3-\delta+o(1)}$ would require
the displayed product of weighted vector norms to be $\ll x^{2-\delta+o(1)}$,
with $\delta>1/400$. This is a sufficient budget for this method, not a necessary
condition for arbitrary signed cancellation. No such physical weighted-norm
estimate is proved here. A small normalized operator norm cannot omit this cost.
