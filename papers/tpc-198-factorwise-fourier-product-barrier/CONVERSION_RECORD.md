# TPC-198 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `0e620e9c535d813966dd60f6c6e806ab525872e511d18f286b37b7de388e32ed`.
- Bibliography: [references.bib](references.bib), SHA-256 `e3de68e5a5b78731b757215d9d557348d348c812eab9b8575355d063f28f59c5`.
- Preserved PDF: [tpc-198-factorwise-fourier-product-barrier.pdf](tpc-198-factorwise-fourier-product-barrier.pdf), SHA-256 `1cb3f8e484ebd54e04615e21feb02b43dc9a32df256f969f4e6d250d8ff6cf20`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `699839feb66ac5e4b1763842b15573d0b08aee1791642a9108283137b53886c3`.
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
| `Rudin--Shapiro witness` | 34 | 1 | `HEADING_TEXT_MATCH` |
| `Scoped interpretation` | 64 | 1 | `HEADING_TEXT_MATCH` |
| `Loss, level and scope ledger` | 75 | 2 | `HEADING_TEXT_MATCH` |
| `Machine certificate` | 90 | 2 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 99 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `25` before writing and `25` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `5`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `1c09708e94c12ac2a86dce8fab01836cddfe68dcc7164550c08ee7bc9534b05a`.
- Source theorem/proof environment starts: theorem at TeX line 48, proof at TeX line 58.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 36–39 | `b64bb11acafadaf2408cac3f2aced657165eb56a8f0154b00b6b61cfbd74213a` |
| D02 | \[...\] | 42–44 | `0387aaa024943e63d78d8a1b1d580f302e010026c1818cef8a2cdd6c6e9f1433` |
| D03 | \[...\] | 52–54 | `adea7f5d6cbad30a1f6c3ed95e640d6fa4026cd41399c91ee2752ff6cd422767` |
| D04 | \[...\] | 67–71 | `3fde55d5dfdd1f3bf82ad0c7c4c7d51d11cd87be8a6b40d1850c595aceeae524` |
| D05 | \[...\] | 77–79 | `701fd46113c1d0ebaf6d3ddad859527576e89bc2cc81f544689a93960ecc8637` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 19: `Rudin--Shapiro coefficients give two factors with uniform square-root Fourier bounds whose modulated pointwise product has a full linear resonance at a prescribed atom.  This stops only the factorwise-single-Fourier black-box implication.`
- TeX line 26: `The target has six simultaneous axes: actual fixed-\(h_0\) packet,`
- TeX line 29: `support.  The value \(h_0=2\) is source-backed data only.  Repository hashes`
- TeX line 50: `\(g(n)=\rho_n \e(\alpha_\star n)\).  Both \(f\) and \(g\) have uniform`
- TeX line 55: `Therefore factorwise uniform Fourier bounds, used as black-box premises,`
- TeX line 65: `The witness is synthetic and is not asserted to model the Möbius function.`
- TeX line 72: `Arithmetic identities that couple the two Möbius factors remain open.`
- TeX line 91: `The adjacent canonical payload freezes the formula or finite witness,`
- TeX line 95: `constant leaves.  The checker recomputes the finite certificate and executes`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
