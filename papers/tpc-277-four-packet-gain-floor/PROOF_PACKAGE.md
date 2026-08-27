# TPC-277 proof package

## Theorem 1 — sharp universal gain floor

For four vectors with `D>0` and `G>0`,

```text
G = ||sum_j V_j||^2 <= (sum_j ||V_j||)^2 <= 4 sum_j ||V_j||^2 = 4D.
```

Therefore `r=D/G >= 1/4`.  Equality is attained by four equal aligned
vectors.

## Theorem 2 — signed floor and cancellation coordinate

With `E=sum_{j<k} Re<V_j,V_k>`, expansion gives `G=D+2E`.  If `E<=0`, then
`G<=D` and `r>=1`.  If `G>0`, define

```text
kappa=(D-G)/D.
```

Then `G/D=1-kappa` and hence `r=(1-kappa)^(-1)`.  In particular a polynomial
gain `r>=b x^gamma` is equivalent to the near-cancellation requirement
`G/D<=b^(-1)x^(-gamma)`, not merely to a signed cross-term inequality.

## Theorem 3 — sharp obstruction to geometric power promotion

There is no `gamma>0` forced by the four-packet axioms alone.  Take four
orthogonal unit vectors for every scale.  Then `D=G=4`, so `r=1`, while all
the axioms (including positive energy) hold.  Thus any positive source-level
power lower bound must use arithmetic structure beyond packet geometry.

## Proposition 4 — finite source certificate

The TPC-277 JSON contains eight exact source replays.  Every row has negative
net cross term and `r>1`; one row has `r<101/100`.  The comparisons are made
from outward rational intervals and the exact replay digests.  The independent
checker recomputes all eight pairs and verifies the three overlapping TPC-275
gains exactly.

## Claim ceiling

```text
PROVED_EXACT = universal floors and cancellation coordinate
NUMERICALLY_CERTIFIED_FINITE = eight literal source rows
REFUTED_SCOPED = one-percent floor on the finite registry
OPEN = growing source-level gain, arithmetic L2, full Gate B
FIXED_POWER_CREDIT = 0
```
