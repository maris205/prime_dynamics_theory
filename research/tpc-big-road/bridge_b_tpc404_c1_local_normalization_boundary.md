# Bridge B: TPC-404 local-normalization boundary

TPC-404 is the finite continuation of the TPC-403 CRT-origin proxy.  It proves
the exact local diagonal identities

```text
G(o) = V_minus S0
G(o+1) = V_minus S1 + V_plus (S1 - T1^2)
M(o,o+1) = T1 P_minus
```

and hence the exact normalized square
`(T1 P_minus)^2/(G(o)G(o+1))` for the selected-prime proxy.  Four rational
cases are independently replayed.  Their float64 square-root observations are
approximately `0.013630716999888`, `0.013610790517299`,
`0.013594253931078`, and `0.013570927022735`.

This finite result does not prove a normalized growing obstruction or an upper
bound on the full operator norm.  Arithmetic sign identification, arithmetic
`L2`, fixed-power credit, Route-B reassembly, and a twin-prime conclusion remain
open/none.
