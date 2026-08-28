# TPC-290 proof package

## Lemma 1 — weighted Gram identity

For a finite family of vectors `g_q` and a nonzero real vector `w`, with
`G_(q,r)=<g_q,g_r>` and `d_q=G_(q,q)>0`,

```text
R(w)=||sum_q w_q g_q||_2^2 / sum_q w_q^2 d_q
    =1+2 sum_{q<r}w_qw_rG_(q,r)/sum_qw_q^2d_q.
```

**Proof.** Expand the squared norm and use symmetry of the real inner
product.  The diagonal terms are exactly the denominator. ∎

## Lemma 2 — nonnegative no-decay

If `w_q>=0` and `G_(q,r)>=0` for all `q!=r`, then `R(w)>=1`.

**Proof.** The denominator in Lemma 1 is positive.  Every summand in its
cross-term numerator is nonnegative. ∎

## Theorem 3 — diffuse positive-block bound

Suppose `w_q>=0`, `G_(q,r)>=eta sqrt(d_qd_r)` for `q!=r`, and
`d_min/d_max>=delta`, where `eta,delta>0`.  Then

```text
R(w)>=1+eta delta (kappa(w)-1),
kappa(w)=(sum_qw_q)^2/sum_qw_q^2.
```

**Proof.** The coherence hypothesis and nonnegativity give
`G_(q,r)>=eta d_min`.  The cross numerator is therefore at least
`2 eta d_min sum_{q<r}w_qw_r`.  The denominator is at most
`d_max sum_qw_q^2`.  Substitute the polarization identity for the pair sum
and divide. ∎

## Lemma 4 — equal-pair formula

For `w_i=w_j=1` and all other weights zero,

```text
R(w)=1+2G_(i,j)/(d_i+d_j).
```

In particular, a negative Gram cross term is a nonnegative sparse witness
with `R(w)<1`.

**Proof.** Substitute the two nonzero coordinates into Lemma 1. ∎

## Finite consequences

The certificate recomputes the literal output vectors over the TPC-289 grid.
It checks three full-support nonnegative policies, all equal two-prime
supports, and all leave-one-out uniform supports.  The 18-row grid has
54 full-support policy records, all with ratio greater than one.  Exactly
three equal-pair records are subunit, all in the one early sign-flip row;
all 18 leave-one-out minima remain amplified.

These are finite certificates.  The theorem does not assert that the
positive-block hypotheses hold for a growing prime shell or for every source.
