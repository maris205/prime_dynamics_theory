# TPC-196 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `86275108260f7ef4405766e6416afca086635c29431b86c745fde9946be2b2e1`.
- Bibliography: [references.bib](references.bib), SHA-256 `e3de68e5a5b78731b757215d9d557348d348c812eab9b8575355d063f28f59c5`.
- Preserved PDF: [tpc-196-rational-atom-residue-determinant-ledger.pdf](tpc-196-rational-atom-residue-determinant-ledger.pdf), SHA-256 `a5525806bf7c711339e1934d1b97beebdad4084f6ee1d9b5bb77438d2698a706`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `a04dc4fdf22dcfe5621b1d73b259afeaf123611f350c89ff2d1df99fedd13977`.
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
| `Exact residue decomposition` | 34 | 1 | `HEADING_TEXT_MATCH` |
| `Imported identities and new crosswalk` | 67 | 2 | `HEADING_TEXT_MATCH` |
| `Firewall` | 74 | 2 | `HEADING_TEXT_MATCH` |
| `Loss, level and scope ledger` | 81 | 2 | `HEADING_TEXT_MATCH` |
| `Machine certificate` | 96 | 2 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 105 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `28` before writing and `28` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `5`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `6b3d35f13f25890422544ab7c2cade63684d9b59a5c1d8c532cf393dd862072a`.
- Source theorem/proof environment starts: theorem at TeX line 50, proof at TeX line 60.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 36–38 | `5c116ecbf6f58513e330962f313edaadf9e18e3017054f7057587070e49f3414` |
| D02 | equation | 40–43 | `e3af83a551a6a5b915290ab359a58860233fdae89a1e38696b8a7f96844a35ca` |
| D03 | \[...\] | 46–48 | `9c5a1a60a07913b851ece3a11d0e6736b905780d37d8df508cce556d30ae03bf` |
| D04 | \[...\] | 54–56 | `d5ecef1f4f00ad1614b9335c6cba8762dd8ae23d673521b5bdfe1a710460f112` |
| D05 | \[...\] | 83–85 | `3d1adcc98ff3df90dc782b1867fd2162fb0366b2d039eec78b27929e49b0ec7e` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 26: `The target has six simultaneous axes: actual fixed-\(h_0\) packet,`
- TeX line 29: `support.  The value \(h_0=2\) is source-backed data only.  Repository hashes`
- TeX line 84: `\texttt{UNIFORM\_\allowbreak{}ALL\_\allowbreak{}RESIDUE\_\allowbreak{}CLASS\_\allowbreak{}CANCELLATION\_\allowbreak{}OR\_\allowbreak{}DIRECT\_\allowbreak{}MODE\_\allowbreak{}THEOREM}.`
- TeX line 97: `The adjacent canonical payload freezes the formula or finite witness,`
- TeX line 101: `constant leaves.  The checker recomputes the finite certificate and executes`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:dft` → `../main.tex#L40` (existing project target or original TeX label line).
