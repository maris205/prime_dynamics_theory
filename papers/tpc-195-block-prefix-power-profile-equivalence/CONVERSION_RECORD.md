# TPC-195 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `416976cfe9b38c6d65135eeba4a490c79a8f08f74a35dd5e0a9d0b52b822e12f`.
- Bibliography: [references.bib](references.bib), SHA-256 `e3de68e5a5b78731b757215d9d557348d348c812eab9b8575355d063f28f59c5`.
- Preserved PDF: [tpc-195-block-prefix-power-profile-equivalence.pdf](tpc-195-block-prefix-power-profile-equivalence.pdf), SHA-256 `af012d50155a13afeff089812b9064fc98a57a0ec99a74378ca3e463e2fba64d`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `c221c9fec18a440ca130c38d95fe7a8599340d687609bbcdc477884549ee60d8`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC195_199.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Target contract and source boundary` | 25 | 1 | `HEADING_TEXT_MATCH` |
| `Abstract sequence theorem` | 34 | 1 | `HEADING_TEXT_MATCH` |
| `Truncated range ledger` | 66 | 2 | `HEADING_TEXT_MATCH` |
| `Route consequence` | 81 | 2 | `HEADING_TEXT_MATCH` |
| `Loss, level and scope ledger` | 87 | 2 | `HEADING_TEXT_MATCH` |
| `Machine certificate` | 102 | 2 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 111 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `32` before writing and `32` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `5`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `53301d70f7cddd1745f2f9114ce0d4f23e304b1b0748316593aa69c5218c447f`.
- Source theorem/proof environment starts: theorem at TeX line 40, proof at TeX line 54.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 42–44 | `206bcd5dfd0219bce3069d5a2dc8433e383a77bb6cc99e3ed0042b510c6a6d81` |
| D02 | \[...\] | 46–48 | `775402968b107fc0a9108309b18aff303bca15404fc793cc579ee91a42df8722` |
| D03 | \[...\] | 50–52 | `7fde46f7c4be698435682a5137d29362b98ef09ce71c12f5fe48e1b19bc020a7` |
| D04 | \[...\] | 72–74 | `1711f56e89dac1bf8078b623bfec2317aa3c468e49cc2e07c0158538707d6ea3` |
| D05 | \[...\] | 89–91 | `4dcd02a84c3d4659a0d2e7d3eee5b9380239d02a3d2d313f7daf080ade1cf1b5` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 26: `The target has six simultaneous axes: actual fixed-\(h_0\) packet,`
- TeX line 29: `support.  The value \(h_0=2\) is source-backed data only.  Repository hashes`
- TeX line 41: `If, uniformly for all \(N>0\),`
- TeX line 76: `full theorem is not a license to identify a terminal block with a cumulative`
- TeX line 77: `prefix, and the truncated theorem does not yield a fixed \(X\)-power for`
- TeX line 103: `The adjacent canonical payload freezes the formula or finite witness,`
- TeX line 107: `constant leaves.  The checker recomputes the finite certificate and executes`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
