# TPC-277 paper plan

## Question

What lower bound on the signed four-packet gain is forced by geometry, and do
the actual source rows support a stronger uniform finite floor?

## Frozen object

- TPC-268 literal prime-shell operator, beta source, masks, deleted diagonal,
  and rank-three four-block Haar projection;
- TPC-275 actual four consecutive source packets;
- TPC-275 result JSON for parent provenance on the overlapping rows.

## Claim-bearing contributions

1. Prove the sharp universal inequality `G<=4D`, and the sharper `G<=D`
   under a nonpositive net cross term.
2. Define the cancellation fraction `kappa=(D-G)/D` and prove
   `r=D/G=(1-kappa)^(-1)`.
3. Replay eight natural/extended source rows exactly with `Fraction`
   arithmetic, transferring the three overlapping parent gains exactly.
4. Record the finite failure of `r>=101/100` and assign zero fixed-power
   credit.

## Route decision

This is a source-level gain-floor attack, not an asymptotic theorem.  The
universal floor is exact, the eight-row source scan is numerically certified,
and the source-level growing lower bound, arithmetic `L2`, full Gate B, and
twin-prime conclusion remain open.
