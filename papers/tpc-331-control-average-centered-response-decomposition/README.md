# TPC-331 — Control-average and centered position-response decomposition

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-331 treats the five TPC-330 coordinate bijections as one finite control
orbit.  For every finite quadratic response it proves the exact decomposition

```text
mean_j E(C P_j v) = E(C v_bar) + mean_j E(C(P_j v-v_bar))
```

and the corresponding identities for the coordinate diagonal `D` and the
off-diagonal term `O=E-D`.  On the locked 32-row panel, the all-plus
control-average and centered-position terms are positive in `32/32` rows,
while the coherent mean term is positive in `31/32` rows.  This localizes the
finite positive response in the position-centered component, but does not
prove an arithmetic `L2` estimate or a twin-prime theorem.

## Parent and frozen panel

The parent is TPC-330, whose producer and certificate are hash-locked.  The
same finite V59 declared source model, literal deleted-diagonal centered
prime-shell operator, origins, scales, shell anchors, exponents, and four sign
laws are retained:

```text
origins = {28001, 36001}
scales = {4096, 8192}; source counts = {2048, 4096}
Q = {24, 36, 54, 80}; s = {1, 2}; H = 66
controls = identity, affine_(3,11), affine_(5,17), affine_(7,29), reversal
```

For a source vector `v`, write `w_j=P_j v`,
`v_bar=(1/5) sum_j w_j`, and `z_j=w_j-v_bar`.  The maps are bijections of
the index set and preserve the source multiset and Euclidean norm exactly.

## Exact finite theorem

For any real finite vector and any one of the coherent matrices `C_e`,

```text
E(w) = ||C_e w||_2^2
D(w) = sum_t w_t^2 sum_u C_e(u,t)^2
O(w) = E(w)-D(w)
```

and `sum_j z_j=0` imply

```text
mean_j E(w_j) = E(v_bar) + mean_j E(z_j)
mean_j D(w_j) = D(v_bar) + mean_j D(z_j)
mean_j O(w_j) = O(v_bar) + mean_j O(z_j).
```

The 16-point anchor on `[36001,36016]`, `Q=4`, shell `{5,7}`, `s=1`, and
`1_(t+2 prime)-1_(t odd)` is evaluated with exact rational arithmetic.  The
three decomposition identities and all reduced-fraction digests are locked
in the certificate.

## Certified decomposition census

Entries are `negative / positive`; no observation is unresolved.

| law | control average | coherent mean | centered position |
|---|---:|---:|---:|
| all-plus | 0 / 32 | 1 / 31 | 0 / 32 |
| alternating index | 23 / 9 | 23 / 9 | 23 / 9 |
| mod-4 character | 32 / 0 | 32 / 0 | 32 / 0 |
| half split | 32 / 0 | 32 / 0 | 32 / 0 |

For all-plus, the ratio intervals over the 32 rows are:

```text
average  : [1.0291358503710915, 2.6078747190560239]
coherent : [0.99496392236342945, 4.7216117506002702]
centered : [1.0059897276060032, 2.7607585737280149]
```

The coherent energy fraction lies in `[0.14793771984595222,
0.39709863476862445]`; the centered fraction is its exact finite complement.
The largest recorded floating-point identity residuals are `4.76837158203125e-6`
for energy, `2.6226043701171875e-6` for the diagonal, and
`5.9604644775390625e-6` for the off-diagonal decomposition.  The exact anchor
is the symbolic certificate; these residuals only describe the float64 panel
replay.

## Claim firewall

```text
PROVED_EXACT_FINITE = mean/centered decomposition of E, D, and O;
                      finite Gram identity; five bijections and norm invariance;
                      exact rational anchor
PROVED_EXACT_FINITE_DECLARED_MODEL = finite V59 source-vector formula
NUMERICALLY_CERTIFIED_FINITE = 32 rows x 4 laws x 3 components;
                               all-plus average/centered 32/32 positive;
                               coherent 31/32 positive; independent replay
NUMERICAL_OBSERVATION = ratio ranges and finite energy fractions
MODELING_CHOICE = fixed five-control orbit, finite panel, float64 guard
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
OPEN = growing source-native L2; uniform position-response bound;
       canonical sign law; strict 1/400 payment; full Gate B; twin-prime endpoint
TWIN_PRIME_RESULT = NONE
```

The Session-named `propose.md` and Route-A/Route-B evaluator files are absent
from this checkout.  The local Bridge-B checker is a fail-closed fallback and
is not an official evaluator pass.

## Reproduction

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-331-control-average-centered-response-decomposition/code/tpc331_control_average_centered_response_decomposition.py --check
python -O -B papers/tpc-331-control-average-centered-response-decomposition/code/tpc331_control_average_centered_response_decomposition.py --check
python -B papers/tpc-331-control-average-centered-response-decomposition/experiments/tpc331_independent_checker.py --check
python -O -B papers/tpc-331-control-average-centered-response-decomposition/experiments/tpc331_independent_checker.py --check
python -B papers/tpc-331-control-average-centered-response-decomposition/experiments/tpc331_control_average_stress.py --check
python -O -B papers/tpc-331-control-average-centered-response-decomposition/experiments/tpc331_control_average_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc331_control_average_centered_response_decomposition_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc331_control_average_centered_response_decomposition_checker.py --check
```

The canonical result is
[results/tpc331_certificate.json](results/tpc331_certificate.json), and the
compiled manuscript is [paper/paper.pdf](paper/paper.pdf).

## Package contents and next clue

`PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, `paper/`,
`code/`, `experiments/`, `results/`, and `notes/` form the auditable package.
The next minimal question is whether this control-average/centered split
survives a growing source ensemble or can be related to a source-native
arithmetic `L2` quantity.  TPC-331 itself makes no asymptotic claim.
