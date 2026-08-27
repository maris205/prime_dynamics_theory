# Bridge B: prime-shell residue factorization and rank obstruction

Date: 2026-08-27

TPC-285 follows the TPC-284 control atlas and isolates the local prime-shell
algebra.  For an odd prime `q`, the centered residue block factors exactly
through the nonzero residue indicators and has rank at most `q-2`.  The
physical convention deletes the diagonal; a direct invariant-subspace proof
shows that the resulting active block is full rank whenever all nonzero
residue classes occur.  On all 20 registered prime/exponent rows, the kernel
Schur product is independently certified full active rank modulo
`1000000007`, with all denominators invertible.

    TPC285_MAXIMUM_CLAIM = PROVED_EXACT_CENTERED_RESIDUE_FACTORIZATION_AND_DELETED_DIAGONAL_FULL_RANK_PLUS_NUMERICALLY_CERTIFIED_KERNEL_RANK
    TPC285_ROUTE_ADVANCE = YES_SCOPED_EXACT_RESIDUE_FACTORIZATION_AND_RANK_OBSTRUCTION
    TPC285_RESIDUE_FACTORIZATION = PROVED_EXACT
    TPC285_CENTERED_RANK_BOUND = PROVED_EXACT_RANK_LE_Q_MINUS_2
    TPC285_DELETED_DIAGONAL_FULL_RANK = PROVED_EXACT_UNDER_FULL_CLASS_COVERAGE
    TPC285_KERNEL_SCHUR_FULL_RANK = NUMERICALLY_CERTIFIED_FINITE_20_ROWS
    TPC285_LOW_RANK_TRANSFER = REFUTED_AS_DIRECT_SHORTCUT
    TPC285_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
    TPC285_FIXED_POWER_CREDIT = 0
    TPC285_FULL_GATE_B = OPEN
    TPC285_TWIN_PRIME_RESULT = NONE
    TPC285_STATUS = PROVED_EXACT_CENTERED_RESIDUE_FACTORIZATION_AND_DELETED_DIAGONAL_FULL_RANK_PLUS_NUMERICALLY_CERTIFIED_KERNEL_RANK
    TPC285_ROUND2_CLUE = SEPARATE_RESIDUE_MODE_FACTORIZATION_FROM_DELETED_DIAGONAL_AND_KERNEL_RANK_BEFORE_LITERAL_L2

The Session-named evaluator files are absent from this checkout.  The local
proof package, exact derivation, independent replay, stress audit, and this
fail-closed checker are the scoped Route-B fallback.
