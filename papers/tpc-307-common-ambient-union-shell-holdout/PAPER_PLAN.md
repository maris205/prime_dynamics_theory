# TPC-307 paper plan

## Question

TPC-306 exposed an operator/target interaction, but its two operator rows
were still supported on different prime shells and the off-overlap target
completion was row-specific.  Can the adjacent shells be placed in one
common ambient row space, fit only on their overlap, and use the exclusive
pieces as a genuine finite holdout diagnostic?

## Minimal contribution

1. Define the union shell `U`, overlap `O`, and disjoint exclusive pieces
   `E_left` and `E_right` for every adjacent pair.
2. Prove that a single union target is not implied by two transported label
   vectors; instead define two directional targets on `O`, each tested on its
   own withheld exclusive piece.
3. Prove the finite partition, global-sign, nested-prefix, and holdout
   separation lemmas.
4. Replay the locked `(N,H,z)=(512,58,5)` spine at two exponents, three
   tolerances, and three source normalizers: 18 cases, 36 directional fits,
   and 54 normalizer rows.
5. Locate the first finite budget/holdout discordance without assigning it a
   causal interpretation.

## Acceptance criteria

- TPC-305/TPC-306 code and result hashes are locked;
- the producer and an independent checker agree on all 18 cases;
- the stress suite tests partition disjointness, sign invariance, nested
  prefix feasibility, and the class truth table;
- the finite replay records 13 concordant, 3 discordant, and 2 unresolved
  cases, with all three discordances at `Q=70 -> 90`, exponent 1;
- the PDF, source, result hash, and Bridge-B checker are reproducible;
- the claim ceiling remains finite and diagnostic: no causal, asymptotic,
  arithmetic `L2`, fixed-power, full Gate-B, or twin-prime claim.

## Next trigger

The three discordances are a targeted stress point.  The next paper should
test whether they survive alternative off-overlap completion envelopes and
small profile-prefix perturbations before any preference language is reused.
