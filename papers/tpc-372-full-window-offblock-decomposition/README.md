# TPC-372 — Full-window block/off-block decomposition

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-372 keeps the TPC-370 full-window normalization and decomposes each
all-plus count-2048 matrix into its fixed 8-block diagonal part `D` and the
off-block remainder `R`.  In the beta=2 panel, the full matrix has six
high-`Q` spectral-cap failures, while `D` and `R` each have zero spectral-cap
failures.  Nevertheless, on every full failure row the reverse triangle
inequality gives a positive lower bound for `||R||_2`.  The finite excess is
therefore a common-normalization sum/coherence phenomenon on this panel; no
causal or asymptotic attribution is claimed.

## Frozen protocol

The complete panel is:

```text
origins       = (1010001, 1018021, 1026041)
window count  = 2048
block mask    = eight contiguous blocks of length 256
Q             = (512, 2048, 8192)
exponent      = 1
law           = all_plus
beta          = (0, 2)
rows          = 3 * 3 * 2 = 18
```

The full-window square-energy geometry is used for the full matrix, the
block-diagonal matrix, and the off-block matrix.  The block mask is fixed
before any component metric is read.  The inherited exact anchor is
`[1010346,1010359)` at `Q=4`, exponent `1`, shell `{5,7}`, inherited from
TPC-371 and not used to select a main-panel row.

## Finite census

| beta | full spectral failures | diagonal spectral failures | off-block spectral failures | full Schur failures |
|---:|---:|---:|---:|---:|
| 0 | 9 | 9 | 6 | 9 |
| 2 | 6 | 0 | 0 | 0 |

For beta=2, the maximum normalized spectral values are:

| component | maximum |
|---|---:|
| full `T` | 0.71099989528234753 |
| block diagonal `D` | 0.51702415681590108 |
| off-block `R` | 0.26329369743038339 |

On the six beta=2 full-failure rows, the lower bound
`||R||_2 >= ||T||_2-||D||_2` is positive (approximately
`0.1936--0.1940`; exact row values are retained in the certificate).  The
off-block norm itself remains below the cap.  Thus neither component alone
crosses the cap, but their sum does.

## Mathematical object

For a normalized full matrix `T` indexed by the 2048-point window, let
`P_0` retain entries whose indices lie in the same fixed 256-point block.  We
set

```text
D = P_0 ⊙ T,       R = (1-P_0) ⊙ T,       T = D + R.
```

For symmetric finite matrices, the reverse triangle inequality supplies
`||R||_2 >= ||T||_2-||D||_2`.  This is the only inference used to label the
off-block component “necessary” on the failing rows.

## Claim firewall

```text
TPC372_FULL_WINDOW_PROTOCOL = PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND
TPC372_COMMON_NORMALIZATION = PROVED_EXACT_FINITE
TPC372_DECOMPOSITION_IDENTITY = NUMERICALLY_CERTIFIED_FINITE
TPC372_FULL_REPLAY = NUMERICALLY_CERTIFIED_FINITE_18_ROWS
TPC372_BETA2_FULL_FAILURE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC372_BLOCK_DIAGONAL_PHASE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC372_OFF_BLOCK_NECESSITY = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC372_CROSS_BLOCK_CAUSALITY = OPEN
TPC372_ORIGIN_UNIFORMITY = OPEN
TPC372_WINDOW_UNIFORMITY = OPEN
TPC372_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC372_GROWING_OPERATOR_BOUND = OPEN
TPC372_SOURCE_UNIFORM_L2 = OPEN
TPC372_ARITHMETIC_ADVANCE = NO
TPC372_FIXED_POWER_CREDIT = 0
TPC372_FULL_GATE_B = OPEN
TPC372_TWIN_PRIME_RESULT = NONE
```

The finite decomposition does not prove that `R` causes the parent failure,
does not establish positivity of `R`, and does not transfer to other windows,
origins, partitions, or asymptotic limits.  Official Route-A/Route-B
evaluator files are absent; local Bridge-B is repository evidence only.

## Auditable package and reproduction

The project contains `PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`,
`PROOF_PACKAGE.md`, `notes/`, `code/`, `experiments/`, `results/`, and
`paper/`.  The canonical result is
`results/tpc372_certificate.json`, and the manuscript is `paper/paper.pdf`.

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-372-full-window-offblock-decomposition/code/tpc372_full_window_offblock_decomposition.py --write
python -B papers/tpc-372-full-window-offblock-decomposition/code/tpc372_full_window_offblock_decomposition.py --check
python -O -B papers/tpc-372-full-window-offblock-decomposition/code/tpc372_full_window_offblock_decomposition.py --check
python -B papers/tpc-372-full-window-offblock-decomposition/experiments/tpc372_independent_checker.py --check
python -O -B papers/tpc-372-full-window-offblock-decomposition/experiments/tpc372_independent_checker.py --check
python -B papers/tpc-372-full-window-offblock-decomposition/experiments/tpc372_adversarial_certificate_stress.py --check
python -O -B papers/tpc-372-full-window-offblock-decomposition/experiments/tpc372_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc372_full_window_offblock_decomposition_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc372_full_window_offblock_decomposition_checker.py --check
```

```text
ROUND2_CLUE = TEST_EIGENMODE_BLOCK_SEPARATION
```
