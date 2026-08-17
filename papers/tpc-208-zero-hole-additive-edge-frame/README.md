# TPC-208: Zero-Hole Additive Edge Frame

## Result

This project identifies the exact additive-frequency geometry of the
standard-zero-hole reduced-residue Barban--Davenport--Halberstam remainder.
For a prime `q`, write

```text
y = (A_hat(k))_(k != 0),
P = I - 1/(q-1) 11*,
Delta_(k,l)(n) = e_q(-kn)-e_q(-ln).
```

Then

```text
V_0(a;v) = 1/q y* P y
         = 1/[q(q-1)] sum_{{k,l} in E(K_(q-1))}
             |sum_n a_n e(vn/H) Delta_(k,l)(n)|^2.
```

The complete graph has `(q-1)(q-2)/2` edges and projection rank `q-2`.
Its edge mass is

```text
sum_e |Delta_e(n)|^2 = q(q-2) 1_(q does not divide n),
```

so the mandatory `(q-2)/(q-1)` coefficient diagonal distributes over the
same cells exactly.  With

```text
E_e^circ[a]
  = |sum_n a_n e(vn/H) Delta_e(n)|^2
    - sum_n |a_n|^2 |Delta_e(n)|^2,
```

every edge cell is purely coefficient-off-diagonal and

```text
q R_0(a;v) = 1/(q-1) sum_e E_e^circ[a](v).
```

The four-packet V59 polarization holds edge by edge.  The resulting physical
kernel is zero on a nonunit coordinate, `q(q-2)` on equal nonzero residues,
and `-q` on distinct nonzero residues, reproducing the frozen V59 scalar
without a normalization change.

Finally, if the projection is represented by scalar-weighted literal edge
vectors `e_k-e_l`, every off-diagonal matrix entry forces the unique weight
`1/(q-1)` on every edge.  No strict edge subset can represent the projection
in this class.  This does not rule out dense bases or a theorem that estimates
the complete frame jointly.

## Claim firewall

```text
V61_ROUTE_ADVANCE=YES
V61_STRUCTURAL_THRESHOLD_A=PASS
V61_ZERO_HOLE_ADDITIVE_EDGE_FRAME=PROVED_EXACT
V61_CELLWISE_Q_MINUS_2_DIAGONAL_CANCELLATION=PROVED_EXACT
V61_TWO_FREQUENCY_NO_SPARSIFICATION=PROVED_EXACT_IN_LITERAL_EDGE_CLASS
V61_FULL_GATE_B_STRICT_1_OVER_400=UNPAID
V61_ARITHMETIC_ADVANCE=NO
V61_FIXED_ATOM_CREDIT=0
V61_L2=NONE
V61_TPC_208_TRIGGER=true
```

This is `PROVED_STRUCTURAL_L1`.  It is not a Kloosterman attachment, a
prime-shell power saving, full Gate B, an arithmetic advance, an `L^2`
theorem, fixed-atom credit, or a twin-prime theorem.  The first remaining
fatal gate is a theorem that transforms the complete oriented `(d,k)` frame
of the literal block packets into source-valid Kloosterman cells and
reassembles blocks, packet signs, and prime moduli with a fixed saving.

## Project layout

```text
README.md
PAPER_PLAN.md
paper/main.tex
paper/references.bib
paper/paper.pdf
code/additive_edge.py
experiments/run_certificate.py
experiments/independent_checker.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```

## Reproduce the exact certificate

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-208-zero-hole-additive-edge-frame/experiments/run_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-208-zero-hole-additive-edge-frame/experiments/independent_checker.py --check
```

To regenerate the canonical JSON:

```bash
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-208-zero-hole-additive-edge-frame/experiments/run_certificate.py --write
```

The producer and independent checker use separate implementations.  They
verify 431 exact finite rows over `q=2,3,5,7,11`; these rows are QA artifacts,
not proof of the general theorems.

## Compile the paper

Compile in an external scratch directory so LaTeX intermediates do not enter
the repository:

```bash
scratch=$(mktemp -d)
cp papers/tpc-208-zero-hole-additive-edge-frame/paper/main.tex "$scratch/"
cp papers/tpc-208-zero-hole-additive-edge-frame/paper/references.bib "$scratch/"
cd "$scratch"
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Author: Liang Wang, Huazhong University of Science and Technology.
