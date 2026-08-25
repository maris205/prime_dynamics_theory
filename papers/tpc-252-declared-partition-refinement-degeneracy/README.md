# TPC-252: Binary Refinement Calculus and Singleton Degeneracy for Declared-Block V59 Margins

Status:

```text
PROVED_STRUCTURAL_L1_DECLARED_PARTITION_REFINEMENT_DEGENERACY
```

TPC-252 determines exactly how the TPC-251 declared-block split behaves under
a binary refinement. If a block `J` is split into nonempty `J1,J2`, its
normalized contrast `z` adds one orthogonal rank-one direction:

```text
M_P'=M_P+z tensor z,
C_long(P')=C_long(P)+conjugate(<z,w>)<z,g>,
Q_trans(P')=Q_trans(P)-conjugate(<z,w>)<z,g>.
```

The exact transverse radius is monotone:

```text
R_trans(P') <= R_trans(P).
```

At the singleton partition, every projected probe and projected Gram entry
vanishes, as do `D,L,mu,U,Q_trans,R_trans,R_coh`; `kappa` is undefined because
`D=0`, and `C_long=C_x`. Consequently, for every fixed independently
certified `E>=0`,

```text
max_P [|C_long(P)|-R_coh(P)-E]_+ = [|C_x|-E]_+.
```

Thus adaptive optimization over all legal declared partitions cannot improve
the direct external lower bound. One fixed two-coordinate synthetic
`A,beta,w` yields different decompositions and margin metrics for the coarse
and singleton partitions, establishing existential non-invariance. The source
triple itself is unchanged. A separate stable source refutes any universal
every-source instability claim.

## Reproduce

Run from the repository root with bytecode disabled:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-252-declared-partition-refinement-degeneracy/code/tpc252_partition_refinement_certificate.py --check
python -O -B papers/tpc-252-declared-partition-refinement-degeneracy/code/tpc252_partition_refinement_certificate.py --check
python -B papers/tpc-252-declared-partition-refinement-degeneracy/experiments/tpc252_independent_checker.py --check
python -O -B papers/tpc-252-declared-partition-refinement-degeneracy/experiments/tpc252_independent_checker.py --check
python -B papers/tpc-252-declared-partition-refinement-degeneracy/experiments/tpc252_partition_refinement_stress.py --check
python -O -B papers/tpc-252-declared-partition-refinement-degeneracy/experiments/tpc252_partition_refinement_stress.py --check
```

The producer emits canonical strict JSON with exact Gaussian-rational data.
The independent checker imports no producer code and rejects typed, semantic,
digest, duplicate-key, nonfinite-token, and noncanonical-byte mutations. The
stress suite checks 192 deterministic exact-rational refinement families.

## Claim boundary

The fixed-family projected-Gram subtraction is not a native probe-array update:
common input/output repartition changes the TPC-251 probe indexing. No
`R_coh` monotonicity is claimed. The non-invariance replay is synthetic, not a
literal numerical V59 instance, and no actual V59 coarse nonzero contrast is
proved. There is no canonical partition, asymptotic or arithmetic advance,
L2, Route A, fixed-atom credit, Gate-B closure, strict `1/400`, or twin-prime
claim.

Maximum supported claim:

```text
UNIVERSAL_SINGLETON_COLLAPSE_AND_MARGIN_OPTIMALITY_WITH_EXACT_BINARY_REFINEMENT_RANK_ONE_COVARIANCE_UPDATE_TRANSVERSE_RADIUS_MONOTONICITY_AND_EXISTENTIAL_SAME_SOURCE_SYNTHETIC_PARTITION_NONINVARIANCE
```
