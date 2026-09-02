# TPC-355 computational protocol

The producer freezes three origin panels before evaluating any response:

```text
low_parent    = (6001, 8001, 10001)
higher_parent = (21001, 23001, 25001)
fresh_holdout = (29001, 33001, 37001)
counts        = (256, 512, 1024)
Q             = (24, 54, 80)
exponents     = (1, 2)
laws          = all_plus, alternating_index, mod4_character, half_split
H             = 66
source cutoff = 50000
```

The Cartesian product has `3*3*3*2*4=648` law-level rows.  The raw signed
matrix is accumulated in increasing shell order.  The unsigned geometry
energy is accumulated from the same literal component before applying any
sign law.  The normalized matrix is the symmetric entrywise congruence
`A[u,t]/sqrt(G_u G_t)`.

The independent checker rebuilds source values with a separate sieve and
Decimal midpoint routine, accumulates shell components in reverse order, and
checks both metric families within a declared float64 tolerance.  It also
recomputes an exact rational fourteen-point raw anchor at `[29001,29014]`
with shell `{5,7}`.  The stress checker mutates in-memory copies only.
