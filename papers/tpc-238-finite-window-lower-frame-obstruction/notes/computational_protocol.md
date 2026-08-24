# Computational Protocol

## Purpose

The code checks finite algebra and numerical matrix consequences. It does not
replace the analytic proof.

## Fixture

- \(U=4\)
- \(N=41\)
- \(L=21\)
- all six primitive fractions of height at most \(4\)
- shifted intervals starting at \(-20,0,17,103\)

The exact minimum circular spacing is \(1/12\), which is stronger than the
theorem floor \(1/16\).

## Classification

- Primitive-fraction enumeration, spacing, triangular support, and weight sum:
  **EXACT_THEOREM_LEDGER**
- Floating-point Gram eigenvalues and Fejér samples:
  **NUMERICALLY_CERTIFIED_FINITE_CHECK**
- Observed gaps between actual eigenvalues and theorem constants:
  **NUMERICAL_OBSERVATION**

No finite computation is labeled as a proof of the general theorem.

## Independence

The independent checker does not import the producer. It reconstructs the
fixture, recomputes the certificate digest, rebuilds Gram matrices, and runs
mutations through its own validation logic.

## Determinism

Every script prints canonical JSON with sorted keys. No validation relies on
Python assert statements, so optimized mode follows the same path as normal
mode. Tests compare stdout bytes across both modes.
