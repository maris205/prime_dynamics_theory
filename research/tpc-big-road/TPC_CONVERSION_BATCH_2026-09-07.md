# TPC TeX-to-Markdown conversion batches: 418–365

Updated 2026-09-07. This is a maintenance record for the first priority
conversion batch after the archive inventory. It does not create a paper,
change the TPC route, or reopen the stopped TPC-418 research line.

## Batch scope and method

Fifty-four current route papers in the contiguous range TPC-418–365 were
converted from their preserved `paper/main.tex` sources with the same method.
Batch 7 closes the previously recorded TPC395–398 gap:

```tex
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

### Batch 4: TPC-403 through TPC-399

| Paper | Full source Markdown | Provenance/page map/formula audit | Abstract/summary | Proof/application notes | TeX | PDF |
|---|---|---|---|---|---|---|
| TPC-403 | [paper/main.md](../../papers/tpc-403-c1-crt-origin-proxy-obstruction/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-403-c1-crt-origin-proxy-obstruction/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-403-c1-crt-origin-proxy-obstruction/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-403-c1-crt-origin-proxy-obstruction/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-403-c1-crt-origin-proxy-obstruction/notes/claim_firewall.md) | [main.tex](../../papers/tpc-403-c1-crt-origin-proxy-obstruction/paper/main.tex) | [main.pdf](../../papers/tpc-403-c1-crt-origin-proxy-obstruction/paper/main.pdf) |
| TPC-402 | [paper/main.md](../../papers/tpc-402-c1-signed-diagonal-term-audit/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-402-c1-signed-diagonal-term-audit/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-402-c1-signed-diagonal-term-audit/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-402-c1-signed-diagonal-term-audit/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-402-c1-signed-diagonal-term-audit/notes/claim_firewall.md) | [main.tex](../../papers/tpc-402-c1-signed-diagonal-term-audit/paper/main.tex) | [main.pdf](../../papers/tpc-402-c1-signed-diagonal-term-audit/paper/main.pdf) |
| TPC-401 | [paper/main.md](../../papers/tpc-401-c1-diagonal-deletion-decomposition/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-401-c1-diagonal-deletion-decomposition/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-401-c1-diagonal-deletion-decomposition/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-401-c1-diagonal-deletion-decomposition/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-401-c1-diagonal-deletion-decomposition/notes/claim_firewall.md) | [main.tex](../../papers/tpc-401-c1-diagonal-deletion-decomposition/paper/main.tex) | [main.pdf](../../papers/tpc-401-c1-diagonal-deletion-decomposition/paper/main.pdf) |
| TPC-400 | [paper/main.md](../../papers/tpc-400-c1-endpoint-microgrid-third-family/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-400-c1-endpoint-microgrid-third-family/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-400-c1-endpoint-microgrid-third-family/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-400-c1-endpoint-microgrid-third-family/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-400-c1-endpoint-microgrid-third-family/notes/claim_firewall.md) | [main.tex](../../papers/tpc-400-c1-endpoint-microgrid-third-family/paper/main.tex) | [main.pdf](../../papers/tpc-400-c1-endpoint-microgrid-third-family/paper/main.pdf) |
| TPC-399 | [paper/main.md](../../papers/tpc-399-c1-endpoint-microgrid-cross-family/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-399-c1-endpoint-microgrid-cross-family/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-399-c1-endpoint-microgrid-cross-family/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-399-c1-endpoint-microgrid-cross-family/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-399-c1-endpoint-microgrid-cross-family/notes/claim_firewall.md) | [main.tex](../../papers/tpc-399-c1-endpoint-microgrid-cross-family/paper/main.tex) | [main.pdf](../../papers/tpc-399-c1-endpoint-microgrid-cross-family/paper/main.pdf) |

### Batch 5: TPC-394 through TPC-390

| Paper | Full source Markdown | Provenance/page map/formula audit | Abstract/summary | Proof/application notes | TeX | PDF |
|---|---|---|---|---|---|---|
| TPC-394 | [paper/main.md](../../papers/tpc-394-c1-origin-uniformity-ladder/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-394-c1-origin-uniformity-ladder/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-394-c1-origin-uniformity-ladder/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-394-c1-origin-uniformity-ladder/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-394-c1-origin-uniformity-ladder/notes/claim_firewall.md) | [main.tex](../../papers/tpc-394-c1-origin-uniformity-ladder/paper/main.tex) | [main.pdf](../../papers/tpc-394-c1-origin-uniformity-ladder/paper/main.pdf) |
| TPC-393 | [paper/main.md](../../papers/tpc-393-c1-normalization-adversarial-holdout/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-393-c1-normalization-adversarial-holdout/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-393-c1-normalization-adversarial-holdout/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-393-c1-normalization-adversarial-holdout/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-393-c1-normalization-adversarial-holdout/notes/claim_firewall.md) | [main.tex](../../papers/tpc-393-c1-normalization-adversarial-holdout/paper/main.tex) | [main.pdf](../../papers/tpc-393-c1-normalization-adversarial-holdout/paper/main.pdf) |
| TPC-392 | [paper/main.md](../../papers/tpc-392-c1-normalization-phase-diagram/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-392-c1-normalization-phase-diagram/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-392-c1-normalization-phase-diagram/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-392-c1-normalization-phase-diagram/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-392-c1-normalization-phase-diagram/notes/claim_firewall.md) | [main.tex](../../papers/tpc-392-c1-normalization-phase-diagram/paper/main.tex) | [main.pdf](../../papers/tpc-392-c1-normalization-phase-diagram/paper/main.pdf) |
| TPC-391 | [paper/main.md](../../papers/tpc-391-c1-recursive-horizon-localization/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-391-c1-recursive-horizon-localization/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-391-c1-recursive-horizon-localization/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-391-c1-recursive-horizon-localization/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-391-c1-recursive-horizon-localization/notes/claim_firewall.md) | [main.tex](../../papers/tpc-391-c1-recursive-horizon-localization/paper/main.tex) | [main.pdf](../../papers/tpc-391-c1-recursive-horizon-localization/paper/main.pdf) |
| TPC-390 | [paper/main.md](../../papers/tpc-390-c1-recursive-slope-composition/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-390-c1-recursive-slope-composition/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-390-c1-recursive-slope-composition/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-390-c1-recursive-slope-composition/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-390-c1-recursive-slope-composition/notes/claim_firewall.md) | [main.tex](../../papers/tpc-390-c1-recursive-slope-composition/paper/main.tex) | [main.pdf](../../papers/tpc-390-c1-recursive-slope-composition/paper/main.pdf) |

### Batch 6: TPC-389 through TPC-385

| Paper | Full source Markdown | Provenance/page map/formula audit | Abstract/summary | Proof/application notes | TeX | PDF |
|---|---|---|---|---|---|---|
| TPC-389 | [paper/main.md](../../papers/tpc-389-c1-long-horizon-slope-stress/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-389-c1-long-horizon-slope-stress/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-389-c1-long-horizon-slope-stress/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-389-c1-long-horizon-slope-stress/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-389-c1-long-horizon-slope-stress/notes/claim_firewall.md) | [main.tex](../../papers/tpc-389-c1-long-horizon-slope-stress/paper/main.tex) | [main.pdf](../../papers/tpc-389-c1-long-horizon-slope-stress/paper/main.pdf) |
| TPC-388 | [paper/main.md](../../papers/tpc-388-c1-cross-family-slope-transfer/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-388-c1-cross-family-slope-transfer/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-388-c1-cross-family-slope-transfer/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-388-c1-cross-family-slope-transfer/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-388-c1-cross-family-slope-transfer/notes/claim_firewall.md) | [main.tex](../../papers/tpc-388-c1-cross-family-slope-transfer/paper/main.tex) | [main.pdf](../../papers/tpc-388-c1-cross-family-slope-transfer/paper/main.pdf) |
| TPC-387 | [paper/main.md](../../papers/tpc-387-c1-count-ladder-renormalization/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-387-c1-count-ladder-renormalization/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-387-c1-count-ladder-renormalization/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-387-c1-count-ladder-renormalization/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-387-c1-count-ladder-renormalization/notes/claim_firewall.md) | [main.tex](../../papers/tpc-387-c1-count-ladder-renormalization/paper/main.tex) | [main.pdf](../../papers/tpc-387-c1-count-ladder-renormalization/paper/main.pdf) |
| TPC-386 | [paper/main.md](../../papers/tpc-386-c1-count-holdout-bandwidth/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-386-c1-count-holdout-bandwidth/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-386-c1-count-holdout-bandwidth/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-386-c1-count-holdout-bandwidth/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-386-c1-count-holdout-bandwidth/notes/claim_firewall.md) | [main.tex](../../papers/tpc-386-c1-count-holdout-bandwidth/paper/main.tex) | [main.pdf](../../papers/tpc-386-c1-count-holdout-bandwidth/paper/main.pdf) |
| TPC-385 | [paper/main.md](../../papers/tpc-385-c1-bandwidth-origin-holdout/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-385-c1-bandwidth-origin-holdout/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-385-c1-bandwidth-origin-holdout/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-385-c1-bandwidth-origin-holdout/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-385-c1-bandwidth-origin-holdout/notes/claim_firewall.md) | [main.tex](../../papers/tpc-385-c1-bandwidth-origin-holdout/paper/main.tex) | [main.pdf](../../papers/tpc-385-c1-bandwidth-origin-holdout/paper/main.pdf) |

### Batch 7: TPC-398 through TPC-395

| Paper | Full source Markdown | Provenance/page map/formula audit | Abstract/summary | Proof/application notes | TeX | PDF |
|---|---|---|---|---|---|---|
| TPC-398 | [paper/main.md](../../papers/tpc-398-c1-interpolation-endpoint-microgrid/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-398-c1-interpolation-endpoint-microgrid/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-398-c1-interpolation-endpoint-microgrid/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-398-c1-interpolation-endpoint-microgrid/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-398-c1-interpolation-endpoint-microgrid/notes/claim_firewall.md) | [main.tex](../../papers/tpc-398-c1-interpolation-endpoint-microgrid/paper/main.tex) | [main.pdf](../../papers/tpc-398-c1-interpolation-endpoint-microgrid/paper/main.pdf) |
| TPC-397 | [paper/main.md](../../papers/tpc-397-c1-interpolation-transition-replication/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-397-c1-interpolation-transition-replication/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-397-c1-interpolation-transition-replication/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-397-c1-interpolation-transition-replication/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-397-c1-interpolation-transition-replication/notes/claim_firewall.md) | [main.tex](../../papers/tpc-397-c1-interpolation-transition-replication/paper/main.tex) | [main.pdf](../../papers/tpc-397-c1-interpolation-transition-replication/paper/main.pdf) |
| TPC-396 | [paper/main.md](../../papers/tpc-396-c1-signed-law-interpolation/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-396-c1-signed-law-interpolation/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-396-c1-signed-law-interpolation/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-396-c1-signed-law-interpolation/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-396-c1-signed-law-interpolation/notes/claim_firewall.md) | [main.tex](../../papers/tpc-396-c1-signed-law-interpolation/paper/main.tex) | [main.pdf](../../papers/tpc-396-c1-signed-law-interpolation/paper/main.pdf) |
| TPC-395 | [paper/main.md](../../papers/tpc-395-c1-origin-cross-family-holdout/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-395-c1-origin-cross-family-holdout/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-395-c1-origin-cross-family-holdout/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-395-c1-origin-cross-family-holdout/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-395-c1-origin-cross-family-holdout/notes/claim_firewall.md) | [main.tex](../../papers/tpc-395-c1-origin-cross-family-holdout/paper/main.tex) | [main.pdf](../../papers/tpc-395-c1-origin-cross-family-holdout/paper/main.pdf) |

### Batch 8: TPC-384 through TPC-380

| Paper | Full source Markdown | Provenance/page map/formula audit | Abstract/summary | Proof/application notes | TeX | PDF |
|---|---|---|---|---|---|---|
| TPC-384 | [paper/main.md](../../papers/tpc-384-c1-bandwidth-normalization-phase-diagram/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-384-c1-bandwidth-normalization-phase-diagram/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-384-c1-bandwidth-normalization-phase-diagram/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-384-c1-bandwidth-normalization-phase-diagram/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-384-c1-bandwidth-normalization-phase-diagram/notes/claim_firewall.md) | [main.tex](../../papers/tpc-384-c1-bandwidth-normalization-phase-diagram/paper/main.tex) | [main.pdf](../../papers/tpc-384-c1-bandwidth-normalization-phase-diagram/paper/main.pdf) |
| TPC-383 | [paper/main.md](../../papers/tpc-383-c1-pooled-normalization-audit/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-383-c1-pooled-normalization-audit/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-383-c1-pooled-normalization-audit/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-383-c1-pooled-normalization-audit/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-383-c1-pooled-normalization-audit/notes/claim_firewall.md) | [main.tex](../../papers/tpc-383-c1-pooled-normalization-audit/paper/main.tex) | [main.pdf](../../papers/tpc-383-c1-pooled-normalization-audit/paper/main.pdf) |
| TPC-382 | [paper/main.md](../../papers/tpc-382-c1-origin-family-magnitude-audit/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-382-c1-origin-family-magnitude-audit/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-382-c1-origin-family-magnitude-audit/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-382-c1-origin-family-magnitude-audit/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-382-c1-origin-family-magnitude-audit/notes/claim_firewall.md) | [main.tex](../../papers/tpc-382-c1-origin-family-magnitude-audit/paper/main.tex) | [main.pdf](../../papers/tpc-382-c1-origin-family-magnitude-audit/paper/main.pdf) |
| TPC-381 | [paper/main.md](../../papers/tpc-381-c1-origin-family-replay/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-381-c1-origin-family-replay/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-381-c1-origin-family-replay/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-381-c1-origin-family-replay/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-381-c1-origin-family-replay/notes/claim_firewall.md) | [main.tex](../../papers/tpc-381-c1-origin-family-replay/paper/main.tex) | [main.pdf](../../papers/tpc-381-c1-origin-family-replay/paper/main.pdf) |
| TPC-380 | [paper/main.md](../../papers/tpc-380-c1-law-control-count-replay/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-380-c1-law-control-count-replay/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-380-c1-law-control-count-replay/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-380-c1-law-control-count-replay/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-380-c1-law-control-count-replay/notes/claim_firewall.md) | [main.tex](../../papers/tpc-380-c1-law-control-count-replay/paper/main.tex) | [main.pdf](../../papers/tpc-380-c1-law-control-count-replay/paper/main.pdf) |

### Batch 9: TPC-379 through TPC-375

| Paper | Full source Markdown | Provenance/page map/formula audit | Abstract/summary | Proof/application notes | TeX | PDF |
|---|---|---|---|---|---|---|
| TPC-379 | [paper/main.md](../../papers/tpc-379-c1-crossholdout-law-control/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-379-c1-crossholdout-law-control/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-379-c1-crossholdout-law-control/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-379-c1-crossholdout-law-control/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-379-c1-crossholdout-law-control/notes/claim_firewall.md) | [main.tex](../../papers/tpc-379-c1-crossholdout-law-control/paper/main.tex) | [main.pdf](../../papers/tpc-379-c1-crossholdout-law-control/paper/main.pdf) |
| TPC-378 | [paper/main.md](../../papers/tpc-378-c1-scale-origin-crossholdout/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-378-c1-scale-origin-crossholdout/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-378-c1-scale-origin-crossholdout/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-378-c1-scale-origin-crossholdout/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-378-c1-scale-origin-crossholdout/notes/claim_firewall.md) | [main.tex](../../papers/tpc-378-c1-scale-origin-crossholdout/paper/main.tex) | [main.pdf](../../papers/tpc-378-c1-scale-origin-crossholdout/paper/main.pdf) |
| TPC-377 | [paper/main.md](../../papers/tpc-377-c1-window-scale-holdout/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-377-c1-window-scale-holdout/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-377-c1-window-scale-holdout/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-377-c1-window-scale-holdout/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-377-c1-window-scale-holdout/notes/claim_firewall.md) | [main.tex](../../papers/tpc-377-c1-window-scale-holdout/paper/main.tex) | [main.pdf](../../papers/tpc-377-c1-window-scale-holdout/paper/main.pdf) |
| TPC-376 | [paper/main.md](../../papers/tpc-376-bandwidth-holdout-replication/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-376-bandwidth-holdout-replication/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-376-bandwidth-holdout-replication/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-376-bandwidth-holdout-replication/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-376-bandwidth-holdout-replication/notes/claim_firewall.md) | [main.tex](../../papers/tpc-376-bandwidth-holdout-replication/paper/main.tex) | [main.pdf](../../papers/tpc-376-bandwidth-holdout-replication/paper/main.pdf) |
| TPC-375 | [paper/main.md](../../papers/tpc-375-bandwidth-stability-minimal-cutoff/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-375-bandwidth-stability-minimal-cutoff/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-375-bandwidth-stability-minimal-cutoff/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-375-bandwidth-stability-minimal-cutoff/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-375-bandwidth-stability-minimal-cutoff/notes/claim_firewall.md) | [main.tex](../../papers/tpc-375-bandwidth-stability-minimal-cutoff/paper/main.tex) | [main.pdf](../../papers/tpc-375-bandwidth-stability-minimal-cutoff/paper/main.pdf) |

This batch extends the contiguous TeX-first reading layer through TPC-375. The
five source manuscripts remain finite computational or finite synthetic
claims; the conversion adds no theorem, arithmetic advance, fixed-power
credit, physical identification, Route-B closure, or twin-prime conclusion.

### Batch 10: TPC-374 through TPC-370

| Paper | Full source Markdown | Provenance/page map/formula audit | Abstract/summary | Proof/application notes | TeX | PDF |
|---|---|---|---|---|---|---|
| TPC-374 | [paper/main.md](../../papers/tpc-374-near-block-band-truncation/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-374-near-block-band-truncation/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-374-near-block-band-truncation/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-374-near-block-band-truncation/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-374-near-block-band-truncation/notes/claim_firewall.md) | [main.tex](../../papers/tpc-374-near-block-band-truncation/paper/main.tex) | [main.pdf](../../papers/tpc-374-near-block-band-truncation/paper/main.pdf) |
| TPC-373 | [paper/main.md](../../papers/tpc-373-eigenmode-block-separation/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-373-eigenmode-block-separation/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-373-eigenmode-block-separation/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-373-eigenmode-block-separation/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-373-eigenmode-block-separation/notes/claim_firewall.md) | [main.tex](../../papers/tpc-373-eigenmode-block-separation/paper/main.tex) | [main.pdf](../../papers/tpc-373-eigenmode-block-separation/paper/main.pdf) |
| TPC-372 | [paper/main.md](../../papers/tpc-372-full-window-offblock-decomposition/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-372-full-window-offblock-decomposition/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-372-full-window-offblock-decomposition/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-372-full-window-offblock-decomposition/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-372-full-window-offblock-decomposition/notes/claim_firewall.md) | [main.tex](../../papers/tpc-372-full-window-offblock-decomposition/paper/main.tex) | [main.pdf](../../papers/tpc-372-full-window-offblock-decomposition/paper/main.pdf) |
| TPC-371 | [paper/main.md](../../papers/tpc-371-block-phase-localization/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-371-block-phase-localization/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-371-block-phase-localization/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-371-block-phase-localization/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-371-block-phase-localization/notes/claim_firewall.md) | [main.tex](../../papers/tpc-371-block-phase-localization/paper/main.tex) | [main.pdf](../../papers/tpc-371-block-phase-localization/paper/main.pdf) |
| TPC-370 | [paper/main.md](../../papers/tpc-370-count-2048-window-audit/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-370-count-2048-window-audit/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-370-count-2048-window-audit/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-370-count-2048-window-audit/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-370-count-2048-window-audit/notes/claim_firewall.md) | [main.tex](../../papers/tpc-370-count-2048-window-audit/paper/main.tex) | [main.pdf](../../papers/tpc-370-count-2048-window-audit/paper/main.pdf) |

This batch records the finite count-2048 window, block-phase, decomposition,
eigenmode-layer, and near-block truncation manuscripts as source-complete
mechanical Markdown. Their finite computational boundaries remain unchanged.

### Batch 11: TPC-369 through TPC-365

| Paper | Full source Markdown | Provenance/page map/formula audit | Abstract/summary | Proof/application notes | TeX | PDF |
|---|---|---|---|---|---|---|
| TPC-369 | [paper/main.md](../../papers/tpc-369-third-origin-family-audit/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-369-third-origin-family-audit/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-369-third-origin-family-audit/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-369-third-origin-family-audit/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-369-third-origin-family-audit/notes/claim_firewall.md) | [main.tex](../../papers/tpc-369-third-origin-family-audit/paper/main.tex) | [main.pdf](../../papers/tpc-369-third-origin-family-audit/paper/main.pdf) |
| TPC-368 | [paper/main.md](../../papers/tpc-368-predeclared-origin-replication/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-368-predeclared-origin-replication/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-368-predeclared-origin-replication/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-368-predeclared-origin-replication/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-368-predeclared-origin-replication/notes/claim_firewall.md) | [main.tex](../../papers/tpc-368-predeclared-origin-replication/paper/main.tex) | [main.pdf](../../papers/tpc-368-predeclared-origin-replication/paper/main.pdf) |
| TPC-367 | [paper/main.md](../../papers/tpc-367-predeclared-long-window-obstruction/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-367-predeclared-long-window-obstruction/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-367-predeclared-long-window-obstruction/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-367-predeclared-long-window-obstruction/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-367-predeclared-long-window-obstruction/notes/claim_firewall.md) | [main.tex](../../papers/tpc-367-predeclared-long-window-obstruction/paper/main.tex) | [main.pdf](../../papers/tpc-367-predeclared-long-window-obstruction/paper/main.pdf) |
| TPC-366 | [paper/main.md](../../papers/tpc-366-beta2-higher-q-ladder/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-366-beta2-higher-q-ladder/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-366-beta2-higher-q-ladder/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-366-beta2-higher-q-ladder/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-366-beta2-higher-q-ladder/notes/claim_firewall.md) | [main.tex](../../papers/tpc-366-beta2-higher-q-ladder/paper/main.tex) | [main.pdf](../../papers/tpc-366-beta2-higher-q-ladder/paper/main.pdf) |
| TPC-365 | [paper/main.md](../../papers/tpc-365-beta2-fresh-holdout/paper/main.md) | [CONVERSION_RECORD.md](../../papers/tpc-365-beta2-fresh-holdout/CONVERSION_RECORD.md) | [README.md](../../papers/tpc-365-beta2-fresh-holdout/README.md) | [PROOF_PACKAGE.md](../../papers/tpc-365-beta2-fresh-holdout/PROOF_PACKAGE.md), [claim firewall note](../../papers/tpc-365-beta2-fresh-holdout/notes/claim_firewall.md) | [main.tex](../../papers/tpc-365-beta2-fresh-holdout/paper/main.tex) | [main.pdf](../../papers/tpc-365-beta2-fresh-holdout/paper/main.pdf) |

This batch records the finite prime-shell tilt, higher-`Q`, long-window, and
origin-family holdout manuscripts as source-complete mechanical Markdown.
Their finite computational boundaries remain unchanged.

## Formula and theorem-boundary verification

The audit covered the formulas that carry each finite claim, rather than
trying to reprove every computational certificate in the Markdown conversion:

- TPC-369: the third predeclared origin-family audit and finite obstruction.
- TPC-368: the second predeclared origin-family replication.
- TPC-367: the predeclared long-window finite obstruction.
- TPC-366: the higher-`Q` finite scale audit of the fixed tilt.
- TPC-365: the response-blind finite fresh holdout.

- TPC-374: the finite near-block truncation and exact failure-census reproduction.
- TPC-373: block-distance Rayleigh-layer separation of the finite extremal mode.
- TPC-372: common-normalization block/off-block decomposition and finite lower bound.
- TPC-371: block-local phase localization for the finite count-2048 audit.
- TPC-370: the predeclared count-2048 four-law finite-window audit.

- TPC-379: the finite four-law control panel and law-dependence obstruction.
- TPC-378: coordinate-disjoint origin transfer at the declared finite counts and scales.
- TPC-377: the nested count holdout and finite c=1 support profile.
- TPC-376: bandwidth holdout replication with the frozen normalization and finite scope.
- TPC-375: the nested bandwidth census and first matching finite cutoff.

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
- TPC-408: the complete-shell `Q`-scale extension and its finite adjacen
  normalized proxy claim, with the route boundary preserved.
- TPC-407: the complete-shell `Q`-scale ladder, exact finite observations,
  and the source's stated proof/scope boundary.
- TPC-406: the first complete-shell local-normalization entry boundary,
  including its exact local identities and finite-only gate.
- TPC-405: the three-height/scale-ladder source claim and its finite synthetic
  normalization scope.
- TPC-404: the initial local-normalization boundary and the exact finite
  adjacent-entry claim recorded by the source package.
- TPC-403: the finite CRT-origin proxy obstruction, exact certificate, and
  explicit route limitation.
- TPC-402: the signed diagonal-term identity, finite audit, and anchor
  obstruction recorded by the source.
- TPC-401: the diagonal-deletion decomposition, exact production identity,
  and finite boundary counterexample.
- TPC-400: the endpoint microgrid's third-family finite construction,
  diagnostics, and route ledger.
- TPC-399: the cross-family endpoint microgrid construction, frozen paren
  interface, diagnostics, and finite claim boundary.
- TPC-394: the origin-uniformity ladder and its finite diagnostic/provenance
  boundary.
- TPC-393: the adversarial normalization holdout and finite robustness scope.
- TPC-392: the normalization phase diagram, finite observations, and route
  boundary.
- TPC-391: recursive horizon localization and its finite proof/audit scope.
- TPC-390: recursive slope composition and the source's finite route boundary.
- TPC-389: long-horizon slope stress, finite composition diagnostics, and its
  explicit route boundary.
- TPC-388: cross-family slope transfer and finite holdout scope.
- TPC-387: count-ladder renormalization and the source's finite diagnostics.
- TPC-386: count holdout/bandwidth analysis and its finite claim boundary.
- TPC-385: bandwidth-origin holdout evidence and the preserved finite-only
  scope.
- TPC-398: interpolation endpoint microgrid, finite diagnostics, and its
  frozen source/claim boundary.
- TPC-397: interpolation transition replication and the preserved finite
  comparison scope.
- TPC-396: signed-law interpolation identities and finite diagnostic scope.
- TPC-395: origin cross-family holdout and its finite claim boundary.
- TPC-384: bandwidth/normalization phase diagram and finite diagnostic scope.
- TPC-383: pooled normalization audit and finite model-relative observations.
- TPC-382: origin-family magnitude audit and finite stability boundary.
- TPC-381: origin-family replay and finite holdout scope.
- TPC-380: count-replay law control and its explicit finite claim boundary.

For all five papers, the prerequisite audit confirms that finite synthetic
assumptions, exact-rational/computational evidence, and claim-firewall
language remain tied to the original package. The conversion does not turn a
certificate into an arithmetic theorem, add references that are absent from
the source, or promote any conditional/open statement.

## Coverage after this batch

The archive still contains 823 paper directories: 420 TPC and 403 RH. The
inventory now records:

```tex
full-source-md      54
reliable-full-md     0
partial-or-notes   768
source-inaccessible  1
```

The remaining 768 `partial-or-notes` entries are the next conversion pool;
they are not silently treated as full manuscripts. TPC-207 remains the single
source-inaccessible entry. The next batch should continue with the highes
route relevance or any `not-converted` source, using the same provenance and
scope-preservation protocol.

## Route boundary

The scientific handoff remains
`TPC418_ROUND2_CLUE = NONE_UNTIL_GROWING_OR_PHYSICAL_GATE_CHANGES`.
This conversion batch supplies a searchable source layer only. It does no
create TPC-419, change arithmetic advance (`NO`), change fixed-power credi
(`0`), or close the full gate (`OPEN`).
