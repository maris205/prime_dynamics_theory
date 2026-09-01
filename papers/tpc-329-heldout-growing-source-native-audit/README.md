# TPC-329 — Held-out growing source-native audit and placement sensitivity

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

The source-native finite V59 residual was evaluated on two previously unused
origins (`28001`, `36001`) and two larger scales (`4096`, `8192`).  On the
actual source vector, the all-plus off-diagonal Gram term was negative on
`31/32` rows and positive on `1/32`; on a fixed affine permutation preserving
the source multiset and its `L2` norm, it was positive on `32/32` rows.  The
classification changed on `31/32` all-plus comparisons.  This is a finite
placement-sensitivity obstruction: the observed sign is not determined by the
source norm or coordinate multiset alone.

The two-scale energy audit gives `64` paired comparisons.  All-plus signs
persist in `15/16` pairs, with one crossing; the all-plus energy growth factor
lies in `[1.9663131482417533, 2.14326466572482]`, corresponding to a base-2
slope in `[0.97549309860589706, 1.0998100153677246]`.  These are finite
observations, not a growing arithmetic estimate.

## Frozen object and protocol

For `I_(o,N)={o,...,o+N/2-1}`, `o` in `{28001,36001}` and `N` in
`{4096,8192}`, define the literal deleted-diagonal block

```text
B_p(u,t) = 1_(u!=t) 1_(p does not divide u) 1_(p does not divide t)
            p H^(2s)/(H^2+(u-t)^2)^s
            (1_(p divides u-t)-1/(p-1)),  H=66.
```

For each shell anchor `Q` in `{24,36,54,80}`, exponent `s` in `{1,2}`, and
declared sign law `e`, set `C_e=sum_p e_p B_p`.  The source is the locked
finite model

```text
beta_o^(2)(t) = Lambda(t+2) - b^(2)(t),
b^(2)(t) = 2 C_2 1_(2 does not divide t)
             product_(p|t,p>2) (p-1)/(p-2).
```

The Euler product is cut off at `50000`, with the inherited positive tail
enclosure; logarithms use the inherited 100-digit midpoint protocol.  The
ratio guard is `5e-8`.  There are `2*2*4*2=32` rows.

The hostile control is fixed before reading the result:

```text
pi(i) = (5*i + 17) mod source_count.
```

Since each source count is a power of two, multiplication by `5` is invertible
modulo the count.  Thus the control is a bijection and preserves the exact
source multiset and the Euclidean `L2` norm, while generally changing the
coordinate placement relative to the physical matrix.

## Certified finite readout

| law | actual negative | actual positive | permuted negative | permuted positive |
|---|---:|---:|---:|---:|
| all-plus | 31 | 1 | 0 | 32 |
| alternating index | 25 | 7 | 30 | 2 |
| mod-4 character | 32 | 0 | 32 | 0 |
| half split | 32 | 0 | 28 | 4 |

No actual or permuted row is unresolved under the declared guard.  The
all-plus placement control changes the classification on `31/32` rows and has
maximum absolute ratio difference `3.1669505870381451`; the corresponding
maximum differences are `0.2512622344035258`, `0.21527386205638832`, and
`0.1981450927371966` for alternating, mod-4, and half-split laws.

The component controls remain positive on all `32/32` rows.  Their minimum
all-plus ratios are `1.3668932693626414` for `Lambda(t+2)` and
`3.0441001012913311` for the comparison component.

## Exact and independent checks

The finite identity

```text
E_e(v) = D_e(v) + O_e(v)
```

is proved by finite Gram expansion.  An exact rational anchor on
`[28001,28016]`, `Q=4`, `s=1`, uses
`1_(t+2 is prime)-1_(t is odd)` and records the following displayed values:

```text
E = 582.0014930371829
D = 649.9719408544561
O = -67.97044781727324
```

The producer, independent reverse-order checker, stress suite, and local
Bridge-B checker all verify the canonical JSON, parent hashes, row geometry,
growth pairing, permutation metadata, exact-anchor digests, and fail-closed
claim firewall.  The Session-named `propose.md` and Route-A/Route-B evaluator
files are absent from this checkout, so no official evaluator pass is claimed.

## Claim firewall

```text
PROVED_EXACT_FINITE = literal finite matrix formula;
                      E=D+O Gram decomposition;
                      exact rational anchor identity
PROVED_EXACT_FINITE_DECLARED_MODEL = finite V59 source-vector formula
NUMERICALLY_CERTIFIED_FINITE = 32-row actual/permuted replay;
                               64 growth pairs;
                               128 placement comparisons;
                               positive component controls
NUMERICAL_OBSERVATION = finite growth factors, slopes, and ratio ranges
REFUTED_SCOPED = source-multiset/L2-only explanation of the all-plus sign;
                 uniform contraction for the actual four-law panel
MODELING_CHOICE = origins, scales, shells, H=66, cutoff, affine permutation,
                  float64 guard
OPEN = source-uniform growing L2 estimate; canonical sign law;
       placement-aware reassembly theorem; strict 1/400 payment;
       full Gate B; twin-prime endpoint
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

The placement control does **not** prove that the actual arithmetic vector has
an asymptotic property; it only shows that this finite diagnostic is sensitive
to coordinate placement.  The next natural problem is to separate
arithmetic-placement information from source-norm information with multiple
predeclared controls or a structural theorem.

## Reproduction

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-329-heldout-growing-source-native-audit/code/tpc329_heldout_growing_source_native_audit.py --check
python -O -B papers/tpc-329-heldout-growing-source-native-audit/code/tpc329_heldout_growing_source_native_audit.py --check
python -B papers/tpc-329-heldout-growing-source-native-audit/experiments/tpc329_independent_checker.py --check
python -O -B papers/tpc-329-heldout-growing-source-native-audit/experiments/tpc329_independent_checker.py --check
python -B papers/tpc-329-heldout-growing-source-native-audit/experiments/tpc329_heldout_growing_stress.py --check
python -O -B papers/tpc-329-heldout-growing-source-native-audit/experiments/tpc329_heldout_growing_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc329_heldout_growing_source_native_audit_checker.py --check
```

The canonical machine-readable result is
[results/tpc329_certificate.json](results/tpc329_certificate.json), and the
compiled manuscript is [paper/paper.pdf](paper/paper.pdf).

## Package contents

`PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, `notes/`,
`code/`, `experiments/`, `results/`, and `paper/` form the auditable project
package.  This paper is a held-out validation and obstruction stage after
TPC-328; it does not create fixed-power credit or a twin-prime conclusion.
