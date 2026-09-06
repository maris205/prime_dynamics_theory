# TPC TeX-to-Markdown conversion batches: 418–404

Updated 2026-09-07. This is a maintenance record for the first priority
conversion batch after the archive inventory. It does not create a paper,
change the TPC route, or reopen the stopped TPC-418 research line.

## Batch scope and method

The ten current route papers TPC-418 through TPC-409 were converted from
their preserved `paper/main.tex` sources with the same method in two adjacent
batches:

```text
pandoc -f latex -t gfm --wrap=none
```

Each output receives a short provenance preface containing the title, author,
source date, repository source commit, and links to the original TeX/PDF. The
original abstract and every numbered or unnumbered manuscript section are
included in `paper/main.md`. Existing TeX, PDF, README, proof package,
certificate, and notes were not overwritten. The source-complete status is
`full-source-md`; it is deliberately distinct from `reliable-full-md` because
these source manuscripts contain no bibliography/reference section and the
conversion is not an independent semantic peer review.

## Per-paper audit and reading links

| Paper | Full source Markdown | Provenance/page map/formula audit | Abstract/summary | Proof/application notes | TeX | PDF |
|---|---|---|---|---|---|---|
| TPC-418 | [paper/main.md](../../papers/tpc-418-c1-shell-parity-envelope/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-418-c1-shell-parity-envelope/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-418-c1-shell-parity-envelope/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-418-c1-shell-parity-envelope/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-418-c1-shell-parity-envelope/notes/claim_firewall.md) | [main.tex](../../papers/tpc-418-c1-shell-parity-envelope/paper/main.tex) | [main.pdf](../../papers/tpc-418-c1-shell-parity-envelope/paper/main.pdf) |
| TPC-417 | [paper/main.md](../../papers/tpc-417-c1-four-shell-finite-operator-bound/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-417-c1-four-shell-finite-operator-bound/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-417-c1-four-shell-finite-operator-bound/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-417-c1-four-shell-finite-operator-bound/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-417-c1-four-shell-finite-operator-bound/notes/claim_firewall.md) | [main.tex](../../papers/tpc-417-c1-four-shell-finite-operator-bound/paper/main.tex) | [main.pdf](../../papers/tpc-417-c1-four-shell-finite-operator-bound/paper/main.pdf) |
| TPC-416 | [paper/main.md](../../papers/tpc-416-c1-four-shell-odd-pooled-extension/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-416-c1-four-shell-odd-pooled-extension/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-416-c1-four-shell-odd-pooled-extension/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-416-c1-four-shell-odd-pooled-extension/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-416-c1-four-shell-odd-pooled-extension/notes/claim_firewall.md) | [main.tex](../../papers/tpc-416-c1-four-shell-odd-pooled-extension/paper/main.tex) | [main.pdf](../../papers/tpc-416-c1-four-shell-odd-pooled-extension/paper/main.pdf) |
| TPC-415 | [paper/main.md](../../papers/tpc-415-c1-three-shell-height-extension/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-415-c1-three-shell-height-extension/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-415-c1-three-shell-height-extension/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-415-c1-three-shell-height-extension/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-415-c1-three-shell-height-extension/notes/claim_firewall.md) | [main.tex](../../papers/tpc-415-c1-three-shell-height-extension/paper/main.tex) | [main.pdf](../../papers/tpc-415-c1-three-shell-height-extension/paper/main.pdf) |
| TPC-414 | [paper/main.md](../../papers/tpc-414-c1-three-shell-pooled-extension/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-414-c1-three-shell-pooled-extension/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-414-c1-three-shell-pooled-extension/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-414-c1-three-shell-pooled-extension/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-414-c1-three-shell-pooled-extension/notes/claim_firewall.md) | [main.tex](../../papers/tpc-414-c1-three-shell-pooled-extension/paper/main.tex) | [main.pdf](../../papers/tpc-414-c1-three-shell-pooled-extension/paper/main.pdf) |

The individual conversion records give exact source SHA-256 values, the
repository commit used as the version anchor, TeX line numbers, inferred PDF
page numbers for every section, displayed-equation marker counts, and a
scoped prerequisite audit against the README and proof package.

### Batch 2: TPC-413 through TPC-409

| Paper | Full source Markdown | Provenance/page map/formula audit | Abstract/summary | Proof/application notes | TeX | PDF |
|---|---|---|---|---|---|---|
| TPC-413 | [paper/main.md](../../papers/tpc-413-c1-pooled-origin-replication/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-413-c1-pooled-origin-replication/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-413-c1-pooled-origin-replication/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-413-c1-pooled-origin-replication/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-413-c1-pooled-origin-replication/notes/claim_firewall.md) | [main.tex](../../papers/tpc-413-c1-pooled-origin-replication/paper/main.tex) | [main.pdf](../../papers/tpc-413-c1-pooled-origin-replication/paper/main.pdf) |
| TPC-412 | [paper/main.md](../../papers/tpc-412-c1-pooled-complete-shell-extension/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-412-c1-pooled-complete-shell-extension/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-412-c1-pooled-complete-shell-extension/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-412-c1-pooled-complete-shell-extension/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-412-c1-pooled-complete-shell-extension/notes/claim_firewall.md) | [main.tex](../../papers/tpc-412-c1-pooled-complete-shell-extension/paper/main.tex) | [main.pdf](../../papers/tpc-412-c1-pooled-complete-shell-extension/paper/main.pdf) |
| TPC-411 | [paper/main.md](../../papers/tpc-411-c1-pooled-odd-complete-shells/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-411-c1-pooled-odd-complete-shells/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-411-c1-pooled-odd-complete-shells/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-411-c1-pooled-odd-complete-shells/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-411-c1-pooled-odd-complete-shells/notes/claim_firewall.md) | [main.tex](../../papers/tpc-411-c1-pooled-odd-complete-shells/paper/main.tex) | [main.pdf](../../papers/tpc-411-c1-pooled-odd-complete-shells/paper/main.pdf) |
| TPC-410 | [paper/main.md](../../papers/tpc-410-c1-odd-complete-shell-height-replication/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-410-c1-odd-complete-shell-height-replication/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-410-c1-odd-complete-shell-height-replication/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-410-c1-odd-complete-shell-height-replication/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-410-c1-odd-complete-shell-height-replication/notes/claim_firewall.md) | [main.tex](../../papers/tpc-410-c1-odd-complete-shell-height-replication/paper/main.tex) | [main.pdf](../../papers/tpc-410-c1-odd-complete-shell-height-replication/paper/main.pdf) |
| TPC-409 | [paper/main.md](../../papers/tpc-409-c1-odd-complete-shell-height-ladder/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-409-c1-odd-complete-shell-height-ladder/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-409-c1-odd-complete-shell-height-ladder/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-409-c1-odd-complete-shell-height-ladder/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-409-c1-odd-complete-shell-height-ladder/notes/claim_firewall.md) | [main.tex](../../papers/tpc-409-c1-odd-complete-shell-height-ladder/paper/main.tex) | [main.pdf](../../papers/tpc-409-c1-odd-complete-shell-height-ladder/paper/main.pdf) |

### Batch 3: TPC-408 through TPC-404

| Paper | Full source Markdown | Provenance/page map/formula audit | Abstract/summary | Proof/application notes | TeX | PDF |
|---|---|---|---|---|---|---|
| TPC-408 | [paper/main.md](../../papers/tpc-408-c1-complete-shell-q-scale-extension/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-408-c1-complete-shell-q-scale-extension/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-408-c1-complete-shell-q-scale-extension/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-408-c1-complete-shell-q-scale-extension/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-408-c1-complete-shell-q-scale-extension/notes/claim_firewall.md) | [main.tex](../../papers/tpc-408-c1-complete-shell-q-scale-extension/paper/main.tex) | [main.pdf](../../papers/tpc-408-c1-complete-shell-q-scale-extension/paper/main.pdf) |
| TPC-407 | [paper/main.md](../../papers/tpc-407-c1-complete-shell-q-scale-ladder/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-407-c1-complete-shell-q-scale-ladder/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-407-c1-complete-shell-q-scale-ladder/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-407-c1-complete-shell-q-scale-ladder/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-407-c1-complete-shell-q-scale-ladder/notes/claim_firewall.md) | [main.tex](../../papers/tpc-407-c1-complete-shell-q-scale-ladder/paper/main.tex) | [main.pdf](../../papers/tpc-407-c1-complete-shell-q-scale-ladder/paper/main.pdf) |
| TPC-406 | [paper/main.md](../../papers/tpc-406-c1-local-normalization-complete-shell-entry-boundary/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-406-c1-local-normalization-complete-shell-entry-boundary/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-406-c1-local-normalization-complete-shell-entry-boundary/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-406-c1-local-normalization-complete-shell-entry-boundary/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-406-c1-local-normalization-complete-shell-entry-boundary/notes/claim_firewall.md) | [main.tex](../../papers/tpc-406-c1-local-normalization-complete-shell-entry-boundary/paper/main.tex) | [main.pdf](../../papers/tpc-406-c1-local-normalization-complete-shell-entry-boundary/paper/main.pdf) |
| TPC-405 | [paper/main.md](../../papers/tpc-405-c1-local-normalization-scale-ladder/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-405-c1-local-normalization-scale-ladder/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-405-c1-local-normalization-scale-ladder/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-405-c1-local-normalization-scale-ladder/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-405-c1-local-normalization-scale-ladder/notes/claim_firewall.md) | [main.tex](../../papers/tpc-405-c1-local-normalization-scale-ladder/paper/main.tex) | [main.pdf](../../papers/tpc-405-c1-local-normalization-scale-ladder/paper/main.pdf) |
| TPC-404 | [paper/main.md](../../papers/tpc-404-c1-local-normalization-boundary/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-404-c1-local-normalization-boundary/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-404-c1-local-normalization-boundary/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-404-c1-local-normalization-boundary/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-404-c1-local-normalization-boundary/notes/claim_firewall.md) | [main.tex](../../papers/tpc-404-c1-local-normalization-boundary/paper/main.tex) | [main.pdf](../../papers/tpc-404-c1-local-normalization-boundary/paper/main.pdf) |

## Formula and theorem-boundary verification

The audit covered the formulas that carry each finite claim, rather than
trying to reprove every computational certificate in the Markdown conversion:

- TPC-418: shell amplitude monotonicity, the alternating-block sign correction
  `sigma_j = epsilon_j * (-1)^(n_j+1)`, the `B_*` envelope, and the finite
  endpoint-star/interior-bulk operator inequality. The mixed-parity
  counterexample and finite-only gate remain explicit.
- TPC-417: the exact diagonal-deletion identities, local diagonal energies,
  Cauchy–Schwarz star estimate, symmetric row-sum bulk estimate, and the
  finite `H={16,32,66,128}` scope.
- TPC-416: the four-shell count/parity data and the finite adjacent normalized
  proxy inequality at `H=66`.
- TPC-415: the three-shell pooled profile, equal parity counts, four listed
  heights, and the finite `4/H` envelope.
- TPC-414: the three-shell pooled profile, `H=66` local identities, equal
  parity counts, and the finite `4/H` envelope.

- TPC-413: the three CRT representatives, four heights, 12-row period
  invariance claim, and finite synthetic scope.
- TPC-412: the pooled two-shell profile, equal parity counts, four heights,
  and the finite `4/H` theorem.
- TPC-411: the pooled two-shell finite theorem, exact local identities, parity
  count, and the finite `4/H` envelope.
- TPC-410: the second odd-shell four-height theorem, explicit parity counts,
  and the finite `4/H` envelope.
- TPC-409: the first odd-shell four-height theorem, explicit parity counts,
  and the finite `4/H` envelope.
- TPC-408: the complete-shell `Q`-scale extension and its finite adjacent
  normalized proxy claim, with the route boundary preserved.
- TPC-407: the complete-shell `Q`-scale ladder, exact finite observations,
  and the source's stated proof/scope boundary.
- TPC-406: the first complete-shell local-normalization entry boundary,
  including its exact local identities and finite-only gate.
- TPC-405: the three-height/scale-ladder source claim and its finite synthetic
  normalization scope.
- TPC-404: the initial local-normalization boundary and the exact finite
  adjacent-entry claim recorded by the source package.

For all five papers, the prerequisite audit confirms that finite synthetic
assumptions, exact-rational/computational evidence, and claim-firewall
language remain tied to the original package. The conversion does not turn a
certificate into an arithmetic theorem, add references that are absent from
the source, or promote any conditional/open statement.

## Coverage after this batch

The archive still contains 823 paper directories: 420 TPC and 403 RH. The
inventory now records:

```text
full-source-md      15
reliable-full-md     0
partial-or-notes   807
source-inaccessible  1
```

The remaining 817 `partial-or-notes` entries are the next conversion pool;
they are not silently treated as full manuscripts. TPC-207 remains the single
source-inaccessible entry. The next batch should continue with the highest
route relevance or any `not-converted` source, using the same provenance and
scope-preservation protocol.

## Route boundary

The scientific handoff remains
`TPC418_ROUND2_CLUE = NONE_UNTIL_GROWING_OR_PHYSICAL_GATE_CHANGES`.
This conversion batch supplies a searchable source layer only. It does not
create TPC-419, change arithmetic advance (`NO`), change fixed-power credit
(`0`), or close the full gate (`OPEN`).
