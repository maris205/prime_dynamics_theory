# TPC-141 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `57ba1c4538560532d4c090ca5f1333f23b36936992f2c865027bb2fb84401035`.
- Bibliography: [references.bib](references.bib), SHA-256 `1d435e5bdf6b2d4126962ca138645c9e72cff58872de13acd0516631a1fa24c9`.
- Preserved PDF: [tpc-141-source-locked-cut-arithmetic-integration.pdf](tpc-141-source-locked-cut-arithmetic-integration.pdf), SHA-256 `6e6efe9d6892c08dd6e9060e6bd25656a36621dcd2e1637895f5525c3998cebf`; 6 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `551e8ee9160de1854aea626b208cc504a7714ce04bea93ce0d61d20673faf5f2`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC140_142.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `The inherited target and the two new branches` | 115 | 1 | `HEADING_TEXT_MATCH` |
| `Source-locked records` | 155 | 2 | `HEADING_TEXT_MATCH` |
| `The complete cut and the frontier` | 217 | 3 | `HEADING_TEXT_MATCH` |
| `What the arithmetic shadow proves` | 262 | 3 | `HEADING_TEXT_MATCH` |
| `Cut-aware synthesis` | 317 | 4 | `HEADING_TEXT_MATCH` |
| `The nonduplicated \texorpdfstring{\(1/400\)}{1/400} ledger` | 365 | 4 | `HEADING_TEXT_MATCH` |
| `The source-locked manifest` | 418 | 5 | `HEADING_TEXT_MATCH` |
| `Deterministic audit and claim boundary` | 477 | 5 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 515 | 6 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 537 | 6 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `65` before writing and `65` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `17`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `28e3741a0c9e13b6777ae32216528e1cf622b185efe3afd04e9ca9f61815f9e7`.
- Source theorem/proof environment starts: definition at TeX line 157, definition at TeX line 171, theorem at TeX line 184, proof at TeX line 206, proposition at TeX line 241, definition at TeX line 255, proposition at TeX line 299, theorem at TeX line 319, proof at TeX line 347, remark at TeX line 353, proposition at TeX line 391.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 69–73 | `800048bb5e8ca28cddbf124d440c8528ac38c6b8964513fb4d52d9a375c91d6e` |
| D02 | \[...\] | 77–81 | `bf590da3b44f6616caab7e0ac3f400dbd08be522654c724e6953e1980e68a4df` |
| D03 | equation | 121–126 | `c1707ffe69b9609d4352aeb079f4dd0505d4437868714e059de73b9cfc35c595` |
| D04 | \[...\] | 159–163 | `ac6ba002f1000ec5c65a08fec638c3d5d1c797a9be60bb8c955e42a445e4c885` |
| D05 | \[...\] | 222–226 | `0d2c67555b31c13a25b9dd289eb96b45f03fb671e2c7195a826b24e0c74af734` |
| D06 | equation | 228–233 | `8ac6b99d21e5b574f024155df373b57fd669d6d498db6781658502ada43095e3` |
| D07 | equation | 236–239 | `88c53abfd893e78d7e2fb167ec0209e7ba01737a11f7c3c0fdb550ed3376705d` |
| D08 | \[...\] | 273–277 | `4aded733f37ed6260d95760acfbe224a6715206fae1771b2e38eaf53a72a87ea` |
| D09 | \[...\] | 291–295 | `517254ff28289833a473748a556554452f499ea3ceef71eb1a368b81918b7c56` |
| D10 | \[...\] | 322–325 | `82adafb1fb4d20da4a4ae6c1c9480adf2744711ea190cb634ea8a49de51a0687` |
| D11 | \[...\] | 327–332 | `fd4f646990b654af0702b77db9c94cdfcd76c72b1e3866b1ac87993a75617338` |
| D12 | \[...\] | 334–340 | `4acb72111db03bba93c7a8bc4eef8aacedd4b47c76494845248e753993c0ec44` |
| D13 | \[...\] | 355–358 | `2ee86f50a25c828dbbe22a22403a1a4f53f090f625837b89e5b87b161c68d0b4` |
| D14 | \[...\] | 368–372 | `25ad952ae66019a08234e43f4513457737b4f7db152d22479b1503fca0e65c0e` |
| D15 | \[...\] | 379–386 | `5b35bb0f04ac427989b18d90d7aee2cffb8bf077255752555288cfe97a0a2b53` |
| D16 | \[...\] | 408–414 | `46ca2d0b9dcf4b92e2d55fb59be9c6a7f5e17dc13f5c7688fa81d0750f8bd180` |
| D17 | \[...\] | 511–513 | `0a884c2fa5f0e3af89b5f7c67554e0b8e61c09b8a716e2e2de1c9cfd09a45a3f` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 35: `\newcommand{\Bhard}{B_{h_0,\delta}}`
- TeX line 38: `\newcommand{\OPEN}{\textnormal{\textsc{open}}}`
- TeX line 56: `TPC-133--140 pursue two branches left open by the MVP3 route audit.`
- TeX line 70: `B_{h_0,\delta}(X)`
- TeX line 78: `|B_{h_0,\delta}(X)|`
- TeX line 90: `upper bound at or above the threshold is not a route obstruction`
- TeX line 106: `The machine audit checks hashes, types, exact finite covers, graph`
- TeX line 107: `syntax, and rational bookkeeping.  It does not prove the mathematical`
- TeX line 117: `Fix a prescribed nonzero even \(h_0\), a fixed rational`
- TeX line 122: `\Delta_{h_0,W}(X)`
- TeX line 128: `bound the literal \(\Bhard\), not a support-only or averaged-shift`
- TeX line 135: `generator for the opened atoms; TPC-134 gives an exact dyadic`
- TeX line 162: `(h_0,\delta,W_{\rm env},{\mathfrak q},\Omega,\nu,{\mathfrak a}),`
- TeX line 186: `Let a finite collection of paper exports and imports pass the`
- TeX line 193: `\item no primitive source assumes the hard-packet target or an`
- TeX line 202: `conditional interface, logarithmic shadow, finite regression or`
- TeX line 247: `coefficientwise compiler is not a complete cover of \(\mathcal A_X\).`
- TeX line 257: `frontier terminal has complete \(Q_D,Q_Z,G\), fixed-\(h_0\), cover,`
- TeX line 278: `appears in the proof DAG.  TPC-139 then names the missing uniform`
- TeX line 303: `logarithmic-density exceptional set does not supply the actual H3`
- TeX line 304: `packet estimate without, respectively, a growing-family uniformity`
- TeX line 314: `power of \(X\); it is not a lower bound showing that the actual family`
- TeX line 321: `Assume that the eligible nonsoft packets admit an amplitude estimate`
- TeX line 342: `eligible corridor but does not imply \(\Bhard=o(X)\) unless`
- TeX line 349: `inequality and then the two assumed eligible-corridor bounds.  The`
- TeX line 356: `|B_{h_0,\delta}(X)|`
- TeX line 400: `bound \(U\ge1/400\) without a lower obstruction is not a stop`
- TeX line 403: `The determinant--zero reserve is not a negative physical token.`
- TeX line 435: `The manifest identity is its canonical content, not a self-referential`
- TeX line 462: `open.\\`
- TeX line 463: `Growing affine uniformity & \(\OPEN\), L2 target &`
- TeX line 465: `uniformly uncontrolled.\\`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 7 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:soft` → `../main.tex#L238` (existing project target or original TeX label line).
- Link relocation: `#eq:soft` → `../main.tex#L238` (existing project target or original TeX label line).
- Link relocation: `#eq:cut` → `../main.tex#L232` (existing project target or original TeX label line).
