# TPC-367 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `fd041e8b82be27c64664400d330690e7fba63296fa4f1081fa8ce335746d08b8`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `26fc4758fdd5baa6a42de3d9019678c5e8f4292869e1242a2da1316a6c637804`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `dc551ef42b3e4ee0cd84c2292993a9884f76236541fdcd5f6f4f735b73d520c1`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 35 | 1 | `HEADING_TEXT_MATCH` |
| `Finite operator and protocol` | 49 | 1 | `HEADING_TEXT_MATCH` |
| `Complete finite audit` | 90 | 2 | `HEADING_TEXT_MATCH` |
| `Exact and independent verification` | 140 | 2 | `HEADING_TEXT_MATCH` |
| `Claim firewall and route decision` | 156 | 2 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 183 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `36` before writing and `36` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `4`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `7c20583c3ab688759d0b16cf45e522431d882c317dec03090f8d14f9d13be61c`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 53–58 | `c760f54a6a8aadfcd106f72892a4361e709173726f747bd37176d9e60d43054b` |
| D02 | equation | 60–66 | `c40da51051994229ef422d8a30d022bb27e344e47886b36c3082f9416616c31e` |
| D03 | equation | 68–73 | `b813279c718a97fd560d492d88e7d2f408c7c0ea15cb1b38c881edab88a72bf0` |
| D04 | equation | 76–81 | `bb57f66b7af183da8f7aa62bc477af1d0a56527fb55de8c048ea26e1597c11f5` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 21: `TPC-366 carried a fixed beta=2 prime-shell tilt through a finite higher-$Q$`
- TeX line 30: `beta=0 control has 36 spectral and 36 Schur failures.  This is a finite`
- TeX line 31: `obstruction to one declared transfer statement, not an asymptotic theorem,`
- TeX line 37: `TPC-364/365 identified beta=2 as a useful finite shell tilt, and TPC-366`
- TeX line 39: `asks a deliberately adversarial finite question: does the same cap survive`
- TeX line 49: `\section{Finite operator and protocol}`
- TeX line 67: `When $G_\beta(u)>0$, the finite normalized matrix is`
- TeX line 74: `The geometry is a finite sum of rational squares.  For any finite real`
- TeX line 85: `is a declaration, not a random-sampling model: no geometry score or response`
- TeX line 87: `prime-modulo-four character, and half-shell split.  The finite working caps`
- TeX line 90: `\section{Complete finite audit}`
- TeX line 133: `the spectral cap in this finite panel, which is a sensitivity observation,`
- TeX line 134: `not a repair theorem.  At count 512, beta=2 remains below the spectral cap at`
- TeX line 142: `The exact anchor is the half-open interval $[620362,620375)$ at $Q=4$,`
- TeX line 159: `TPC367_ORIGIN_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND`
- TeX line 160: `TPC367_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE`
- TeX line 161: `TPC367_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_288_ROWS`
- TeX line 162: `TPC367_LONG_WINDOW_AUDIT = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 163: `TPC367_UNSELECTED_ORIGIN_AUDIT = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 165: `TPC367_BETA2_EXPONENT_SENSITIVITY = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 166: `TPC367_BETA2_ASYMPTOTIC_REPAIR = OPEN`
- TeX line 167: `TPC367_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN`
- TeX line 168: `TPC367_GROWING_OPERATOR_BOUND = OPEN`
- TeX line 169: `TPC367_SOURCE_UNIFORM_L2 = OPEN`
- TeX line 172: `TPC367_FULL_GATE_B = OPEN`
- TeX line 179: `predeclared origins.  The finite evidence does not close any official route`
- TeX line 185: `The finite beta=2 signal is window-sensitive in the declared model: it holds`
- TeX line 191: `the arithmetic bridge, growing bounds, and twin-prime endpoint remain open.`
- TeX line 196: `\texttt{TPC367\_FULL\_GATE\_B=OPEN}.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
