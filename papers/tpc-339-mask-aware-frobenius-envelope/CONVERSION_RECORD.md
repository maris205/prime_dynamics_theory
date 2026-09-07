# TPC-339 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `024fd8d535671c377bc5714346cb3c1b3136c9d5`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `a55203013d3db0fa1c4dcd19c48cb0a7bf1c7ca3e2d05ecd064f6f392951c51c`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `24d1d2f648031c26e367d009e03fb1bbaaeafce9183941130adda9391f9c2696`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `50d02f86a6ec4353755b9cdccc498fbd938d1aa83ac42e877c790a86feb1ff8c`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC335_339.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Motivation and finite object` | 30 | 1 | `HEADING_TEXT_MATCH` |
| `Support-restricted bound` | 48 | 1 | `HEADING_TEXT_MATCH` |
| `Audit protocol` | 69 | 2 | `HEADING_TEXT_MATCH` |
| `Finite results` | 84 | 2 | `HEADING_TEXT_MATCH` |
| `Claim firewall and next step` | 114 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `25` before writing and `25` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `6`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `00c31f94a51083cbb45f6b1df72947edab8a634babbf10bb30d8cb2ebb974a96`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 34–37 | `3ea7bfc980e239a3a92ea7bd13b8d660840ff26a93f8477e5c4f6c768109da93` |
| D02 | equation | 52–56 | `e4113e0fdf2e235e2a9e736b2926cce72c72f0c9b1bb1a47a1084d1a23704703` |
| D03 | \[...\] | 58–60 | `e11a72df7b1c10f570f9aff740dd37135ccace7460ed36beac10bef96d5a5d4e` |
| D04 | \[...\] | 62–64 | `92bf6b555cb3f3e275c8e454e656b06e9d7daf9ca01e4df5f389a0ad1ffd865b` |
| D05 | \[...\] | 78–80 | `9e8bdfda537ee89b8b24843cdd743bf6054a652e7a71a0b576ea00296b96ab92` |
| D06 | \[...\] | 122–126 | `b1ecb493a23905cd4330ee82c941a731d747254a15a561fc47d6d449060a62e0` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 11: `\large A Sign-Free Response Bound for the Finite Twin-Prime Model}`
- TeX line 23: `submatrix.  The bound is an exact finite inequality and passes all 216 declared`
- TeX line 30: `\section{Motivation and finite object}`
- TeX line 45: `not a safe interface.  This paper asks how far an elementary sign-free bound`
- TeX line 66: `source entries.  A small $\eta$ measures slack in the bound, not a payment of`
- TeX line 84: `\section{Finite results}`
- TeX line 117: `\texttt{PROVED\_EXACT\_FINITE\_DECLARED\_MODEL}; the 216-record replay and`
- TeX line 118: `zero-violation census are \texttt{NUMERICALLY\_CERTIFIED\_FINITE}.  The`
- TeX line 119: `occupancy ranges are \texttt{NUMERICAL\_OBSERVATION}.  Uniform tightness of`
- TeX line 120: `this elementary envelope is \texttt{REFUTED\_SCOPED} at the finite factor-five`
- TeX line 121: `diagnostic.  There is no arithmetic advance or fixed-power credit:`
- TeX line 125: `\texttt{FULL\_GATE\_B=OPEN}.`
- TeX line 128: `fail-closed and is not an official route pass.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#eq:bound` → `main.tex#L52` (existing project target or original TeX label line).
