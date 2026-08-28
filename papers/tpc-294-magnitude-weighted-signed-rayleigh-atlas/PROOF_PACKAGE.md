# TPC-294 proof package

## Theorem 1 — exact trace-normalized identity

Let $G$ be a real symmetric Gram matrix with positive trace and let
$a_i\in\{-1,+1\}$.  Then

\[
 \frac{a^{\mathsf T}Ga}{\operatorname{tr}G}
 =1+\frac{2\sum_{i<j}a_i a_jG_{i,j}}{\operatorname{tr}G}.
\]

**Proof.** Expand the quadratic form into diagonal and upper-triangular
terms.  Since $a_i^2=1$, the diagonal sum is
$\sum_iG_{i,i}=\operatorname{tr}G$.  Symmetry identifies the two copies of
each off-diagonal term, giving the displayed formula after division by the
positive trace. ∎

## Theorem 2 — exact finite sign optimum

Suppose the entries of $G$ are rational and $\operatorname{tr}G>0$.  Let
$D$ be a common positive denominator and $M=DG$.  Exhaustive enumeration of
the $2^{m-1}$ sign vectors with $a_0=+1$, followed by minimization of
$a^{\mathsf T}Ma$, returns the global minimum of $R(a)$ over all sign vectors.

**Proof.** Multiplication by the positive scalar $D$ preserves the ordering
of quadratic values.  Every sign vector is either represented by exactly one
vector with first coordinate $+1$ or by its global reversal, and global
reversal leaves the quadratic form unchanged.  Thus the restricted list
contains one representative of every equivalence class and its minimum is the
unrestricted minimum. ∎

## Lemma 3 — Gray update

Let $M$ be symmetric, let $a_v$ be flipped while all other labels are fixed,
and let $F_v=\sum_{j\ne v}M_{v,j}a_j$.  If the old label is $a_v$, then

\[
 (a')^{\mathsf T}Ma-a^{\mathsf T}Ma=-4a_vF_v.
\]

For every $u\ne v$, the field $F_u$ changes by
$-2a_vM_{u,v}$.

**Proof.** Only the two off-diagonal terms incident to $v$ change.  Their
combined contribution changes from $2a_vF_v$ to $-2a_vF_v$.  The field update
follows because the contribution of vertex $v$ to $F_u$ changes from
$M_{u,v}a_v$ to $-M_{u,v}a_v$. ∎

## Lemma 4 — Gram nonnegativity

If $G_{ij}=\langle g_i,g_j\rangle$, then $a^{\mathsf T}Ga\ge0$ for every
real vector $a$.

**Proof.** It is the squared norm
$\|\sum_i a_i g_i\|^2$. ∎

## Finite certificate consequence

The producer and independent source-first checker agree on the complete
18-row payload.  The finite audit is

```text
rows = 18
edges = 1,380
minimum below one = 18 / 18
all-positive above one = 18 / 18
max-cut candidate below one = 18 / 18
weighted optimum differs from max-cut = 18 / 18
weighted optimum <= 1/4 = 13 / 18
weighted optimum <= 1/10 = 8 / 18
```

These are finite certificate facts.  They do not imply that the minimizing
sign vectors are in the admissible source-coefficient image or that a
sequence of such minima survives as the scale grows.
