# TPC-294 derivation package

## Physical shell and Gram matrix

For the frozen integer interval $I=I_N$, rational source vector $\beta$, odd
prime $q$, height $H$, and kernel exponent $s$, write

\[
 K_{H,s}(h)=\frac{H^{2s}}{(H^2+h^2)^s},\qquad
 B_q(u,t)=\mathbf 1_{q\nmid u}\mathbf 1_{q\nmid t}
 \left(\mathbf 1_{u\equiv t\pmod q}-\frac1{q-1}\right).
\]

The deleted-diagonal component is $g_q=A_q\beta$, with

\[
 (A_q)_{u,t}=qK_{H,s}(u-t)\mathbf 1_{u\ne t}B_q(u,t).
\]

For a finite shell $S$ define

\[
 G_{q,r}=\langle g_q,g_r\rangle,\qquad
 \operatorname{tr}G=\sum_{q\in S}G_{q,q}.
\]

## Equal-sign Rayleigh layer

For $a\in\{-1,+1\}^{S}$, set

\[
 R(a)=\frac{a^{\mathsf T}Ga}{\operatorname{tr}G}.
\]

Since $a_q^2=1$,

\[
 a^{\mathsf T}Ga=\sum_qG_{q,q}+2\sum_{q<r}a_qa_rG_{q,r},
\]

and hence

\[
 R(a)=1+\frac{2\sum_{q<r}a_qa_rG_{q,r}}{\operatorname{tr}G}.
\]

This is the exact weighted analogue of TPC-293's sign-only edge objective.
The diagonal contribution is fixed; all optimization occurs in the weighted
cross-term sum.  Because $G$ is a Gram matrix, $a^{\mathsf T}Ga\ge0$ for
every sign vector, so $R(a)\ge0$.

## Exact finite optimization

All source and kernel quantities are rational on the declared grid.  Let $D$
be the least common multiple of all Gram denominators and put $M=DG$.
Then $M$ is an integer symmetric matrix and

\[
 R(a)=\frac{a^{\mathsf T}Ma}{\operatorname{tr}M}.
\]

Global reversal leaves the quotient invariant, so the enumeration fixes
$a_0=+1$ and visits the remaining $2^{|S|-1}$ vectors.  The producer uses a
Gray walk: when one label $a_v$ changes sign, the quadratic value changes by

\[
 -4a_v\sum_{j\ne v}M_{v,j}a_j.
\]

Updating the corresponding fields gives every candidate exactly once using
integer arithmetic.  The independent checker uses direct reflected-binary
enumeration and source-coordinate-first accumulation, so agreement is not a
shared implementation artifact.

## Relation to the signed max-cut layer

TPC-293 replaces each nonzero $G_{q,r}$ by its sign and gives every edge unit
weight.  TPC-294 retains $|G_{q,r}|$ and minimizes the actual quadratic
quotient.  A max-cut label can therefore be suboptimal even when it makes the
largest number of edge signs favorable.  This is exactly what happens on all
18 rows of the finite atlas.

## Scope boundary

The sign vectors live in the ambient coefficient-sign cube.  The frozen
source map may have a much smaller image, and no surjectivity or approximate
surjectivity is established here.  Consequently the finite contraction is a
weighted shell diagnostic and a target for the next source-image audit, not
an admissible-source theorem.
