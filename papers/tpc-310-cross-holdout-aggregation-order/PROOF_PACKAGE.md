# TPC-310 proof package

## Lemma 1 — selector census

There are seven nonempty subsets of a three-element ladder set and seven
nonempty subsets of a three-element radius set.  Their Cartesian product has
49 selectors.  Each selector contains `18 |L| |R|` parent cases/envelopes,
because each ladder contributes 18 profile cases and each case contributes one
record at each selected radius.

## Lemma 2 — finite pooled extrema

Let `x_i` range over a finite nonempty set with minimum `x_i^-` and maximum
`x_i^+`.  Independent choices imply

```text
min sum_i x_i = sum_i x_i^-,       max sum_i x_i = sum_i x_i^+.
```

Apply this separately to right and left completion losses.  Since every left
loss is positive, the minimum of the quotient is bounded by right minima over
left maxima, and the maximum by right maxima over left minima.  This is the
pooled interval used by the producer.

## Lemma 3 — positive interval maps

For positive intervals, arithmetic averaging is coordinatewise monotone.  The
functions `log` and `exp` are increasing on `(0,infinity)`, so applying them
coordinatewise and exponentiating the averaged endpoints gives a sound
geometric interval.  A strict class follows whenever the resulting interval
lies wholly below `0.9` or wholly above `1.1`.

## Lemma 4 — weighted-mean identity

For `b_i>0` and `q_i=a_i/b_i`,

```text
(sum_i a_i)/(sum_i b_i)
 = (sum_i b_i q_i)/(sum_i b_i).
```

This follows by substituting `a_i=b_i q_i`.  Consequently pooled and balanced
aggregation agree only under a special weighting relation; no general
aggregation-order invariance is available.

## Finite audit theorem

Applying Lemmas 1–3 to the locked TPC-309 decimal intervals yields a finite,
fail-closed aggregation protocol.  The independent replay confirms all 49
selectors and all 147 aggregate rows.  The full selector has

```text
P = [0.2423655855..., 0.3112477031...]  RIGHT
A = [5.2417686281..., 14.4871333703...] LEFT
G = [0.1993188213..., 0.8609189558...] RIGHT.
```

Therefore the finite record does not support an aggregation-independent
preference claim.  This conclusion is a scoped obstruction, not a statement
about the twin-prime conjecture or a growing asymptotic regime.

## Scope

The proof is exact for the declared finite interval algebra.  The numerical
parent is not directed-rounded, and target labels inherit physical-Gram
dependence from TPC-302.  Arithmetic `L2`, uniform asymptotic budget, fixed
power credit, full Gate B, and a twin-prime conclusion remain open or absent.
