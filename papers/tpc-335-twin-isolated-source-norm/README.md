# TPC-335 — Twin-isolated source norm decomposition

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-335 applies the TPC-334 support masks to the full residual
`beta=Lambda-b` and obtains an exact finite orthogonal norm split.  On the six
windows, twin-prime coordinates carry `9.5561720872944358%`--
`12.241598178733512%` of residual `L2` energy, the non-twin prime-shift
background carries `67.049701649956917%`--`69.656908745054080%`, and the
zero-cross-support remainder carries roughly `18.9%`--`21.3%`.  Relative to
their raw cross-term share, twin coordinates are amplified by a stable factor
`1.7065194950664935`--`1.7705815591117822`.

This is a useful separation: twins are not the dominant residual-energy class,
but their residual energy is larger than their cross-term mass share would
suggest.  It is a finite source diagnostic, not a density theorem or a
twin-prime proof.

## New contribution

TPC-334 showed that the raw cross term is background-dominated.  TPC-335 asks
whether that conclusion survives after looking at `||beta||_2^2` itself rather
than at `<Lambda,b>`.  The four coordinate masks are disjoint, so the norm
partition is exact before any operator is applied.

## Frozen object and masks

The parent is TPC-334, locked by normalized LF SHA-256.  We retain origins
`{42001,44001}`, scales `{2048,4096,8192}`, source counts `{1024,2048,4096}`,
and cutoff `50000`.  Each coordinate is assigned to:

```text
twin_prime             : t and t+2 prime
non_twin_prime_shift   : t+2 prime, t not prime
prime_power_shift      : t+2=p^k, k>=2
zero_support           : Lambda(t+2)b(t)=0
```

The masked residuals `beta_C=beta*1_C` satisfy
`||beta||_2^2=sum_C ||beta_C||_2^2` exactly in the finite array.

## Certified finite readout

| quantity | minimum | maximum |
|---|---:|---:|
| twin residual-norm fraction | 0.095561720872944358 | 0.12241598178733512 |
| non-twin background norm fraction | 0.67049701649956917 | 0.69656908745054080 |
| prime-power norm fraction | 0 | 0.0018737060121997208 |
| twin norm / twin cross share | 1.7065194950664935 | 1.7705815591117822 |

All six twin norm fractions lie in `(0.09,0.13)` and all six background
fractions lie in `(0.65,0.72)`.  The independent checker rebuilds the masks
with a separate trial sieve and reverse factorization.

## Claim firewall

```text
PROVED_EXACT_FINITE_DECLARED_MODEL = disjoint mask norm identity
NUMERICALLY_CERTIFIED_FINITE = 6 windows and 4 support classes
NUMERICALLY_CERTIFIED_FINITE = twin norm share in 9--13% for 6/6 windows
NUMERICALLY_CERTIFIED_FINITE = background norm share in 65--72% for 6/6 windows
NUMERICAL_OBSERVATION = twin amplification range
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
SOURCE_UNIFORM_L2 = OPEN
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-335-twin-isolated-source-norm/code/tpc335_twin_isolated_source_norm.py --write
python -B papers/tpc-335-twin-isolated-source-norm/code/tpc335_twin_isolated_source_norm.py --check
python -O -B papers/tpc-335-twin-isolated-source-norm/code/tpc335_twin_isolated_source_norm.py --check
python -B papers/tpc-335-twin-isolated-source-norm/experiments/tpc335_independent_checker.py --check
python -O -B papers/tpc-335-twin-isolated-source-norm/experiments/tpc335_independent_checker.py --check
python -B papers/tpc-335-twin-isolated-source-norm/experiments/tpc335_norm_stress.py --check
python -O -B papers/tpc-335-twin-isolated-source-norm/experiments/tpc335_norm_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc335_twin_isolated_source_norm_checker.py --check
```

The canonical result is [results/tpc335_certificate.json](results/tpc335_certificate.json)
and the PDF is [paper/paper.pdf](paper/paper.pdf).

## Next clue

The twin mask is a modest but nonzero portion of source norm.  The next test
is to feed the twin-isolated, background, and full vectors through a fixed
signed-Gram operator and measure whether the operator response preserves or
reverses these source-level proportions.
