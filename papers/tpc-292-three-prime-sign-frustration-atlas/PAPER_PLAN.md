# TPC-292 paper plan

## Question

TPC-291 gives an optimal signed cancellation direction for one pair of prime
components.  Can the preferred signs for three components be realized
simultaneously, and what is the exact residual of projecting one component
onto the other two?

## Claim spine

1. Encode each nonzero Gram edge by its sign.
2. Prove that all three cross terms can be made nonpositive by coefficient
   signs exactly when the edge-sign product is negative.
3. Derive the three-vector Schur residual
   `det(G_ijk)/(d_i det(G_jk))`.
4. Enumerate every triple in the inherited literal prime shells with exact
   rational arithmetic.
5. Treat the observed frustration ratio as a finite obstruction and expose
   the next problem: signed-graph optimization followed by source-restricted
   reassembly.

## Claim ceiling

The parity and Schur statements are finite-dimensional algebraic facts.  The
atlas is an exact-rational finite certificate.  No growing-shell limit,
source-native coefficient theorem, arithmetic `L2` bound, Gate-B closure, or
twin-prime conclusion is claimed.
