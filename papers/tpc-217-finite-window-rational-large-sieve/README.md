# TPC-217: Finite-Window Attachment by Reduced Rational-Frequency Large Sieve

## Result

TPC-216 controlled the complete-period direct-sum row energy but left the
literal physical interval open.  TPC-217 keeps the same common-source kernel,
regroups it exactly by reduced rational frequencies, and applies the additive
large sieve at spacing `delta >= U^(-2)`.

For `I_x=(x/2,x] intersect Z` and `N=|I_x|`, the resulting structural bound is

```text
N^(-1) sum_(n in I_x)|K(n)|^2
  <<_psi x^(11/32)(log x)^5.
```

The unnormalized finite-window exponent is `43/32+o(1)`.  The `U^2` spacing
term is lower order because `U^2/x=x^(-67/200)`.

Release QA is complete: `paper/paper.pdf` is 5 pages with all fonts embedded;
the final LaTeX pass has no warning, undefined-reference, or undefined-citation
markers.  The independent certificate, optimized checker, frequency-crowding
adversary, and the pre-release 47-pair Bridge-B regression all pass.

## Claim firewall

```text
TPC217_ROUTE_ADVANCE = YES
TPC217_STRUCTURAL_THRESHOLD_A = PASS
TPC217_REDUCED_FREQUENCY_REGROUPING = PROVED_EXACT
TPC217_FAREY_SPACING = PROVED_EXACT
TPC217_ADDITIVE_LARGE_SIEVE = PROVED_STANDARD
TPC217_FINITE_WINDOW_ATTACHMENT = PROVED_X_11_OVER_32_LOG_FIVE_NORMALIZED
TPC217_UNNORMALIZED_WINDOW_EXPONENT = PROVED_43_OVER_32
TPC217_WINDOW_LOSS = PROVED_1_PLUS_U2_OVER_N
TPC217_FINITE_WINDOW_OFF_FREQUENCY_GRAM = CONTROLLED_BY_LARGE_SIEVE
TPC217_ALIGNED_ONE_POINT_ORTHOGONALITY = REFUTED_SCOPED
TPC217_PRIME_SHELL_REASSEMBLY = OPEN
TPC217_FOUR_PACKET_SIGNED_REASSEMBLY = OPEN
TPC217_ARITHMETIC_CANCELLATION = NONE
TPC217_ARITHMETIC_ADVANCE = NO
TPC217_FIXED_ATOM_CREDIT = 0
TPC217_L2 = NONE
TPC217_FULL_GATE_B = OPEN
TPC217_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

The standard large sieve is used as a named input.  The new Session result is
the exact attachment of that input to the TPC common-source object and the
exponent ledger, not a new prime-distribution theorem.

## Finite certificate

The fixture uses `Q={11,13,17}`, `H=40`, the squarefree family in `(2,35]`,
and `psi(t)=(1+t^2)^(-2)`.  It checks 14 active divisors, 16 reduced
denominators, three translated windows, and exact pointwise agreement between
the original divisor expansion and the reduced-frequency expansion.

The separate aligned-shell adversary uses `d=5`, `H=500`, and
`q={101,131,151,181}`.  A one-point window has exact coherent-to-diagonal ratio
`2`; this is a scoped obstruction to free finite-window orthogonality.

## Layout

```text
README.md
DERIVATION_PACKAGE.md
PAPER_PLAN.md
PROOF_PACKAGE.md
paper/main.tex
paper/references.bib
paper/paper.pdf
code/finite_window_attachment.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/frequency_crowding.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```

## Reproduce

```bash
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-217-finite-window-rational-large-sieve/experiments/run_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-217-finite-window-rational-large-sieve/experiments/independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B papers/tpc-217-finite-window-rational-large-sieve/experiments/independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-217-finite-window-rational-large-sieve/experiments/frequency_crowding.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B papers/tpc-217-finite-window-rational-large-sieve/experiments/frequency_crowding.py --check
PYTHONDONTWRITEBYTECODE=1 python -B research/tpc-big-road/tpc_bridge_b_finite_window_rational_large_sieve_checker.py --check
```

Author: Liang Wang, Huazhong University of Science and Technology.
