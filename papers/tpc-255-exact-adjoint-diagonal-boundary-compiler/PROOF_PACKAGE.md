# Proof package

## Theorem

For the literal TPC-247 operator, the TPC-253 ordered-rank vector, real
`x` with `N>=2`, and sufficiently large `x` such that `H>2Q`,

```text
(A_x^*z)(t)=sum_q q 1_(q does not divide t)
 [-z(t)E*_(q,t)+J*_(q,t)-(q-2)/(q-1)z(t)].
```

Consequently `<z,A_x beta>` is the exact sum of a deleted-diagonal lane, a
hard-window lane, and a child-jump lane, with the deleted diagonal equal to a
`B_Q`-weighted literal beta midpoint plus an explicit input-unit correction.

## Proof

Fix `q` and `t` with `q` not dividing `t`, and abbreviate

```text
F(u)=conjugate(K_H(u-t))v_(q,t)(u).
```

Then

```text
z(t)P*-z(t)E*+J*
 =sum_(u in I_x)F(u)z(u).
```

The operator deletes `u=t`.  Since `v_(q,t)(t)=(q-2)/(q-1)`, subtraction of
that one coordinate gives the stated coordinate formula, including its minus
sign, outer `q`, and conjugated `K_H(0)`.

For the Poisson step, set `phi(v)=conjugate(psi_+(-v))`.  Reflection and
conjugation preserve compact support in `[-1,1]`, and its inverse physical
kernel is `conjugate(K_H(-h))`.  The V43 complete unit-centered row therefore
applies in the adjoint orientation.  Every nonzero dual frequency has
absolute profile argument at least `H/q>1` when `q<=2Q<H`; hence `P*=0`.

The vector `z` is constant on each child.  If `t in L`, only `u in R`
contributes to `z(u)-z(t)`, with value `-1/rho`; for `t in R`, only `u in L`
contributes, with value `+1/rho`.  This proves the child-jump formulas for
every real clock because the children are defined by ordered rank.

Finally, use the conjugate-linear first slot:

```text
<z,A_x beta>=<A_x^*z,beta>.
```

Since `z,beta` and `K_H(0)` are real at the diagonal, conjugation of the
coordinate formula produces the unstarred hard-window and child-jump rows.
Restoring the excluded `q|t` coordinates converts the diagonal lane into the
displayed `B_Q` identity.

## Unit-mask proof

When `q` does not divide `t`, direct coordinate inspection gives
`v=c+d`.  Across one complete period, `c` and `d` have means
`-1/(q-1)` and `+1/(q-1)`.  Thus applying centered Poisson to either part
alone is invalid.  If `q|t`, the input mask makes the literal summand zero;
the unit-centered row theorem is not invoked.

## Scope

The proof establishes an exact normal form and a source-backed complete-row
zero.  It contains no upper bound for the three surviving signed lanes, no
sign or nonzero theorem, no `L2` estimate, and no Gate-B promotion.
