# TPC-211: Product-Coupled Euler Profiles and the Mobius-Logarithmic Gram Constraint

## Result

TPC-211 answers the physical-coupling question left open by TPC-210 at the
finite structural level.  The V46 local profiles are not independent: for a
squarefree divisor (d_S),

```text
Delta_S = product_(p in S) F_p - product_(p in S) G_p.
```

After lifting every divisor profile to the common CRT space modulo
(M=product p), the nonempty family `Delta_S` is nevertheless linearly
independent.  Its dimension is exactly the number of nonempty squarefree
divisors.  Thus literal product coupling does not by itself create a
low-rank Gram saving.

The paper also proves an exact positive identity.  On a complete divisor
packet, the physical transition weight `mu(d) log(d)` compresses the whole
Boolean divisor lattice to a sum of marked-prime Euler derivative atoms:

```text
sum_S mu(d_S) log(d_S) Delta_S
  = -sum_p log(p) [ F_p product_(r != p)(1-F_r)
                    - G_p product_(r != p)(1-G_r) ].
```

The common endpoint term cancels exactly for packets with at least two active
primes.  This is the reusable route advance.  The actual transition window is
not a complete packet: the lower/upper divisor cut and reciprocal emitter
leave a boundary remainder that is not bounded here.

Finally, because the literal product defects are full rank, a shared finite
endpoint surrogate can be chosen by Gram duality so that

```text
<w, Delta_S> = mu(d_S)
```

for every divisor in a finite packet.  This is a scoped obstruction to any
saving theorem based only on product coupling, rank, or a common endpoint.  It
is not an arithmetic counterexample to the literal Lambda sequence.

## Claim firewall

```text
TPC211_ROUTE_ADVANCE = YES
TPC211_STRUCTURAL_THRESHOLD_A = PASS
TPC211_PRODUCT_COUPLING_COCYCLE = PROVED_EXACT
TPC211_LITERAL_PRODUCT_PROFILE_FULL_RANK = PROVED_EXACT
TPC211_LOG_MOBIUS_PACKET_DERIVATIVE = PROVED_EXACT
TPC211_COMPLETE_PACKET_ENDPOINT_CANCELLATION = PROVED_EXACT
TPC211_SHARED_ENDPOINT_ALIGNMENT = PROVED_STRUCTURAL_FINITE
TPC211_PRODUCT_COUPLING_UNIVERSAL_SAVING = REFUTED_SCOPED
TPC211_TRANSITION_BOUNDARY_CONTROL = OPEN
TPC211_PHYSICAL_CROSS_DIVISOR_GRAM_BOUND = OPEN
TPC211_ARITHMETIC_ADVANCE = NO
TPC211_FIXED_ATOM_CREDIT = 0
TPC211_L2 = NONE
TPC211_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

## Project layout

```text
README.md
PAPER_PLAN.md
paper/main.tex
paper/references.bib
paper/paper.pdf
code/product_coupled.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/product_rank_sanity.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```

## Reproduce

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-211-product-coupled-euler-gram/experiments/run_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-211-product-coupled-euler-gram/experiments/independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B papers/tpc-211-product-coupled-euler-gram/experiments/independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-211-product-coupled-euler-gram/experiments/product_rank_sanity.py
```

The certificate uses exact rational arithmetic for the prime sets
`(5,7)`, `(5,7,11)`, and `(5,7,11,13)`.  It covers 25 profile rows, 77,875
CRT residue coordinates, 9 marked-prime derivative rows, three nonzero Gram
determinants, and three shared-endpoint alignment constructions.  These are
finite structural checks, not asymptotic prime-distribution evidence.

Author: Liang Wang, Huazhong University of Science and Technology.
