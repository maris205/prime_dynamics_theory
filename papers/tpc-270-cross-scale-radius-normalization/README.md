# TPC-270 — Cross-Scale Endpoint-Normalized Radius Audit

Author: Liang Wang
Affiliation: School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

Status:

```text
NUMERICALLY_CERTIFIED_FINITE_CROSS_SCALE_RADIUS_NORMALIZATION_AUDIT
```

TPC-269 showed a finite profile-path flip but did not measure the size of its
Schur radius across scales. TPC-270 defines the dimensionless finite observable

```text
Xi=(R_squared)^3/N^10=(R/N^(5/3))^6
```

and keeps the prime shell, masks, deleted diagonal, source beta, registered
`z_N=floor(log(N))` cutoff, profiles, and rank-three projection source-compatible.
Six base rows, four dyadic ratios, five adjacent ratios, and three profile
controls are certified.

The dyadic ratio intervals are:

```text
64->128:  [0.231753859227, 0.231847466257]
96->192:  [23.9597604587, 23.9685339622]
128->256: [7.17162080603, 7.17448479796]
192->384: [0.802913654645, 0.803207691586]
```

They give a finite `DROP_RISE_RISE_DROP` pattern in the endpoint-normalized
radius. The profile controls satisfy
`1/2 < Xi_(theta=1/2)/Xi_(theta=0) < 3/4` at `N=96,128,256`.
This is a scoped finite variation audit: it is not an asymptotic radius
counterexample or a power-saving theorem. Fixed-power credit remains zero;
arithmetic `L2`, full Gate B, and the twin-prime conclusion remain open.

## Reproduce

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-270-cross-scale-radius-normalization/code/tpc270_cross_scale_radius_certificate.py --check
python -O -B papers/tpc-270-cross-scale-radius-normalization/code/tpc270_cross_scale_radius_certificate.py --check
python -B papers/tpc-270-cross-scale-radius-normalization/experiments/tpc270_independent_checker.py --check
python -O -B papers/tpc-270-cross-scale-radius-normalization/experiments/tpc270_independent_checker.py --check
python -B papers/tpc-270-cross-scale-radius-normalization/experiments/tpc270_normalization_stress.py --check
python -O -B papers/tpc-270-cross-scale-radius-normalization/experiments/tpc270_normalization_stress.py --check
```

The required paper layout is present, including `paper/paper.pdf`.
