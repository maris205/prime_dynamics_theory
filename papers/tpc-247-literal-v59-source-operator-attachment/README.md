# TPC-247: Literal V59 Source-Operator Two-Lane Block Attachment

Status: `PROVED_STRUCTURAL_L1_LITERAL_V59_SOURCE_OPERATOR_ATTACHMENT_WITH_NORM_OBSTRUCTION`

TPC-247 writes the exact V59 Gate-B scalar on the literal physical index
space as

```text
C_x=<w,A_x beta>
```

and proves an exactly-once hard block decomposition

```text
C_x=sum_(b,c)<w_c,A_cb beta_b>.
```

Putting these terms in tagged external copies gives a genuine two-lane
covariance identity.  It also exposes the first exact payment obstruction:
the same output lane is copied once per input block, so
`||W_ext||^2=m||w||^2`, while the separated `B`-lane norm need not equal
`||A_x beta||`.  Thus the source-index attachment is exact but is not yet the
primitive-frequency, norm-payable attachment required by TPC-243--TPC-246.

## Main files

- `PROOF_PACKAGE.md`: theorem, proof, boundary cases and counterexamples.
- `DERIVATION_PACKAGE.md`: source lock and invariant-object derivation.
- `paper/paper.pdf`: complete five-section manuscript.
- `code/tpc247_source_operator_certificate.py`: exact-rational producer/checker.
- `experiments/tpc247_independent_checker.py`: independent replay and mutation audit.
- `experiments/tpc247_source_operator_stress.py`: partition and orientation stress tests.
- `results/tpc247_certificate.json`: canonical certificate.

## Claim firewall

```text
TPC247_LITERAL_V59_SOURCE_INDEX_OPERATOR = PROVED_EXACT
TPC247_HARD_SUPPORT_BLOCK_DECOMPOSITION = PROVED_EXACT
TPC247_ADMISSIBLE_TRIPLE_EXACTLY_ONCE = PROVED_EXACT
TPC247_TAGGED_EXTERNAL_TWO_LANE_COVARIANCE = PROVED_EXACT
TPC247_W_LANE_NORM_INFLATION = PROVED_EXACT_SQRT_BLOCK_COUNT
TPC247_B_LANE_NORM_PRESERVATION = REFUTED_SCOPED
TPC247_PRIMITIVE_FREQUENCY_ATTACHMENT = OPEN
TPC247_TPC243_NEAR_ISOMETRY_ATTACHMENT = OPEN
TPC247_ARITHMETIC_ADVANCE = NO
TPC247_L2 = NONE
TPC247_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC247_TWIN_PRIME_RESULT = NONE
```

Strongest positive result: exact literal V59 source-operator and tagged
two-lane covariance attachment.  Strongest obstruction: exact external-copy
norm inflation and loss of cross-input-block cancellation.  Open theorem:
characterize the shared-output-lane joint feasible set.  Reusable structure:
physical kernel, hard support projections, tagged covariance and explicit loss
ledger.

`ROUND2_CLUE = CHARACTERIZE_THE_SHARED_OUTPUT_LANE_JOINT_FEASIBLE_SET_BEFORE_ANY_CARTESIAN_PRODUCT_PROMOTION`
