# TPC-257 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T257.1 | Four ordered blocks are nonempty for all sufficiently large clocks | PROVED | real `x` |
| T257.2 | `z0,z1,z2` are source-only and exactly orthonormal | PROVED_EXACT | every admissible finite clock |
| T257.3 | Zero-extended variation is `2/rho_i` | PROVED_EXACT | each contrast |
| T257.4 | Each truncated divisor contrast is `O(U/rho_i)` | PROVED | no Möbius cancellation hypothesis |
| T257.5 | Three second-order PNT curvature constants are positive and explicit | PROVED_SOURCE_BACKED | real `x` asymptotic |
| T257.6 | General bounded-variation adjoint normal form | PROVED_SOURCE_BACKED | literal V59 operator |
| T257.7 | Each frame coefficient has main exponent `7/6` and boundary gap `1/48` | PROVED_SOURCE_BACKED | complex asymptotic |
| T257.8 | Three-mode projected norm floor | PROVED_SOURCE_BACKED | finite projection only |
| T257.9 | Transverse projected norm floor | PROVED_SOURCE_BACKED | `span(z1,z2)` |
| T257.10 | Full vector upper `L2` estimate | NONE | not supplied |
| T257.11 | Full Gate B / strict global `1/400` | OPEN / UNPAID_GLOBAL | not promoted |
| T257.12 | Twin-prime conclusion | NONE | no implication |

## Refuted shortcut

```text
REFUTED_SCOPED: a nonzero midpoint Haar coefficient permits the whole
orthogonal output to be treated as lower order.
```

The refutation is scoped to the literal V59 object and the source-frozen
four-block frame; it is not a universal statement about unrelated operators.
