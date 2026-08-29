# TPC-303 proof package

## Proposition 1 - interval order

If (x\in[L_x,U_x]), (y\in[L_y,U_y]), and (U_y<L_x), then (y<x).
Likewise (L_y>U_x) implies (y>x).  This is immediate from the definition
of an interval and is the exact certificate used for every transition.

## Proposition 2 - scoped finite refutation

Let (B(Q)) be the represented budget on the declared finite Q-spine.  If one
adjacent pair satisfies (B(Q_{j+1})<B(Q_j)), then (B) is not
nondecreasing on that spine.  The conclusion is purely finite and makes no
claim about an eventual asymptotic sequence.

## Proposition 3 - same-prefix firewall

If the two budgets use the same profile prefix index (k), their source
profile space and all three row/prefix normalizers are held at the same
declared prefix.  A certified budget descent in such a pair therefore cannot
be explained by a change in the number of available profiles.  It may still
come from the moving physical shell or from the source-first target label.

## Numerical status

The parent TPC-302 intervals are frozen by SHA-256.  Recomputing their order
gives 21 certified descents, 33 certified ascents, and no interval overlap over
54 transitions.  This is a finite obstruction, not arithmetic (L^2) evidence.
