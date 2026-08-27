# Bridge B: diagonal-deletion attachment ledger

Date: 2026-08-27

TPC-286 follows the TPC-285 residue-rank obstruction.  It defines a
diagonal-including prime-shell output and subtracts the exact diagonal
correction to recover the physical off-diagonal output.  The identity is
proved for every finite declared shell and every linear scalar attachment.
The finite certificate replays all 72 TPC-284 control rows.  All three
component intervals are sign-separated; the full and physical signs flip in
15 rows, the diagonal correction opposes the physical component in 30 rows,
and its certified absolute magnitude is strictly larger in 21 rows.

    TPC286_MAXIMUM_CLAIM = PROVED_EXACT_LINEAR_DIAGONAL_DELETION_ATTACHMENT_SPLIT_PLUS_NUMERICALLY_CERTIFIED_FINITE_DIAGONAL_SENSITIVITY_LEDGER
    TPC286_ROUTE_ADVANCE = YES_SCOPED_EXACT_DIAGONAL_SPLIT_AND_FINITE_SENSITIVITY_LEDGER
    TPC286_ATTACHMENT_SPLIT = PROVED_EXACT_LINEARITY
    TPC286_COMPONENT_SIGN_LEDGER = NUMERICALLY_CERTIFIED_FINITE_72_ROWS
    TPC286_FULL_VS_PHYSICAL_FLIPS = NUMERICALLY_CERTIFIED_FINITE_15_ROWS
    TPC286_DIAGONAL_OPPOSITION = NUMERICALLY_CERTIFIED_FINITE_30_ROWS
    TPC286_DIAGONAL_DOMINANCE = NUMERICALLY_CERTIFIED_FINITE_21_ROWS
    TPC286_ASYMPTOTIC_DIAGONAL_DOMINANCE = OPEN
    TPC286_SIGNED_FULL_SHELL_CANCELLATION = OPEN
    TPC286_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
    TPC286_FIXED_POWER_CREDIT = 0
    TPC286_FULL_GATE_B = OPEN
    TPC286_TWIN_PRIME_RESULT = NONE
    TPC286_STATUS = PROVED_EXACT_LINEAR_DIAGONAL_DELETION_ATTACHMENT_SPLIT_PLUS_NUMERICALLY_CERTIFIED_FINITE_DIAGONAL_SENSITIVITY_LEDGER
    TPC286_ROUND2_CLUE = SEEK_SIGNED_FULL_SHELL_CANCELLATION_AFTER_DIAGONAL_ATTACHMENT_LEDGER

The Session-named evaluator files are absent from this checkout.  The exact
proof package, canonical certificate, independent replay, hostile stress
audit, and this fail-closed checker are the scoped local Route-B fallback.
The finite ledger does not provide asymptotic diagonal dominance or an
arithmetic $L^2$ estimate.
