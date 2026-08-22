# TPC-224 paper plan

## Research question

Can the prime-AP/collision channel and the four-packet polarized channel be
defined on one literal coefficient family, with one normalization and one
clock, so that their full reassembly has a proved structural interface?

## One-sentence contribution

For a common family of literal vectors `W_(q,j)`, the full reassembly obeys the
sharp identity-compatible envelope
`E_all <= min(J E_AP, P E_pol) <= PJ/(P+J)(E_AP+E_pol)`, while the unit-constant
version is refuted by a growing congruence-aligned prime-shell stress family.

## Claims and evidence

| Claim | Evidence | Status |
|---|---|---|
| The AP and polarized channels are restrictions of one common Hilbert family | Theorem 1 and the shared `W_(q,j)(h,a)` construction | `PROVED_STRUCTURAL_L1` |
| Full reassembly is bounded by the two marginal channels | Cauchy plus the exact min-to-sum inequality | `PROVED` |
| The constant `PJ/(P+J)` is sharp | Aligned-vector theorem and exact literal stress records | `PROVED_EXACT` / `NUMERICALLY_CERTIFIED` |
| A unit structural constant is not valid in general | `H=5Q`, `h=5`, `q=1 (mod 5)` stress records | `REFUTED_SCOPED` |
| The two arithmetic savings exist on the source-locked growing shell | No source theorem supplied | `OPEN` |
| TPC-223's exponent compiler is instantiated unconditionally | Marginal estimates remain absent | `OPEN` |

## Experimental design

1. `source_surrogate`: actual primes in `(Q,2Q]`, `x=Q^3`, `H=4Q^2`,
   `h=4Q`, affine four-packet profiles; nine increasing values of `Q`.
2. `collision_stress`: actual primes congruent to `1 mod 5`, `x=Q^3`,
   `H=5Q`, `h=5`, constant profiles; five increasing values of `Q`.
3. All vectors use the same exact coefficient normalization `C_h=1/h`.
4. The two clocks are recorded separately and are never combined into an
   asymptotic claim.

## Claim ceiling

The paper proves a finite/common-Hilbert structural theorem and a scoped
adversarial obstruction. It does not prove prime dispersion, polarized
cross-correlation, an `L2` estimate, fixed-atom credit, or the twin-prime
conjecture.
