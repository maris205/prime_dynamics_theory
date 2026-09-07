# TPC-366 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `e061dd122c2990d8864fc0fbb0a70831a5a04679a7cc2b13e984a3fc874789e1`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `10f3e6ece6d28bcfb4e1e1e7596fab17df032ad2fe0ddeeb04038188568f5627`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `42cbf0b163d6fb895043afe94d052cc8d2230489c2fabbd2df70aa36d35c609e`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 37 | 1 | `HEADING_TEXT_MATCH` |
| `Finite operator and frozen selection` | 55 | 1 | `HEADING_TEXT_MATCH` |
| `Higher-\texorpdfstring{$Q$}{Q} audit` | 101 | 2 | `HEADING_TEXT_MATCH` |
| `Exact and independent verification` | 153 | 2 | `HEADING_TEXT_MATCH` |
| `Claim firewall and route decision` | 170 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 197 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `43` before writing and `43` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `6`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `9ee41d70ee425e42ebe0deb2231efaf78500f4cb8faa5f61997504ce218f0006`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 41–43 | `5de884eda888f239b9d81cf9099e832779df4b759e4308567568b0fff1d45618` |
| D02 | equation | 58–63 | `6b0e9473983563404c16a548e53e57c77c15ce73f878f8b178750e51ea961afd` |
| D03 | equation | 65–71 | `d65a354a44e8aaccd96d81e038bfd80708d29d3c4c48e1a71a8859d22ff98442` |
| D04 | equation | 73–78 | `0ca9324786e0e8d6541e20adb128b9b67fe85e6dbb3cffd4f7c12e7570067e26` |
| D05 | equation | 81–85 | `2d3818e79a61fefc3a7564cd40dba816b28de86d22459e9e63471c9c51c06996` |
| D06 | equation | 90–94 | `679c8b9221b4f1e082817b2b140740522b64dd093fd075d57cb93e18088bb912` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 22: `finite holdout through $Q=512$.  We now freeze beta=2 and attack scale on a`
- TeX line 32: `This is a finite higher-$Q$ observation, not a shell-uniform operator theorem,`
- TeX line 39: `TPC-362 located a finite cap failure beginning at $Q=128$ for the inherited`
- TeX line 44: `and TPC-365 showed that the fixed choice beta=2 transferred to a new finite`
- TeX line 46: `frozen, how far does the finite cap observation extend in $Q$?`
- TeX line 49: `route and locating scale obstructions, but it is not a random independent`
- TeX line 50: `sample or a uniform-in-origin claim.  No source vector, adaptive sign, or`
- TeX line 55: `\section{Finite operator and frozen selection}`
- TeX line 72: `The normalized matrix is the finite symmetric congruence`
- TeX line 80: `operator bounds used are the elementary finite envelopes`
- TeX line 107: `law.  The spectral value $0.64$ and Schur value $0.83$ are inherited finite`
- TeX line 145: `beta=2 maximum remains below both finite caps, but it is not monotone: it`
- TeX line 150: `$0.66944805377549699$, so the finite observation is not described as a`
- TeX line 155: `At $Q=4$, exponent one, the half-open interval`
- TeX line 162: `masks, weights, four laws, geometry, finite envelopes, and all true spectra`
- TeX line 173: `TPC366_GEOMETRY_SELECTION = PROVED_EXACT_FINITE_RESPONSE_BLIND`
- TeX line 174: `TPC366_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE`
- TeX line 175: `TPC366_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_480_ROWS`
- TeX line 176: `TPC366_HIGHER_Q_LADDER = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 177: `TPC366_BETA2_HIGHER_Q_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 178: `TPC366_BETA2_SCALE_UNIFORMITY = OPEN`
- TeX line 179: `TPC366_BETA2_ASYMPTOTIC_REPAIR = OPEN`
- TeX line 180: `TPC366_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN`
- TeX line 181: `TPC366_GROWING_OPERATOR_BOUND = OPEN`
- TeX line 182: `TPC366_SOURCE_UNIFORM_L2 = OPEN`
- TeX line 185: `TPC366_FULL_GATE_B = OPEN`
- TeX line 190: `$Q=8192$ on the declared finite panel.  The strongest obstruction is the`
- TeX line 191: `nonmonotone finite scale profile together with geometry-based origin`
- TeX line 199: `TPC-366 extends the finite beta=2 signal by four additional shell scales,`
- TeX line 202: `the tested shell size, but the lack of a uniform statement across windows,`
- TeX line 203: `origins, and the arithmetic source.  The result remains a finite modeling`
- TeX line 204: `audit.  A growing operator bound, source-uniform $L^2$, source-valid`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
