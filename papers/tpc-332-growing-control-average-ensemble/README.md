# TPC-332 — Growing-ensemble replication of the control-average split

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-332 moves the five-control mean/centered decomposition of TPC-331 to a
disjoint two-origin, three-scale source ensemble.  Across 48 rows, the
all-plus control-average and centered-position components are positive in
`48/48` rows, while the coherent mean is positive in `47/48`.  The underlying
unpermuted arithmetic residual has both signs (`27` negative and `21`
positive), so the decomposition is more stable than the source-native sign.

The source layer adds an independently checked finite polarization ledger

```text
||Lambda-b||_2^2 = ||Lambda||_2^2 + ||b||_2^2 - 2 <Lambda,b>.
```

Its six window records show residual-energy-per-source values between
`8.1067880951799047` and `8.9320414698285227`, and adjacent residual-energy
growth factors between `1.8736551016394614` and `2.037675446375288`.  These
are finite observations, not an asymptotic arithmetic `L2` theorem.

## Frozen finite object

The parent is TPC-331, locked by normalized SHA-256.  The new source windows
are disjoint from its intervals:

```text
origins       = {42001, 44001}
scales        = {2048, 4096, 8192}
source counts = {1024, 2048, 4096}
Q             = {24, 36, 54, 80}
kernel powers = {1, 2}
H             = 66
tail cutoff  = 50000
ratio guard   = 5e-8
```

For `I_(o,N)={o,...,o+N/2-1}`, the literal block is

```text
B_p(u,t) = 1_(u!=t) 1_(p does not divide u) 1_(p does not divide t)
           p H^(2s)/(H^2+(u-t)^2)^s
           (1_(p divides u-t)-1/(p-1)).
```

The four shell laws and the five bijective controls are unchanged from
TPC-331.  Every new `t+2` remains below the declared cutoff, so no silent
extension of the finite source model is made.

## Exact finite structure

For `w_j=P_jv`, `vbar=mean_j w_j`, and `z_j=w_j-vbar`, finite bilinearity
proves, for every finite quadratic form used here,

```text
mean_j E(w_j) = E(vbar) + mean_j E(z_j)
mean_j D(w_j) = D(vbar) + mean_j D(z_j)
mean_j O(w_j) = O(vbar) + mean_j O(z_j).
```

The source vectors are the declared finite V59 midpoints
`Lambda(t+2)-b^(2)(t)`.  For each window, the producer also records the
`Lambda` norm, comparison norm, cross inner product, residual norm, normalized
correlation, and the residual polarization identity error.  The independent
checker computes those quantities without importing the producer.

## Certified finite readout

Entries below are negative / positive / unresolved counts over the 48 rows.

| law | control average | coherent mean | centered position |
|---|---:|---:|---:|
| all-plus | 0 / 48 / 0 | 1 / 47 / 0 | 0 / 48 / 0 |
| alternating index | 31 / 17 / 0 | 38 / 10 / 0 | 29 / 19 / 0 |
| mod-4 character | 48 / 0 / 0 | 44 / 4 / 0 | 47 / 1 / 0 |
| half split | 48 / 0 / 0 | 39 / 9 / 0 | 48 / 0 / 0 |

For the unpermuted all-plus residual, the sign census is `27 / 21 / 0` and
the guarded ratio range is
`[0.44646203339149909, 1.1102919670326215]`.  The coherent all-plus energy
fraction ranges from `0.12487732823422547` to `0.244815364950286`; the
centered fraction therefore ranges from `0.755184635049714` to
`0.87512267176577452`.

The four adjacent-scale source-energy slopes are

```text
0.90585540926787733, 0.97785213162340834,
0.93659600353467931, 1.0269242825184262.
```

The finite panel thus supports near-linear energy growth in these windows,
while also showing that the per-source residual energy need not be monotone
across origins and scales.

## Claim firewall

```text
PROVED_EXACT_FINITE = mean/centered quadratic identities;
                      finite Gram split; source polarization identity;
                      five control bijections; exact rational anchor
PROVED_EXACT_FINITE_DECLARED_MODEL = finite V59 source formula
NUMERICALLY_CERTIFIED_FINITE = 48 rows x 4 laws x 3 components;
                               6 source windows; 4 adjacent growth pairs;
                               independent reverse-order replay; stress suite
NUMERICAL_OBSERVATION = ratio ranges, energy fractions, and scale slopes
MODELING_CHOICE = two disjoint origins, three scales, fixed controls,
                  50000 tail cutoff, float64 replay guard
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
GROWING_SOURCE_NATIVE_L2 = OPEN
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

The finite result does not establish a canonical sign law, a uniform
position-response estimate, a source-uniform `L2` bound, a strict `1/400`
payment, or the twin-prime conjecture.  The Session-named Route-A and
Route-B evaluator files are absent; the local Bridge-B checker is a
fail-closed fallback and is not an official route pass.

## Reproduction

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-332-growing-control-average-ensemble/code/tpc332_growing_control_average_ensemble.py --check
python -O -B papers/tpc-332-growing-control-average-ensemble/code/tpc332_growing_control_average_ensemble.py --check
python -B papers/tpc-332-growing-control-average-ensemble/experiments/tpc332_independent_checker.py --check
python -O -B papers/tpc-332-growing-control-average-ensemble/experiments/tpc332_independent_checker.py --check
python -B papers/tpc-332-growing-control-average-ensemble/experiments/tpc332_growing_ensemble_stress.py --check
python -O -B papers/tpc-332-growing-control-average-ensemble/experiments/tpc332_growing_ensemble_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc332_growing_control_average_ensemble_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc332_growing_control_average_ensemble_checker.py --check
```

The canonical machine-readable result is
[results/tpc332_certificate.json](results/tpc332_certificate.json), and the
compiled manuscript is [paper/paper.pdf](paper/paper.pdf).

## Next clue

The growing ensemble confirms the exact decomposition but leaves the arithmetic
source norm as the live gate.  The next minimal project should separate the
`Lambda`/comparison cross term and then test whether its support is genuinely
twin-prime-specific or is dominated by the composite odd background.
