# TPC-336 — Masked signed-Gram response and output interference

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-336 sends the full, twin, non-twin, prime-power, and zero-cross-support
residual vectors from TPC-335 through one fixed all-plus signed-Gram operator
(`Q=54`, `s=1`, `H=66`).  In all six rows the self-response gain ordering is

```text
zero_support > non_twin_prime_shift > twin_prime > prime_power_shift.
```

The gain ranges are approximately `393547.8--419768.8`,
`117431.4--127558.6`, `37443.6--44607.8`, and `0--34676.1`, respectively.
All six full-response identities require destructive output cross terms: the
sum of self energies is `4.8538536--5.4814134` times the full response energy.
Thus source-level support proportions do not transfer directly through the
operator; output interference is the final obstruction of this batch.

This is a finite fixed-operator response certificate.  It provides no
source-uniform operator bound, arithmetic power credit, or twin-prime theorem.

## New contribution

TPC-335 established a stable source norm split and a non-dominant twin
component.  TPC-336 adds the missing operator layer and records the complete
output Gram matrix between masks.  The identity

```text
||C beta||^2 = sum_C ||C beta_C||^2
               + 2 sum_{C<D} <C beta_C,C beta_D>
```

is checked row by row, so the observed cancellation is not hidden by adding
component energies alone.

## Frozen operator and source panel

The parent is TPC-335, locked by normalized LF SHA-256.  The source windows
are origins `{42001,44001}` and scales `{2048,4096,8192}`.  The operator is
the literal all-plus prime-shell matrix with `Q=54`, kernel exponent `1`, and
height `66`, using the same deleted diagonal and residue masks as the prior
papers.  The four source masks are the TPC-334 support classes; `zero_support`
means zero contribution to `<Lambda,b>`, not a zero residual vector.

## Certified finite readout

| mask | response-gain minimum | response-gain maximum |
|---|---:|---:|
| twin prime | 37443.5863 | 44607.7734 |
| non-twin prime shift | 117431.3630 | 127558.5613 |
| prime-power shift | 0 | 34676.0605 |
| zero cross support | 393547.76798 | 419768.84446 |

The gain ordering holds in `6/6` rows.  The self-energy sum divided by full
response energy lies in `[4.8538535937774503,5.4814134328177246]`, and the
full-versus-component output identity is independently replayed in all six
rows.  The largest producer identity residual is below `1e-6` (summation-order
roundoff); the independent checker uses a `5e-6` fail-closed bound.

The strongest pairwise interference is the background/zero-support pair, with
inner products between `-590513160.96` and `-2389523857.63` over the panel.

## Claim firewall

```text
PROVED_EXACT_FINITE_DECLARED_MODEL = finite output-Gram expansion
NUMERICALLY_CERTIFIED_FINITE = fixed operator on 6 rows and 4 masks
NUMERICALLY_CERTIFIED_FINITE = gain ordering in 6/6 rows
NUMERICALLY_CERTIFIED_FINITE = destructive interaction in 6/6 rows
REFUTED_SCOPED = source-share ordering transfers unchanged to response
NUMERICAL_OBSERVATION = gain and interference ranges
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
SOURCE_UNIFORM_L2 = OPEN
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-336-masked-signed-gram-response/code/tpc336_masked_signed_gram_response.py --write
python -B papers/tpc-336-masked-signed-gram-response/code/tpc336_masked_signed_gram_response.py --check
python -O -B papers/tpc-336-masked-signed-gram-response/code/tpc336_masked_signed_gram_response.py --check
python -B papers/tpc-336-masked-signed-gram-response/experiments/tpc336_independent_checker.py --check
python -O -B papers/tpc-336-masked-signed-gram-response/experiments/tpc336_independent_checker.py --check
python -B papers/tpc-336-masked-signed-gram-response/experiments/tpc336_response_stress.py --check
python -O -B papers/tpc-336-masked-signed-gram-response/experiments/tpc336_response_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc336_masked_signed_gram_response_checker.py --check
```

The canonical result is [results/tpc336_certificate.json](results/tpc336_certificate.json)
and the manuscript is [paper/paper.pdf](paper/paper.pdf).

## Batch endpoint

The response layer does not preserve the source-level ordering without a
position-aware interaction estimate.  This closes the planned TPC-332--336
batch at a useful obstruction: the next research decision should return to
control covariance or seek a genuinely uniform masked operator bound.
