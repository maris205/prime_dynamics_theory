# TPC-333 — Source polarization and the arithmetic cross-term ledger

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-333 isolates the source identity left live by TPC-332:

```text
||Lambda-b||_2^2 = ||Lambda||_2^2 + ||b||_2^2 - 2 <Lambda,b>.
```

On the same two disjoint origins `{42001,44001}` and three scales
`{2048,4096,8192}`, all six normalized cancellation coefficients

```text
kappa = 2 <Lambda,b> / (||Lambda||_2^2 + ||b||_2^2)
```

lie in `[0.35486589921455675, 0.36250235375855522]`.  The residual therefore
retains `[0.63749764624144467, 0.64513410078544309]` of the component-sum
energy.  This is a finite, independently replayed obstruction to treating
the two source components as nearly orthogonal or as almost completely
canceling.  It is not a source-uniform `L2` estimate and gives no twin-prime
conclusion.

## Why this is a separate paper

TPC-332 certified a control-orbit decomposition but left the arithmetic
source layer as the live gate.  TPC-333 removes the dense operator entirely
and audits the source polarization terms directly.  That makes the result a
new source-level diagnostic rather than a subdivision of the prior matrix
paper.

## Frozen finite object

The parent is TPC-332, locked by normalized LF SHA-256.  The six windows are

```text
origins       = {42001, 44001}
scales        = {2048, 4096, 8192}
source counts = {1024, 2048, 4096}
source model  = beta_x^(2)(t) = Lambda(t+2) - b_x^(2)(t)
cutoff        = 50000 (inherited finite tail cutoff)
```

Each row stores `Lambda` and comparison squared norms, their inner product,
the residual norm, the exact algebraic identity error, normalized correlation,
and nonzero/sign counts.  Four adjacent nested-scale pairs are also stored.

## Main finite readout

| quantity | minimum | maximum |
|---|---:|---:|
| `kappa` | 0.35486589921455675 | 0.36250235375855522 |
| residual fraction | 0.63749764624144467 | 0.64513410078544309 |
| normalized correlation | 0.46455337638475735 | 0.48443427505641973 |

All six rows fall inside the predeclared open interval `(0.35,0.37)`.
The largest float64 replay identity error is
`1.4551915228366852e-11`.  Adjacent residual-energy growth factors inherited
from the six-window ledger are `1.8736551016...`, `1.9695310093...`,
`1.9140068639...`, and `2.0376754464...`; these remain finite descriptors.

## Claim firewall

```text
PROVED_EXACT_FINITE_DECLARED_MODEL = polarization identity
NUMERICALLY_CERTIFIED_FINITE = 6 source windows + 4 growth pairs
NUMERICALLY_CERTIFIED_FINITE = kappa interval census 6/6
REFUTED_SCOPED = near-orthogonality / near-total cancellation on this panel
NUMERICAL_OBSERVATION = coefficient range and scale drifts
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
SOURCE_UNIFORM_L2 = OPEN
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

The exact anchor uses rational vectors `(3,-2,5,1)` and `(1,1,-1,2)` and
records the exact values `39`, `7`, `-2`, and `50`.  It validates the algebra,
not an asymptotic prime statement.

## Reproduction

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-333-source-polarization-cross-term/code/tpc333_source_polarization_cross_term.py --write
python -B papers/tpc-333-source-polarization-cross-term/code/tpc333_source_polarization_cross_term.py --check
python -O -B papers/tpc-333-source-polarization-cross-term/code/tpc333_source_polarization_cross_term.py --check
python -B papers/tpc-333-source-polarization-cross-term/experiments/tpc333_independent_checker.py --check
python -O -B papers/tpc-333-source-polarization-cross-term/experiments/tpc333_independent_checker.py --check
python -B papers/tpc-333-source-polarization-cross-term/experiments/tpc333_polarization_stress.py --check
python -O -B papers/tpc-333-source-polarization-cross-term/experiments/tpc333_polarization_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc333_source_polarization_cross_term_checker.py --check
```

The canonical result is [results/tpc333_certificate.json](results/tpc333_certificate.json)
and the compiled manuscript is [paper/paper.pdf](paper/paper.pdf).

## Next clue

The cross term is substantial but not close to complete cancellation.  The
next minimal question is support attribution: split the cross term into
actual twin-prime coordinates, prime-power coordinates, and the odd
composite background.
