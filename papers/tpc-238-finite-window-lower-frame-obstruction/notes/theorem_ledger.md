# TPC-238 Theorem Ledger

## Exact theorem

For \(N\geq1\), \(L=\lfloor(N+1)/2\rfloor\), and distinct primitive rational
frequencies of height at most \(U\),

\[
E_I(z)\geq
\left[L-\frac{\pi^2U^4}{12L}\right]_+\|z\|_2^2.
\]

Status: **PROVED**

## Exact normalized corollary

\[
\frac{E_I(z)}N\geq
\left[\frac12-\frac{\pi^2U^4}{6N^2}\right]_+\|z\|_2^2.
\]

Status: **PROVED**

## V59 specialization

\[
U=x^{133/400},\qquad N\asymp x,\qquad
\frac{U^4}{N^2}=x^{-67/100+o(1)}.
\]

Status: **PROVED**

## Structural conclusion

After \(q\)-collapse, distinct reduced-frequency interference cannot produce a
fixed-power saving relative to the collapsed coefficient energy at V59.

Status: **PROVED_STRUCTURAL_OBSTRUCTION_L1**

## Gate ledger

| Item | State |
|---|---|
| TPC238_ROUTE_ADVANCE | YES |
| ARITHMETIC_ADVANCE | NO |
| C_H_SIGNED_CANCELLATION | NONE |
| L2 | NONE |
| FULL_GATE_B | OPEN |
| STRICT_1_OVER_400 | UNPAID_GLOBAL |
| FIXED_ATOM | 0 |
| Route A A0 | FALSE |
| Route A A1 | FALSE |
| Route A A2 | FALSE |
| Route A A3 | FALSE |
| Route A A4 | FALSE |
| constant sharpness | NOT_CLAIMED |

## Strongest positive

An explicit, uniform finite-window lower frame with defect
\(\pi^2U^4/(12L)\).

## Strongest obstruction

At V59 the normalized lower-frame constant tends to \(1/2\), excluding any
\(x^{-\eta}\) gain that is attributed only to cancellation between distinct
collapsed frequencies.

## Open theorem

Prove a fixed-power upper bound for the literal \(C_h\)-weighted
same-frequency \(q\)-collision energy before reduced-frequency reassembly.

## Reusable structure

Translated triangular minorant, exact Fejér transform, primitive Farey
spacing, circular inverse-square packing, and Schur/Gershgorin.

## ROUND2 clue

    MOVE_THE_POWER_SAVING_SEARCH_INSIDE_THE_LITERAL_C_H_WEIGHTED_Q_COLLISION_BUCKETS
