# Bridge B V89: physical multi-wrap collision envelope

For `4Q<H`, `h<=Q`, and prime rows `Q<q<=2Q`, fix a residue `a mod h`, set
`g=gcd(a,h)`, and put `M_h=floor(2hQ/H)`.  Exact gcd-fiber counting gives

\[
R_h(a)\le2\lfloor M_h/g\rfloor\lceil Qg/h\rceil
\le4Q^2/H+4hQ/(gH)\le8Q^2/H.
\]

The first inequality counts possible signed multipliers and then shell integers in one
class modulo `h/g`.  The second uses `h<=Q`.  Pointwise Cauchy therefore yields an
unnormalized fixed-`h` Bessel bound, and summing with explicit `|C_h|^2` yields the same
factor in the orthogonal physical `h`-direct sum.  A common linear packet transform is
legal with its operator norm explicit.

At V59, the sharper source-scale toll is
`4x^(1/96)+4x^(23/2400)=(4+o(1))x^(1/96)`.  The exact V59-shaped floor fixture
`(Q,H,U,h)=(101,8830,99,80)` has rows
`q=113,127,193` all supported on `{17,63}`.  Its multiplicity and equal-row Bessel ratio
are both three, so physical transfer of TPC-234 multiplicity two is refuted.

```text
TPC236_ROUTE_ADVANCE = YES
TPC236_PHYSICAL_ROW_INTERNAL_INJECTIVITY = PROVED_FOR_H_GT_4Q
TPC236_BUCKET_GCD_FIBER_BOUND = PROVED_EXACT
TPC236_BUCKET_MULTIPLICITY = PROVED_LE_8Q_SQUARED_OVER_H
TPC236_WEIGHTED_FIXED_H_BESSEL = PROVED_EXACT_WITHOUT_ROW_NORMALIZATION
TPC236_WEIGHTED_PHYSICAL_H_DIRECT_SUM = PROVED_EXACT
TPC236_COMMON_LINEAR_PACKET_TRANSFORM = PRESERVED_WITH_OPERATOR_NORM
TPC236_DIVISOR_WEIGHT_C_H = PRESERVED_EXPLICITLY
TPC236_V59_MULTIPLICITY_TOLL = PROVED_4X_1_OVER_96_PLUS_4X_23_OVER_2400
TPC236_Q101_TRIPLE_COLLISION = PROVED_EXACT
TPC236_Q101_EQUAL_ROW_RATIO = PROVED_EXACT_3
TPC236_PHYSICAL_MULTIPLICITY_TWO_TRANSFER = REFUTED_SCOPED
TPC236_GCD_FIBER_REDUCTION = REQUIRED
TPC236_CROSS_H_RATIONAL_FREQUENCY_REASSEMBLY = OPEN
TPC236_C_H_WEIGHTED_CANCELLATION = OPEN
TPC236_ARITHMETIC_ADVANCE = NO
TPC236_ARITHMETIC_CANCELLATION = NONE
TPC236_FIXED_ATOM_CREDIT = 0
TPC236_L2 = NONE
TPC236_FULL_GATE_B = OPEN
TPC236_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC236_STATUS = PROVED_STRUCTURAL_L1
TPC236_ROUND2_CLUE = COMBINE_PHYSICAL_H_FIBER_ENVELOPE_WITH_REDUCED_FREQUENCY_LARGE_SIEVE_AND_TEST_C_H_WEIGHTED_CANCELLATION
```

Strongest positive result: source-valid physical-fiber Bessel envelope.  Strongest
obstruction: multiplicity two fails and the surviving loss has exponent `1/96`.  Open
theorem: cross-`h` reduced-frequency reassembly with `C_h`-weighted cancellation.
Reusable structure: gcd-fiber bucket compiler and unnormalized coordinate Bessel step.

No arithmetic saving, `L2`, fixed-atom credit, strict `1/400`, full Gate B, or
twin-prime theorem is claimed.
