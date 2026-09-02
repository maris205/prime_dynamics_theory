# TPC-347 — Convolution interface and the divisibility-mask defect

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-347 separates the locked literal prime-shell operator into an unmasked
translation-invariant convolution and an explicit divisibility-mask defect.
For every finite interval compression, the identity

```text
A_I = T_I + D_I,
T_I = R_I K_e E_I,
D_I = A_I - T_I
```

is exact.  The unmasked kernel has the standard Fourier interface

```text
||K_e||_(ell^2(Z)->ell^2(Z)) = ess sup_theta |khat_e(theta)|
```

and a Young majorant.  On two disjoint origins, three source counts, four
shell anchors, two exponents, and four predeclared sign laws, the finite
certificate contains `192` rows and `96/96` translation-invariance checks for
the ideal operator.  The mask defect-to-ideal spectral ratio ranges from
`0.0312337689685` to `0.467075645603`; `93/192` rows exceed `1/4`.

Thus the divisibility masks cannot be silently discarded on the declared
panel.  This is a precise interface and a finite obstruction to one tempting
shortcut, not a source-uniform arithmetic `L2` theorem.

## What is new

* The physical entry is written as `R_I P_p K_p P_p E_I`, with the two
  endpoint masks retained separately from the residue kernel.
* The unmasked coherent sum is proved to be a convolution, so its `ell^2`
  norm is controlled by a Fourier multiplier rather than by a Frobenius
  proxy.
* An explicit tail majorant gives a reproducible Young envelope for every
  declared shell/sign law.
* A disjoint two-origin, three-scale spectral audit measures the defect and
  proves finite translation invariance of the ideal comparison object.

## Claim firewall

```text
PROVED_EXACT_FINITE_DECLARED_MODEL = mask factorisation; convolution identity;
                                     Fourier multiplier norm interface;
                                     compression and triangle inequalities
NUMERICALLY_CERTIFIED_FINITE = 192 spectral rows; 96 ideal translation checks;
                               192 combined-envelope checks; exact rational anchor
REFUTED_SCOPED = discarding the divisibility masks as a uniformly negligible
                 finite-panel operation
NUMERICAL_OBSERVATION = defect/ideal ratio range and origin dependence of D_I
OPEN = source-uniform arithmetic L2; uniform masked operator bound; canonical
       sign law; fixed-power payment; full Route-B Gate B; twin-prime endpoint
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

The Fourier statement concerns the explicitly defined unmasked kernel.  The
finite mask defect is not replaced by that kernel, and no numerical row is an
asymptotic estimate.  The Session-named `propose.md` and Route-A/Route-B
evaluator files are absent from this checkout; `notes/route_evaluation.md`
records the available fail-closed local assessment.

## Reproduction

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-347-convolution-mask-defect-interface/code/tpc347_convolution_mask_defect_interface.py --write
python -B papers/tpc-347-convolution-mask-defect-interface/code/tpc347_convolution_mask_defect_interface.py --check
python -O -B papers/tpc-347-convolution-mask-defect-interface/code/tpc347_convolution_mask_defect_interface.py --check
python -B papers/tpc-347-convolution-mask-defect-interface/experiments/tpc347_independent_checker.py --check
python -O -B papers/tpc-347-convolution-mask-defect-interface/experiments/tpc347_independent_checker.py --check
python -B papers/tpc-347-convolution-mask-defect-interface/experiments/tpc347_mask_defect_stress.py
python -O -B papers/tpc-347-convolution-mask-defect-interface/experiments/tpc347_mask_defect_stress.py
python -B research/tpc-big-road/tpc_bridge_b_tpc347_convolution_mask_defect_interface_checker.py --check
```

The canonical machine-readable result is
[results/tpc347_certificate.json](results/tpc347_certificate.json), and the
compiled manuscript is [paper/paper.pdf](paper/paper.pdf).

## Package contents

`PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, `notes/`,
`code/`, `experiments/`, `results/`, and `paper/` form the auditable project
package.  The next route question is whether a position-aware lower witness
can show that the mask defect remains necessary, or whether a canonical
source-native projection controls it.
