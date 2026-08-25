# TPC-245: Sharp Longitudinal--Transverse Covariance Disks

This project gives the exact feasible set of one local covariance after a
one-direction longitudinal/transverse split.  Let a complex Hilbert space use
an inner product conjugate-linear in the first slot, fix a unit vector `u`, and
write

```text
b=<u,B>,  w=<u,W>,
B_perp=B-bu,  W_perp=W-wu,
E_B=||B_perp||^2,  E_W=||W_perp||^2,
c=conjugate(w)b,  r=sqrt(E_B E_W).
```

Then

```text
<W,B> = c + <W_perp,B_perp>,
|<W_perp,B_perp>| <= r.
```

The containment is sharp, with a dimension-sensitive classification.  If
`dim_C(u^perp)>=2`, the exact feasible set at fixed moments and energies is the
closed disk `c+r Dbar`.  If the transverse dimension is one, it is the boundary
circle `c+r T` when `r>0` and the singleton `{c}` when `r=0`.  In transverse
dimension zero, positive transverse energy is unrealizable and zero energy
again gives `{c}`.

For transverse dimension at least two, zero covariance is feasible exactly
when `|c|<=r`, and the exact uniform lower margin is
`max(|c|-r,0)`.  When `r<|c|`, every feasible covariance stays in the sharp
phase sector of half-angle `arcsin(r/|c|)` about `c`.

## Main progress

- proves the complete disk/circle/singleton feasible-set classification;
- proves exact zero-feasibility and minimum-modulus formulas in every dimension;
- proves a sharp phase-sector bound when the disk misses zero;
- isolates transverse dimension two as the first dimension permitting interior
  cancellation;
- proves that the TPC-219 constant-prime-label subspace is only a projection
  ancestor, not a literal one-dimensional block direction for TPC-244.

## Physical boundary

The unit vector `u` is abstract.  No committed source defines a canonical
one-dimensional `u_h` inside the TPC-244 primitive block, and the literal V59
`beta,w` two-lane attachment is still absent.  Therefore the exact feasible set
is structural coefficient-space geometry, not an existential statement about
the actual arithmetic vectors and not an arithmetic cancellation estimate.

## Artifacts

- `PROOF_PACKAGE.md`: complete theorem and dimension branches;
- `DERIVATION_PACKAGE.md`: derivation and physical type boundary;
- `results/tpc245_certificate.json`: canonical exact finite certificate;
- `code/tpc245_covariance_disk_certificate.py`: producer/checker;
- `experiments/tpc245_independent_checker.py`: independent strict checker;
- `experiments/tpc245_covariance_disk_stress.py`: exhaustive exact stress;
- `paper/paper.pdf`: compiled manuscript.

## Reproduction

Run from this project directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc245_covariance_disk_certificate.py --write
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc245_covariance_disk_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B code/tpc245_covariance_disk_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc245_independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/tpc245_independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc245_covariance_disk_stress.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/tpc245_covariance_disk_stress.py --check
```

All finite calculations use exact Gaussian-rational arithmetic.  They are
`NUMERICAL_FINITE_ILLUSTRATION_ONLY`; the theorem is proved symbolically.

## Maximum status

`PROVED_STRUCTURAL_L1_SHARP_LONGITUDINAL_TRANSVERSE_COVARIANCE_DISKS`.

`ARITHMETIC_ADVANCE = NO`.  A source-native canonical block direction, literal
V59 two-lane attachment, payable norms and energies, signed arithmetic margin,
arithmetic `L2`, fixed-atom credit, strict `1/400`, full Gate B, and every
twin-prime conclusion remain open.
