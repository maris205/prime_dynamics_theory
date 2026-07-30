# TPC-205: Pair-Native Post-TT-star Registry Interface

## Exact result

TPC-205 freezes the finite, source-locked interface required by a
pair-native post-TT-star architecture reroute.  It separates four relation
types:

```text
TTSTAR_BILINEAR_PAIR_TERM
LINEAR_CUT_TO_OCCURRENCE_EDGE
TPC93_RETAINED_SOURCE_ATOM
TPC93_SOURCE_CHILD
```

The exact classification and verdict are:

```text
classification = PAIR_NATIVE_POST_TTSTAR_REGISTRY_INTERFACE_L1
theorem_status = PROVED_TYPED_INTERFACE_AND_FIRST_MISSING_L1
verdict = PAIR_NATIVE_ARCHITECTURE_REROUTE_INTERFACE_CERTIFIED_NOT_REOPENED
source_locks = 17
required_registry_fields = 42
production_pair_records_in_declared_TPC205_registry_source_lock_corpus = 0
finite fixtures = 2
loss-ledger rows = 17
gates = 23
```

The two finite fixtures have deliberately disjoint evidence modes:

```text
DUAL_SOURCE_LOCKED_ROW_PAIR_CANDIDATE = ROW_ONLY
TPC32_PRIMITIVE_FIXTURE_PLUS_TPC93_FORMULAS_DERIVED_L0_ONLY
  = DERIVED_L0_ONLY
```

Neither evidence mode is accepted as a production pair occurrence.  The
separate L0 interface schema has no production-record mode.

The zero production-row count is scoped to the declared TPC-205
registry/source-lock corpus.  It is not an exhaustive nonexistence claim
about every file in the repository snapshot.

The exact first missing node is:

```text
SOURCE_LOCKED_POST_TTSTAR_ORDERED_PAIR_REGISTRY_WITH_COMPLETE_PAIR_COEFFICIENT_AND_GLOBAL_NORMALIZATION
```

The final route state is:

```text
PAIR_NATIVE_FORMULA_GATE = PASS
ACTIVE_PRODUCTION_PAIR_OCCURRENCE = NOT_TESTABLE
SOURCE_LOCKED_PAIR_TO_OMEGA_CROSSWALK = FAIL
H1_E_REPAIR = FAIL
PAIR_NATIVE_ARCHITECTURE_REROUTE_CANDIDATE = OPEN
PAIR_NATIVE_PRODUCTION_REOPEN_TRIGGER = FAIL
PAIR_NATIVE_STRUCTURAL_REOPEN_TRIGGER = FAIL
```

This is an L0/L1 interface theorem.  It supplies no production occurrence,
positive saving exponent, endpoint `1/400` credit, L2 estimate, prime-pair
lower bound, or twin-prime theorem.

## Registry and normalization firewalls

The registry contract keeps the ordered pair `(alpha,gamma,j)` and forbids a
swap quotient.  It separates:

- `pair_record_id`, `edge_instance_id`, and `target_occurrence_id`;
- formula support, evaluated mask, coefficient evaluability, and nonzero
  status;
- source, linear, quadratic TT-star, and target-return normalizations; and
- the displayed TPC-18 coefficient carrier from the unsupplied full literal
  expansion of its `B` aliases.

The archived string `"nu_X"` is retained only as a scope label.  If a future
theorem supplies a multiplicative scalar `c_X`, the only licensed quadratic
identity is

```text
|c_X T_D|^2 <= C_W |c_X|^2 J(E_D+C_D^off).
```

The generic hard remainder, square-root return, and full-block/endpoint
reassembly remain uncontrolled or unsupplied.  Every retained TPC-18,
TPC-25, TPC-32, or TPC-93 bound remains under its own source theorem's
hypotheses; the loss ledger does not compose those rows onto a production
TPC-18 pair.  TPC-93's weighted sign reassembly is licensed only on its
physical squarefree and target-primitive support.

## Machine certificate

The active release contains:

- exact payload, audit, and L0 fixture schemas;
- 17 source locks with canonical UTF-8/LF hashes and pinned anchors;
- semantic-ID selection and independent integrity recomputation for the four
  TPC-133/TPC-136 archive records;
- independent integer reconstruction of the two finite fixtures;
- full deep strict-type comparison of every nested payload, audit, and L0
  contract;
- 12 active-schema mutations;
- 37 regenerated-schema semantic mutations;
- 6 additional strict `bool`/`int` type-confusion mutations; and
- a separate checker that imports neither builder nor materializer.

The adjacent manifest is a repository review pin, not an external signature
or theorem source.

## Reproduce

From the repository root:

```powershell
python papers/tpc-205-pair-native-post-ttstar-registry-interface/experiments/build_tpc205.py
python papers/tpc-205-pair-native-post-ttstar-registry-interface/experiments/tpc205_pair_native_registry_interface.py --refresh-manifest
python papers/tpc-205-pair-native-post-ttstar-registry-interface/experiments/build_tpc205.py --check
python papers/tpc-205-pair-native-post-ttstar-registry-interface/experiments/tpc205_pair_native_registry_interface.py --check
python papers/tpc-205-pair-native-post-ttstar-registry-interface/experiments/tpc205_independent_checker.py --check
```

Build the paper:

```powershell
Push-Location papers/tpc-205-pair-native-post-ttstar-registry-interface
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
Copy-Item -LiteralPath main.pdf `
  -Destination tpc-205-pair-native-post-ttstar-registry-interface.pdf `
  -Force
Pop-Location
```
