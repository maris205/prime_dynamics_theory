# Bridge B: matched-resonance mass ceiling

For a matching graph, let `D` be total diagonal mass and `M` mass on matched vertices.
Then exact block decomposition gives

```text
E_AP >= D-M,
D-E_AP <= M.
```

The ceiling is sharp under perfect anti-alignment. Hence a `delta` saving requires
`M/D>=delta`. If row-mass ratio is at most `kappa`, with `P` rows and `E` edges,

```text
M/D <= 2 kappa E/P,
E/P >= delta/(2 kappa) is necessary.
```

Literal aligned dilation-four rows have between two and eight primitive atoms, so
`kappa<=4`; strict `1/400` saving requires `E/P>=1/3200`.

```text
TPC230_ROUTE_ADVANCE = YES
TPC230_UNMATCHED_ENERGY_FLOOR = PROVED_EXACT
TPC230_MATCHED_MASS_SAVING_CEILING = PROVED_EXACT_SHARP
TPC230_NECESSARY_MASS_FRACTION = PROVED_EXACT
TPC230_COMPARABLE_ROW_DENSITY_TOLL = PROVED_EXACT
TPC230_LITERAL_ALIGNED_KAPPA_LE_4 = PROVED_EXACT
TPC230_STRICT_1_OVER_400_EDGE_DENSITY_TOLL = 1/3200
TPC230_ASYMPTOTIC_RESONANCE_EDGE_DENSITY = OPEN
TPC230_ACTUAL_V59_SOURCE_MASS_COMPARABILITY = OPEN
TPC230_ARITHMETIC_ADVANCE = NO
TPC230_FIXED_ATOM_CREDIT = 0
TPC230_L2 = NONE
TPC230_FULL_GATE_B = OPEN
TPC230_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC230_STATUS = PROVED_STRUCTURAL_L1
TPC230_ROUND2_CLUE = APPLY_A_TWO_LINEAR_FORM_UPPER_BOUND_SIEVE_TO_THE_3_7_RESONANCE_COUNT
```

Strongest positive result: sharp global capacity ceiling and explicit endpoint density
toll. Strongest obstruction: unmatched mass is untouchable. Open theorem: asymptotic
two-linear-form resonance density and actual source comparability. Reusable structure:
matched/unmatched mass ledger.
