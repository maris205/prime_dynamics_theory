# Bridge B V87: normalized collision-Bessel stability

TPC-233 refutes fixed raw row-mass comparability at critical depth.  Normalize every
nonzero modeled row to unit norm.  TPC-232's one-wrap geometry gives residue-bucket
multiplicity at most two, hence for `Tc=sum_q c_q u_q`,

\[
\|Tc\|^2\le2\sum_q|c_q|^2.
\]

Therefore

\[
0\le G=T^*T\le2I,
\qquad -I\le G-I\le I,
\qquad \|G-I\|\le1.
\]

This repairs depth-dependent conditioning for arbitrary row amplitudes.  The constant
two is sharp in the ambient multiplicity-two class.  It is not a saving theorem:
the literal `Q=39,L=7` rows `67,71` have exact normalized symmetric/antisymmetric
ratios `4/3` and `2/3`.

```text
TPC234_ROUTE_ADVANCE = YES
TPC234_BUCKET_MULTIPLICITY_TWO = INHERITED_PROVED_EXACT
TPC234_UNIT_ROW_NORMALIZATION = MODELING_TRANSFORM
TPC234_NORMALIZED_SYNTHESIS_BESSEL_BOUND = PROVED_EXACT_2
TPC234_NORMALIZED_GRAM_SPECTRUM = PROVED_EXACT_IN_0_2
TPC234_OFFDIAGONAL_GRAM_NORM = PROVED_EXACT_LE_1
TPC234_DEPTH_UNIFORM_CONDITIONING = PROVED_EXACT
TPC234_AMBIENT_CONSTANT_TWO = PROVED_EXACT_SHARP
TPC234_Q39_LITERAL_NORMALIZED_RATIOS = PROVED_EXACT_4_OVER_3_AND_2_OVER_3
TPC234_NORMALIZATION_AUTOMATIC_SAVING = REFUTED_SCOPED
TPC234_SOURCE_VALID_NORMALIZATION = OPEN
TPC234_ACTUAL_V59_CROSSWALK = OPEN
TPC234_ARITHMETIC_ADVANCE = NO
TPC234_ARITHMETIC_CANCELLATION = NONE
TPC234_FIXED_ATOM_CREDIT = 0
TPC234_L2 = NONE
TPC234_FULL_GATE_B = OPEN
TPC234_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC234_STATUS = PROVED_STRUCTURAL_L1
TPC234_ROUND2_CLUE = TRACE_ACTUAL_V59_ROW_WEIGHTS_AND_TEST_SOURCE_VALID_NORMALIZATION
```

Strongest positive result: depth-uniform normalized Bessel bound.  Strongest
obstruction: normalized literal geometry can still amplify.  Open theorem: actual V59
row crosswalk and source-valid normalization.  Reusable structure:
multiplicity-to-Bessel compiler and pointwise residual identity.

The finite package includes five literal scales, an exact Q39 block, abstract sharpness,
and a rejected triple-bucket mutation.  No source attachment, arithmetic cancellation,
`L2`, fixed-atom credit, or full Gate B is claimed.
