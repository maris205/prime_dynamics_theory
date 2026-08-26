# TPC-269 — Growing-Cutoff and Convex-Profile Transfer

Author: Liang Wang
Affiliation: School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

Status:

```text
NUMERICALLY_CERTIFIED_FINITE_GROWING_CUTOFF_PROFILE_TRANSFER
```

TPC-268 found that a fixed finite cutoff can reverse the quarter-sector
classification. TPC-269 makes the next controlled substitution: the cutoff is
the registered finite proxy z_N=floor(log N), and the kernel moves through the
convex family K_theta=(1-theta)K_1+theta K_2. The physical prime shell, masks,
deleted diagonal, beta source and rank-three projection are unchanged.

Outward rational intervals classify twelve rows: eight contractions and four
obstructions. The growing-cutoff base has obstruction rows at N=64 and N=96.
More sharply, at the same central row (N,H,Q)=(64,15,4), the profile path gives

```text
theta=9/10: rho^2 in [0.0634078324659, 0.0634208686352]  obstruction
theta=24/25: rho^2 in [0.0622500850692, 0.0622630874560]  contraction
```

Thus the finite proxy family has a certified profile flip. This is a finite
model-relative result. z_N, the profile family, and the registered scales do
not by themselves prove uniformity for the source-level V59 construction.
No asymptotic radius estimate, fixed-power credit, arithmetic L2, full Gate B,
or twin-prime conclusion is claimed.

## Reproduce

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-269-growing-cutoff-profile-transfer/code/tpc269_growing_cutoff_profile_certificate.py --check
python -O -B papers/tpc-269-growing-cutoff-profile-transfer/code/tpc269_growing_cutoff_profile_certificate.py --check
python -B papers/tpc-269-growing-cutoff-profile-transfer/experiments/tpc269_independent_checker.py --check
python -O -B papers/tpc-269-growing-cutoff-profile-transfer/experiments/tpc269_independent_checker.py --check
python -B papers/tpc-269-growing-cutoff-profile-transfer/experiments/tpc269_profile_stress.py --check
python -O -B papers/tpc-269-growing-cutoff-profile-transfer/experiments/tpc269_profile_stress.py --check
```

The required paper layout is present, including paper/paper.pdf.
