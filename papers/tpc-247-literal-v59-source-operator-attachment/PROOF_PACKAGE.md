# Proof Package

## Claim

Let `H_x=C^(I_x)` with inner product conjugate-linear in the first slot.  For
the real V59 physical sequences define

```text
A_x(u,t)=1_(u!=t) sum_(q in Q_x)
 q 1_(q does not divide u)1_(q does not divide t)K_H(u-t)
 [1_(u=t mod q)-1/(q-1)].
```

Then `C_x=<w,A_x beta>`.  For a finite disjoint coordinate partition with
support projections `P_b`, define `A_cb=P_cA_xP_b`, `beta_b=P_b beta` and
`w_c=P_cw`.  Then

```text
A_x=sum_(b,c)A_cb,
C_x=sum_(b,c)<w_c,A_cb beta_b>,
```

and each admissible triple `(q,t,u)` occurs exactly once.  In tagged copies
`H_c^(b,c)`, the vectors

```text
B_ext=direct_sum_(b,c)A_cb beta_b,
W_ext=direct_sum_(b,c)w_c
```

satisfy `<W_ext,B_ext>=C_x`.  If there are `m` input blocks,

```text
||W_ext||^2=m||w||^2,
||B_ext||^2=sum_(b,c)||A_cb beta_b||^2,
```

and no general identity relates the latter to `||A_x beta||^2`.

## Status

`PROVABLE AS STATED` with the tagged-copy and norm caveats included.

## Assumptions

- Every active modulus is prime and both source indices are units modulo it.
- `w` is the real physical V59 sequence.
- The blocks are disjoint coordinate supports, not an overlapping partition.

## Notation

`P_b` multiplies by the indicator of block `I_b`.  An admissible triple means
`q in Q_x`, `t!=u`, and `q` divides neither `t` nor `u`.

## Proof Strategy

Use the two resolutions of the identity and then compute the Hilbert direct
sum coordinatewise.  No spectral property of `A_x` is used.

## Dependency Map

1. The operator identity uses only the exact V59 kernel.
2. The block identity uses orthogonal support projections.
3. Exactly-once uses unique block membership.
4. The covariance identity and norm formulas use tagged direct sums.
5. A three-coordinate matrix gives the sharp norm-preservation obstruction.

## Proof

The unit masks make the inverse of `t` modulo `q` legal.  Moreover,
`u t^(-1)=1 mod q` if and only if `u=t mod q`; hence the displayed matrix is
the literal V59 kernel.  Since `w` is real and the inner product is linear in
its second slot, direct expansion gives `C_x=<w,A_x beta>`.

The projections are self-adjoint, pairwise orthogonal, and sum to the
identity.  Therefore

```text
sum_(b,c)A_cb=(sum_cP_c)A_x(sum_bP_b)=A_x.
```

Also `A_cb beta_b` belongs to `P_cH_x`, so orthogonality of output supports
and finite bilinearity give

```text
<w,A_x beta>=sum_(b,c)<w_c,A_cb beta_b>.
```

For every admissible `(q,t,u)`, the disjoint partition supplies one label
`b(t)` and one label `c(u)`.  The entire summand belongs to that block and to
no other, proving exactly-once occurrence.

Now replace each occurrence of `P_cH_x` by a separately tagged Hilbert copy.
Orthogonality of those copies gives

```text
<W_ext,B_ext>=sum_(b,c)<w_c,A_cb beta_b>=C_x.
```

Each `w_c` occurs once for every one of the `m` input blocks.  Pythagoras
therefore gives `||W_ext||^2=m sum_c||w_c||^2=m||w||^2`.  The second norm
formula follows in the same way.

For failure of `B`-norm preservation, use singleton blocks on three
coordinates and

```text
A=[[0,1,-1],[0,0,0],[0,0,0]],  beta=(0,1,1).
```

Then `A beta=0`, while two distinct tagged block outputs are `+1` and `-1`.
Thus `||B_ext||^2=2` but `||A beta||^2=0`.  This proves the obstruction and
the theorem. `QED`

## Corrections or Missing Assumptions

If a genuinely complex coefficient is inserted without conjugating the
physical scalar, the first lane must be `conjugate(w)`.  No correction is
needed for the real V59 sequence.

## Open Risks

The external copies do not supply primitive rational frequencies, a common
TPC-243 synthesis map, norm payment, a TPC-244 common multiplier, or any
arithmetic bound.
