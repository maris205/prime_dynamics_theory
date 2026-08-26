# TPC-259: Same-Clock Null-Channel Coupling

Author: Liang Wang
Affiliation: School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

Status:

```text
PROVED_SOURCE_BACKED_SAME_CLOCK_NULL_CHANNEL_SUPPRESSION_FOR_LITERAL_V59_SIGNED_COUPLING
```

TPC-259 follows the TPC-258 `ROUND2_CLUE`.  On the same literal V59 clock, use
the source-frozen transverse null vector `z_null` and the literal hybrid
residual `w`.  TPC-254's maximal-interval theorem applies to each of the four
consecutive source blocks, so for every fixed `M,K`

```text
|<z_null,w>| <<_(M,K) sqrt(x)/(log x)^M.
```

The exact Hilbert decomposition of the signed scalar is

```text
<w,A_x beta>
 =conjugate(<z_null,w>)<z_null,A_x beta>
  +<w_perp,A_x beta>.
```

Combining the new `w` estimate with TPC-258's
`<z_null,A_x beta>=o(x^(7/6)/log^3 x)` proves that the first, explicitly
identified rank-one channel is

```text
o(x^(5/3)/log^(M+3) x).
```

This is a genuine same-clock signed-coupling advance.  The perpendicular
residual is kept visible and remains open.  A finite real zero-diagonal matrix
shows that a vanishing null channel does not force the full scalar to vanish;
the witness is structural and is not claimed to be a literal V59
counterexample.

## Project structure and reproduction

```text
README.md
paper/paper.pdf
code/
experiments/
results/
notes/
```

From the repository root:

```bash
python -B papers/tpc-259-same-clock-null-coupling/code/tpc259_null_coupling_certificate.py --check
python -O -B papers/tpc-259-same-clock-null-coupling/code/tpc259_null_coupling_certificate.py --check
python -B papers/tpc-259-same-clock-null-coupling/experiments/tpc259_independent_checker.py --check
python -O -B papers/tpc-259-same-clock-null-coupling/experiments/tpc259_independent_checker.py --check
python -B papers/tpc-259-same-clock-null-coupling/experiments/tpc259_null_coupling_stress.py --check
python -O -B papers/tpc-259-same-clock-null-coupling/experiments/tpc259_null_coupling_stress.py --check
```

The finite certificate checks exact clock/block geometry, the source-frozen
null weights, the projection identity, the exponent ledger, and the synthetic
residual witness.  It does not treat finite values as proof of a prime
asymptotic.

## Claim firewall

```text
TPC259_ROUTE_ADVANCE = YES_SCOPED_NULL_CHANNEL
TPC259_ARITHMETIC_ADVANCE = YES_SCOPED_SIGNED_COUPLING_CHANNEL
TPC259_W_NULL_MOMENT = PROVED_SOURCE_BACKED_ARBITRARY_FIXED_LOG_POWER
TPC259_NULL_CHANNEL = PROVED_SOURCE_BACKED_o_ONE
TPC259_RESIDUAL_DECOMPOSITION = PROVED_EXACT
TPC259_RESIDUAL_FULL_SCALAR = OPEN
TPC259_FIXED_POWER_SAVING = NONE
TPC259_L2 = NONE
TPC259_FULL_GATE_B = OPEN
TPC259_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC259_FIXED_ATOM_CREDIT = 0
TPC259_TWIN_PRIME_RESULT = NONE
```

## Batch handoff fields

```text
STRONGEST_POSITIVE_RESULT = THE_SOURCE_FROZEN_NULL_RANK_ONE_SIGNED_COUPLING_CHANNEL_IS_ARBITRARILY_LOG_SMALL_ON_THE_SAME_LITERAL_CLOCK
STRONGEST_OBSTRUCTION = THE_ORTHOGONAL_RESIDUAL_CAN_CARRY_THE_ENTIRE_SIGNED_SCALAR_EVEN_WITH_ZERO_NULL_CHANNEL
OPEN_THEOREM = CONTROL_W_PERP_AGAINST_A_X_BETA_OR_REASSEMBLE_ALL_FOUR_SIGNED_PACKETS_WITH_THE_RESIDUAL_RETAINED
REUSABLE_STRUCTURE = SAME_CLOCK_TO_HAAR_NULL_TO_W_MOMENT_TO_EXACT_RANK_ONE_SPLIT_TO_RESIDUAL_FIREWALL
ROUND2_CLUE = AUDIT_FULL_FOUR_PACKET_SIGNED_REASSEMBLY_WITH_THE_ORTHOGONAL_RESIDUAL_EXPLICITLY_PRESENT
```

The Session-specific evaluator files named in the planning note are not in
this checkout; `notes/route_evaluation.md` records the local fail-closed
fallback review.
