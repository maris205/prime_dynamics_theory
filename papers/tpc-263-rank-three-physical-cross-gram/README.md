# TPC-263: Rank-Three Physical Cross-Gram Channel

Author: Liang Wang
Affiliation: School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

Status:

```text
PROVED_SOURCE_BACKED_RANK_THREE_PHYSICAL_CROSS_GRAM_CHANNEL
```

TPC-263 is the direct continuation of TPC-262's signed-operator interface.
It combines two already source-typed ingredients on the same literal V59
clock: TPC-254 controls sums of the hybrid residual `w` on every consecutive
rank block to arbitrary fixed logarithmic order, while TPC-257 gives the three
adjoint coefficients of the source-only four-block Haar frame.  The resulting
rank-three channel is now explicitly paid:

```text
C_3(x)=<P3 w,P3 A_x beta>
     =sum_(i=0)^2 conjugate(<z_i,w>) <z_i,A_x beta>
     =O_(M,K)(x^(5/3)/(log x)^(M+3)).
```

Here `P3` projects onto `span(z0,z1,z2)`, and the estimate holds for every
fixed admissible hybrid parameter `K` and every fixed logarithmic strength
`M`.  It is a genuine physical cross-Gram statement: the four block sums are
controlled before the signed combination is formed, and the TPC-257 adjoint
asymptotics are retained with their explicit curvature constants.

The exact coupling still splits as

```text
<w,A_x beta> = C_3(x) + C_perp(x),
C_perp(x)=<(I-P3)w,(I-P3)A_x beta>.
```

TPC-263 proves no estimate for `C_perp`.  Therefore it supplies logarithmic
channel progress but zero fixed-power credit; arithmetic `L2`, full Gate B,
the strict global `1/400` payment, and any twin-prime conclusion remain open.

## Claim firewall

```text
TPC263_MAXIMUM_CLAIM = PROVED_SOURCE_BACKED_RANK_THREE_PHYSICAL_CROSS_GRAM_CHANNEL
TPC263_ROUTE_ADVANCE = YES_SCOPED_RANK_THREE_LOG_CHANNEL
TPC263_W_FRAME_MOMENTS = PROVED_SOURCE_BACKED_ARBITRARY_FIXED_LOG_POWER
TPC263_ADJOINT_FRAME_COEFFICIENTS = PROVED_SOURCE_BACKED_TPC257
TPC263_PROJECTION_SPLIT = PROVED_EXACT
TPC263_RANK_THREE_CHANNEL = PROVED_SOURCE_BACKED_X_5_OVER_3_LOG_M_PLUS_3
TPC263_ORTHOGONAL_RESIDUAL = OPEN
TPC263_FIXED_POWER_CREDIT = 0
TPC263_ARITHMETIC_ADVANCE = YES_SCOPED_FIXED_LOG_ONLY
TPC263_L2 = NONE
TPC263_FULL_GATE_B = OPEN
TPC263_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC263_TWIN_PRIME_RESULT = NONE
TPC263_STATUS = PROVED_SOURCE_BACKED_RANK_THREE_PHYSICAL_CROSS_GRAM_CHANNEL
TPC263_ROUND2_CLUE = ATTACK_THE_ORTHOGONAL_COMPLEMENT_AFTER_PAYING_THE_RANK_THREE_LOG_CHANNEL
```

The finite certificate validates the frame algebra, the projection identity,
the exponent multiplication, and a nonzero residual fixture.  It does not
pretend to prove the source-backed asymptotic inputs numerically.

## Reproduce

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-263-rank-three-physical-cross-gram/code/tpc263_rank_three_certificate.py --check
python -O -B papers/tpc-263-rank-three-physical-cross-gram/code/tpc263_rank_three_certificate.py --check
python -B papers/tpc-263-rank-three-physical-cross-gram/experiments/tpc263_independent_checker.py --check
python -O -B papers/tpc-263-rank-three-physical-cross-gram/experiments/tpc263_independent_checker.py --check
python -B papers/tpc-263-rank-three-physical-cross-gram/experiments/tpc263_rank_three_stress.py --check
python -O -B papers/tpc-263-rank-three-physical-cross-gram/experiments/tpc263_rank_three_stress.py --check
```

The project follows the required `README.md`, `paper/`, `code/`,
`experiments/`, `results/`, and `notes/` layout and includes
`paper/paper.pdf`.
