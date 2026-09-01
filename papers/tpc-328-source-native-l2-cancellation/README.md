# TPC-328 — Source-native arithmetic `L2` cancellation and the finite signed-Gram obstruction

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

The actual finite V59 source vector

```text
beta_o^(2)(t) = Lambda(t+2) - b^(2)(t)
```

was inserted into the literal deleted-diagonal prime-shell operator and its
source-coordinate Gram decomposition was replayed on `96` rows (three origins,
four nested scales, four shell anchors, and two kernel exponents).  For the
all-plus law, the off-diagonal contribution is negative on `81/96` rows and
positive on `15/96`; the positive and negative cases are both separated from
zero by the declared `5e-8` ratio guard.  The two positive component controls
(`Lambda(t+2)` and `b^(2)(t)`) are positive on all `96/96` rows.

This is the first release in the current line that applies the coherent
operator to the source-native arithmetic residual itself.  It is a finite
signed-Gram atlas and a scoped obstruction to a uniform contraction claim for
the four declared sign laws.  It is not a growing arithmetic `L2` theorem.

## Frozen finite object

For `I_(o,N)={o,...,o+N/2-1}`, `o` in `{12001,16001,20001}` and
`N` in `{320,640,1280,2560}`, let

```text
B_(p,Q,s)(u,t) = 1_(u!=t) 1_(p does not divide u t)
                 p H^(2s)/(H^2+(u-t)^2)^s
                 (1_(p divides u-t)-1/(p-1)),  H=66.
```

For a predeclared sign law `e` on the shell `(Q,2Q]`,
`C_e=sum_p e_p B_p`.  The four laws are `all_plus`, `alternating_index`,
`mod4_character`, and `half_split`; `Q={24,36,54,80}` and `s={1,2}`.

The source model is the locked finite V59 comparison model:

```text
Lambda(m) = log p       if m=p^k,
             0          otherwise,

b^(2)(t) = 2 C_2 1_(2 does not divide t)
            product_(p|t,p>2) (p-1)/(p-2).
```

The Euler product is evaluated through `50000`, with the declared positive
tail multiplier `1-1/(50000-1)` and a high-precision logarithm enclosure.
The producer stores midpoint values; the source identity and all finite
formulae are retained explicitly so this modeling choice cannot be confused
with an asymptotic twin-prime theorem.

## Exact finite identity

For every finite vector `v`,

```text
E_e(v) = ||C_e v||_2^2
D_e(v) = sum_t v_t^2 ||C_e e_t||_2^2
O_e(v) = E_e(v)-D_e(v)
       = sum_(t != t') v_t v_t' <C_e e_t,C_e e_t'>.
```

Thus `O_e` is exactly the source-coordinate off-diagonal Gram term.  A ratio
`E_e(v)/D_e(v)<1` means cancellation in this decomposition; a ratio above one
means a positive off-diagonal contribution.  This finite identity is proved
algebraically.  The reported ratios are guarded numerical replays, not
interval claims about a growing family.

## Main finite readout

| law | negative off-diagonal | positive off-diagonal | unresolved |
|---|---:|---:|---:|
| all-plus | 81 | 15 | 0 |
| alternating index | 73 | 23 | 0 |
| mod-4 character | 74 | 22 | 0 |
| half split | 61 | 35 | 0 |

Across all laws and rows, the all-plus residual ratio lies in
`[0.15702348685234854, 1.4021661919173145]`.  The all-plus component-control
ratios have minima `1.4345187728485156` for the von-Mangoldt component and
`3.1071920015130248` for the comparison component.  These controls are
positive on every row, so the residual sign changes are not caused by a zero
energy component or an unresolved ratio.

At the exact rational anchor `[20001,20016]`, `Q=4`, `s=1`, the shell is
`{5,7}` and the source vector is
`1_(t+2 is prime)-1_(t is odd)`.  The exact finite values are approximately

```text
E = 673.6882555385803
D = 576.5224534951882
O =  97.16580204339213
```

The certificate records numerator/denominator digests for all three values and
checks `E=D+O` over `Fraction` arithmetic.  The anchor contains the local
twin-prime indicator at `t=20009`, but makes no claim about its asymptotic
frequency.

## Claim firewall

```text
PROVED_EXACT_FINITE = source-coordinate Gram decomposition;
                      literal finite matrix formula;
                      exact rational anchor identity
PROVED_EXACT_FINITE_DECLARED_MODEL = finite V59 source-vector formula
NUMERICALLY_CERTIFIED_FINITE = 96-row four-law replay;
                               81/96 all-plus cancellation;
                               15/96 all-plus positive obstruction;
                               96/96 positive component controls
REFUTED_SCOPED = no uniform contraction for the four declared laws on this
                 finite panel
NUMERICAL_OBSERVATION = ratio ranges and finite row census
MODELING_CHOICE = three origins, four scales, Q anchors, H=66, tail cutoff 50000
OPEN = growing source-native arithmetic L2 estimate; canonical sign law;
       source-uniformity; full Gate B; strict 1/400 payment
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

The Session-named `propose.md` and Route-A/Route-B evaluator files are absent
from this checkout.  `notes/route_evaluation.md`, the proof package, the
independent checker, the stress suite, and the local Bridge-B checker are
fail-closed fallbacks; no official evaluator pass is asserted.

## Reproduction

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-328-source-native-l2-cancellation/code/tpc328_source_native_l2_cancellation.py --write
python -B papers/tpc-328-source-native-l2-cancellation/code/tpc328_source_native_l2_cancellation.py --check
python -O -B papers/tpc-328-source-native-l2-cancellation/code/tpc328_source_native_l2_cancellation.py --check
python -B papers/tpc-328-source-native-l2-cancellation/experiments/tpc328_independent_checker.py --check
python -O -B papers/tpc-328-source-native-l2-cancellation/experiments/tpc328_independent_checker.py --check
python -B papers/tpc-328-source-native-l2-cancellation/experiments/tpc328_source_native_l2_stress.py --check
python -O -B papers/tpc-328-source-native-l2-cancellation/experiments/tpc328_source_native_l2_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc328_source_native_l2_cancellation_checker.py --check
```

The canonical machine-readable result is
[results/tpc328_certificate.json](results/tpc328_certificate.json), and the
compiled manuscript is [paper/paper.pdf](paper/paper.pdf).

## Package contents

`PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, `notes/`,
`code/`, `experiments/`, `results/`, and `paper/` form the auditable project
package.  The next natural question is whether this source-native sign atlas
survives a held-out growing origin/scale family or whether a structural
off-diagonal obstruction can be proved before enlarging the panel.
