# TPC-392 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `aaaa03076242b229cb65b6702ebd04aad42d0aa3ab60975c26845e1716a594b5`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `23598498d34b6c6de3209b49cf03880c7a78eeb58a999a49c79a0122d83d5889`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `21b2a5d2edcf405d4f9740b2100d97896ea5583786366cfb90b692341b284384`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and claim boundary` | 33 | 1 | `HEADING_TEXT_MATCH` |
| `Finite proxy and normalization panel` | 62 | 1 | `HEADING_TEXT_MATCH` |
| `Certification protocol` | 97 | 2 | `HEADING_TEXT_MATCH` |
| `Finite results` | 118 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and next clue` | 159 | 3 | `HEADING_TEXT_MATCH` |
| `Reproduction` | 178 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `38` before writing and `38` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `8`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `0616c6057971733f88ec56c1f51b01891957afb34ddb415a3206c79f07ac7fce`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 43–45 | `8b425e96fe14871a85912820dfe1f789f9a8e1384fcace3430741cdf1d4b3f20` |
| D02 | \[...\] | 54–58 | `b1ecb493a23905cd4330ee82c941a731d747254a15a561fc47d6d449060a62e0` |
| D03 | align* | 65–69 | `1523c178a1e7cea0660f3469721d0ba97a206c9acc487e57603ea1c06cdbd611` |
| D04 | \[...\] | 71–74 | `5cdd5822d4f143f9718cd594d05d77fcf553e5d1be58889f4f7c52a0d55735e9` |
| D05 | \[...\] | 91–94 | `935112e9e7a7d2f83efd9fadf76dadb783176819c1577d77b276e636957dfadf` |
| D06 | \[...\] | 109–116 | `d6d053a10a20bf6fa8d400f105446b1db6f37800f8cd3cda4fc58087810f74a1` |
| D07 | \[...\] | 144–147 | `2de3cfdc01c85fcb7dc6ab2a82dba2842c7ceba70fc0b88662b9e98da56126e7` |
| D08 | \[...\] | 171–173 | `375df120e1e47110c2d016e2144ae09994241c5a04a27d15cece8a5581904653` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 8: `\title{TPC-392: A Finite Normalization Phase Diagram for a $c=1$ Proxy}`
- TeX line 18: `TPC-391 localized a finite forecast obstruction for a frozen interface.  The`
- TeX line 19: `next question is whether the finite phase depends on the normalization used`
- TeX line 27: `with error $0.0341068507$.  The scalar choices change the finite level by`
- TeX line 29: `scoped numerical phase diagram for a $c=1$ proxy, not an asymptotic,`
- TeX line 57: `\texttt{FULL\_GATE\_B=OPEN}.`
- TeX line 62: `\section{Finite proxy and normalization panel}`
- TeX line 64: `For $p\in(Q,2Q]$, $H=66$, and $u,v$ in a finite interval, define`
- TeX line 89: `origins available at count $N$.  The finite calibration slope and terminal`
- TeX line 101: `independent implementation evaluates the same finite source in descending`
- TeX line 108: `The finite status labels are deliberately narrow:`
- TeX line 111: `\text{panel and definitions:}&\text{PROVED\_EXACT\_FINITE},\\`
- TeX line 112: `\text{phase and forecast counts:}&\text{NUMERICALLY\_CERTIFIED\_FINITE\_SCOPED},\\`
- TeX line 113: `\text{source-valid normalization and growing bounds:}&\text{OPEN},\\`
- TeX line 118: `\section{Finite results}`
- TeX line 150: `the finite level while preserving a largely common trajectory on this panel;`
- TeX line 156: `These counts are diagnostics of the declared finite envelope, not analytic`
- TeX line 163: `one predeclared high-$Q$ alternating cell.  This supports a finite`
- TeX line 164: `normalization-phase distinction, but it does not establish that any scalar`
- TeX line 166: `origin uniformity, count uniformity, a growing operator bound, and the`
- TeX line 167: `arithmetic $L^2$ reassembly gate remain open.`
- TeX line 176: `adversarial holdout.  No arithmetic power credit is assigned.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#tab:phase` → `main.tex#L126` (existing project target or original TeX label line).
