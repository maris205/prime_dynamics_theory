# TPC-282 proof package

## Projection identity

For each declared block contrast `a` with denominator `d`, the projection
coefficient is the block sum divided by `d`.  Orthogonality of the three
contrasts gives

```text
<P_3 w, P_3 g> = sum_a <a,w> <a,g>/d_a.
```

Consequently the recorded scalar is the exact decomposition

```text
C = <w,g> - <P_3 w,P_3 g> = <(I-P_3)w,(I-P_3)g>.
```

Here `g=A beta` and `S=(I-P_3)g`.  The code uses interval arithmetic for the
source weights and exact rational arithmetic for `g` and `S`.

## Finite source-lock proposition

For each of the six scales and two kernel exponents in the registered schedule,
the certificate verifies `C<0` or `C>0`, `W>0`, `Y>0`, and
`0<C^2/(WY)<1`.  Therefore every registered row has a nonzero actual source
attachment.  This is a finite proposition about the frozen operator family.

## Scope firewall

No implication from twelve finite rows to a bound of the form
`|C_X| >= c X^{-theta}` is made.  In particular, the sign change and the small
minimum of `rho^2` are evidence against silently treating finite attachment
as a uniform positive margin.
