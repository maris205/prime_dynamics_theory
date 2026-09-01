# TPC-323 route evaluation

The Session-named `propose.md`, `skills/route-a-evaluator.md`, and
`skills/route-b-evaluator.md` are absent from this checkout.  Therefore no
official Route-A or Route-B pass is asserted.

Available fail-closed evidence:

1. exact trace/profile factorisation in `PROOF_PACKAGE.md`;
2. producer certificate with parent lock to TPC-322;
3. independent reverse/einsum replay;
4. deterministic profile stress suite;
5. local Bridge-B checker, including normal/optimized subprocess equality and
   sealed source/PDF hashes.

Local route label:

```text
ROUTE_B_LOCAL = YES_SCOPED_FINITE_SIGNED_PROFILE_READOUT
ARITHMETIC_ROUTE_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
```
