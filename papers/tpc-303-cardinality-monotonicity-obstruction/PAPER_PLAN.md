# TPC-303 paper plan

## Question

Does increasing prime-shell cardinality force the native weighted source budget
to increase along a fixed source-scale spine?

## Design

Use TPC-302's frozen common-prefix weighted budgets on
`(N,H,z)=(512,58,5)`, `Q=(50,60,70,90)`.  Repeat for both kernel exponents,
three relative RMS tolerances, and three source normalizers.  Compare published
outward intervals rather than rounded centers.

## Decision rule

An interval-separated descent is a finite counterexample to monotonicity on the
declared spine.  A same-prefix descent is recorded separately because it rules
out a profile-dimension explanation.  No finite descent is promoted to an
asymptotic refutation.

## Follow-on

Transport labels across overlapping shells and decompose the budget change into
target-label switching versus physical-shell/operator change.
