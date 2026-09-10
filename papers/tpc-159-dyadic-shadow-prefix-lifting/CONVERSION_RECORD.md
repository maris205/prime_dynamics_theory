# TPC-159 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `a1b375fcbceb9d470f7817b99eac7b4688163fb783351f18831fa34169316968`.
- Bibliography: [references.bib](references.bib), SHA-256 `272eaf6d2162387fd217a0e5be3e5c53dc9cb698e8728065b726e38c5c5dc9b4`.
- Preserved PDF: [tpc-159-dyadic-shadow-prefix-lifting.pdf](tpc-159-dyadic-shadow-prefix-lifting.pdf), SHA-256 `b4b56682f54424e619fe183e90012a69d3a0e75956672cbcd7b60e6fae758f81`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `a9ad1953917e7cb84955e7d031ce50ea70acba905437494124defd8aae6c3afb`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC157_159.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Source theorem and notation` | 61 | 1 | `HEADING_TEXT_MATCH` |
| `The dyadic shadow` | 92 | 2 | `HEADING_TEXT_MATCH` |
| `Cumulative prefix lifting` | 125 | 2 | `HEADING_TEXT_MATCH` |
| `Why this is not all-prefix control` | 204 | 3 | `HEADING_TEXT_MATCH` |
| `Audit and level` | 234 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 252 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 262 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `56` before writing and `56` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `18`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `a5147ad5caaa0106f540b958a93a949c9e60df20c9eab15502d7b06b974aa498`.
- Source theorem/proof environment starts: proposition at TeX line 102, proof at TeX line 113, theorem at TeX line 133, proof at TeX line 157, corollary at TeX line 195, proposition at TeX line 206, proof at TeX line 212.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 64–67 | `f156a8f484ecb49fa25af9acd52c92ad7d8dc67a301840244ac346c6d6a87639` |
| D02 | \[...\] | 69–72 | `5d3d74ee5d64cbc95b147c3615687fd78da366598b1baf79a43b5af6c04bb5e2` |
| D03 | equation | 76–80 | `de4609bf92814b16bab9adf00d3da1a5b2707866705d40303d95ec597025a191` |
| D04 | equation | 82–88 | `c3be52235d61b8bac6995a20236796ec58c7d526e5500dafe65d940d875e645f` |
| D05 | equation | 95–99 | `6a3df43e2dfd6cdee2f7b6bcaee6022e7c18f72581c969e6efbcbb128a411c12` |
| D06 | equation | 104–110 | `f037c3b4d89f755171ddb1e1438743f58970c35984b4c34e710e1cb1e4ffb122` |
| D07 | \[...\] | 116–119 | `4513d21bb5b62a736f4b4aaf8acd95b15a3379aca61e89a0566b0a5a4ab77c9a` |
| D08 | \[...\] | 128–131 | `ea9ca407303cdee0c0f43e3b16a99244b96b79eae061578a58e12218c5a6a2a5` |
| D09 | \[...\] | 135–139 | `2b6f3ca9cb506cc927e0dde553b3f34c64da3a1be92db85a749701fff38473d2` |
| D10 | equation | 141–147 | `91c7b54fdfcfed7eef56a1b4699bd0d7e001c8fd071f140b6f888755b8d06d52` |
| D11 | \[...\] | 149–153 | `fc4a828519523d741df1e3e92091542a5e22ae9589b29ede777e8718f64917d6` |
| D12 | equation | 159–166 | `33e9000812836c9f724be189205b58b4568c172be091b7a50ea27a830d0ce548` |
| D13 | \[...\] | 170–175 | `c6334db4b83c6c3d0a586cc5eb9f97d4c48bbb6e8463ff5705a1fc39c47c3d41` |
| D14 | \[...\] | 177–181 | `13ea746a0a34ee1a9168e83934b27953cef6fd1086fb67e216acc138105f65f1` |
| D15 | \[...\] | 187–190 | `ccae4bd53178bc21bfb04cb8c4941e7ff873d2cde252b3437a7114a997925a0e` |
| D16 | \[...\] | 197–200 | `196b26b1d585594389ca543b5305346c7b201b3dd3602da3d9acfc712f9beb0f` |
| D17 | \[...\] | 216–219 | `e3aabfec85dff5043daf3a0211b75968001f75b69dd8cf81fc4b6e7bec1123e7` |
| D18 | \[...\] | 242–247 | `adef65b3916e5fb79c7bd95e0e9669504f0194fb43953900770414ff317aa20e` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 44: `It does not control every predetermined atomic endpoint.`
- TeX line 55: `explicit sparse shadow.  Logarithmic density does not prove that a`
- TeX line 168: `\(N_j=T/2^j\) avoids \(\E_X^\star\).  The endpoint assumptions put`
- TeX line 207: `The measure estimate \eqref{eq:shadowmeasure}, by itself, does not`
- TeX line 208: `imply that a prescribed finite or discrete endpoint set`
- TeX line 220: `This is a finite or countable subset of \([\sqrt X,X]\), so it has`
- TeX line 256: `does not accumulate a \(\log\log X\) factor; only the exceptional`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:exception` → `../main.tex#L79` (existing project target or original TeX label line).
- Link relocation: `#eq:source` → `../main.tex#L87` (existing project target or original TeX label line).
- Link relocation: `#thm:main` → `../main.tex#L133` (existing project target or original TeX label line).
- Link relocation: `#eq:shadowmeasure` → `../main.tex#L109` (existing project target or original TeX label line).
- Link relocation: `#eq:telescoping` → `../main.tex#L165` (existing project target or original TeX label line).
