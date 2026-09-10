# TPC-184 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `c45f5f83c6e9f066e9c4ab5b6c8bac586bf4ec7fde66e1c33726475c7fef5306`.
- Bibliography: [references.bib](references.bib), SHA-256 `5a682d60c3fcfa3237ac3236302d5747bc272ba10ebbf9d903bb9c36a080272a`.
- Preserved PDF: [tpc-184-bad-endpoint-literal-target-contract.pdf](tpc-184-bad-endpoint-literal-target-contract.pdf), SHA-256 `e90e79fa7e4768429d3bddda7d92de6f22ceeefd4b0600abb82444f1b0481aa5`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `639fa642863212d57c30b8609a7116b8ffeba06cdc8e20dd590fb69e1737bb43`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC180_184.md).
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

- TeX line 17: `The bad-endpoint target is frozen as a q/T-normalized cumulative actual-core sum at the prescribed atom, uniformly over every prefix endpoint and deterministic scale.  TPC-159 supplies only the complement of its dyadic shadow; TPC-169 supplies all prefixes only in phase L2.  Neither matches the contract.`
- TeX line 24: `signature is actual fixed-$h_0$ packet, named fixed atom, deterministic every`
- TeX line 26: `active support.  Throughout $h_0=2$ is only a source-backed data fact.`
- TeX line 43: `not named atoms.  Fixed $h_0=2$ is not decay.  Archive addressing is not`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
