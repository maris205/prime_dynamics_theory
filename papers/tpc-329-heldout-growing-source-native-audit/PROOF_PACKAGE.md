# TPC-329 proof and scope package

## Exact finite proposition: Gram split

Let `I` be finite, let `B_p` be the displayed deleted-diagonal blocks, let
`e_p` be fixed real signs, and put `C_e=sum_p e_p B_p`.  For every finite real
vector `v`,

```text
||C_e v||_2^2
 = sum_t v_t^2 ||C_e e_t||_2^2
   + sum_(t != t') v_t v_t' <C_e e_t,C_e e_t'>.
```

### Proof

The finite matrix-vector product is `sum_t v_t C_e e_t`.  Expanding its
Euclidean square by bilinearity produces the finite double sum over `t,t'`.
Partitioning that sum into `t=t'` and `t!=t'` gives the displayed identity.
No limiting interchange or analytic estimate is used.

## Exact finite proposition: placement null

For `M=2048` or `4096`, define `pi(i)=(5i+17) mod M` and let `P_pi` be the
associated permutation matrix.  Since `gcd(5,M)=1`, `pi` is bijective and

```text
P_pi^T P_pi = I,
||P_pi v||_2 = ||v||_2,
```

for every finite vector `v`.  This proves preservation of the source `L2`
norm and coordinate multiset.  It does **not** prove
`C_e P_pi=P_pi C_e`; the literal divisibility masks and distance kernel have
no assumed invariance under this affine relabeling.

## Source-model proposition

Under the declared finite V59 model, the source coordinate is

```text
beta_o^(2)(t)=Lambda(t+2)-2 C_2 1_(2 does not divide t)
               product_(p|t,p>2)(p-1)/(p-2).
```

The finite product cutoff, positive tail enclosure, and logarithm guard are
part of the executable protocol.  The producer and independent checker use
separate implementations and lock the TPC-328 and TPC-267 ancestors.  This
supports a finite declared-model replay only; it is not an asymptotic theorem
about the twin-prime singular series.

## Certified finite readout

The canonical certificate contains `32` actual rows, `32` corresponding
placement-control rows, `64` two-scale law pairings, and `128` placement
comparisons.  The actual and permuted four-law censuses are:

```text
actual:
  all_plus           31 negative /  1 positive
  alternating_index  25 negative /  7 positive
  mod4_character     32 negative /  0 positive
  half_split         32 negative /  0 positive

permuted:
  all_plus            0 negative / 32 positive
  alternating_index  30 negative /  2 positive
  mod4_character     32 negative /  0 positive
  half_split         28 negative /  4 positive.
```

Every row is separated from the ratio threshold by the declared guard.  The
two component controls are positive on `32/32` rows.  The exact anchor on
`[28001,28016]` is replayed with rational arithmetic and its three digests are
locked in both certificate implementations.

## Narrowest obstruction

On the declared finite panel, a source-multiset-only or source-`L2`-only
explanation cannot determine the all-plus sign of the diagnostic: the source
and its permutation have the same multiset and norm, yet the actual census is
`31/1` negative/positive while the permuted census is `0/32`.  The result is a
finite placement-sensitivity obstruction.  It does not refute a different
operator, a different sign law, or a growing arithmetic theorem.

The earlier finite contraction statement is also refuted on this panel: each
actual declared law has at least one positive off-diagonal row.

## Missing theorem

No source-uniform estimate for the actual arithmetic residual is proved.  In
particular, the release pays zero fixed-power credit and leaves the full
Route-B arithmetic gate and twin-prime endpoint open.  A next theorem must
control the position-sensitive cross term, or explicitly isolate a
permutation-invariant component before attempting a bound.
