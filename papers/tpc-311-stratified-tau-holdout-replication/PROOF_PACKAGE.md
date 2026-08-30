# TPC-311 proof package

## Lemma 1 — independent extrema of a finite sum

Let `X_j` be nonempty finite sets with extrema `x_j^-` and `x_j^+`.  If the
choices are independent, then

```text
min sum_j x_j = sum_j x_j^- ,
max sum_j x_j = sum_j x_j^+ .
```

Indeed, termwise endpoint inequalities give both bounds, and choosing every
lower or every upper endpoint attains them.

## Lemma 2 — positive profile-pooled interval

For every nonempty design stratum, all four endpoint sums in `P_s` are
positive.  Lemma 1 gives the lower and upper numerator extrema and the lower
and upper denominator extrema.  Quotient monotonicity on positive inputs then
gives

```text
P_s^- = sum R^- / sum L^+,
P_s^+ = sum R^+ / sum L^- .
```

Thus `P_s` is a sound enclosure for the declared finite pooled ratio.

## Lemma 3 — equal-stratum interval map

If `P_s^- <= P_s^+` for every `s` in a nonempty block, then

```text
S^- = |B|^{-1} sum P_s^-
S^+ = |B|^{-1} sum P_s^+
```

is an ordered positive interval.  This follows by summing the coordinatewise
inequalities and dividing by the positive integer `|B|`.

## Lemma 4 — finite tau partition

The sets `{0.25,0.5}` and `{0.75}` are disjoint, and their union is
`{0.25,0.5,0.75}`.  Crossing either set with the fixed transition,
exponent, and radius sets therefore gives the stated calibration,
confirmation, and full blocks without overlap.

## Proposition — two-stage protocol is well-defined

Every declared TPC-311 block has a nonempty finite set of design strata, each
stratum has exactly three profile-ladder rows, and all denominators are
positive.  By Lemmas 1–4, the producer's interval and class operations are
well-defined and fail closed on malformed input.

## What is not proved

The parent decimal intervals are not directed-rounding intervals for the
underlying physical calculation.  The proof package therefore does not prove
that the finite numerical classes hold for an unrounded physical source.  It
also does not prove that equal design-stratum weights are canonical, that the
held-out tau slice is statistically independent, or that the observed finite
reversal persists as the prime shells grow.  No arithmetic `L2`, fixed-power
credit, Gate-B passage, or twin-prime theorem follows.
