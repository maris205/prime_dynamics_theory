# TPC-244 computational protocol

All fixtures use `fractions.Fraction` and Gaussian pairs of exact fractions.
Quarter frequencies are synthesized using exact fourth roots of unity.  Bounds
involving complex moduli are compared after squaring, so no floating point or
square-root approximation enters a theorem-facing check.

The producer writes one-line canonical ASCII JSON with sorted keys and a final
newline.  Its digest covers the payload without the digest field.  Check mode
is read-only.  The independent checker does not import the producer and uses a
strict parser rejecting duplicate keys and nonfinite constants.

Normal and optimized Python outputs must be byte-identical.  No theorem gate
uses `assert`.

Finite direct-sum, sign-cut, and hard-window records are
`NUMERICAL_FINITE_ILLUSTRATION_ONLY`; the theorem is symbolic.
