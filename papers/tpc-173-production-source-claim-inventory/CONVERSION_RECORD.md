# TPC-173 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `746486b11a2bf7607f86018ccdddda233dd802e32b14f49d500168bc1bfec4e7`.
- Bibliography: [references.bib](references.bib), SHA-256 `77ca3916bfe7f13c0c7f141003d89c57ff3f2fbd45fe204afb9e693b85646030`.
- Preserved PDF: [tpc-173-production-source-claim-inventory.pdf](tpc-173-production-source-claim-inventory.pdf), SHA-256 `e93a8f1e4a78a844580d6a993ab065ed94f87b804f7f19c3b804f43388a15984`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `70fe23f0662636f19daf92ccc103df065627f27f533dacc74b1e4b791c58769d`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC170_174.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Declared corpus` | 55 | 1 | `HEADING_TEXT_MATCH` |
| `Qualification contract` | 75 | 1 | `HEADING_TEXT_MATCH` |
| `Exact corpus partition` | 95 | 2 | `HEADING_TEXT_MATCH` |
| `Why the near-claims do not qualify` | 132 | 2 | `HEADING_TEXT_MATCH` |
| `Scoped maximal conclusion` | 161 | 2 | `HEADING_TEXT_MATCH` |
| `Claim firewall` | 180 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 189 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `21` before writing and `21` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `3`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `1ff8aa4bbf60ace52d802073f709336a293bfc9d7a33547c791bcb1cf4b09b38`.
- Source theorem/proof environment starts: definition at TeX line 57, definition at TeX line 77, theorem at TeX line 97, proof at TeX line 120, proposition at TeX line 163, proof at TeX line 170.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 60–62 | `bad5b7ce1f5794f1724c4257342f811d80a545e9f9a697f9e33798efcd9f3abe` |
| D02 | \[...\] | 99–111 | `d88f4610b4750f03b22c0df2a914d9b2ca1b8bc4df1e4b7b6fbe9014c03ede10` |
| D03 | \[...\] | 114–117 | `993af3a970ba2d9a8bd16e7fa6341656a8c8a22d329cfc78a19932f2c2b26e6e` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 37: `eleven artifacts from six papers and explicitly was not a future-schema`
- TeX line 49: `with exact edge weight, fixed \(h_0=2\), and physical-normalization lineage.`
- TeX line 64: `number-based; it is not a keyword sample.`
- TeX line 87: `\item fixed \(h_0=2\) and physical-normalization lineage.`
- TeX line 142: `the row is explicitly not an actual occurrence\\`
- TeX line 157: `In particular, ''actual core'' on the arithmetic branch does not supply a`
- TeX line 159: `weight one does not acquire actual-carrier semantics.`
- TeX line 165: `in \(\mathcal C_{173}\).  It does not imply that no local actual-occurrence`
- TeX line 171: `The corpus is finite and explicitly declared.  No completeness theorem for`
- TeX line 172: `all mathematical sources is assumed.  New source mathematics or an`
- TeX line 177: `contract.  That contract can be proved nonvacuous synthetically, but it`
- TeX line 182: `This paper is an \(\Lone\) source-census obstruction with finite`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#def:qualifying` → `../main.tex#L77` (existing project target or original TeX label line).
- Link relocation: `#eq:zero` → `../main.tex#L116` (existing project target or original TeX label line).
