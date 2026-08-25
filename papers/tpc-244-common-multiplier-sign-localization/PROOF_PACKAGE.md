# TPC-244 proof package

## Claim

All Hilbert spaces below are complex and their inner products are
conjugate-linear in the first slot.

### Theorem A: common-multiplier phase blindness

Let `A` be a finite index set and let

```text
H = direct_sum_(h in A) H_h.
```

For `b_h,w_h in H_h` and `C_h in C`, define

```text
B=direct_sum_h C_h b_h,
W=direct_sum_h C_h w_h.
```

Then

```text
<W,B> = sum_h |C_h|^2<w_h,b_h>,
||B||^2 = sum_h |C_h|^2||b_h||^2,
||W||^2 = sum_h |C_h|^2||w_h||^2.
```

In particular, replacing `C_h` by `eta_h C_h` in both lanes, where
`|eta_h|=1`, leaves all three quantities invariant.

### Theorem B: nonorthogonal sign-cut localization

Let `J_h:H_h->K` be linear maps into a common complex Hilbert space.  Assume
`C_h` is real and let `s_h in {-1,1}`.  Set

```text
W(s)=sum_h s_h C_h J_h w_h,
B(s)=sum_h s_h C_h J_h b_h,
Q(s)=<W(s),B(s)>.
```

Define

```text
M_hk=<J_h w_h,J_k b_k>,
D=sum_h C_h^2 M_hh,
S_hk=C_h C_k(M_hk+M_kh), h<k.
```

Then

```text
Q(s)=D+sum_(h<k)s_hs_k S_hk,                    (B1)
Q(s)-Q(1)=-2 sum_(h<k,s_h!=s_k)S_hk.            (B2)
```

Moreover, `Q` is constant on every sign pattern if and only if `S_hk=0` for
every unordered pair.  This does not require the two directed terms in
`S_hk` to vanish separately.

### Corollary C: hard-window sign leakage

Assume the coefficient vectors of Theorem A are supported on one finite
`delta`-separated frequency set and are synthesized by the common TPC-243 map
`T` on `N` consecutive integers.  Write

```text
epsilon=delta^(-1)H_floor(1/(2delta))/N,
Q_I(eta)=N^(-1)<TW(eta),TB(eta)>.
```

For any two common unit-phase patterns `eta` and `xi`,

```text
|Q_I(eta)-Q_I(xi)| <= 2epsilon||W||||B||.        (C1)
```

The norms on the right are coefficient-space norms.  Under the primitive V59
height specialization, `epsilon=x^(-67/200+o(1))`.

## Status

Theorems A--B and Corollary C are `PROVABLE AS STATED`.

Maximum program status:

`PROVED_STRUCTURAL_L1_COMMON_MULTIPLIER_SIGN_LOCALIZATION`.

The V59 physical interpretation is
`CONDITIONAL_ON_LITERAL_V59_PHASEWISE_PRIMITIVE_TWO_LANE_ATTACHMENT`.

## Proof

### Proof of Theorem A

Orthogonality of the direct sum removes every pair with different block
indices.  Therefore

```text
<W,B>
 =sum_h <C_h w_h,C_h b_h>
 =sum_h conjugate(C_h)C_h<w_h,b_h>
 =sum_h |C_h|^2<w_h,b_h>.
```

The two norm identities follow by setting the two lane vectors equal.  If
`|eta_h|=1`, then `|eta_h C_h|^2=|C_h|^2`, which proves simultaneous
blockwise phase invariance.  The proof includes zero multipliers, zero
vectors, empty index sets, and one-block spaces without modification.

The common-lane hypothesis is essential.  With lane-dependent multipliers
`A_h` and `D_h`, the block coefficient is `conjugate(A_h)D_h`, whose phase is
generally visible.  This observation is an invalidation condition, not an
arithmetic result.

### Proof of Theorem B

Finite expansion gives

```text
Q(s)=sum_(h,k)s_hs_k C_hC_k M_hk.
```

The diagonal terms have `s_h^2=1` and sum to `D`.  Pairing the two directed
terms for `h<k` gives `(B1)`.  Relative to the all-positive pattern, an
unordered pair is unchanged when `s_h=s_k` and changes from `+S_hk` to
`-S_hk` when `s_h!=s_k`.  This proves `(B2)`.

If every `S_hk` vanishes, `(B1)` makes `Q` constant.  Conversely, suppose `Q`
is constant on the sign cube of size `2^m`.  For a fixed pair `a<b`, multiply
`(B1)` by the Walsh character `s_as_b` and average over all sign patterns.
Every constant and every distinct Walsh character has zero average, while
`(s_as_b)^2=1`.  Thus

```text
2^(-m)sum_s Q(s)s_as_b=S_ab.
```

The left side is zero because `Q` is constant and `s_as_b` is nontrivial.
Hence `S_ab=0`.  Since the pair was arbitrary, all cross coefficients vanish.
For `m<2`, there are no pairs and the condition is vacuous.

For complex `C_h`, the same expansion is valid after replacing the paired
coefficient by

```text
conjugate(C_h)C_k M_hk + conjugate(C_k)C_h M_kh.
```

The real formula is used for literal Möbius-log `C_h`.

### Proof of Corollary C

TPC-243 gives for any coefficient vectors `u,v`

```text
|N^(-1)<Tu,Tv>-<u,v>|<=epsilon||u||||v||.
```

By Theorem A, every common unit-phase pattern has the same coefficient
covariance `q_0=<W,B>` and the same two norms.  Hence

```text
|Q_I(eta)-q_0|<=epsilon||W||||B||,
|Q_I(xi)-q_0|<=epsilon||W||||B||.
```

The triangle inequality proves `(C1)`.  The orientation is the TPC-242
selected mode: with `X=N^(-1/2)TB` and `Y=N^(-1/2)TW`, one has
`F_1=<Y,X>=Q_I`.  No physical-signal norm is substituted on the right.

For distinct primitive rational frequencies of height at most `U`, TPC-243
allows `delta=U^(-2)`.  Its V59 specialization gives

```text
epsilon=(133/100+o(1))x^(-67/200)log x
       =x^(-67/200+o(1)).
```

This exponent statement remains conditional on the literal coefficient
attachment and a payable bound for `||W||||B||`.

## Source interface and claim boundary

TPC-214 proves exact reduced-frequency clustering and already exhibits
`|C_h|^2` in the complete-period unsigned energy.  TPC-237 supplies primitive
exactly-once frequency coordinates and retains one literal `C_h` in each
packet.  Those facts support the coefficient-space geometry.

The current sources do **not** prove that the literal V59 sequences `beta,w`
produce vectors `b_h,w_h` in one common primitive synthesis map with identical
block multipliers.  TPC-228 explicitly leaves this physical crosswalk open.
Accordingly, the paper does not claim:

- literal V59 two-lane attachment;
- a signed `C_h` cancellation theorem;
- a coefficient norm estimate;
- arithmetic `L2` or fixed-atom credit;
- payment of strict `1/400` or full Gate B;
- any twin-prime result.

The theorem erases only an externally applied aggregate phase.  Möbius signs
inside the sum defining `C_h` may change `|C_h|` and remain fully relevant.

## Reusable structure and next theorem

The exact reusable structure is

```text
common multiplier diagonal
  -> |C_h|^2 local covariance
  -> cross-block sign-cut polynomial
  -> hard-window leakage bound.
```

The next minimal object is the local covariance `<w_h,b_h>`.  Decomposing each
lane into its longitudinal component along a canonical block vector and its
transverse component yields an exact center-radius disk.  That is the TPC-245
candidate; it stays in the same twin-prime dynamical family.
