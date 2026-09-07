# TPC-368 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `77397e82c262fddf2a2926a9542308b8edf65149291c65b73ca63ed257bd71ad`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `ab8c7a4767b3cdfde44a70a7862432aff71d8478eeba841943db0db302e9e56f`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `762c72d8671d100a7bdef058a9b8444703db10552c73de83f17532682e3ee627`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 36 | 1 | `HEADING_TEXT_MATCH` |
| `Finite operator and frozen protocol` | 50 | 1 | `HEADING_TEXT_MATCH` |
| `Complete finite audit` | 92 | 2 | `HEADING_TEXT_MATCH` |
| `Exact and independent verification` | 148 | 2 | `HEADING_TEXT_MATCH` |
| `Claim firewall and route decision` | 169 | 2 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 197 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `34` before writing and `34` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `5`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `8a85ab955a02e5541492a094abb7ffd771a7941fb2a784efef7f321198c4f154`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 54–59 | `c1f0bbb0c9cea23f88b23971864c031c25d6c1cfdfc63a885eb90e6f1f621ba0` |
| D02 | equation | 61–67 | `c908900b200033e492fd5f7287d257063d684a40ea598d62d3a5e302336db652` |
| D03 | equation | 69–74 | `b813279c718a97fd560d492d88e7d2f408c7c0ea15cb1b38c881edab88a72bf0` |
| D04 | equation | 77–82 | `bb57f66b7af183da8f7aa62bc477af1d0a56527fb55de8c048ea26e1597c11f5` |
| D05 | equation* | 133–136 | `a6c85ade055e1edb2942a3b2668381afba691be60695e339c2735ec1e05b915e` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 10: `Finite Prime-Shell Obstruction}`
- TeX line 22: `TPC-367 found a finite long-window failure of a fixed beta=2 prime-shell`
- TeX line 31: `spectral and 18 Schur failures.  This is a finite replication and obstruction`
- TeX line 32: `audit, not an asymptotic theorem, an arithmetic estimate, or a twin-prime`
- TeX line 38: `The beta=2 point was selected as a useful finite shell tilt in the preceding`
- TeX line 48: `below are restricted to the explicitly declared finite panel.`
- TeX line 50: `\section{Finite operator and frozen protocol}`
- TeX line 68: `Whenever $G_\beta(u)>0$, the normalized finite matrix is`
- TeX line 75: `The geometry is a finite sum of rational squares.  For a finite real`
- TeX line 92: `\section{Complete finite audit}`
- TeX line 137: `for each $a\in\{810001,817061,824121\}$.  Thus the finite failure key,`
- TeX line 145: `$5.474780509384658\times10^{-6}$.  This is a finite descriptive comparison;`
- TeX line 150: `The exact anchor is the half-open interval $[810342,810355)$ at $Q=4$,`
- TeX line 172: `TPC368_ORIGIN_FAMILY_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND`
- TeX line 173: `TPC368_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE`
- TeX line 174: `TPC368_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_144_ROWS`
- TeX line 175: `TPC368_SECOND_ORIGIN_FAMILY = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 176: `TPC368_BETA2_LONG_WINDOW_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 177: `TPC368_BETA2_FAILURE_PATTERN = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 178: `TPC368_ORIGIN_UNIFORMITY = OPEN`
- TeX line 179: `TPC368_WINDOW_UNIFORMITY = OPEN`
- TeX line 180: `TPC368_BETA2_ASYMPTOTIC_REPAIR = OPEN`
- TeX line 181: `TPC368_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN`
- TeX line 182: `TPC368_GROWING_OPERATOR_BOUND = OPEN`
- TeX line 183: `TPC368_SOURCE_UNIFORM_L2 = OPEN`
- TeX line 186: `TPC368_FULL_GATE_B = OPEN`
- TeX line 191: `six-key finite pattern on a second origin family.  The strongest obstruction`
- TeX line 194: `but it does not establish origin uniformity, window uniformity, an asymptotic`
- TeX line 200: `second predeclared origin family.  The next minimal finite questions are a`
- TeX line 203: `the finite obstruction.  In either case, no arithmetic credit is paid and`
- TeX line 209: `\texttt{TPC368\_FULL\_GATE\_B=OPEN}.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#tab:beta` → `main.tex#L101` (existing project target or original TeX label line).
