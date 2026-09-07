# TPC-335 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `024fd8d535671c377bc5714346cb3c1b3136c9d5`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `f835c18b462df0ddc0fca2f1b51a60e5a1aee30396fa662524e8345b7845494d`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `bf0c5439ec7ae9cd409383847a325af8bfa9a7a6b737198cc00b666113e710f3`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `ac9f7eee20f21b0d64e522aad0e09576344b6d77c302e3b761811fc8342d05be`.
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
| `Motivation` | 35 | 1 | `HEADING_TEXT_MATCH` |
| `Finite source and masks` | 50 | 1 | `HEADING_TEXT_MATCH` |
| `Exact masked norm identity` | 76 | 2 | `HEADING_TEXT_MATCH` |
| `Certificate protocol` | 94 | 2 | `HEADING_TEXT_MATCH` |
| `Finite results` | 109 | 2 | `HEADING_TEXT_MATCH` |
| `Claim firewall` | 139 | 2 | `HEADING_TEXT_MATCH` |
| `Next question` | 151 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `35` before writing and `35` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `7`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `d873c97196fed2e0e46017b531c6e2a532b80260e3a8ff4b6cd66d8ac0e2a1b2`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 38–40 | `c12483e87b40287ce02cfdea8aeef4c3aa1f354f0593f5817d0314b46167c484` |
| D02 | \[...\] | 54–56 | `ef00deb1077ad608cf8719ca830a5278889cb260b18a0c1c71d2acd970398f30` |
| D03 | equation | 58–61 | `d5f4e8498affe2b03240ecaab5f148a2b26b9a113eb89272acdb3e786ac89fbf` |
| D04 | align* | 64–69 | `668cbd98d6f17234b6b5958f848483c4b6e63486a4368e6ae9ef2387a4596919` |
| D05 | \[...\] | 72–74 | `2de96985136629c63e38352ba16537a9ae562bd69976e25a1b60c17244ad3886` |
| D06 | equation | 79–82 | `c1c4b77193992fbbe7b28bbc198afebfbc4d0c8ad6187627cdbaca72773fbfd7` |
| D07 | \[...\] | 86–90 | `c8f4024e4a613c8a10138679c382dd83d11be8b7ecc49d8441df5ce0ded4ca2c` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 11: `\title{Twin-Isolated Source Norms in a Finite Prime-Shift Model}`
- TeX line 30: `This is a finite source-level separation and a precise input for the next`
- TeX line 31: `operator test; it is not a density estimate, power saving, or twin-prime`
- TeX line 47: `We answer this on the exact finite panel inherited from those papers.  The`
- TeX line 48: `word ''twin-isolated'' means a coordinate mask, not a new asymptotic source.`
- TeX line 50: `\section{Finite source and masks}`
- TeX line 62: `with the inherited finite Euler-tail cutoff $50000$ and midpoint guard.`
- TeX line 83: `This is simply a regrouping of a finite sum, but it is useful because it`
- TeX line 91: `where $X_{\mathsf T}$ is the twin cross-term mass.  This ratio is a finite`
- TeX line 92: `descriptive statistic, not a universal invariant.`
- TeX line 109: `\section{Finite results}`
- TeX line 141: `The finite mask identity \eqref{eq:normsplit} is`
- TeX line 142: `\texttt{PROVED\_EXACT\_FINITE} for the declared arrays.  The six-row norm`
- TeX line 144: `\texttt{NUMERICALLY\_CERTIFIED\_FINITE}.  The share and amplification ranges`
- TeX line 145: `are \texttt{NUMERICAL\_OBSERVATION}.  A source-uniform $L^2$ theorem, a`
- TeX line 147: `\texttt{OPEN}; \texttt{ARITHMETIC\_ADVANCE=NO} and`
- TeX line 149: `absent, so the local Bridge-B check is not an official route pass.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#tab:shares` → `main.tex#L115` (existing project target or original TeX label line).
- Link relocation: `#eq:normsplit` → `main.tex#L79` (existing project target or original TeX label line).
