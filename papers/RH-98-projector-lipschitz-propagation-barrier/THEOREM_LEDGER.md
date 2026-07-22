# RH-98 theorem ledger

## Proved

1. **Endpoint tail/projector Lipschitz theorem:** endpoint tail differences
   are bounded by the endpoint Gram Frobenius norm times projector distance.
2. **Local gap loss-to-projector theorem:** compressed capture loss epsilon and
   Ritz gap gamma imply projector distance at most `sqrt(2 epsilon/gamma)`.
3. **Conditional projector block envelope:** a future projector-Lipschitz
   constant composes the two bounds into an endpoint estimate.
4. **Universal unit-propagation counterexample:** a normalized strictly
   positive two-step projected-cross Ritz system amplifies local tail loss by
   more than 44.4949.

## Validated on production channels

- 38 omissions across cutoffs 1e-8, 1e-6, and 1e-4.
- 38/38 gap-distance, endpoint-Lipschitz, and conditional-envelope gates.
- Maximum tail amplification: 1.0000000000000004.
- Maximum projector secant multiplier: 8.8511197441.

## Not proved

- A neighborhood-uniform production projector-Lipschitz constant.
- A replay-free block envelope or repeated-block theorem.
- Stage-A closure, Hilbert--Polya, zero identification, or RH.
