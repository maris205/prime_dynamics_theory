# TPC-244 paper plan

## Question

After TPC-243 transports coefficient covariance to the hard window, can the
outer sign of the literal clustered coefficient `C_h` supply the signed main
term needed by the four-packet channel?

## Claim sequence

1. Prove common-unit-phase invariance in an orthogonal block direct sum.
2. Expand a general nonorthogonal reassembly into diagonal and cross-block
   terms.
3. For real sign flips, identify the exact graph-cut polynomial and prove its
   all-sign invariance criterion by Walsh orthogonality.
4. Attach the direct-sum theorem conditionally to TPC-243 and bound physical
   sign-pattern variation by `2 epsilon ||W|| ||B||`.
5. Audit the V59 source chain and stop at the missing literal two-lane
   primitive coefficient map.

## Contribution

The paper proves a structural obstruction rather than an arithmetic saving:
the same aggregated multiplier on both lanes contributes `|C_h|^2`, so its
outer sign cannot control the same-bucket main covariance.  All possible outer
sign sensitivity is localized to cross-block leakage or asymmetric lane
attachment.

## Claim ceiling

```text
PROVED_STRUCTURAL_L1_COMMON_MULTIPLIER_SIGN_LOCALIZATION
CONDITIONAL_ON_LITERAL_V59_PHASEWISE_PRIMITIVE_TWO_LANE_ATTACHMENT
ARITHMETIC_ADVANCE = NO
```
