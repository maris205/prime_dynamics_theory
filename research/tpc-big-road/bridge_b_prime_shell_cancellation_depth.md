# Bridge B: prime-shell cancellation depth

Date: 2026-08-28

TPC-287 is the next map marker after the TPC-286 diagonal-deletion ledger.  It
keeps the literal physical off-diagonal operator fixed, exposes one component
for each prime in a finite shell, and measures the signed shell attachment
against the unsigned component mass.  The exact finite identity is

```text
g_shell = sum_q g_q
C_shell = sum_q C_q
```

The finite certificate uses seven explicitly declared shell anchors with
cardinalities one through seven, six frozen source baselines, and two kernel
exponents.  It contains 84 rows and 336 prime components.  Every component
interval is sign-separated; 57 shell rows have mixed signs; the conservative
retention upper bound is below 1/2, 1/4, and 1/10 in 31, 22, and 8 rows.  The
leave-one-prime-out diagnostic has 48 nonzero sign flips and 12 zero
remainders.

    TPC287_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_SHELL_ADDITIVE_ATTACHMENT_DECOMPOSITION_PLUS_NUMERICALLY_CERTIFIED_FINITE_CANCELLATION_DEPTH_LEDGER
    TPC287_ROUTE_ADVANCE = YES_SCOPED_PRIME_COMPONENT_LEDGER_AND_FINITE_CANCELLATION_DEPTH
    TPC287_SHELL_ADDITIVITY = PROVED_EXACT_FINITE
    TPC287_ATTACHMENT_ADDITIVITY = PROVED_EXACT_FINITE
    TPC287_RETENTION_ENVELOPE = PROVED_CONDITIONAL_INTERVAL
    TPC287_COMPONENT_LEDGER = NUMERICALLY_CERTIFIED_FINITE_336_COMPONENTS
    TPC287_MIXED_SIGN_ROWS = NUMERICALLY_CERTIFIED_FINITE_57_OF_84
    TPC287_RETENTION_THRESHOLDS = NUMERICALLY_CERTIFIED_FINITE_31_22_8
    TPC287_LEAVE_ONE_OUT = NUMERICALLY_CERTIFIED_FINITE_48_FLIPS_12_ZERO
    TPC287_GROWING_SHELL_STABILITY = OPEN
    TPC287_SOURCE_CONTROL_UNIFORMITY = OPEN
    TPC287_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
    TPC287_FIXED_POWER_CREDIT = 0
    TPC287_FULL_GATE_B = OPEN
    TPC287_TWIN_PRIME_RESULT = NONE
    TPC287_STATUS = PROVED_EXACT_FINITE_SHELL_ADDITIVE_ATTACHMENT_DECOMPOSITION_PLUS_NUMERICALLY_CERTIFIED_FINITE_CANCELLATION_DEPTH_LEDGER
    TPC287_ROUND2_CLUE = TEST_CANCELLATION_STABILITY_UNDER_GROWING_SHELL_AND_SOURCE_CONTROLS

## Proof and certificate boundary

The algebraic theorem uses only finiteness of the shell and linearity of the
attachment.  The retention inequality is conditional on valid interval
enclosures and component sign separation.  The 84-row census is a finite
numerical certificate tied to the declared ladder and the frozen TPC-268
source engine.  It is not an asymptotic estimate, a positive-density claim, or
a fixed-power saving.

The producer locks TPC-286 and the frozen TPC-268 engine by normalized-LF
SHA-256 hashes.  The independent replay does not import the producer; it
rebuilds shell primes by trial division and recomputes all components,
intervals, ratios, and leave-one-out fields.  The stress audit rejects nine
mutations.  `tpc_bridge_b_prime_shell_cancellation_depth_checker.py` is
fail-closed: it checks the project manifest, certificate and PDF, then runs
producer, independent, and stress checks in ordinary and optimized Python,
requiring empty stderr and byte-identical paired output.

The Session-named Route-A/Route-B evaluator files are not present in this
checkout.  Accordingly this document records a local fallback status and does
not claim an official evaluator pass.

## Route consequence

The reusable segment is

```text
physical prime shell -> prime components -> signed scalar sum
                     -> interval retention envelope -> leave-one-out map
```

The next test is a growing-shell/source-control stability audit.  If the
finite cancellation disappears under that enlargement, the failure identifies
the missing uniform hypothesis; if it survives, the next paper can attempt a
more rigid theorem rather than silently extrapolating this finite table.
