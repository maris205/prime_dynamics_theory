# TPC-289 derivation package

## 1. Frozen physical components

For an odd-prime shell `S`, let `A_q` be the literal deleted-diagonal
component retained from TPC-288, let `beta` be the frozen source, and write

```text
g_q = A_q beta,
G_(q,r) = <g_q,g_r>,
d_q = G_(q,q).
```

The aggregate output is `g_S=sum_(q in S) g_q`.  No scalar four-block
attachment is applied in this paper.

## 2. Normalized coherence

For distinct `q,r` with `d_q,d_r>0`, define

```text
Gamma_(q,r) = G_(q,r)^2/(d_q d_r).
```

The square removes the choice of orientation while retaining the exact size
of the cross term.  Its sign is recorded separately as
`sign(G_(q,r))`.

## 3. Energy decomposition

Expanding the aggregate square gives

```text
||g_S||_2^2 = sum_q d_q + sum_(q != r) G_(q,r),
R_E = ||g_S||_2^2 / sum_q d_q
    = 1 + sum_(q != r) G_(q,r) / sum_q d_q.
```

The second sum is over ordered distinct pairs.  Thus pairwise positivity is
a sufficient mechanism for energy amplification, but it is not necessary.

## 4. Conditional accumulation envelope

Fix `0<=eta,delta<=1`.  If every distinct pair satisfies

```text
G_(q,r)>0,
Gamma_(q,r)>=eta^2,
d_min/d_max>=delta,
```

then `G_(q,r)>=eta sqrt(d_q d_r)>=eta d_min`.  There are `k(k-1)` ordered
off-diagonal terms, while `sum_q d_q<=k d_max`.  Therefore

```text
R_E >= 1 + eta (d_min/d_max)(k-1)
    >= 1 + eta delta (k-1).
```

TPC-289 uses `eta=3/5` and `delta=4/5` only as a finite audit threshold.

## 5. What the finite scan tests

The scan tests the conjunction above on an eight-row late-shell block.  It
also deliberately includes the early `N=256,Q=27,s=1` crossover, where the
conjunction fails: pairs `(29,53)`, `(31,53)`, and `(41,53)` are negative,
and pair `(31,53)` has a very small squared coherence.  This is an exact
finite obstruction to promoting the late-block pattern to all declared rows.
