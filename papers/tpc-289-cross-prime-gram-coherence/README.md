# TPC-289 — Cross-prime Gram coherence

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

On 18 finite rows and 1,380 unordered cross-prime comparisons, 17 rows have
pairwise-positive physical Gram cross terms, while the early
`(N,H,Q,z,s)=(256,38,27,5,1)` row has three exact negative pairs, including a
near-zero normalized coherence.  All 18 rows still have aggregate energy
ratio greater than one; eight late-shell rows pass the finite
`eta=3/5, delta=4/5` accumulation test.

## What advances

- replaces TPC-288's full-rank question by a source-native signed coherence
  decomposition of the output Gram;
- proves an exact conditional lower bound turning a positive coherence floor
  and diagonal balance into aggregate energy accumulation;
- identifies a finite sign/coherence phase diagram rather than assuming that
  late-shell behavior is uniform;
- records an explicit three-pair sign-flip obstruction and a two-group control
  signature degeneracy;
- preserves the distinction between finite evidence and the still-open
  growing-shell/arithmetic `L2` gates.

## Claim ceiling

```text
PROVED_EXACT = Gram PSD, normalized coherence bound, conditional accumulation envelope
NUMERICALLY_CERTIFIED_FINITE = 17/18 pairwise-positive rows over 1,380 pairs
NUMERICALLY_CERTIFIED_FINITE = 3 negative pairs in one early crossover row
NUMERICALLY_CERTIFIED_FINITE = 8-row eta=3/5, delta=4/5 strong block
NUMERICALLY_CERTIFIED_FINITE = 18/18 aggregate energy-amplified rows
REFUTED_FINITE = uniform pairwise positivity/coherence-floor rule on declared grid
MODELING_CHOICE = finite rows and late-block thresholds
OPEN = source-restricted or growing-shell coherence theorem
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

The sign flip refutes only the tested finite uniform rule.  It does not
refute every weighted, restricted, or asymptotic cross-prime estimate.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc289_cross_prime_gram_coherence_certificate.py --write
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc289_cross_prime_gram_coherence_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B code/tpc289_cross_prime_gram_coherence_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc289_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/tpc289_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc289_coherence_stress.py
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  The Session-named
Route-A/Route-B evaluator files are absent from this checkout;
`notes/route_evaluation.md` records the fail-closed local fallback.
