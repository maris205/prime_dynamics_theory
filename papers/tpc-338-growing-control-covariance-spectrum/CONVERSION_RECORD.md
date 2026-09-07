# TPC-338 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `024fd8d535671c377bc5714346cb3c1b3136c9d5`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `3cee5ca8cdb64c93c59da9e8735dba02669714e8041ddf3b551ed5be1d1f5eb4`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `99dd435f668b7f00edc4bc0cf01317b78e0086f6b814dbe6a96d9e0f749a1110`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `1e19fed4216dce748d38dd2294f828194e8ebb782cabb3c695d39a70a15ff23a`.
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
| `Question and nested ensembles` | 31 | 1 | `HEADING_TEXT_MATCH` |
| `Finite identity and spectrum` | 58 | 1 | `HEADING_TEXT_MATCH` |
| `Audit and exact anchor` | 84 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 94 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and firewall` | 125 | 2 | `HEADING_TEXT_MATCH` |
| `Next question` | 145 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `28` before writing and `28` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `7`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `5c6b7f231c261d8ac3e92f22e8babd087d03af8ff349977c593fb3d8b44748a6`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 34–37 | `c92fbb3523d1b4e59b60eef59db450ea1c100886301b2f4eb2f88de288060554` |
| D02 | \[...\] | 43–45 | `435482212c7c84c1a9f5f419b12829a4821e4d25ee448778d35c6abc8c6d8448` |
| D03 | \[...\] | 52–56 | `fe4418c93ca6abfe81d85e34473b73733cd454a02d701943f6f0d3652251fa08` |
| D04 | equation | 61–65 | `a118e7dd8256c9fcce9889bfb31ebfc28f7eadf738d735efda9fd75036c5bfb1` |
| D05 | \[...\] | 67–70 | `eb57cc3b7545bc1c94bb498aecad109cd077df67955b6fb832aedfb4bb1b1fcc` |
| D06 | \[...\] | 72–75 | `eda88a86195a27ef1cc3781ee396258462e8e1df47675f056f64974a7948b031` |
| D07 | \[...\] | 138–142 | `b1ecb493a23905cd4330ee82c941a731d747254a15a561fc47d6d449060a62e0` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 27: `for the nine-control ensemble in all six rows.  Thus the finite energy`
- TeX line 58: `\section{Finite identity and spectrum}`
- TeX line 76: `This proves positive semidefiniteness but says nothing about the sign of an`
- TeX line 78: `there is no nested sign monotonicity to assume.`
- TeX line 81: `the overall response scale for a descriptive finite spectral comparison; it`
- TeX line 82: `does not create a limiting object.`
- TeX line 119: `The sign reversal is not a numerical borderline phenomenon.  The smallest`
- TeX line 122: `It nevertheless remains a finite statement about two explicitly chosen`
- TeX line 133: `The identities are \texttt{PROVED\_EXACT\_FINITE\_DECLARED\_MODEL}; the`
- TeX line 134: `nested replay, energy census, and finite spectral distances are`
- TeX line 135: `\texttt{NUMERICALLY\_CERTIFIED\_FINITE}.  The sign reversal is`
- TeX line 136: `\texttt{REFUTED\_SCOPED} for ensemble invariance.  There is no arithmetic`
- TeX line 141: `\texttt{FULL\_GATE\_B=OPEN}.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
