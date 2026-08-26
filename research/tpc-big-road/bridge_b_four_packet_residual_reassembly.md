# Bridge B V113: null-compatible four-packet residual reassembly

Date: 2026-08-26

Status: `PROVED_STRUCTURAL_NULL_COMPATIBLE_FOUR_PACKET_COMPLETION_OBSTRUCTION`

TPC-260 is the direct continuation of TPC-259.  It keeps the source-frozen
transverse null direction and asks whether packet marginals plus the existing
Haar projections can determine the orthogonal signed residual.

## 1. Four-block complement

For positive block lengths `s_0,...,s_3`, the three TPC-257 contrasts
`z_0,z_1,z_2` are exactly orthonormal under the block-counting inner product.
Their weighted sums vanish, so the normalized scaling vector

`e_sc = 1/sqrt(s_0+s_1+s_2+s_3)`

is the fourth orthonormal Haar mode.  Since

`z_null=(L2 z1-L1 z2)/sqrt(L1^2+L2^2),
L1=log(3456/3125), L2=log(884736/823543),`

the source-frozen TPC-258 null direction is also orthogonal to `e_sc`.

## 2. New completion theorem

Let `z,w` be orthonormal and take four packets
`V_j=d_j exp(i theta_j)w`.  Then `<z,sum_j V_j>=0` for every phase choice.
Writing

`D=sum_j d_j, d_max=max_j d_j,
R=<w,sum_j V_j>,`

the possible residual moduli are exactly

`max(2*d_max-D,0) <= |R| <= D.`

For `d_j=1`, the residual energy fills `[0,16]`.  In the four-block realization
take `z=z_null` and `w=e_sc`; every packet has zero projection on all three
Haar contrasts and the TPC-259 null coefficient `<z,w>` is zero.

## 3. Missing mode

The packet DFT

`Vhat_k=1/2 sum_(j=0)^3 i^(-jk)V_j`

obeys

`sum_k ||Vhat_k||^2=sum_j||V_j||^2,
sum_j V_j=2 Vhat_0,
||sum_j V_j||^2=4||Vhat_0||^2.`

The plus family `V_j=w` has mode energies __(4,0,0,0)` and full energy `16`;
the alternating family `V_j=(-1)^j w` has mode energies __(0,0,4,0)` and full
energy `0`.  Both have diagonal __(1,1,1,1)`, total packet energy `4`, zero
Haar projections, and zero null channel.

This is stronger and more specific than the generic TPC-222 diagonal/trace
fixture: it embeds the source-frozen null direction in the actual four-block
Haar complement and gives a sharp completion interval rather than two isolated
Gram matrices.

## 4. Claim firewall

`TPC260_MAXIMUM_CLAIM = PROVED_STRUCTURAL_NULL_COMPATIBLE_FOUR_PACKET_COMPLETION_OBSTRUCTION
TPC260_ROUTE_ADVANCE = YES_SCOPED_MODE_AUDIT
TPC260_HAAR_COMPLEMENT = PROVED_EXACT_FINITE
TPC260_POLYGON_COMPLETION = PROVED_EXACT_FINITE
TPC260_DFT_MODE_LEDGER = PROVED_EXACT
TPC260_NULL_CHANNEL_COMPATIBILITY = PROVED_EXACT_SYNTHETIC
TPC260_FULL_RESIDUAL_IDENTIFIABILITY = REFUTED_SCOPED
TPC260_LITERAL_PRIME_SHELL_COUNTEREXAMPLE = NONE
TPC260_ARITHMETIC_ADVANCE = NO
TPC260_FIXED_ATOM_CREDIT = 0
TPC260_L2 = NONE
TPC260_FULL_GATE_B = OPEN
TPC260_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC260_TWIN_PRIME_RESULT = NONE
TPC260_STATUS = PROVED_STRUCTURAL_NULL_COMPATIBLE_FOUR_PACKET_COMPLETION_OBSTRUCTION`

Strongest positive result: a sharp null-compatible polygon completion and an
exact mode-zero DFT ledger.

Strongest obstruction: fixed packet marginals and all existing Haar/null
projections permit residual energies `0` and `16`.

Open theorem: estimate the literal common-clock mode-zero or signed cross-Gram
sum with the hard window, deleted diagonal, unit masks, and boundary lanes
retained.

Reusable structure:

`four-block Haar complement -> null-compatible completion
-> DFT mode ledger -> residual identifiability firewall`

`ROUND2_CLUE = PROVE_A_LITERAL_MODE_ZERO_OR_CROSS_GRAM_ESTIMATE_FOR_THE_COMMON_V59_FOUR_PACKET_OUTPUT`

The named Session Route-A/Route-B evaluator files are absent from this checkout.
The project proof package, theorem ledger, certificate, bridge checker, and
`AGENTS.md` are the available fail-closed local authority.
