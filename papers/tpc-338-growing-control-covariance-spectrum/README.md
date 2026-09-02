# TPC-338 — Growing-control covariance spectrum

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-338 enlarges TPC-337's five-control orbit to nine controls while keeping
the source windows and operator fixed.  Centered covariance still carries
`87.72%--89.73%` of the full response in all six rows, and the normalized
covariance spectrum changes by only `0.0264396313--0.0440591812` in `L1`.
However, twin--zero covariance reverses sign: negative in `6/6` five-control
rows and positive in `6/6` nine-control rows.  Energy structure is therefore
more stable than signed interaction structure.

## New contribution

The paper performs a nested ensemble comparison rather than repeating one
covariance decomposition.  For `J` equal to the first five or all nine
controls,

```text
K_J(C,D) = mean_(j in J) <y_(C,j)-ybar_(C,J), y_(D,j)-ybar_(D,J)>.
```

It records both covariance spectra and a direct sign census.  The result
rejects promotion of a selected finite covariance sign to a canonical law,
while preserving the more robust observation that placement variation
dominates the coherent mean.

## Frozen finite panel

```text
origins       = {42001, 44001}
scales        = {2048, 4096, 8192}
operator      = all-plus, Q=54, exponent=1, H=66
five controls = identity, affine_(3,11), affine_(5,17), affine_(7,29), reversal
extra controls= affine_(9,1), affine_(11,13), affine_(13,17), affine_(17,19)
```

## Certified finite readout

| quantity | five controls | nine controls |
|---|---:|---:|
| centered fraction range | `0.7850322548--0.8552982168` | `0.8771801838--0.8972635786` |
| coherent fraction range | `0.1447017832--0.2149677452` | `0.1027364214--0.1228198162` |
| twin/background covariance | positive `6/6` | positive `6/6` |
| background/zero covariance | negative `6/6` | negative `6/6` |
| twin/zero covariance | negative `6/6` | positive `6/6` |
| normalized spectrum `L1` change | -- | `0.0264396313--0.0440591812` |

The relative Frobenius change of the unnormalized covariance matrix is
`0.2178935295--0.2379031579`.  The exact finite mean/centered identity and
covariance-Gram PSD statement hold for both ensembles.

## Claim firewall

```text
PROVED_EXACT_FINITE_DECLARED_MODEL = nested mean/centered identity; covariance PSD
NUMERICALLY_CERTIFIED_FINITE = 6 rows x (5,9) controls
NUMERICAL_OBSERVATION = finite spectral distances
REFUTED_SCOPED = twin-zero signed covariance is ensemble-invariant
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
SOURCE_UNIFORM_L2 = OPEN
UNIFORM_MASKED_OPERATOR_BOUND = OPEN
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

The official Session evaluator files are absent.  Local Bridge-B is a
fail-closed repository fallback, not an official Route-A/Route-B pass.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-338-growing-control-covariance-spectrum/code/tpc338_growing_control_covariance_spectrum.py --write
python -B papers/tpc-338-growing-control-covariance-spectrum/code/tpc338_growing_control_covariance_spectrum.py --check
python -O -B papers/tpc-338-growing-control-covariance-spectrum/code/tpc338_growing_control_covariance_spectrum.py --check
python -B papers/tpc-338-growing-control-covariance-spectrum/experiments/tpc338_independent_checker.py --check
python -O -B papers/tpc-338-growing-control-covariance-spectrum/experiments/tpc338_independent_checker.py --check
python -B papers/tpc-338-growing-control-covariance-spectrum/experiments/tpc338_spectrum_stress.py --check
python -O -B papers/tpc-338-growing-control-covariance-spectrum/experiments/tpc338_spectrum_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc338_growing_control_covariance_spectrum_checker.py --check
```

The canonical result is [results/tpc338_certificate.json](results/tpc338_certificate.json),
and the manuscript is [paper/paper.pdf](paper/paper.pdf).

## Next clue

Since signed covariance is not canonical, the next project should test a
sign-free, mask-aware operator envelope against the finite response gains.
