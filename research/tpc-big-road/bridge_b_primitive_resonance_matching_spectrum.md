# Bridge B: primitive 3--7 resonance matching and spectrum

For every edge `p<r` with `7p+3r=16Q`,

```text
10Q/7 < p < 8Q/5 < r < 2Q.
```

The endpoint intervals are disjoint and each endpoint uniquely determines its partner;
therefore the graph is a matching for every `Q>=8`.

Each edge has two shared coordinates and swap block

```text
J=[[0,I2],[I2,0]], spectrum=(-1,-1,+1,+1).
```

For symmetric row vectors, with `E_sym=||u+v||^2/2` and
`E_anti=||u-v||^2/2`,

```text
E_diag=E_sym+E_anti
E_collision=E_sym-E_anti
E_AP=2E_sym
0<=E_AP/E_diag<=2
E_AP<=(1-delta)E_diag iff (1+delta)E_sym<=(1-delta)E_anti.
```

The TPC-228 source block obeys the sharp half-source-mass bound. The `Q=8..4096`
replay checks 4089 scales, 13,754 edges and maximum degree one.

```text
TPC229_ROUTE_ADVANCE = YES
TPC229_RESONANCE_GRAPH_MATCHING = PROVED_EXACT
TPC229_LOW_HIGH_ENDPOINT_SEPARATION = PROVED_EXACT
TPC229_EDGE_SPECTRUM = PROVED_EXACT
TPC229_GLOBAL_BLOCK_DIRECT_SUM = PROVED_EXACT
TPC229_SHARP_AP_RATIO_RANGE = PROVED_EXACT
TPC229_DELTA_SAVING_CRITERION = PROVED_EXACT
TPC229_SOURCE_BILINEAR_BLOCK_BOUND = PROVED_EXACT_SHARP
TPC229_ARITHMETIC_ANTISYMMETRIC_DOMINANCE = OPEN
TPC229_ACTUAL_V59_ATOM_CROSSWALK = OPEN
TPC229_ARITHMETIC_ADVANCE = NO
TPC229_FIXED_ATOM_CREDIT = 0
TPC229_L2 = NONE
TPC229_FULL_GATE_B = OPEN
TPC229_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC229_STATUS = PROVED_STRUCTURAL_L1
TPC229_ROUND2_CLUE = QUANTIFY_MATCHED_RESONANCE_MASS_BEFORE_SEEKING_A_FIXED_PROPORTIONAL_SAVING
```

Strongest positive result: global graph complexity collapses to sharp independent edge
blocks. Strongest obstruction: geometry supplies neither antisymmetric source dominance
nor matched mass. Open theorem: quantify matched source mass and its sign. Reusable
structure: endpoint separation, matching, and symmetric/antisymmetric block ledger.
