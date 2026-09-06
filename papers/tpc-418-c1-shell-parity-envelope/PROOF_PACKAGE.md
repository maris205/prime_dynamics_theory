# Proof Package

## Claim

Let $P_j=\{p:Q_j<p\le2Q_j\}$ be $K$ disjoint ordered complete prime
shells, with $Q_j\ge2$, $n_j=|P_j|\ge1$, $L=\sum_jn_j\ge2$, and every
selected prime larger than $N=4H$. Give global even indices positive sign and
odd indices negative sign. Put

$$
 \alpha_{j,r}=\frac{p_{j,r}^3}{Q_j^2(p_{j,r}-1)},\quad
 \epsilon_j=(-1)^{\sum_{\ell<j}n_\ell},\quad
 \sigma_j=\epsilon_j(-1)^{n_j+1},
$$

and

$$
 b_j=\begin{cases}\alpha_{j,n_j}-\alpha_{j,1},&n_j\text{ even},\\
 \alpha_{j,n_j},&n_j\text{ odd},\end{cases}\qquad
 B_\sigma=\sum_{j:\sigma_j=\sigma}b_j,\quad B_*=\max(B_+,B_-).
$$

Then $1<\alpha_{j,r}<4$, $|A|\le B_*<3E+4\lceil O/2\rceil\le3K+1$,
where $E,O$ count even- and odd-cardinality shells. With the exact TPC417
endpoint-star/interior-bulk decomposition and local diagonal normalization,

$$
 \|Z\|_2\le\frac{2}{a_{\min}\sqrt H}+\frac{16B_*}{V_-}
 <\frac2{\sqrt H}+\frac{16(3K+1)}{m_-},\qquad m_-=\lfloor L/2\rfloor.
$$

## Status

**PROVABLE AS STATED after the user-specified sign correction.** This is a
finite-family synthetic envelope only, not a growing or uniform asymptotic
theorem.

## Assumptions and notation

Shell intervals are ordered and disjoint, concretely $2Q_j\le Q_{j+1}$.
The global index is zero-based. Let $T_d=H^2/(H^2+d^2)$,
$S_r=\sum_{s\ne r}T_{|s-r|}^2$, $P_-$ and $P_+$ be amplitude sums at odd and
even global indices, and $V_-,V_+$ their squared-amplitude sums. Let
$A=P_+-P_-$ and $a_{\min}=\min\alpha_{j,r}$.

## Proof Strategy

Use amplitude monotonicity and the integer-prime endpoint for the shell range;
prove the alternating-block lemma with both the global start sign
$\epsilon_j$ and actual signed-block sign $\sigma_j$; count parity groups; then
reuse the exact TPC417 matrix decomposition.

## Dependency Map

1. The derivative gives within-shell monotonicity.
2. Since $2Q_j$ is even and $p$ is an odd prime, $p\le2Q_j-1$, which is
   needed for $\alpha<4$.
3. The alternating-block lemma gives $|A|\le B_*$.
4. Odd shell signs alternate, so either actual-sign group has at most
   $\lceil O/2\rceil$ odd shells; even shells contribute at most $E$.
5. CRT endpoint masks, exact diagonal deletion, Cauchy--Schwarz, and a
   symmetric row-sum estimate give the operator bound.

## Proof

### Step 1: amplitude range

For fixed integer $Q\ge2$, $f_Q(x)=x^3/[Q^2(x-1)]$ satisfies

$$f_Q'(x)=\frac{x^2(2x-3)}{Q^2(x-1)^2}>0\qquad(x\ge3).$$

Thus amplitudes increase within a shell. Also $f_Q(p)>p^2/Q^2>1$. An
selected prime is odd and $p\le2Q$, while $2Q$ is even, hence $p\le2Q-1$.
Therefore

$$
 \alpha\le f_Q(2Q-1)=\frac{(2Q-1)^3}{Q^2(2Q-2)}<4,
$$

because $8Q^2(Q-1)-(2Q-1)^3=4Q^2-6Q+1>0$ for $Q\ge2$.

### Step 2: alternating-block lemma

For $0<x_1<\cdots<x_n$, let $s=\sum_{k=1}^n(-1)^{k-1}x_k$. If $n$ is
even, adjacent pairing gives

$$s=-\sum_{k=1}^{n/2}(x_{2k}-x_{2k-1})<0,\qquad |s|\le x_n-x_1.$$

If $n$ is odd, then

$$s=x_1+\sum_{k=1}^{(n-1)/2}(x_{2k+1}-x_{2k})>0,\qquad s\le x_n.$$

The bounds follow because the displayed gaps are a subcollection of the
telescoping gaps. Applying this to each shell gives a contribution
$\sigma_jc_j$ with $0<c_j\le b_j$, where
$\sigma_j=\epsilon_j$ for odd $n_j$ and $\sigma_j=-\epsilon_j$ for even
$n_j$. Hence

$$
 A=\sum_j\sigma_jc_j,qquad |A|\le
 \max\left(\sum_{\sigma_j=+1}b_j,\sum_{\sigma_j=-1}b_j\right)=B_*.
$$

This parity flip is the reason the old grouping by $\epsilon_j$ is invalid;
the mixed-parity regression stores both groupings and rejects the old one.

### Step 3: coarse envelope

Every even shell has $b_j<4-1=3$, and every odd shell has $b_j<4$. Odd
shells flip the start sign at each odd block, so each actual-sign group has at
most $\lceil O/2\rceil$ odd shells; even shells contribute at most $E$.
Thus

$$B_*<3E+4\left\lceil\frac O2\right\rceil\le3K+1.$$

The last inequality is $3E+2O\le3K$ for even $O$, and
$3E+2O+2=3K-O+2\le3K+1$ for odd $O$.

### Step 4: TPC417 endpoint-star/interior-bulk decomposition

For distinct window coordinates, $|r-s|<N<Q_j<p$ in the replay domain, so
no selected prime divides two distinct window points. The CRT endpoint masks
and exact diagonal deletion give

$$M_{0r}=P_-T_r,\qquad M_{rs}=-AT_{r-s}\quad(r,s\ge1,r\ne s),$$

with zero diagonal, and exact local energies

$$D_0=V_-S_0,\qquad D_r=V_-S_r+V_+(S_r-T_r^2)\quad(r\ge1).$$

Consequently $Z=D^{-1/2}MD^{-1/2}$ has
$Z=\left[\begin{smallmatrix}0&q^T\\q&C\end{smallmatrix}\right]$ with
$q_r=P_-T_r/\sqrt{D_0D_r}$ and
$C_{rs}=-AT_{r-s}/\sqrt{D_rD_s}$.

At least $H$ distances from every row are at most $H$, so $S_r\ge H/4$.
Using $P_-^2\le m_-V_-$, $V_-\ge m_-a_{\min}^2$, and
$\sum_{r\ge1}T_r^2\le S_0$ gives
$\|q\|_2^2\le4/(a_{\min}^2H)$. Also $D_r\ge V_-H/4$ and the one-sided
kernel sum is at most $2H$, so every row sum of $C$ is at most
$16|A|/V_-\le16B_*/V_-$. Symmetry gives the same $2$-norm bound. The
triangle inequality proves the displayed estimate.

## Edge cases and audit status

$L=1$ is outside the theorem because $m_-=0$; $Q=1$ is rejected because the
range proof assumes $Q\ge2$; overlapping or interleaved shells are rejected
rather than silently reordered. No growing uniform theorem, physical $h_0$,
arithmetic sign or $L^2$ claim, fixed-power credit, Route-B closure, or
twin-prime result follows.
