# TPC-206: Selected-Lineage Pair-Registry Projection

## Exact result

TPC-206 freezes one finite, source-locked projection of the 42-field TPC-205
pair-registry contract. The selected ordered rows are

```text
alpha = (103,1)
gamma = (107,1)
j = 5
X = 512
h0 = 2
```

The exact classification and verdict are:

```text
classification = PAIR_NATIVE_SELECTED_LINEAGE_PROJECTION_L1
theorem_status =
  PROVED_SELECTED_SOURCE_LOCKED_13_OF_42_PROJECTION_AND_FIRST_MISSING_D_L1
verdict =
  SELECTED_SOURCE_LOCKED_13_OF_42_PAIR_REGISTRY_PROJECTION_CERTIFIED_NOT_REOPENED
```

The explicit selected-lineage graph has six source records, four typed
derivation nodes, and twelve dependency edges. Its field closure is:

```text
required fields = 42
materialized fields = 13
missing fields = 29
first missing field = D
first missing one-based index = 9
full completions inside the explicit selected graph = 0
```

This is not a corpus-wide maximality theorem. In particular:

```text
corpus-wide maximum materialized fields = null
corpus-wide full-join count = null
CORPUS_WIDE_MAXIMALITY = NOT_TESTABLE
```

The separate TPC-32/TPC-93 L0 fixture exposes 14 contract slots in its own
lineage. It cannot be spliced into the selected 103/107 graph, and TPC-206
draws no maximum conclusion from it.

## Exact typed firewalls

The thirteen selected fields are:

```text
X, h0, delta, R, V, D0, L, K,
alpha, gamma, j, N_alpha(j), N_gamma(j).
```

The source chain distinguishes three pairs of look-alike symbols:

```text
TPC-133 truncation Q_133 = 4  ->  TPC-18 truncation R = 4
TPC-18 row scale Q_18 = L D   ->  missing

native row divisor d = 1      !=  opened dyadic scale D
native row index k = 5        !=  dyadic block scale K = 8
```

The value `delta=1/4` is a chosen finite-manifest provenance lift at
`X=512`, tied through the TPC-133 certificate to the 866-row JSONL archive.
It is not recovered uniquely from either selected row and is not a
cross-scale packet schedule.

The first eight missing identity fields are:

```text
D, J, Q, T, U0, G_X_row, packet_id, source_locator.
```

The remaining missing fields are five ordered-pair fields, all twelve
source/child fields, and all four normalization fields. The archived string
`nu_X` remains a scope label, not a scalar.

## Claim boundary

The certificate proves no active production pair occurrence, pair-to-omega
crosswalk, H1-E repair, fixed-atom decay, positive saving exponent, endpoint
`1/400` payment, L2 estimate, prime-pair lower bound, or twin-prime theorem.

The pair-native architecture reroute, both O161 parents, H1 architecture,
and the global architecture remain open. Earlier stopped cells remain
`STOP_SCOPED`; the new selected-lineage graph cell is also scoped rather
than global.

## Machine certificate

The release independently checks:

- 29 frozen source locks against both the working tree and source snapshot;
- six unique JSONL selectors and all record, parent, and upstream hashes;
- the TPC-133 manifest/certificate/866-row archive chain;
- the typed `Q_133 -> R_18` bridge and the `Q_18` firewall;
- a ten-node, twelve-edge selected graph and its 13-field closure;
- the 42-row field ledger and 29 selected-graph blockers;
- a frozen 34-ref/28-tip Git closure with 12,203 reachable objects;
- 1,707 strict RFC-8259 JSON blobs and 17 rejected non-finite JSON files;
- 12 base, 52 semantic, and 12 strict bool/int mutation rows; and
- a strict eleven-artifact repository manifest.

The archive census is contextual reopen-trigger evidence. It is explicitly
not used as a semantic census of every JSONL/TeX candidate and not used to
prove corpus-wide maximality.

## Reproduce

From the repository root:

```powershell
python -B papers/tpc-206-selected-lineage-pair-registry-projection/experiments/build_tpc206.py
python -B papers/tpc-206-selected-lineage-pair-registry-projection/experiments/tpc206_selected_lineage_pair_registry.py --refresh-manifest
python -B papers/tpc-206-selected-lineage-pair-registry-projection/experiments/build_tpc206.py --check
python -B papers/tpc-206-selected-lineage-pair-registry-projection/experiments/tpc206_selected_lineage_pair_registry.py --check
python -B papers/tpc-206-selected-lineage-pair-registry-projection/experiments/tpc206_independent_checker.py --check
```

Build the paper:

```powershell
Push-Location papers/tpc-206-selected-lineage-pair-registry-projection
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
Copy-Item -LiteralPath main.pdf `
  -Destination tpc-206-selected-lineage-pair-registry-projection.pdf `
  -Force
Pop-Location
```
