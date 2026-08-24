# Bridge B V88: V59 physical-depth crosswalk

For a physical V59 denominator `h`, define

\[
\lambda_h=hQ/H.
\]

The source row is exactly

\[
B_{h,q}(a)=\sum_{0<|m|\le\lfloor\lambda_hq/Q\rfloor}
\psi(mQ/(\lambda_hq))\mathbf1_{mq^{-1}=a\ (h)}.
\]

Its modulus remains `h=(H/Q)lambda_h`.  Exact attachment to the TPC-226 row requires
both `h=4LQ` and `H=4Q^2`.  V59 instead has

\[
4Q^2/H=4x^{1/96},
\]

so the one-clock attachment fails by a growing factor.  The actual depth range is
`1/2<=lambda_h<=x^(23/2400)`, with `x^(31/96)` available integer-denominator grid
points per unit depth; this does not count the nonzero support of `C_h`.

TPC-234 output normalization also cannot be inserted packetwise: every normalized
packet has squared norm one, so its four-phase signed sum is zero.  The raw scalar
fixture `beta=1,w=2` has target two and normalized value zero.

```text
TPC235_ROUTE_ADVANCE = YES
TPC235_V59_PHYSICAL_DEPTH_VARIABLE = PROVED_EXACT_LAMBDA_H_EQ_HQ_OVER_H
TPC235_PHYSICAL_ROW_REPARAMETERIZATION = PROVED_EXACT
TPC235_SINGLE_CLOCK_COMPATIBILITY_IFF_H_EQ_4Q_SQUARED = PROVED_EXACT
TPC235_V59_CLOCK_RATIO = PROVED_EXACT_4X_TO_1_OVER_96
TPC235_TPC226_EXACT_SINGLE_CLOCK_ATTACHMENT = REFUTED_SCOPED
TPC235_PHYSICAL_DEPTH_RANGE = PROVED_EXACT_HALF_TO_X_23_OVER_2400
TPC235_PHYSICAL_DENOMINATOR_GRID_PER_DEPTH = PROVED_X_31_OVER_96
TPC235_DIVISOR_WEIGHT_C_H = SOURCE_LOCKED_REQUIRED
TPC235_FULL_H_SUM = SOURCE_LOCKED_REQUIRED
TPC235_COMMON_PACKET_TRANSFORM = SOURCE_LOCKED_REQUIRED
TPC235_OUTPUT_UNIT_NORMALIZATION_POLARIZATION = REFUTED_SCOPED
TPC235_SOURCE_VALID_NORMALIZATION = OPEN_WEIGHTED_LINEAR_ONLY
TPC235_ARITHMETIC_ADVANCE = NO
TPC235_ARITHMETIC_CANCELLATION = NONE
TPC235_FIXED_ATOM_CREDIT = 0
TPC235_L2 = NONE
TPC235_FULL_GATE_B = OPEN
TPC235_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC235_STATUS = PROVED_STRUCTURAL_L1
TPC235_ROUND2_CLUE = BUILD_PHYSICAL_H_FIBER_DIRECT_SUM_WITH_COMMON_PACKET_TRANSFORM_AND_EXPLICIT_WEIGHTS
```

Strongest positive result: exact physical-depth row and compatibility iff theorem.
Strongest obstruction: single-clock mismatch and packet-output normalization erase the
source polarization.  Open theorem: weighted physical `h`-fiber direct sum with a
common packet transform.  Reusable structure: clock/cutoff/profile compatibility
triangle and packet normalization firewall.

No arithmetic saving, `L2`, fixed-atom credit, strict `1/400`, or full Gate B is
claimed.
