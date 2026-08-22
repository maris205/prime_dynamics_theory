# TPC-225 route evaluation

`Route A`: **NOT_APPLICABLE**. No unconditional arithmetic estimate for the fixed atom is
claimed.

`Route B`: **PROVED_STRUCTURAL_L1**. The named cutoff-one source clock has exact pairwise
prime-row orthogonality. This proves `E_AP=E_diag` and `E_all=E_pol`, and therefore refutes a
strict AP marginal saving on that clock.

Strongest positive result: a reusable exact support lemma converts the source clock into a
block-orthogonal prime-row decomposition.

Strongest obstruction: the AP marginal is identically the diagonal energy, so no amount of
notation-level shared-clock compilation can manufacture prime-label cancellation on this
clock.

Open theorem: find a source-locked clock with nontrivial `m` support and legitimate
cross-prime overlap, or prove that the required overlap still cannot pay the AP marginal.

Reusable structure: `E_AP=E_diag` and `E_all=E_pol` in the cutoff-one regime.

`ROUND2_CLUE`:

```text
MOVE_TO_NONTRIVIAL_CUTOFF_CLOCK_BEFORE_CLAIMING_AP_DISPERSION
```

Claim firewall:

```text
TPC225_CUTOFF_ONE = PROVED_EXACT
TPC225_SUPPORT_DISJOINTNESS = PROVED_EXACT
TPC225_AP_SAVING_ON_NAMED_CLOCK = REFUTED_SCOPED
TPC225_POLARIZED_SAVING = PROFILE_DEPENDENT_OPEN
TPC225_V46_CLOCK_TRANSFER = OPEN
TPC225_ARITHMETIC_ADVANCE = NO
TPC225_FIXED_ATOM_CREDIT = 0
TPC225_L2 = NONE
TPC225_FULL_GATE_B = OPEN
TPC225_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```
