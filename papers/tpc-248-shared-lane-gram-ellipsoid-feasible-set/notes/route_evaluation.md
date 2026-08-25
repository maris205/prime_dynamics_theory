# Route evaluation

Route A remains untouched.  On Route B this is a structural `L1` advance: the
actual TPC-247 shared-lane joint feasible set is now exact, including its rank
defects and group-budget coupling.  It is not arithmetic `L2`.

- strongest positive result: exact shared-lane Gram ellipsoid and sphere/slack law;
- strongest obstruction: marginal disks can overstate the joint set from a diagonal disk to a bidisk;
- open theorem: sharp weighted aggregate radius on the literal grouped probes;
- reusable structure: `V`, `G`, `G^dagger`, minimum preimage, orthogonal slack;
- `ROUND2_CLUE`: `CONTRACT_WEIGHTED_PROBES_INSIDE_EACH_SHARED_OUTPUT_LANE_BEFORE_SUMMING_ACROSS_OUTPUT_BLOCKS`.
