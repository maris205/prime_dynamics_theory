# TPC-193: Literal fixed-atom candidate-mechanism gate

## Exact result

TPC-193 reviews a declared, source-locked theorem corpus for a mechanism that
acts directly on the determinant-two two-Möbius coefficients at a prescribed
atom and preserves all six MVP9 axes.

```text
primary_source_records = 7
direct_candidates = 2
eligible_candidates = 0

verdict = NO_ELIGIBLE_MECHANISM_IN_DECLARED_CORPUS
target_contract = NOT_TESTABLE_FORMULA_INCOMPLETE
gate_first_missing = DIRECT_TARGET_SUMMATION_DOMAIN_AND_PREFIX_INDEX
arithmetic_first_missing = LITERAL_FIXED_ATOM_ARITHMETIC_CANCELLATION
next_action = USER_CONFIRMATION_REQUIRED
```

The two direct theorem-backed candidates are:

1. Teräväinen–Walker, Lemma 4.2(1): every fixed additive atom on a
   fixed nonparallel two-Möbius affine pair, but only in a qualitative
   logarithmic average;
2. Tao–Teräväinen, Theorem 3.1, through the TPC-149/TPC-158 periodic
   reassembly: a natural `q/N` shell estimate at a source-backed rational
   atom, but only outside exceptional scales and with logarithmic saving.

Neither supplies a natural all-prefix, all-scale fixed-`X` power theorem on
the actual active packet.

The gate also finds a formula-level contract blocker. TPC-167 writes the
direct transform on the terminal block `N < t(z) <= 2N`; TPC-159 writes
the cumulative domain `0 < t(z) <= T` with `q/T` normalization for a
periodic multiplier, and TPC-184 freezes the cumulative actual-core object
as the prescribed-atom bad-endpoint contract. The audited bad-endpoint
formula combines the TPC-159 domain with the TPC-167 additive-character
convention. TPC-183 and TPC-189 do not write a direct-prefix summation
domain that makes the block and cumulative formulas identical. The named
atom, packet schedule, admissible ranges, uniform constant, exponent, and
physical loss ledger are also absent. Therefore the old `direct => bad`
statement is not imported here as formula-certified.

This is a scoped corpus exhaustion and a fail-closed L1 audit. It is not a
claim that no mathematical mechanism exists. Both O161 pointwise parents
remain open, the architecture is not stopped, fixed-atom endpoint credit is
zero, and the strict `1/400` budget is unpaid. Per `TPC_HANDOFF.md`, no
TPC-194 paper is created before user confirmation.

## Reproduce

From the repository root:

```powershell
$paper = 'papers/tpc-193-literal-fixed-atom-candidate-mechanism-gate'
$stem = 'tpc193_literal_fixed_atom_candidate_mechanism_gate'

python "$paper/experiments/$stem.py"
python "$paper/experiments/$stem.py" --check

Push-Location $paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
Copy-Item -LiteralPath main.pdf `
  -Destination 'tpc-193-literal-fixed-atom-candidate-mechanism-gate.pdf' `
  -Force
Pop-Location
```
