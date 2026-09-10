# TPC-249 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `6d8846f878b7ff3b54b0964264d31d31e246687bc9d758254b7676b4f546cc8a`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `13ce9b99e1e2965a36367db1b6a8d0ff8cdf7d4026cd4321699e4b2ef2a77eee`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `4e00ae77e8debd8b40584bc29a034757158a2d2065c662c2ce4e966158965995`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `95cfe3e787b113299fc91d67698cfe69e807896a507b3db873b4094eef214d2a`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC245_249.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Literal weighted probes` | 60 | 1 | `HEADING_TEXT_MATCH` |
| `Exact independent-lane radius` | 81 | 2 | `HEADING_TEXT_MATCH` |
| `One global budget` | 126 | 2 | `HEADING_TEXT_MATCH` |
| `Exact comparison with tagged marginals` | 149 | 3 | `HEADING_TEXT_MATCH` |
| `Exact certificate` | 181 | 3 | `HEADING_TEXT_MATCH` |
| `Route boundary and conclusion` | 192 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 214 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `67` before writing and `67` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `11`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `2fe4151a5b6a24e5ad499756e2cd87f1f92e8ef218de00425e14a29e72f643ec`.
- Source theorem/proof environment starts: theorem at TeX line 83, proof at TeX line 95, corollary at TeX line 110, remark at TeX line 121, theorem at TeX line 130, proof at TeX line 141, theorem at TeX line 156, proof at TeX line 162.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 46–49 | `b38d38b0bee9e6fc7ef5a571a8c5dbe3a6e1ed20033399b8b331d2228dce8f94` |
| D02 | \[...\] | 67–70 | `8613fbcd9fef485605c2f6dfdcacbd95ef25e4db3c9df019f821edba901de7be` |
| D03 | \[...\] | 73–78 | `82687ad0e99f19e842321c2eb053ef39f9dc9394183cfdec854875420fb17d78` |
| D04 | \[...\] | 86–91 | `2d69d339baceedf9b8a876b61da0f1feb9b307ac53d97ee903fdf13baa826165` |
| D05 | \[...\] | 99–102 | `9ef3677a5dc7eaec4fd8b73ad0e96a48a6bf1c951599da278e61e1c0c4748c66` |
| D06 | \[...\] | 113–116 | `9470c5644f19ec3de9e1fca6d0d1ba912a9018915835baa294f7b43fe80b77f2` |
| D07 | \[...\] | 132–134 | `9b49f7241592d8282338d626287c3d51af09b0740263525ba76b4f4a037b9249` |
| D08 | \[...\] | 136–138 | `a6b60a035d920605bd4e37c4588c124d87e0a5892e4b821bc4d576defde655d9` |
| D09 | \[...\] | 152–154 | `9a444c3a1c026060f77afbd85a6d8d17ae53ce04c629ca0d87423cde1aacb49b` |
| D10 | \[...\] | 175–177 | `de170990da86a3a0abf40f035fb88521018ee781bd120501010e90a5bdd66a5d` |
| D11 | \[...\] | 199–203 | `21f7ab8964cb71fc1feea44e6364453a595e7864965561c6e4e409fdf42d40ef` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 84: `Let $c$ range over a finite set, let $\rho_c\geq0$, and let`
- TeX line 122: `The affine domain is a modeling choice, not a source-forced V59 uncertainty`
- TeX line 123: `family.  The centered support theorem remains unconditional finite geometry.`
- TeX line 165: `condition for a finite sum in a complex Hilbert space is precisely that all`
- TeX line 183: `The finite certificate contains orthogonal, aligned, and exact-cancellation`
- TeX line 201: `\texttt{FULL\_GATE\_B=OPEN},\qquad`

## Conversion limitations

- The preamble-only glyphtounicode input was resolved with kpsewhich and checked against the audited SHA-256; its non-content mapping table was not expanded. The original command, source line, and dependency hash are retained in the reading layer.
- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
