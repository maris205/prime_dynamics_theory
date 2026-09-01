# TPC-328 proof and scope package

## Exact finite proposition

Let `I` be a finite source interval, let `B_p` be the displayed deleted-
diagonal matrices, let `e_p` be any fixed real signs, and put
`C_e=sum_p e_p B_p`.  For every finite vector `v`,

```text
||C_e v||_2^2
 = sum_t v_t^2 ||C_e e_t||_2^2
   + sum_(t != t') v_t v_t' <C_e e_t,C_e e_t'>.
```

### Proof

The finite product `C_e v` equals `sum_t v_t C_e e_t`.  Bilinearity of the
Euclidean inner product gives the double sum over `t,t'`.  Partitioning that
finite sum into its diagonal and off-diagonal parts gives the displayed
identity.  No limiting interchange or analytic estimate is used.

## Source-model proposition

Under the declared V59 finite model, each source coordinate is evaluated from
the finite formula

```text
beta_o^(2)(t)=Lambda(t+2)-2 C_2 1_(2 does not divide t)
               product_(p|t,p>2)(p-1)/(p-2),
```

where the finite product through `50000`, its positive tail enclosure, and the
100-digit logarithm centers are frozen in the producer.  The producer and the
independent checker use the same formula but separate implementations.  This
supports a finite declared-model replay; it does not identify the model with
an unproved asymptotic twin-prime law.

## Certified finite readout

The canonical certificate contains all 96 rows.  The producer and independent
checker agree on the four-law census:

```text
all_plus           81 negative / 15 positive
alternating_index  73 negative / 23 positive
mod4_character     74 negative / 22 positive
half_split         61 negative / 35 positive
```

No row is unresolved under the `5e-8` ratio guard.  The Lambda and comparison
component controls have positive off-diagonal ratios on `96/96` rows.  At the
small exact anchor `[20001,20016]`, `Q=4`, `s=1`, the rational values satisfy
`E=D+O`; their certificate digests are independently recomputed.

## Narrowest obstruction

The all-plus ratio is below one on 81 rows and above one on 15 rows.  Hence
the statement

```text
E_all_plus(beta) <= D_all_plus(beta)
```

is refuted on the declared finite panel, and the same uniform contraction
statement is not supplied by any of the other three declared laws either.
This is a scoped finite obstruction only.  It does not refute the existence
of another sign law, another normalization, or a growing theorem.

## Missing theorem

No source-uniform estimate for the actual arithmetic residual is proved.  In
particular, the release pays zero fixed-power credit and leaves the full
Route-B arithmetic gate and twin-prime endpoint open.
