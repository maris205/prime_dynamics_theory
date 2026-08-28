# TPC-295 derivation package

## Shell matrix

For a finite shell $S$ and frozen integer interval $I$, let

\[
 A=(g_q)_{q\in S}\in\mathbb Q^{I\times S},\qquad
 G=A^{\mathsf T}A,
\]

where each column $g_q$ is the exact deleted-diagonal physical output used in
TPC-294.  The source-coordinate space in this paper is the unrestricted
finite rational vector space $V=\mathbb Q^I$ with its standard inner product.

## Source-correlation image

The map tested here is

\[
 C=A^{\mathsf T}:V\longrightarrow\mathbb Q^S,
 \qquad C(h)=(\langle h,g_q\rangle)_{q\in S}.
\]

It is a correlation map, not a claim that the original Mobius/comparison
profile can be changed arbitrarily.  This distinction is the central scope
firewall.

## Full-rank implication

If $G$ is nonsingular, then for any target $b\in\mathbb Q^S$ define

\[
 h_b=A G^{-1}b.
\]

Then

\[
 A^{\mathsf T}h_b=A^{\mathsf T}A G^{-1}b=G G^{-1}b=b.
\]

Thus $C$ is surjective and every sign target is attained.  In particular, the
TPC-294 weighted minimum sign vector $a_{\min}$ has a finite source witness.

## Modular certificate

All Gram entries are rational.  For a prime $p$ not dividing any displayed
denominator, reduce each entry modulo $p$.  If the resulting matrix has a
nonzero determinant, the rational determinant is nonzero.  The producer uses
$p_1=1000000007$ and $p_2=998244353$; the independent checker uses a separate
source-first accumulation and repeats both reductions.

## Remaining image question

The unrestricted map is intentionally broad.  A native source profile may be
required to have a prescribed Mobius form, interval-weight realization,
support, positivity, or norm budget.  None of those restrictions is encoded
in $V=\mathbb Q^I$ here.  The next stage must therefore measure the least
native witness cost or impose the actual source class, rather than treating
finite surjectivity as an arithmetic theorem.
