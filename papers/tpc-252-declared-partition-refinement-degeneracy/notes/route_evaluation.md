# Route Evaluation

TPC-252 closes the declared-partition optimization question at the structural
level. Binary refinement transfers exactly one contrast covariance from
`Q_trans` to `C_long` and cannot increase the true transverse radius. Repeated
refinement reaches the singleton partition, where every transverse and
coherence quantity degenerates and the partition margin becomes the direct
external bound.

The equality

```text
max_P [|C_long(P)|-R_coh(P)-E]_+=[|C_x|-E]_+
```

shows that unconstrained adaptive partition search is not a route to a
stronger certificate. This conclusion does not select a meaningful coarse
partition, control intermediate `R_coh`, or show any nonzero literal V59
contrast. The same-source partition dependence is demonstrated only by a
synthetic exact operator replay, and a stable fixture rules out every-source
instability.

Strongest supported claim:

```text
UNIVERSAL_SINGLETON_COLLAPSE_AND_MARGIN_OPTIMALITY_WITH_EXACT_BINARY_REFINEMENT_RANK_ONE_COVARIANCE_UPDATE_TRANSVERSE_RADIUS_MONOTONICITY_AND_EXISTENTIAL_SAME_SOURCE_SYNTHETIC_PARTITION_NONINVARIANCE
```

Remaining gates are source-specific: a certified external error, direct
control of the literal `C_x`, any useful restriction or arithmetic selection
of a non-singleton partition, actual projected coherence estimates, and every
global Gate-B loss including strict `1/400` remain open. Arithmetic status is
unchanged.

Narrowest next action: stop optimizing over all declared partitions and freeze
one nontrivial partition from the physical interval alone.  The minimal test is
the coefficient-independent midpoint split of `I_x`: compile its single
normalized contrast against the literal `w` and `A_x beta`, without inspecting
the realized margin when choosing the split.  A direct certificate still
requires `|C_x|>E`; the midpoint test is instead the smallest honest audit of
whether a source-only coarse direction contains additional arithmetic
structure.  Any later admissible class must remain fixed independently of the
observed margin, or singleton attainment makes the optimization tautological.
