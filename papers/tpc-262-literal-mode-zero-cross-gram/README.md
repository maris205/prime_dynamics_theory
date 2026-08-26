# TPC-262: Literal Signed Reduced-Residue Operator and Phase-Character Firewall

Author: Liang Wang
Affiliation: School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

Status:

```text
PROVED_EXACT_LITERAL_SIGNED_REDUCED_RESIDUE_OPERATOR_AND_PHASE_CHARACTER_FIREWALL
```

TPC-262 is the first follow-up to TPC-261's exact `1/400` budget. It freezes
the actual reduced-residue signed operator at a fixed additive phase. For a
prime `q`, with literal residue synthesis `S_(q,v)` and unit mask `P_q`, the
exact remainder operator is

```text
J_(q,v)=S_(q,v)^* C_q S_(q,v) - ((q-2)/(q-1)) P_q.
```

At the finite certificate phase `v=0`, this includes the deleted diagonal and
the outer prime weight; it is not merely a positive variance. The underlying
unit-class projection is:

```text
C_q=I_(q-1)-(q-1)^(-1)11^T,
Q={5,7,11,13}.
```

The centered matrices are exact projections. For four literal packet outputs
`Y_j`, the full mode-zero energy is exactly

```text
D+2 Re(sum_(j<k) Gamma_jk),
Gamma_jk=<<Y_j,Y_k>>,
```

and equivalently `4||Yhat_0||^2`. This turns the missing theorem into one
signed cross-Gram estimate, with the strict endpoint requirement inherited
from TPC-261: effective saving `>1/400` after all losses.

The finite operator-image certificate uses actual prime unit-class matrices to
show that equal packet diagonals and PSD constraints alone allow both
`16||Y||^2` and `0` mode-zero energy. It is a literal finite-fiber
structural obstruction, not a growing-shell counterexample and not an estimate
for the actual `beta,w` packets.

## Claim firewall

```text
TPC262_MAXIMUM_CLAIM = PROVED_EXACT_LITERAL_SIGNED_REDUCED_RESIDUE_OPERATOR_AND_PHASE_CHARACTER_FIREWALL
TPC262_ROUTE_ADVANCE = YES_SCOPED_LITERAL_SIGNED_OPERATOR_INTERFACE
TPC262_UNIT_CLASS_PROJECTION = PROVED_EXACT_FINITE
TPC262_CROSS_GRAM_IDENTITY = PROVED_EXACT
TPC262_SIGNED_REMAINDER_OPERATOR = PROVED_EXACT_FINITE_X
TPC262_DELETED_DIAGONAL = PROVED_EXACT_Q_MINUS_2
TPC262_ENDPOINT_THRESHOLD = PROVED_EXACT_ONE_OVER_400
TPC262_OPERATOR_IMAGE_WITNESS = NUMERICALLY_CERTIFIED_STRUCTURAL
TPC262_PHASE_CHARACTER_SEPARATION = PROVED_EXACT
TPC262_POLARIZED_V59_CHARACTER = OPEN
TPC262_GROWING_SHELL_COUNTEREXAMPLE = NONE
TPC262_ARITHMETIC_ADVANCE = NO
TPC262_FIXED_ATOM_CREDIT = 0
TPC262_L2 = NONE
TPC262_FULL_GATE_B = OPEN
TPC262_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC262_TWIN_PRIME_RESULT = NONE
TPC262_LITERAL_BETA_W_CROSS_GRAM = OPEN
TPC262_STATUS = PROVED_EXACT_LITERAL_SIGNED_REDUCED_RESIDUE_OPERATOR_AND_PHASE_CHARACTER_FIREWALL
```

Strongest positive result: the literal signed reduced-residue remainder
operator, its deleted diagonal, and its phase-character typing are exact at
finite x, with prime weights and unit masks retained. Strongest obstruction:
the same literal finite operator image admits aligned and alternating packet
endpoints, so diagonal/PSD information cannot pay the endpoint. Open theorem:
identify and estimate the correct growing-shell character of the actual V59
beta,w packets with effective credit above `1/400`.

```text
ROUND2_CLUE = CENSUS_THE_LITERAL_GROWING_PRIME_SHELL_CROSS_GRAM_BEFORE_PROPOSING_ANY_SIGNED_REASSEMBLY_ESTIMATE
```

The finite certificate proves algebra and provenance only. It does not sample
or estimate a growing prime shell.
