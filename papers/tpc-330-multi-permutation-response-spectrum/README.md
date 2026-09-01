# TPC-330 — Multi-permutation response spectrum

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-330 replaces the single TPC-329 placement null by five predeclared
source-multiset- and `L2`-preserving coordinate bijections.  Across the same
32-row source-native panel, all three nontrivial affine controls make the
all-plus off-diagonal Gram term positive on `32/32` rows, whereas identity and
reversal both retain the actual `31 negative / 1 positive` classification
census.  Thus the TPC-329 sign reversal is independently replicated by a
three-control affine family, while a geometrically different reversal control
does not cause it.

The result is a finite position-response spectrum, not a growing arithmetic
estimate.  It strengthens the placement-sensitivity obstruction but provides
no fixed-power credit or twin-prime conclusion.

## Frozen object

For

```text
I_(o,N) = {o,...,o+N/2-1},
o in {28001,36001},  N in {4096,8192},
Q in {24,36,54,80},  s in {1,2},  H=66,
```

the literal deleted-diagonal centered prime-shell block is

```text
B_p(u,t) = 1_(u!=t) 1_(p does not divide u) 1_(p does not divide t)
            p H^(2s)/(H^2+(u-t)^2)^s
            (1_(p divides u-t)-1/(p-1)).
```

For each of four fixed sign laws, `C_e=sum_p e_p B_p`.  The source is the
hash-locked finite V59 residual

```text
beta_o^(2)(t) = Lambda(t+2) - b^(2)(t),
b^(2)(t) = 2 C_2 1_(2 does not divide t)
             product_(p|t,p>2) (p-1)/(p-2).
```

The Euler product cutoff is `50000`; logarithms use the inherited 100-digit
midpoint protocol; the ratio guard is `5e-8`.  The five controls are frozen
before the certificate is read:

```text
identity:     pi_0(i)    = i
affine_3_11:  pi_3,11(i) = (3i+11) mod M
affine_5_17:  pi_5,17(i) = (5i+17) mod M
affine_7_29:  pi_7,29(i) = (7i+29) mod M
reversal:     pi_rev(i)  = M-1-i
```

Here `M=N/2` is `2048` or `4096`.  The odd affine multipliers are invertible
modulo `M`; all five maps are bijections and exactly preserve the source
multiset and Euclidean norm.

## Certified five-control spectrum

Each table entry is `negative / positive`; no row is unresolved.

| control | all-plus | alternating | mod-4 | half split |
|---|---:|---:|---:|---:|
| identity | 31 / 1 | 25 / 7 | 32 / 0 | 32 / 0 |
| affine `(3,11)` | 0 / 32 | 20 / 12 | 27 / 5 | 31 / 1 |
| affine `(5,17)` | 0 / 32 | 30 / 2 | 32 / 0 | 28 / 4 |
| affine `(7,29)` | 0 / 32 | 21 / 11 | 32 / 0 | 29 / 3 |
| reversal | 31 / 1 | 25 / 7 | 32 / 0 | 32 / 0 |

The three affine controls agree on a positive all-plus classification in
`32/32` rows.  Identity and reversal have the same all-plus classification in
`32/32` rows.  Relative to identity, each affine control changes `31/32`
all-plus classifications; their all-plus ratio ranges are respectively

```text
affine (3,11): [1.1086266653921864, 5.8662166822283597]
affine (5,17): [1.0796604870824567, 3.7402812188967256]
affine (7,29): [1.0729497333260283, 2.7548351258227446].
```

Across all five controls, the all-plus spectrum has `31` mixed-control rows
with signature `negative|positive|positive|positive|negative` and one
unanimously positive row.  The other laws have the following finite response
types:

| law | unanimous negative | unanimous positive | mixed |
|---|---:|---:|---:|
| all-plus | 0 | 1 | 31 |
| alternating | 17 | 0 | 15 |
| mod-4 | 27 | 0 | 5 |
| half split | 25 | 0 | 7 |

The certificate contains `640` law/control observations and all `10`
pairwise-control summaries.  Identity versus reversal changes no
classification among `128` law-level comparisons and has maximum ratio
difference `0.022723042898999735`; this is a finite observation, not an exact
reflection-invariance theorem.

## Exact finite layer

For any finite vector `v`,

```text
E_e(v) = ||C_e v||_2^2,
D_e(v) = sum_t v_t^2 ||C_e e_t||_2^2,
O_e(v) = E_e(v)-D_e(v),
E_e(v) = D_e(v)+O_e(v).
```

The last identity is a finite Gram expansion.  An exact rational anchor on
`[36001,36016]`, `Q=4`, `s=1` gives

```text
E = 306.7544239093389
D = 332.4445614235858
O = -25.69013751424689
```

with all three reduced-fraction digests independently replayed.

## Claim firewall

```text
PROVED_EXACT_FINITE = finite matrix formula; E=D+O; five bijections;
                      multiset/L2 preservation; exact rational anchor
PROVED_EXACT_FINITE_DECLARED_MODEL = finite V59 source-vector formula
NUMERICALLY_CERTIFIED_FINITE = 32 rows; 5 placement controls;
                               640 law/control observations;
                               10 pairwise summaries; 64 scale pairs
NUMERICAL_OBSERVATION = control-specific ratios, response signatures,
                        finite growth factors and slopes
REFUTED_SCOPED = source-multiset/L2-only determination of the all-plus sign;
                 single-affine-control accident on this frozen panel
MODELING_CHOICE = finite panel, four laws, five controls, H=66, cutoff,
                  float64 guard
OPEN = structural decomposition of the position response;
       source-uniform growing arithmetic L2; canonical sign law;
       strict 1/400 payment; full Gate B; twin-prime endpoint
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

The Session-named `propose.md` and Route-A/Route-B evaluator files are absent
from this checkout.  The proof package, independent replay, stress checker,
and local Bridge-B checker are therefore fallback controls; no official Route
pass is claimed.

## Reproduction

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-330-multi-permutation-response-spectrum/code/tpc330_multi_permutation_response_spectrum.py --check
python -O -B papers/tpc-330-multi-permutation-response-spectrum/code/tpc330_multi_permutation_response_spectrum.py --check
python -B papers/tpc-330-multi-permutation-response-spectrum/experiments/tpc330_independent_checker.py --check
python -O -B papers/tpc-330-multi-permutation-response-spectrum/experiments/tpc330_independent_checker.py --check
python -B papers/tpc-330-multi-permutation-response-spectrum/experiments/tpc330_multi_permutation_stress.py --check
python -O -B papers/tpc-330-multi-permutation-response-spectrum/experiments/tpc330_multi_permutation_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc330_multi_permutation_response_spectrum_checker.py --check
```

The canonical result is
[results/tpc330_certificate.json](results/tpc330_certificate.json), and the
compiled paper is [paper/paper.pdf](paper/paper.pdf).

## Package contents and next theorem

`PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, `paper/`,
`code/`, `experiments/`, `results/`, and `notes/` form the auditable package.
The next minimal problem is to decompose the finite response into a
control-average component and a position-aligned deviation, then test whether
that decomposition exposes a reusable structural bound.
