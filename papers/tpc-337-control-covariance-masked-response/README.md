# TPC-337 — Control covariance of masked signed-Gram responses

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-337 transports each of the four TPC-336 source masks through five
predeclared coordinate bijections before applying the same all-plus operator.
The finite mean/centered decomposition is exact, but the centered orbit
variation carries `78.50%--85.53%` of the full output energy on all six
windows; the coherent mean carries only `14.47%--21.50%`.  The twin--zero and
background--zero centered covariances are negative in `6/6` rows, while the
twin--background covariance is positive in `6/6`.

This is a finite covariance obstruction, not an arithmetic estimate or a
twin-prime theorem.

## New contribution

For class `C` and control `j`, the output is

```text
y_(C,j) = A P_j beta_C,
K_CD = (1/5) sum_j <y_(C,j)-ybar_C, y_(D,j)-ybar_D>.
```

The certificate proves the mean/centered identities and the positive
semidefiniteness of `K` by finite Gram algebra.  It then measures where the
response energy lives and records the signed cross-class covariance entries.
This makes precise why a control average cannot be treated as an automatic
interference suppressor.

## Frozen finite panel

```text
origins       = {42001, 44001}
scales        = {2048, 4096, 8192}
operator      = all-plus, Q=54, exponent=1, H=66
controls      = identity, affine_(3,11), affine_(5,17), affine_(7,29), reversal
classes       = twin, non-twin prime shift, prime-power shift, zero support
```

The parent is TPC-336, locked by normalized LF SHA-256.  `zero_support` is a
complement mask for zero source cross-support; it is not a zero input vector.

## Certified finite readout

| quantity | finite range / census |
|---|---:|
| full coherent fraction | `0.1447017832--0.2149677452` |
| full centered fraction | `0.7850322548--0.8552982168` |
| twin centered fraction | `0.6115723683--0.6937370120` |
| background centered fraction | `0.3476363325--0.3847105734` |
| twin/background covariance | positive `6/6` |
| twin/zero covariance | negative `6/6` |
| background/zero covariance | negative `6/6` |
| covariance Gram eigenvalue guard | nonnegative within tolerance |

The exact rational anchor has average cross term `0`, coherent cross term
`1/2`, and centered cross term `-1/2`.

## Claim firewall

```text
PROVED_EXACT_FINITE_DECLARED_MODEL = mean/centered identities; covariance PSD
NUMERICALLY_CERTIFIED_FINITE = 6 rows x 5 controls x 4 masks
NUMERICAL_OBSERVATION = energy and covariance ranges
REFUTED_SCOPED = control averaging uniformly removes output interference
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
SOURCE_UNIFORM_L2 = OPEN
UNIFORM_MASKED_OPERATOR_BOUND = OPEN
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

The official Session evaluator files are absent in this checkout.  The local
Bridge-B wrapper is therefore explicitly fail-closed and is not an official
Route-A/Route-B pass.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-337-control-covariance-masked-response/code/tpc337_control_covariance_masked_response.py --write
python -B papers/tpc-337-control-covariance-masked-response/code/tpc337_control_covariance_masked_response.py --check
python -O -B papers/tpc-337-control-covariance-masked-response/code/tpc337_control_covariance_masked_response.py --check
python -B papers/tpc-337-control-covariance-masked-response/experiments/tpc337_independent_checker.py --check
python -O -B papers/tpc-337-control-covariance-masked-response/experiments/tpc337_independent_checker.py --check
python -B papers/tpc-337-control-covariance-masked-response/experiments/tpc337_covariance_stress.py --check
python -O -B papers/tpc-337-control-covariance-masked-response/experiments/tpc337_covariance_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc337_control_covariance_masked_response_checker.py --check
```

The canonical result is [results/tpc337_certificate.json](results/tpc337_certificate.json),
and the manuscript is [paper/paper.pdf](paper/paper.pdf).

## Next clue

The control covariance is too large to dismiss as roundoff.  The next minimal
question is whether enlarging the same affine control orbit changes this
conclusion or merely redistributes the covariance spectrum.
