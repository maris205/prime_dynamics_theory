# TPC-293 — A signed max-cut obstruction for multi-prime cancellation

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong
University of Science and Technology (HUST), Wuhan, China

## One-line result

The pairwise sign problem from TPC-291 can be lifted to a whole finite prime
shell as a signed complete-graph max-cut problem. On the inherited 18-row
literal grid, the exact sign atlas contains 1,380 Gram edges: 17 rows attain
the all-positive benchmark, while one early exponent-crossover row gains only
3 favorable edges. The corresponding minimum unsatisfied-edge total is 636.

This is a sign-only structural result. It is not a weighted Rayleigh bound,
not a source-image theorem, and not an arithmetic $L^2$ estimate.

## What advances

- proves the exact all-positive complete-graph max-cut formula
  $\lfloor m^2/4\rfloor$;
- defines the signed-shell frustration index as the complement of the exact
  sign max-cut objective and records its switching invariance;
- reconstructs the signed complete graph for every one of the 18 inherited
  rows and every 1,380 shell edge;
- identifies a single finite exceptional row with a `+3` sign-only gain and
  verifies that all other rows coincide with the all-positive benchmark;
- supplies an independent physical replay and an exhaustive signed-graph
  stress test over every graph on 3--6 vertices.

## Finite headline

```text
rows = 18
shell edges = 1,380
max favorable edges = 744
minimum unsatisfied edges = 636
signed gain over all-positive benchmark = 3
benchmark rows = 17 / 18
signed-gain rows = 1 / 18
triangles = 5,727
sign-frustrated triangles = 5,718
```

The `+3` gain occurs at
`(N,H,Q,z,s)=(256,38,27,5,1)`, where the seven-prime shell has three
negative Gram edges and a signed max-cut value of 15 instead of the
all-positive value 12. Edge counts intentionally ignore Gram magnitudes;
the next paper tests whether this combinatorial exception survives a
magnitude-weighted quadratic objective.

## Claim ceiling

```text
PROVED_EXACT_CONDITIONAL = all-positive K_m max-cut formula
PROVED_EXACT_FINITE = signed objective/frustration identity and switching invariance
NUMERICALLY_CERTIFIED_FINITE = complete signed atlas on 18 frozen rows
NUMERICALLY_CERTIFIED_FINITE = 1,380 edges, 744 favorable, 636 unsatisfied
NUMERICALLY_CERTIFIED_FINITE = one exceptional +3 sign-only row
MODELING_CHOICE = frozen literal source, shells, kernel, and 18-row grid
OPEN = growing signed-shell theorem, magnitude-weighted objective, source image
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

The finite sign atlas does not claim that the exceptional row yields a
physical energy improvement. It only says that edge signs alone permit a
small combinatorial improvement over the all-positive benchmark in that row.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc293_signed_shell_maxcut_certificate.py --write
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc293_signed_shell_maxcut_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B code/tpc293_signed_shell_maxcut_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc293_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/tpc293_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc293_signed_graph_stress.py
```

The manuscript is [paper/paper.pdf](paper/paper.pdf). The Session-named
Route-A/Route-B evaluator files are absent from this checkout; the local
proof package, canonical rational certificate, independent replay, stress
test, and Bridge-B checker are the fail-closed validation package.
