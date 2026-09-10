# TPC-187 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `a6ab02eaf7e4d037eaad9963d2301d2f2ce6d78f62559576991c9acd6882be40`.
- Bibliography: [references.bib](references.bib), SHA-256 `5a682d60c3fcfa3237ac3236302d5747bc272ba10ebbf9d903bb9c36a080272a`.
- Preserved PDF: [tpc-187-size-only-local-oscillation-barrier.pdf](tpc-187-size-only-local-oscillation-barrier.pdf), SHA-256 `4d7beb88ae8243483512c2de5c8de1cdc33bb19ec32c727b4de53d1217ca3dce`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `a0debe41e03b54f572e8de7d04b6a26bfa0feffdb27f7955122d130bc3e184ba`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC185_189.md).
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

- TeX line 17: `The triangle inequality gives only block length after q/T normalization.  A constant-sign synthetic sequence attains that bound, so boundedness and support size alone cannot yield any fixed-X power saving.  This stops only the size-only local oscillation method.`
- TeX line 24: `signature is actual fixed-$h_0$ packet, named fixed atom, deterministic every`
- TeX line 26: `active support.  Throughout $h_0=2$ is only a source-backed data fact.`
- TeX line 30: `For |a\_\allowbreak{}j|<=1 on a block of length L, max\_\allowbreak{}r|sum\_\allowbreak{}{j<=r}a\_\allowbreak{}j|<=L, with equality for a\_\allowbreak{}j=1.  Hence no uniform X\^{}{-sigma} follows from coefficient size and cardinality alone.`
- TeX line 33: `Triangle inequality gives max\_\allowbreak{}{r<=L}|sum\_\allowbreak{}{j<=r}a\_\allowbreak{}j|<=L whenever |a\_\allowbreak{}j|<=1.  The synthetic fixture a\_\allowbreak{}j=1 attains L at r=L.  Therefore no argument using only these two premises can force a factor X\^{}{-sigma}; arithmetic cancellation is an additional necessary input.`
- TeX line 40: `The cell \texttt{SIZE\_\allowbreak{}ONLY\_\allowbreak{}LOCAL\_\allowbreak{}OSCILLATION\_\allowbreak{}METHOD} is \textsc{stop-scoped}. This does not stop either O161 pointwise parent or the global architecture.`
- TeX line 43: `not named atoms.  Fixed $h_0=2$ is not decay.  Archive addressing is not`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
