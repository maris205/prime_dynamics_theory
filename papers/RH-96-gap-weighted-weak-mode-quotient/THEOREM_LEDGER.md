# RH-96 theorem ledger

## Proved

1. **Universal omitted-block bound.** The increase in the leading rank-r Ky
   Fan sum after adjoining an omitted positive block is at most
   `2 ||C||_* + trace(D)`.
2. **Gap-weighted weak-mode tail-loss theorem.** If the retained rank-r cutoff
   `alpha` lies above an omitted spectral upper bound `beta`, then the lost
   capture is at most `||C||_F^2 / (alpha - beta)`.
3. **Adaptive relative cutoff rule.** Cross modes are retained according to a
   singular-value ratio, subject to fixed minimum and maximum widths.

## Validated

- 120 primary updates at relative cutoff 1e-8.
- Five width-three updates and 115 width-four updates.
- Five of five omitted losses gap-certified.
- Ten of ten endpoints below 1.01; worst 1.0011723197.
- Largest adaptive/full one-step tail ratio 1.0000046481.

## Negative branch

- Cutoff 1e-6 fails the endpoint gate: worst ratio 1.02492119.
- Cutoff 1e-4 fails the endpoint gate: worst ratio 1.01409152.
- Local loss certificates do not by themselves control recursive cumulative
  loss.

## Not proved

- A uniform retained-to-omitted gap or threshold theorem.
- A horizon composition budget or repeated-block law.
- Stage-A closure, Hilbert--Polya, zero identification, or RH.
