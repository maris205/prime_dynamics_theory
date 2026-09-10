# TPC-177 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `81ce3d6e2224cb63a1d3e394aafa462369e5089cbd0ecd6011934f0bc129b04b`.
- Bibliography: [references.bib](references.bib), SHA-256 `4eb10ee2beaab38afe05d1f4393a2aa22d71d5e3a0aa93dc0645fe0391b3bdcb`.
- Preserved PDF: [tpc-177-actual-active-support-vacuity-firewall.pdf](tpc-177-actual-active-support-vacuity-firewall.pdf), SHA-256 `d976164346e469d8c268fd5b245a91d2196e41d551a38a60f43615b36c654b79`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `f1fa9cbadc3dfa619f85e6c8aa1db8bbdaef45921097675a7192150f5fea086f`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC175_179.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Two independent prerequisites` | 63 | 1 | `HEADING_TEXT_MATCH` |
| `The eligible domain` | 86 | 1 | `HEADING_TEXT_MATCH` |
| `The vacuity firewall` | 123 | 2 | `HEADING_TEXT_MATCH` |
| `Separation from the H9 literal-weight registry` | 170 | 2 | `HEADING_TEXT_MATCH` |
| `Reproducibility and claim boundary` | 191 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 205 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 216 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `23` before writing and `23` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `8`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `cc18531987d5fa2edbab839bb424562246b44c1d16c3e18fddb9449e1e821724`.
- Source theorem/proof environment starts: proposition at TeX line 111, proof at TeX line 119, theorem at TeX line 136, proof at TeX line 142.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 67–73 | `82f4b292bfb931f28d5575b9bdda88cccb5ff60ff8c5d2983fc3c8390ca1ca9e` |
| D02 | \[...\] | 80–82 | `73695fb24bb794bbab68dc21cf4177a74428e087adc5f3d12916a6c54a83c1ea` |
| D03 | \[...\] | 90–92 | `b4e6b40ba37600754bf649cdf2af2597f470afe55dbaefa4bffff8527db4c5ec` |
| D04 | \[...\] | 98–107 | `37f0d67f11e919dbcf1d9f184b0fbe9caa43e1dc010af26fad17cdc9f9ff9f84` |
| D05 | \[...\] | 113–116 | `05cd67093857e5a3261d9e58c0041855a8a49a2f3986d73bbee811d3bf2bd3a7` |
| D06 | \[...\] | 126–128 | `cbbae74d6ff56ae201bb1970234fcc8f56a60243ca91233d95a6b43b570b5685` |
| D07 | \[...\] | 131–134 | `f9cdb6e4a8763969d225cace15b7e250afd85d5368d5793aa024d2bc2ac25336` |
| D08 | \[...\] | 181–187 | `5c93c44f60170f281f9d978eef0a613ec8541f890731360ec180f7f6f477142b` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 84: `synthetic fixture does not satisfy (2).`
- TeX line 94: `formal archived cut or a synthetic carrier would fabricate the`
- TeX line 137: `Equation (6) does not prove (7).  The executable audit status is`
- TeX line 145: `This does not prove that an actual active carrier is mathematically`
- TeX line 177: `decay axis \texttt{NONE}; it does not manufacture a cancellation`
- TeX line 200: `No fixed physical \(h_0=2\), named phase, deterministic endpoint,`
- TeX line 210: `the H1 support root open and keeps it disjoint from the H9`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
