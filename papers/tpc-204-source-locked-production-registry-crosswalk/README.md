# TPC-204: Source-Locked Production Registry Crosswalks

## Exact result

TPC-204 audits a fixed, source-locked corpus of nine distinct plausible
production-crosswalk objects.  Every object is checked against all seven
production axes and against the three noninterchangeable formula types frozen
by TPC-194.

```text
classification = PRODUCTION_REGISTRY_CROSSWALK_CENSUS_L1
verdict = FIRST_MISMATCH_CERTIFIED_NOT_TESTABLE
declared_candidate_count = 9
production_axis_cells = 63
formula_crosswalk_cells = 27
complete_crosswalk_count = 0
first_common_missing_production_axis = named_production_atom
direct_trigger = FAIL
```

The nine audited objects are:

1. the empty `H9.phase_cell_registry` slot from TPC-180;
2. the TPC-159/TPC-193 rational terminal-block theorem;
3. the TPC-159 dyadic-shadow cumulative prefix;
4. the TPC-167 phase-\(L^2\) direct transform;
5. the TPC-183 `N=T` specialization proposal;
6. the verbal TPC-184 bad-endpoint fixed-atom contract;
7. the verbal TPC-189 direct fixed-atom contract;
8. the Teräväinen--Walker logarithmically weighted affine theorem; and
9. the TPC-194 resolved physical packet prefix.

For every row, the first production-axis mismatch is the absence of a
source-locked named production atom.  Native formula data, fixed phases,
implicit constants, logarithmic savings, or phase-\(L^2\) bounds are retained
in the audit but receive no production-crosswalk credit.

The three formula objects remain distinct:

```text
CORE_TERMINAL_BLOCK
  domain = N<t(z)<=2N
  normalization = q/N

CORE_CUMULATIVE_PREFIX
  domain = 0<t(z)<=T
  normalization = q/T

PHYSICAL_PACKET_PREFIX
  domain = z in I_xi_X and z<=T
  normalization = UNNORMALIZED_INSIDE_OUTER_PACKET_SUM
```

The new scoped cell is

```text
TPC204_DECLARED_PLAUSIBLE_PRODUCTION_CROSSWALK_CORPUS_V1 = STOP_SCOPED
```

It stops only extraction from this exact finite corpus.  It does not stop
either O161 parent or the global architecture, does not prove global
nonexistence, and does not supply a natural-\(q/N\) named fixed-atom
positive-power theorem.

User authorization is recorded only as workflow input.  It is not theorem
evidence and does not imply a reopen trigger.

## Machine certificate

The independent checker verifies:

- an independently frozen nine-row contract without importing the builder or
  materialization module;
- 15 source locks and bounded source anchors;
- the active TPC-194/203 hardening contract;
- 9 candidates, 63 axis cells, and 27 formula-crosswalk cells;
- 12 exact-schema mutations;
- 45 coordinated semantic mutations under regenerated schemas;
- 5 additional nested `bool`/`int` type-confusion mutations;
- strict JSON types, including the Python `bool`/`int` boundary;
- zero endpoint credit, `1/400` unpaid, and `L2 = NONE`.

The adjacent manifest is a repository review pin, not an external signature.

## Reproduce

From the repository root:

```powershell
python papers/tpc-204-source-locked-production-registry-crosswalk/experiments/build_tpc204.py
python papers/tpc-204-source-locked-production-registry-crosswalk/experiments/build_tpc204.py --check
python papers/tpc-204-source-locked-production-registry-crosswalk/experiments/tpc204_source_locked_production_registry_crosswalk.py --check
python papers/tpc-204-source-locked-production-registry-crosswalk/experiments/tpc204_independent_checker.py --check
```

Build the paper:

```powershell
Push-Location papers/tpc-204-source-locked-production-registry-crosswalk
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
Copy-Item -LiteralPath main.pdf `
  -Destination tpc-204-source-locked-production-registry-crosswalk.pdf `
  -Force
Pop-Location
```
