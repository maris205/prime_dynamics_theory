# TPC-310 derivation package

## 1. Parent row

For every TPC-309 envelope observation `i`, write

```text
I_i = [rho_i^-, rho_i^+]
rho_i = right_holdout_MSE / left_holdout_MSE.
```

The parent certificate also supplies positive extrema intervals.  Denote the
lower endpoint of the right minimum by `r_i^-`, the upper endpoint of the
right maximum by `r_i^+`, and analogously `l_i^-`, `l_i^+` for the left side.

## 2. Pooled envelope

For a nonempty selector `S`, independent completion choices across rows give

```text
P(S) = [ sum_{i in S} r_i^- / sum_{i in S} l_i^+,
         sum_{i in S} r_i^+ / sum_{i in S} l_i^- ].
```

The numerator minimum and maximum of a sum are attained by taking the rowwise
minima and maxima.  Positive denominators make the displayed quotient the
conservative endpoint enclosure.

## 3. Balanced and geometric maps

The equal-case arithmetic map is

```text
A(S) = [ |S|^(-1) sum rho_i^-, |S|^(-1) sum rho_i^+ ].
```

The geometric map is

```text
G(S) = [ exp(|S|^(-1) sum log rho_i^-),
         exp(|S|^(-1) sum log rho_i^+) ].
```

All endpoints are positive.  Addition, division by a positive scalar, `log`,
and `exp` are monotone on the declared domains, so each map preserves the
parent interval order.

## 4. Why aggregation can reverse a class

For positive point values `a_i,b_i` and `q_i=a_i/b_i`,

```text
sum_i a_i / sum_i b_i = sum_i b_i q_i / sum_i b_i.
```

Thus pooled MSE is a `b_i`-weighted mean of row ratios, whereas `A(S)` gives
each row equal weight.  Their difference is a weighting effect, not an
algebraic contradiction.  TPC-310 records this identity as a reusable
analytic structure and tests it with an exact rational reversal fixture.

## 5. Selector family

The profile subset and radius subset are both required to be nonempty.  Hence
there are `((2^3)-1)^2 = 49` selectors and three aggregate rows per selector,
for 147 aggregate observations.  The budget anchor is a strict majority vote
over profile-budget classes in the selected ladders; it is a diagnostic anchor,
not a theorem about an asymptotic budget.

## 6. Numerical boundary

All formulas above are exact finite operations on the decimal intervals locked
by TPC-309.  The parent physical values came from a float replay with padded
enclosures, so the atlas is `NUMERICALLY_REPRODUCED_FINITE`; it is not a
directed-rounding interval theorem and carries no new arithmetic or fixed-power
credit.
