# TPC-283 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `928077a9bd66c38f38bd0a9ee65d7b903ff25814`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `3909a015c96862e61a74fc65a4ad23d99359db23f50efc6c075d50b8899744f1`.

- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `4c0a50f8af69bfbdb6fb3451a5e02f44082cdffa64b0db4f7584551d4ce7a597`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `271d2503b88433f3715792347b73186a65a168d428f101cef8abd7625dc4da62`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC280_284.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Motivation` | 28 | 1 | `HEADING_TEXT_MATCH` |
| `Exact zeroing-radius theorem` | 40 | 1 | `HEADING_TEXT_MATCH` |
| `Finite transfer` | 74 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation for Gate B` | 110 | 2 | `HEADING_TEXT_MATCH` |
| `Verification and claim firewall` | 119 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 127 | 3 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 133 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `43` before writing and `43` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `6`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `b4d214e269c465d53d5a31d959722ebbdd885b4d4690765e34c7c95650e72abf`.
- Source theorem/proof environment starts: theorem at TeX line 41, proof at TeX line 60, remark at TeX line 68.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 31–34 | `850332846051e150750e52183f4e4a973f05a345a53796faed79383d45b9582c` |
| D02 | \[...\] | 43–45 | `0daba99cef13826946d673e9632643f8d531c2f75fad5b2869d94e9c5b82eead` |
| D03 | \[...\] | 48–50 | `c0620288d45ea9f0cb4e07ea193e9d83ad4e5689a9a33a5e32f8337a92d20907` |
| D04 | \[...\] | 52–58 | `b236b6a7f0977c68b847403e60e9c118ec41bb8d2b42319e681def43951bd683` |
| D05 | \[...\] | 62–64 | `d13c21508b7ca84d52a14e480f01ae8e5bec5bcab3ff3edc02ec6b2f8f6fd610` |
| D06 | \[...\] | 76–78 | `2b70c2a6207f41a49256bc29840e988a7447521e321d715b90a414be1e25bd0f` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 17: `literal V59 prime-shell operator on twelve finite rows.  We prove an exact`
- TeX line 24: `obstruction to inferring robust arithmetic nondegeneracy from a finite table.`
- TeX line 26: `class; admissible source stability remains open.`
- TeX line 74: `\section{Finite transfer}`
- TeX line 107: `$3.36\times10^{-5}$.  Thus the finite source is genuinely nonzero while its`
- TeX line 117: `characterized here.  Consequently no arithmetic exponent or fixed-power`
- TeX line 118: `credit is paid, and full Gate B remains open.`
- TeX line 125: `output.  The adversary is explicitly information-model only, not a physical`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:radius` → `main.tex#L57` (existing project target or original TeX label line).
