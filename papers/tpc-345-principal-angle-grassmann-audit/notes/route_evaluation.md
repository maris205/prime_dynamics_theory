# TPC-345 route evaluation

The Session-named `propose.md`, `skills/route-a-evaluator.md`, and
`skills/route-b-evaluator.md` files are absent in this checkout.  This is
therefore a local fail-closed evaluation and must not be called an official
Route-A or Route-B pass.

`text
ROUTE_A = OPEN
ROUTE_B = FINITE_CERTIFICATE_ONLY
TPC345_FINITE_RESULT = NUMERICALLY_CERTIFIED_FINITE_PRINCIPAL_ANGLE_GRASSMANN_AUDIT
TPC345_EXACT_STRUCTURE = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC345_BASIS_INVARIANCE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC345_WEIGHTING_STABILITY = REFUTED_SCOPED
TPC345_MUTUAL_TRANSFER = REFUTED_SCOPED
TPC345_ARITHMETIC_ADVANCE = NO
TPC345_FIXED_POWER_CREDIT = 0
TPC345_FULL_GATE_B = OPEN
TPC345_TWIN_PRIME_RESULT = NONE
`

Strongest positive: a dominant nuisance direction aligns across the two
panels and a transverse direction remains near orthogonal under all 18
leave-one-control-out angle checks.

Strongest obstruction: the dominant angle changes by `18.5577949387` degrees
under row weighting, and at least one target-transfer direction has residual
retention above `0.30` in both weightings.

Open theorem: a source-uniform arithmetic `L2` estimate or a canonical
weighting-stable nuisance structure.

Reusable structure:

`text
panel-adaptive span -> coordinate-invariant subspaces
                   -> principal angles -> weighting/transfer obstruction
`

`ROUND2_CLUE = FINITE_NO_GO_OR_FREEZE_PANEL_ADAPTIVE_ROUTE`.
