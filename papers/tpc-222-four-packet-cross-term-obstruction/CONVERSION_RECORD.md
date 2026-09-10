# TPC-222 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `90db2a4c0085cc8a97cd13d317a703481e6f5f932e2ddfa95d38beacd638af9f`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `717d8ec6127bb965a00816bf961fd051d416ca47efb548f9d3eaa9ba0e953041`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `8ab5c80850757b36a7d4c3309055e86df849297fb6290e23200955ad58b38460`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC220_224.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Four packet interface` | 34 | 1 | `HEADING_TEXT_MATCH` |
| `Exact four-point polarization` | 68 | 2 | `HEADING_TEXT_MATCH` |
| `Same trace, different signed reassembly` | 109 | 2 | `HEADING_TEXT_MATCH` |
| `Certificate and route position` | 138 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 169 | 3 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 176 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `38` before writing and `38` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `9`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `c070f213de3faf25d98dbf2de4d043d03b8b851f9925980fb0f5bb4ad60e5fa1`.
- Source theorem/proof environment starts: theorem at TeX line 51, proof at TeX line 59, theorem at TeX line 70, proof at TeX line 79, corollary at TeX line 94, proof at TeX line 103, theorem at TeX line 111, proof at TeX line 124.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 37–42 | `63039c08e6a0500379bfef368bbe1737bb2f126f5c9eef4693632acfa37fd234` |
| D02 | \[...\] | 45–47 | `b6d5ac1262ebc629c00c422eb5e15075f1813f34169df2d82b1f0704e5d7133a` |
| D03 | \[...\] | 53–56 | `20cc23cd34712850ee50db3ad645af07531e74a43e7fcb56a39d5d6cf3c9b51f` |
| D04 | \[...\] | 72–76 | `a02c81556d8bce52661e2f0992a05334c28b15a1ac70ebe6cab27eafb921d2f0` |
| D05 | \[...\] | 81–84 | `f408ee85e834f9d63bfa2b91ea8554b1ed71b71dfae76c5a639f182146f4ca9f` |
| D06 | \[...\] | 96–99 | `72db83f6854d8f259553b103d10c3f8c2fae25546deab63ea5deee69bb651431` |
| D07 | \[...\] | 113–115 | `2ae75536eaec0dc1b9a61856a7b611444bb23d9e7325c0ab6cd351951a83b0df` |
| D08 | \[...\] | 118–121 | `07f59c51d7f34b05f740437375706335fd58b4b4ef7fb65a8d04052cc31eb2d9` |
| D09 | \[...\] | 163–167 | `86c25b9a4a2a7757caa675ed2b2cce1a0bf8426fbd1c2fead9a9e5309f48731b` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 22: `form.  The four-packet Gram is positive semidefinite, its coefficient energy is a Rayleigh`
- TeX line 28: `cross-correlation theorem; no arithmetic $L^2$ advance is claimed.`
- TeX line 52: `The matrix $\G$ is Hermitian positive semidefinite and`
- TeX line 66: `envelope, but does not determine these phases.`
- TeX line 135: `reassembly.  This is a finite scoped obstruction; it is not an assertion that these two`
- TeX line 148: `object & finite scope & status\\`
- TeX line 166: `\texttt{FULL\_GATE\_B=OPEN}.`
- TeX line 174: `cross-correlation estimate remains the open bridge to the prime shell.`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
