# TPC-212: Truncated Divisor Bands and the Reciprocal-Emitter Boundary Operator

## Result

TPC-211 proved an exact complete-packet `mu(d) log(d)` derivative for the
literal product-coupled Euler profiles, but left the physical band
`Y0<d<=U` and the divisor-dependent reciprocal emitter `A_d(r)` open.  TPC-212
isolates those two mechanisms.

For any squarefree active-prime set and any divisor selector `A`, the endpoint
coefficient of the cut packet is the signed Boolean incidence

```text
eta_p(A) = sum_(S in A, p in S) (-1)^|S|.
```

The complete packet has `eta_p=0` for every active prime.  A cut band need not:
for `t=35` and `5<d<=35`, the active divisors are `{7,35}` and
`eta=(1,0)`, so the logarithmic endpoint leakage is exactly `log(5)`.
The selected packet is exactly the complete packet minus the missing-subset
boundary, coefficientwise in the independent `log(p)` basis.

For a finite reciprocal fixture, let

```text
E_d(q,m -> r) = 1_{r = m q^{-1} (mod d)}.
```

The exact occupancy Gram identity is

```text
||E_d||_2^2
 = sum_(q1,m1,q2,m2) 1_{d | m1*q2 - m2*q1}.
```

When residual profiles are kept in the natural direct sum over divisors, the
emitter Gram is block diagonal and full rank.  A unit-weight aligned residual
fixture reaches coherent-to-diagonal ratios 2, 4, and 3 for the tested
divisor packets.  Therefore the cut and reciprocal map alone do not provide a
universal cross-divisor saving.

This is a scoped structural obstruction, not an arithmetic counterexample.
The physical `psi`, prime shell, literal residual coupling, and fixed-power
Gate-B estimate remain open.

## Claim firewall

```text
TPC212_ROUTE_ADVANCE = YES
TPC212_STRUCTURAL_THRESHOLD_A = PASS
TPC212_CUT_ENDPOINT_LEAKAGE = PROVED_EXACT
TPC212_BOUNDARY_DECOMPOSITION = PROVED_EXACT
TPC212_RECIPROCAL_COLLISION = PROVED_EXACT_FINITE
TPC212_EMITTER_GRAM = PROVED_EXACT_BLOCK_DIAGONAL
TPC212_EMITTER_ONLY_UNIVERSAL_SAVING = REFUTED_SCOPED
TPC212_LITERAL_PHYSICAL_BOUNDARY_BOUND = OPEN
TPC212_PHYSICAL_CROSS_DIVISOR_GRAM_BOUND = OPEN
TPC212_ARITHMETIC_ADVANCE = NO
TPC212_FIXED_ATOM_CREDIT = 0
TPC212_L2 = NONE
TPC212_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

## Project layout

```text
README.md
PAPER_PLAN.md
paper/main.tex
paper/references.bib
paper/paper.pdf
code/boundary_emitter.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/boundary_sanity.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```

## Reproduce

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-212-truncated-boundary-emitter/experiments/run_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-212-truncated-boundary-emitter/experiments/independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B papers/tpc-212-truncated-boundary-emitter/experiments/independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-212-truncated-boundary-emitter/experiments/boundary_sanity.py
```

The finite certificate uses exact integer and rational arithmetic.  Its
reciprocal fixture takes `psi=1` on the finite `(q,m)` set; this is explicitly
a modeling choice for the emitter algebra and is not a claim about the smooth
physical weight.

Author: Liang Wang, Huazhong University of Science and Technology.
