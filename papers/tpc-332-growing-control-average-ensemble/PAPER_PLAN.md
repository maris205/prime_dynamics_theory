# TPC-332 paper plan

## Research question

Does the exact five-control mean/centered response split observed by TPC-331
survive a disjoint growing source ensemble, and what happens to the separate
source-native `L2` quantities on the same windows?

## Frozen design

- Parent: TPC-331 producer and certificate, both hash-locked.
- Origins: `42001, 44001`, disjoint from the parent windows.
- Scales: `2048, 4096, 8192`, giving source counts `1024, 2048, 4096`.
- Shells: `Q={24,36,54,80}`; kernel powers `{1,2}`; `H=66`.
- Four inherited shell laws and five inherited bijective coordinate controls.
- V59 finite Euler/log enclosure, tail cutoff `50000`, ratio guard `5e-8`.

## Work packages

1. Rebuild the literal shell matrices and declared source on all 48 rows.
2. Recompute the control-average, coherent, and centered `E/D/O` triples.
3. Add the finite source polarization ledger for `Lambda`, `b`, and
   `beta=Lambda-b`.
4. Pair adjacent source scales at each origin and report finite energy factors
   and base-2 slopes without calling them asymptotic exponents.
5. Recompute the exact rational 16-point anchor at the second fresh origin.
6. Use an independent reverse-order implementation and a mutation stress suite.

## Predeclared interpretation rules

- A resolved sign is read only from the outward interval with guard `5e-8`.
- An unresolved ratio is retained as unresolved; it is never rounded into a sign.
- A positive component census is a finite observation, not a source-uniform
  estimate.
- Source `L2` identities are algebraic; scale slopes are descriptive only.
- No result receives fixed-power credit unless a named Route evaluator pays it.

## Decision rule for the next paper

- If the source polarization cross term is stable, isolate it as a standalone
  arithmetic object and quantify its cancellation coefficient.
- If the cross term is dominated by broad odd/composite support, split its
  prime-power and twin-prime portions before sending it back through the
  operator.
- If either component becomes unstable, record the obstruction and test the
  smallest source/operator-compatible null or control family.
