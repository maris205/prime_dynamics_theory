# TPC-192 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `12e9b14b13b9fe4a552743832efd78b6c31e83e1a73f88473ee94dc16bd08f9e`.
- Bibliography: [references.bib](references.bib), SHA-256 `5a682d60c3fcfa3237ac3236302d5747bc272ba10ebbf9d903bb9c36a080272a`.
- Preserved PDF: [tpc-192-mvp9-pointwise-frontier-route-decision.pdf](tpc-192-mvp9-pointwise-frontier-route-decision.pdf), SHA-256 `7f0bfd3ff2456324fdbe30e1091d8a68af441fde808f8a64a897c07a76bbc1d8`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `dc4852b9ec5e7dab530c73982fd06b754efe288475941424a8c2315cc7dd7796`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC190_194.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Frozen target` | 22 | 1 | `HEADING_TEXT_MATCH` |
| `Exact result` | 28 | 1 | `HEADING_TEXT_MATCH` |
| `Scoped stop and claim firewall` | 39 | 1 | `HEADING_TEXT_MATCH` |
| `Reproducibility` | 49 | 1 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 54 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `5` before writing and `5` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `0`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `14381cf0ec9c68506dd2b3efd1875f0394a6814d86bf8ab2668d2c8454865729`.
- Source theorem/proof environment starts: theorem at TeX line 29, proof at TeX line 32.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| — | No explicit display environment | — | — |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 17: `MVP9 imports TPC-183--191 fail-closed.  The structural first missing node and seven-root minimal blocker antichain are unchanged. Both pointwise O161 parents remain open; three method cells are STOP\_\allowbreak{}SCOPED.  Fixed-atom endpoint credit is zero and the strict 1/400 budget remains unpaid.`
- TeX line 23: `The selected route is \texttt{POINTWISE\_\allowbreak{}FRONTIER\_\allowbreak{}REMAINS\_\allowbreak{}OPEN} \citep{TPC182}.  The required`
- TeX line 24: `signature is actual fixed-$h_0$ packet, named fixed atom, deterministic every`
- TeX line 26: `active support.  Throughout $h_0=2$ is only a source-backed data fact.`
- TeX line 33: `The MVP9 checker opens TPC-183--191 in paper order, verifies each canonical payload hash, expected verdict, selected route, six-axis signature, firewall, L2=false and zero endpoint credit.  It reads the new scoped cells from TPC-187 and TPC-190 and the inherited selector cell from TPC-181.  It also rechecks the unchanged TPC-182 global first missing node.  These imports compute the stated route status without promoting a method stop to a theorem stop.`
- TeX line 43: `not named atoms.  Fixed $h_0=2$ is not decay.  Archive addressing is not`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
