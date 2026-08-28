# TPC-290 derivation package

## 1. Physical components

Keep the literal deleted-diagonal prime components from TPC-289:
`g_q=A_q beta`, with `G_(q,r)=<g_q,g_r>` and `d_q=G_(q,q)>0`.
For a real weight vector `w`, set `S_w=sum_q w_q g_q`.

## 2. Weighted Rayleigh quotient

Let `D=diag(d_q)`.  Direct expansion gives

```text
||S_w||_2^2 = w^T G w
             = sum_q w_q^2 d_q + 2 sum_{q<r} w_q w_r G_(q,r).
```

Consequently

```text
R(w) = (w^T G w)/(w^T D w)
     = 1 + 2 sum_{q<r} w_q w_r G_(q,r)/(sum_q w_q^2 d_q).
```

The denominator is positive for every nonzero `w` because every `d_q>0`.

## 3. Nonnegative no-decay rule

If `w_q>=0` and every `G_(q,r)>=0`, each cross term in the last display is
nonnegative.  Thus `R(w)>=1`.  If a positive cross term meets two positive
weights, the inequality is strict.  This is an exact sign statement, not a
statistical assumption.

## 4. Effective-support lower bound

Assume in addition that `G_(q,r)>=eta sqrt(d_q d_r)` for every distinct pair
and `d_min/d_max>=delta`.  For nonnegative `w`,

```text
2 sum_{q<r} w_q w_r G_(q,r)
 >= 2 eta d_min sum_{q<r} w_q w_r.
```

The denominator is at most `d_max sum_q w_q^2`.  Since

```text
2 sum_{q<r} w_q w_r = (sum_q w_q)^2-sum_q w_q^2,
```

division yields

```text
R(w) >= 1 + eta (d_min/d_max) (kappa(w)-1)
      >= 1 + eta delta (kappa(w)-1).
```

For uniform weights `kappa=k`, recovering the TPC-289 bound.  The new term
`kappa(w)` quantifies how much a purported adaptive rule has concentrated its
mass.

## 5. Sparse sign-flip witness

For weights supported equally on two indices `i,j`,

```text
R_(i,j) = (d_i+d_j+2G_(i,j))/(d_i+d_j)
         = 1+2G_(i,j)/(d_i+d_j).
```

Thus a negative cross term gives an explicit nonnegative two-component
subunit witness.  It does not give decay for the full physical shell; it
shows exactly how a sign-flip row can evade the positive-block lemma by
collapsing effective support.

## 6. Route interpretation

TPC-290 therefore separates two mechanisms that were conflated by the phrase
“adaptive weighting”: positive full-support reweighting remains behind the
coherence wall, while sparse support can exploit an exceptional negative pair.
The natural next attack is signed two-component Schur cancellation or a
source restriction that proves a diffuse positive block asymptotically.
