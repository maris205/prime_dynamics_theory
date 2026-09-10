# Short-window shell and coordinate-prefix corollary

Unnumbered working result, 2026-09-09. Location: island 2, image Bridge A,
synthetic operator branch of repository Gate B. No physical arithmetic credit.

Status: **VERIFIED_SCOPED_CANDIDATE**, not publication GO. The candidate and
its independent audit are retained in [the scout report](agent-reports/recon418-growing.md)
and [the proof-audit report](agent-reports/recon-shortwindow-proof-audit.md).
This integrated statement incorporates the audit's nondegenerate-prefix threshold
and retains the original exterior CRT endpoint when the coordinate window shrinks.

## Complete contract

Let $H$ be a positive integer and $N=4H$. Take a finite nonempty ordered
family of complete, nonempty prime shells $(Q_j,2Q_j]$, with integer $Q_j\ge2$
and $2Q_j\le Q_{j+1}$. Require every selected prime to exceed $N$.
List the primes by shell and then in increasing order, globally indexed from zero.
Set $a_i=p_i^3/[Q_j^2(p_i-1)]$ on shell $j$, and $\varepsilon_i=(-1)^i$.
Choose an integer origin $o$ satisfying

$$
p_i\mid o\quad(i\text{ even}),\qquad
p_i\mid o+N\quad(i\text{ odd}).
$$

CRT guarantees some such origins for each finite family, not origins inside a
prescribed physical interval. Define $T_d=H^2/(H^2+d^2)$ and use the literal
masked zero-diagonal C1 components

$$
K_i(u,v)=a_iT_{u-v}
\big((p_i-1)\mathbf1_{p_i\mid u-v}-1\big)
\mathbf1_{u\ne v}\mathbf1_{p_i\nmid u}\mathbf1_{p_i\nmid v}.
$$

For the first $k$ complete shells, let $L_k$ be their prime count. For
$2\le R\le N$, restrict coordinates to $o,\ldots,o+R-1$ and recompute both
$M_{k,R}=\sum_{i<L_k}\varepsilon_iK_i$ and the unsigned component row energy
$D_{k,R}(u,u)=\sum_{i<L_k}\sum_{v=o}^{o+R-1}|K_i(u,v)|^2$ on this restriction.
The endpoint in the CRT condition remains $o+N$, **not** $o+R$.
Write $Z_{k,R}=D_{k,R}^{-1/2}M_{k,R}D_{k,R}^{-1/2}$ where $L_k\ge2$.

## Uniform theorem

There is an absolute integer $H_0\ge8$ such that, for all $H\ge H_0$,
every admissible shell prefix has $L_k\ge2$, and for every integer
$2\le R_0\le4H$,

$$
\boxed{
\sup_{1\le k\le K}\ \sup_{R_0\le R\le4H}\|Z_{k,R}\|_2
\le\frac{2}{\sqrt{\min(H,\lfloor R_0/2\rfloor)}}
+\frac{192\log(4H)}{H}.}
$$

The constants and threshold are independent of the number of shells, their
maximum scale, their cardinalities, and the prescribed CRT origin. Consequently
the bound tends to zero when $H\to\infty$ and $R_0\to\infty$ within this model.

## Proof

Put $J_R=\min(H,\lfloor R/2\rfloor)$ and
$S_r=\sum_{0\le s<R,\,s\ne r}T_{r-s}^2$.
An even-index prime divides only coordinate zero; an odd-index prime divides
none of the retained coordinates, since $0\le r<R\le N<p_i$.
No off-diagonal difference is divisible by any $p_i$.

For the first $k$ shells, put
$P_-=\sum_{i\text{ odd}}a_i$, $V_-=\sum_{i\text{ odd}}a_i^2$,
$V_+=\sum_{i\text{ even}}a_i^2$, and $A=\sum_{i<L_k}(-1)^ia_i$.
The [TPC417 identities](../../../../papers/tpc-417-c1-four-shell-finite-operator-bound/PROOF_PACKAGE.md)
therefore remain exact with the freshly restricted sums:

$$
M_{0r}=P_-T_r,\qquad M_{rs}=-AT_{r-s}\quad(r,s\ge1,\ r\ne s),
$$
$$
D_0=V_-S_0,\qquad
D_r=V_-S_r+V_+(S_r-T_r^2)\quad(r\ge1).
$$

One side of every row contains at least $\lfloor R/2\rfloor$ coordinates.
Thus $S_r\ge J_R/4$. The absolute kernel row sum is at most $4J_R$:
for $R<2H$ it is at most $R-1\le2\lfloor R/2\rfloor$, and otherwise the
two-sided integral bound is at most $\pi H<4H$.
In particular $D_r\ge V_-J_R/4>0$ when $L_k\ge2$.

The normalized endpoint star has norm at most
$2P_-/(V_-\sqrt{J_R})\le2/(a_{\min,k}\sqrt{J_R})$;
here $\sum_{r=1}^{R-1}T_r^2=S_0$ is exact.
The symmetric interior bulk has norm at most $16|A|/V_-$ by absolute row sums.
The [corrected TPC418 parity envelope](../../../../papers/tpc-418-c1-shell-parity-envelope/PROOF_PACKAGE.md)
uses the actual shell sign $\sigma_j=\epsilon_j(-1)^{n_j+1}$ and yields
$|A|\le B_{*,k}<3k+1$. Integer shell scales give $1<a_i<4$.
Writing $m=\lfloor L_k/2\rfloor$, it follows that

$$
\|Z_{k,R}\|_2
\le\frac{2}{a_{\min,k}\sqrt{J_R}}
+\frac{16(3k+1)}{\lfloor L_k/2\rfloor}.
$$

For completeness, the required uniform census follows from the prime number
theorem $\vartheta(x)/x\to1$; the following constant is our consequence, not
a source-quoted explicit estimate. [Selberg, 1949, equation (1.1)](https://www.math.lsu.edu/~mahlburg/teaching/handouts/2014-7230/Selberg-ElemPNT1949.pdf)
Choose an absolute $x_*$ such that $|\vartheta(x)-x|\le x/6$ for $x\ge x_*$,
and choose integer $H_0\ge8$ with $2H_0\ge x_*$.
Every nonempty admissible shell has $Q_j>2H$. For $H\ge H_0$,

$$
n_j\ge\frac{\vartheta(2Q_j)-\vartheta(Q_j)}{\log(2Q_j)}
\ge\frac{Q_j}{2\log(2Q_j)}
\ge\frac{H}{\log(4H)}\ge2.
$$

The middle comparison uses monotonicity of $Q/\log(2Q)$ for $Q\ge2$.
Therefore $L_k\ge kH/\log(4H)$, $\lfloor L_k/2\rfloor\ge L_k/3$,
and $3k+1\le4k$. Substitution gives the stated $192\log(4H)/H$ bound.
Finally $a_{\min,k}>1$ and monotonicity of $J_R$ prove the supremum. $\square$

## Boundaries that matter

- The eventual threshold is essential for defining every normalized shell prefix.
  For $H=1$, shells $Q_1=3,Q_2=6$ have prime sets $\{5\}$ and $\{7,11\}$;
  the full pool has at least two primes but its first shell has $V_-=0$.
- At $R=2$, $\|Z_{k,2}\|_2=P_-/(V_-T_1)>1/4$.
  More generally, using $m\ge L_k/3$, $P_->m$, $V_-<16m$,
  $V_-+V_+<16L_k$, and $S_r\le R-1$ gives
  $|Z_{01}|\ge1/[32\sqrt3(R-1)]$.
  Thus a bounded subsequence of $R_0$ prevents uniform vanishing.
- Principal compressions with the **ambient** diagonal energy fixed are different
  matrices; they inherit the ambient bound without this local-renormalization assertion.
- Complete-shell prefixes preserve the original global prime indices. Arbitrary
  signs, incomplete-shell deletions, or reordering are not covered by this parity proof.
- Integer scales are necessary for the quoted amplitude bound. At $Q=13/2,p=13$,
  $a=13/3>4$; a real-scale extension cannot reuse $a<4$.

## Interpretation and novelty boundary

TPC418 already quantifies over arbitrary finite shell families. Merely allowing
their finite count to grow is not a new cancellation quantifier. The contribution
here is eliminating family dependence through a classical shell census and
extending the local energy bookkeeping to coordinate prefixes, with an exact
short-prefix obstruction. It is a uniform vanishing corollary, not a new arithmetic
cancellation mechanism. Publication novelty is unestablished.

There is no fixed physical $h_0$ in this theorem: $H$ is a kernel height.
Physical coefficients, ordered global coverage, bounded physical origins,
normalization, reassembly, and the strict $1/400$ loss remain unpaid.
The long-window result in [the root proof](../../../../PROOF_PACKAGE.md) concerns
a different regime and must not be substituted for this short-window theorem.
