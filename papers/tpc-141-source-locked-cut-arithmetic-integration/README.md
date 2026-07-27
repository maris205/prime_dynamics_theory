# TPC-141: Source-locked cut/arithmetic integration

Paper title:

> *Source-Locked Integration at the First Unsupported Carrier:
> Cut Archives, Arithmetic Shadows, and a Nonduplicated \(1/400\)
> Ledger*

## Core result

TPC-133--136 give an exact cut decomposition

```text
B_h0,delta = S_soft + S_eligible + S_frontier.
```

The eligible-prefix term is imported as a complete original-scale
`o(X)` term.  The eligible tail is attached to the arithmetic route,
while the frontier remains explicitly unmapped.  Consequently the
paper proves the cut-aware conditional bound

```text
|B_h0,delta|
  <= o(X) + |S_frontier|
     + X^(1-sigma_eligible+Lambda_eligible+o(1)).
```

It never deletes or relabels the frontier.
The three-way cut is complete only as a partition of the declared cut
archive; it is not a totalized full-carrier H1 certificate.

TPC-137--140 supply a fixed-form logarithmic arithmetic shadow and a
proved small-polylog affine power-of-log estimate outside a small
logarithmic-density exceptional set, together with scoped
non-transfer and selector firewalls and a conditional power-ledger
interface. The new estimate is a restricted positive arithmetic
shadow. Actual CRT-family containment, squarefree/periodic reassembly,
local exceptional-set control on every terminal window, deterministic
prefixes, and a fixed \(X\)-power saving remain open. A global
cumulative logarithmic-density estimate is not silently reused as a
same-rate terminal-window estimate.
Both logarithmic inputs have exponent zero on the fixed \(X\)-power
ledger; that is not a lower obstruction to a future actual-family
power saving.

## Machine certificate

The deterministic standard-library audit:

- content-hashes TPC-133--140 for drift detection only--a matching
  hash is not evidence that a theorem or generator is correct;
- source-locks imports and exports by scope, carrier, and
  normalization;
- distinguishes proof imports from shadow-only evidence;
- validates the proof DAG and its explicit topological order;
- checks the exact terminal-role cover;
- keeps four tail namespaces disjoint;
- validates an occurrence-level physical registry with acyclic,
  nonoverlapping joint replacements;
- refuses to fill unknown physical costs with zero;
- keeps the H5 determinant reserve out of the physical ledger;
- rejects direct or indirect arithmetic dependencies in H9; and
- records the first missing node as `H1.frontier_totalization`.

`PASS` means that this certificate format and frozen snapshot are
internally consistent.  It is not `GO`, not a positive L2 result, and
not numerical evidence for a prime-pair theorem.

## Reproduce

```powershell
python experiments/tpc141_batch_integration_audit.py
python experiments/tpc141_batch_integration_audit.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Generated artifacts:

```text
experiments/tpc141_batch_manifest.json
experiments/tpc141_batch_integration_audit.json
```

Stable archival PDF:

`tpc-141-source-locked-cut-arithmetic-integration.pdf`
