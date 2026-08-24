# Bridge B: source-native polarized collision compiler

## Theorem

For common-profile source rows `U_q=T_q beta`, `V_q=T_q w`, define

```text
W_q^(j)=U_q+i^j V_q,
E_AP^(j)=||sum_q W_q^(j)||^2,
E_diag^(j)=sum_q ||W_q^(j)||^2.
```

Then exact finite Hilbert algebra gives

```text
1/4 sum_j i^j(E_AP^(j)-E_diag^(j))
  = sum_(q!=r)<U_q,V_r>.
```

The same-prime diagonal is deleted before polarization, so the right side is supported
only on cross-prime collision coordinates.

## First-resonance block

At `Q=25`, `h=400`, `(p,r)=(37,47)`, residues `119,281`, the source-native block is

```text
1/400^2 * (
 beta_(37,3)  w_(47,-7) + beta_(47,-7) w_(37,3)
+beta_(37,-3) w_(47,7)  + beta_(47,7)  w_(37,-3)).
```

Exact source fixtures give:

```text
all positive      =  1/40000
all w negative    = -1/40000
opposite row signs=  0
directed p-to-r   =  1/80000
one coordinate    =  1/160000
```

Thus geometry does not determine sign, but the missing sign is now a named source
cross-correlation rather than a profile choice.

## Claim firewall

```text
TPC228_ROUTE_ADVANCE = YES
TPC228_COMMON_PROFILE_PACKET_RULE = PROVED_EXACT
TPC228_POLARIZED_AP_MINUS_DIAGONAL_COMPILER = PROVED_EXACT
TPC228_SOURCE_LABELLED_COLLISION_SUM = PROVED_EXACT
TPC228_Q25_3_7_SOURCE_BLOCK = PROVED_EXACT_FINITE
TPC228_ACTUAL_V59_TO_PRIMITIVE_ATOM_CROSSWALK = OPEN
TPC228_ARITHMETIC_SIGN_THEOREM = OPEN
TPC228_ARITHMETIC_CANCELLATION = NONE
TPC228_ARITHMETIC_ADVANCE = NO
TPC228_FIXED_ATOM_CREDIT = 0
TPC228_L2 = NONE
TPC228_FULL_GATE_B = OPEN
TPC228_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC228_STATUS = PROVED_STRUCTURAL_L1
TPC228_ROUND2_CLUE = ANALYZE_THE_SOURCE_NATIVE_3_7_COLLISION_GRAPH_AS_EXACT_TWO_BY_TWO_BLOCKS
```

Strongest positive result: exact conversion of packet AP-minus-diagonal energies into
the source-labelled off-diagonal collision scalar.

Strongest obstruction: the same collision block supports positive, negative and zero
source correlations.

Open theorem: attach literal V59 coefficients to primitive atom amplitudes and prove a
growing-scale signed bound.

Reusable structure: ordered source collision form, diagonal-first deletion and exact
Q25 four-term block.
