# TPC-289 proof package

## Lemma 1 — Gram positivity

For every finite shell, `G=(<g_q,g_r>)` is positive semidefinite.

**Proof.**  For any real coefficients `c_q`,

```text
c^T G c = sum_(q,r)c_q c_r <g_q,g_r>
          = ||sum_q c_q g_q||_2^2 >= 0.
```

Symmetry is immediate from the real inner product. ∎

## Lemma 2 — exact coherence bound

If `d_q,d_r>0`, then `0<=Gamma_(q,r)<=1`.

**Proof.**  The lower bound is a square.  Cauchy--Schwarz gives
`|G_(q,r)|^2<=||g_q||_2^2||g_r||_2^2=d_qd_r`; divide by the positive
denominator. ∎

## Lemma 3 — conditional coherence accumulation

Let `k` be the shell cardinality, `d_min=min d_q`, and
`d_max=max d_q`.  If all off-diagonal entries are positive,
`Gamma_(q,r)>=eta^2`, and `d_min/d_max>=delta`, then

```text
||sum_q g_q||_2^2 / sum_q ||g_q||_2^2
>= 1 + eta delta (k-1).
```

**Proof.**  Positivity chooses the positive square-root branch, so
`G_(q,r)>=eta sqrt(d_qd_r)>=eta d_min`.  Summing over the `k(k-1)` ordered
distinct pairs and using `sum_qd_q<=kd_max` yields

```text
1 + sum_(q!=r)G_(q,r)/sum_qd_q
>= 1 + k(k-1)eta d_min/(k d_max).
```

This is a conditional theorem about a finite family of vectors; it is not an
asymptotic assertion about prime shells. ∎

## Lemma 4 — exact finite sign obstruction

If one declared row contains a negative `G_(q,r)`, then the row cannot satisfy
the all-positive hypothesis of Lemma 3, regardless of its aggregate energy.

**Proof.**  The hypothesis explicitly requires every off-diagonal entry to be
positive.  A negative exact rational entry violates it. ∎

## Certificate consequences

The producer and independent replay reconstruct the same rational vectors and
all 1,380 unordered pair comparisons.  They certify 17/18 pairwise-positive
rows, three negative pairs in one row, eight rows satisfying the
`eta=3/5,delta=4/5` finite threshold block, and energy amplification on all
18 rows.  The mutation audit rejects altered signs, thresholds, counts,
energy, provenance, and row census.

These are finite numerical certificates attached to exact rational
calculations.  A source-restricted or growing-shell coherence theorem remains
open.
