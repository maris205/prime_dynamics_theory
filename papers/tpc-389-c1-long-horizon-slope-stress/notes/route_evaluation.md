# TPC-389 route evaluation

The Session files `propose.md`, `skills/route-a-evaluator.md`, and
`skills/route-b-evaluator.md` are absent from this checkout.  Applying the
available fail-closed local authority:

```text
ROUTE_A = OPEN
ROUTE_B = OPEN
FINITE_CERTIFICATE = PASS (producer + independent replay + stress)
LONG_HORIZON_PARENT_TRANSFER = FINITE_SCOPED_PASS
RECURSIVE_COMPOSITION = FINITE_SCOPED_PASS
SPECTRAL_CAP = FINITE_OBSTRUCTION (64/256)
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
```

The local Bridge-B checker verifies provenance, certificate semantics, both
replay modes, PDF identity, and the claim firewall.  It is not an official
Route-B evaluator and cannot close the missing arithmetic gates.
