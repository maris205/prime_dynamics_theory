# Derivation Package

## Target

Derive an exact two-lane covariance representation of the literal V59 scalar,
then record every loss introduced by a block-pair direct sum.

## Status

`COHERENT AFTER REFRAMING`: the target survives on the physical source-index
space, but not as an automatic primitive-frequency attachment.

## Invariant Object

The invariant object is the full V59 scalar with outer prime weight, both unit
masks, deleted diagonal and the kernel orientation `K_H(u-t)` unchanged.

## Assumptions

- `I_x` and the prime shell are finite.
- The physical `beta` and `w` are real.
- Inner products are conjugate-linear in their first slot.
- The hard source blocks form an explicitly declared disjoint partition.

## Notation

```text
A_x(u,t)=1_(u!=t) sum_q q 1_(q does not divide u)1_(q does not divide t)
         K_H(u-t)[1_(u=t mod q)-1/(q-1)].
```

For support projections `P_b`, put `A_cb=P_cA_xP_b`,
`beta_b=P_b beta`, and `w_c=P_cw`.

## Derivation Strategy

First package the literal double sum as an operator pairing.  Only then insert
the resolution of the identity on the input and output coordinates.  Finally
use tagged copies to turn the finite sum of pairings into one direct-sum
pairing and compute its norms exactly.

## Derivation Map

1. Literal V59 sum -> source operator: exact identity.
2. Two resolutions of identity -> ordered hard blocks: exact identity.
3. Unique coordinate membership -> exactly-once triple ledger: exact identity.
4. Tagged copies -> one covariance: exact identity.
5. Direct-sum norm calculation -> duplication toll: exact proposition.
6. Primitive-frequency interpretation: remains open.

## Main Derivation

Because the unit masks make `t` invertible modulo every active prime,

```text
u_1(u t^(-1);q)=1_(u=t mod q)-1/(q-1).
```

The physical reality of `w` therefore gives

```text
<w,A_x beta>=sum_(u,t)w(u)A_x(u,t)beta(t)=C_x.
```

Using `sum_bP_b=I` on both sides of the operator,

```text
A_x=sum_(b,c)P_cA_xP_b=sum_(b,c)A_cb.
```

Orthogonality of the output supports yields

```text
<w,A_x beta>=sum_(b,c)<w_c,A_cb beta_b>.
```

Every source coordinate has one block label, so an admissible triple
`(q,t,u)` appears only in `(c(u),b(t))`.  In tagged copies the last sum is
`<W_ext,B_ext>`.  If there are `m` input blocks, every `w_c` occurs in `m`
copies and hence `||W_ext||^2=m||w||^2`.  The `B` norm is the sum of the
separate block-output squares and retains no cross-`b` cancellation.

## Remarks and Interpretation

This closes the existence question for a literal physical-index two-lane
covariance.  It simultaneously explains why existence alone does not pay the
TPC-243 bilinear error: the coefficient norm has changed.

## Boundaries and Non-Claims

- No hard partition is canonically selected by V59.
- No smooth-partition equality, primitive rational map, PSD factorization or
  common scalar multiplier is asserted.
- No asymptotic estimate or arithmetic cancellation follows.

## Open Risks

The next exact object must keep one shared `w_c` across all input probes and
audit its joint feasible set before using TPC-246's Cartesian-product theorem.
