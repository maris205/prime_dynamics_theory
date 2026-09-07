# TPC-364 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `947cb84cdf6db4fc614864e38f4faa19db4794d07bc9644e539130e0685a7995`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `161bc8084413323cf62b8e3ffe6f55a7939782d3312a7245c76227d663143047`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `1e1d244d0d04e38d3f932bc9c85ba7802619a88d38b19c969cc264462bcc697f`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 38 | 1 | `HEADING_TEXT_MATCH` |
| `Weighted finite operator` | 59 | 1 | `HEADING_TEXT_MATCH` |
| `Phase diagram` | 98 | 2 | `HEADING_TEXT_MATCH` |
| `Exact and independent checks` | 158 | 2 | `HEADING_TEXT_MATCH` |
| `Claim firewall and route decision` | 177 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 204 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `40` before writing and `40` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `5`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `51d85d2f6ced240c82d243af7fc30d1cb5b9571bc96aba5828a4073476827d42`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 46–49 | `001c15b1e6743ff15de089ddd090b1e45fb4c1695ff4a7b899595e8fae8dfea3` |
| D02 | equation | 62–67 | `b0a28707730955a18c77823c0cdaae78ac7e40cb5264725fc1baf4dabf92a1a3` |
| D03 | equation | 69–75 | `530e49574419b8a99d826856ed52e499880db8d3fa0ffacceac809253e693565` |
| D04 | equation | 77–82 | `ac81fc3c6066b90080752abefc5fb811aa0c93263ae4cb8230bfec0674b6c81d` |
| D05 | equation | 86–91 | `bb57f66b7af183da8f7aa62bc477af1d0a56527fb55de8c048ea26e1597c11f5` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 9: `\title{A Prime-Shell Tilt Phase Diagram\ for a Finite Twin-Prime Operator}`
- TeX line 21: `The preceding TPC-362 shell ladder found that a finite normalized spectral`
- TeX line 24: `test a different finite modeling choice: multiply the literal block for`
- TeX line 31: `finite phase point with maximum normalized spectrum`
- TeX line 33: `$0.66938300094026681$.  This is a scoped finite phase diagram and a modeling`
- TeX line 34: `observation, not an asymptotic operator bound, an arithmetic estimate, or a`
- TeX line 44: `changes the finite geometry at all.  We use the dimensionless family`
- TeX line 53: `the finite phase diagram, while the next holdout must test any apparent`
- TeX line 59: `\section{Weighted finite operator}`
- TeX line 84: `certificate checks positivity on every declared row.  The exact finite`
- TeX line 96: `inherited finite working cap; it is not asserted uniformly in $Q$.`
- TeX line 102: `it is a diagnostic, not a new normalization theorem.`
- TeX line 106: `\caption{Complete finite phase diagram over 192 rows per tilt.}`
- TeX line 127: `The effective fraction remains at least $0.6693830$, so the finite result is`
- TeX line 154: `dependence is itself useful evidence.  It says that a finite cap can be`
- TeX line 155: `strongly affected by the chosen shell geometry, but does not identify which`
- TeX line 160: `The finite algebra is straightforward but important.  Positive weights`
- TeX line 163: `well-defined.  Schur and Frobenius inequalities then apply to every finite`
- TeX line 164: `matrix without an asymptotic assumption.`
- TeX line 180: `TPC364_WEIGHTED_BLOCK_DEFINITION = PROVED_EXACT_FINITE`
- TeX line 181: `TPC364_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE`
- TeX line 182: `TPC364_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_960_ROWS`
- TeX line 183: `TPC364_PHASE_DIAGRAM = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 184: `TPC364_BETA2_PANEL_CAP_REPAIR = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 185: `TPC364_BETA2_ASYMPTOTIC_REPAIR = OPEN`
- TeX line 186: `TPC364_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN`
- TeX line 187: `TPC364_GROWING_OPERATOR_BOUND = OPEN`
- TeX line 188: `TPC364_SOURCE_UNIFORM_L2 = OPEN`
- TeX line 191: `TPC364_FULL_GATE_B = OPEN`
- TeX line 195: `The strongest positive result is a finite, all-law beta=2 cap repair on the`
- TeX line 197: `point was identified from a finite menu on the same panel, and the weighting`
- TeX line 207: `prime-shell tilt changes the finite normalized operator substantially: the`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#tab:phase` → `main.tex#L107` (existing project target or original TeX label line).
- Link relocation: `#tab:q` → `main.tex#L137` (existing project target or original TeX label line).
