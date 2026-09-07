# TPC-369 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `9ef67952e78f286d375990863c722c2705ca3474f4c05404d019c370ad30775c`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `a91b334ca999cbef29f6c82a2b3c533ece9e926ab28fb9d442c7ff784220b0bd`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `66d61f37ef8fc474114d56315065f0c41acb3db27f502a8a849263c839f10ce0`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and claim boundary` | 38 | 1 | `HEADING_TEXT_MATCH` |
| `Finite operator and frozen protocol` | 52 | 1 | `HEADING_TEXT_MATCH` |
| `Exact-anchor obstruction and repair` | 99 | 2 | `HEADING_TEXT_MATCH` |
| `Complete finite audit` | 117 | 2 | `HEADING_TEXT_MATCH` |
| `Independent and hostile verification` | 155 | 2 | `HEADING_TEXT_MATCH` |
| `Claim firewall and route decision` | 172 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 204 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `36` before writing and `36` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `6`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `1bbf0b63908db7a2f882f1f3ad6c3a850dc02a2b40d57cd2146b4d1a2a140241`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 57–62 | `c1f0bbb0c9cea23f88b23971864c031c25d6c1cfdfc63a885eb90e6f1f621ba0` |
| D02 | equation | 64–71 | `326b50f08060dfba4bedd267e67fc6e5acf576e6e9808f33896f7e293c0b4abd` |
| D03 | equation | 73–78 | `b813279c718a97fd560d492d88e7d2f408c7c0ea15cb1b38c881edab88a72bf0` |
| D04 | equation | 81–86 | `bb57f66b7af183da8f7aa62bc477af1d0a56527fb55de8c048ea26e1597c11f5` |
| D05 | equation* | 90–92 | `b6e4d0e018bcc5f9966d613025ef08fa8ca8ab438ebcb815c2e930fe3bc311ce` |
| D06 | equation* | 139–142 | `e5a8a30134301ce1993f8c216554f9406d5e106719a9506ce7d95e6ce97666b6` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 10: `Finite Prime-Shell Obstruction}`
- TeX line 22: `We test a third response-blind origin family against the finite beta=2`
- TeX line 33: `replay.  The result is a finite third-family replication and obstruction`
- TeX line 34: `audit, not an asymptotic theorem, an arithmetic estimate, or a twin-prime`
- TeX line 43: `does the same finite pattern survive a third family with a different start and`
- TeX line 50: `restricted to the declared finite panel.`
- TeX line 52: `\section{Finite operator and frozen protocol}`
- TeX line 72: `When $G_\beta(u)>0$, the normalized finite matrix is`
- TeX line 79: `The geometry is a finite sum of rational squares.  For a finite real`
- TeX line 101: `The first proposed proof anchor was the half-open interval`
- TeX line 104: `initial finite positivity assertion before any main-panel spectrum or signed`
- TeX line 114: `geometry digests.  This repair certifies a small finite witness only; it does`
- TeX line 117: `\section{Complete finite audit}`
- TeX line 143: `for every $a\in\{1010001,1018021,1026041\}$.  Hence the full finite failure`
- TeX line 151: `of $2.9920783610748458\times10^{-6}$.  This close agreement is a finite`
- TeX line 152: `descriptive fact.  It proves neither origin uniformity nor convergence to a`
- TeX line 175: `TPC369_ORIGIN_FAMILY_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND`
- TeX line 176: `TPC369_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE`
- TeX line 177: `TPC369_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_144_ROWS`
- TeX line 178: `TPC369_THIRD_ORIGIN_FAMILY = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 179: `TPC369_BETA2_PHASE_AUDIT = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 180: `TPC369_BETA2_FAILURE_PATTERN = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 182: `TPC369_REPAIRED_ANCHOR_RULE = PROVED_EXACT_FINITE`
- TeX line 183: `TPC369_ORIGIN_UNIFORMITY = OPEN`
- TeX line 184: `TPC369_WINDOW_UNIFORMITY = OPEN`
- TeX line 185: `TPC369_BETA2_ASYMPTOTIC_REPAIR = OPEN`
- TeX line 186: `TPC369_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN`
- TeX line 187: `TPC369_GROWING_OPERATOR_BOUND = OPEN`
- TeX line 188: `TPC369_SOURCE_UNIFORM_L2 = OPEN`
- TeX line 191: `TPC369_FULL_GATE_B = OPEN`
- TeX line 195: `The strongest positive result is exact finite replication of the six-key`
- TeX line 199: `declared finite repair.  None of these results proves a growing operator`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#tab:beta` → `main.tex#L126` (existing project target or original TeX label line).
