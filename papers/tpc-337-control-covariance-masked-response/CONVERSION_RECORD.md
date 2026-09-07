# TPC-337 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `024fd8d535671c377bc5714346cb3c1b3136c9d5`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `4e8355e16c0bcf30f655707c26cf42a3d310b8b1e9f4dff22c98909519192d73`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `c68f9ea1bf8aaf371bb87376837084ed0e4e2564f4bfb446b606ecbb57cab698`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `199f98b20772a5c0bb2766db4afb5e4d28888a78cdeed0cb4b379505f891e956`.
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
| `Question and finite model` | 34 | 1 | `HEADING_TEXT_MATCH` |
| `Exact covariance structure` | 65 | 1 | `HEADING_TEXT_MATCH` |
| `Certificate and checks` | 96 | 2 | `HEADING_TEXT_MATCH` |
| `Finite readout` | 114 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and firewall` | 146 | 3 | `HEADING_TEXT_MATCH` |
| `Next question` | 169 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `32` before writing and `32` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `13`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `4fe784720c5c831d9547852cde5318b8a17ce9d0ab4c9a32725fb92941f7197b`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 37–40 | `f9ad2a590bcd693e00adc58d3f09ecaee9a10f34c790d2c42c1ece72e6cec930` |
| D02 | \[...\] | 44–47 | `5f3303a0b950dec2df0540edc550c7698d3e415469409a8eb4df7853c72244ef` |
| D03 | \[...\] | 50–52 | `5a654eac8714e69899c48e95ed295d9428f60a0329ee1c542d7550315a9e0b21` |
| D04 | \[...\] | 55–58 | `c117e103aacdc65455d32e0c412b029838de2e62ffe17ccf51bca9070fbba9f3` |
| D05 | \[...\] | 60–63 | `2afb25471e4a923aea30cae0a5ba1c75b918fcbb17e8911b40fdafaa61427fed` |
| D06 | equation | 68–71 | `65c9df78715d398bfcf756ad4a0a4559e787b1c860b8dc3a1cfc9bb7a0aa239e` |
| D07 | \[...\] | 73–75 | `fdc887f34afb9d954bd637dfc268f648e37f5e02abbc1e962115d98f70a0c677` |
| D08 | equation | 77–80 | `86050be1a5a4d68aba11868472e9a582f68637be088ec32b368fe69554e95383` |
| D09 | \[...\] | 82–84 | `294eff16f56fc07c7182dff7a2bf4198c0f086c140f4c946c2f264878ce882e0` |
| D10 | equation | 86–90 | `40bd12ef8d177493e196aace171a3eb16fc3ce90df53c689f120dda692c37094` |
| D11 | \[...\] | 107–109 | `c5954bab356c02a953503d306e98df4efde0f46ea40d542f38ed2b9e514b09f5` |
| D12 | \[...\] | 135–138 | `9beb1e1d286bd01b6fb112161aadcac0a9ab4d81b94505f81d48ac84ba66c8f5` |
| D13 | \[...\] | 161–165 | `b1ecb493a23905cd4330ee82c941a731d747254a15a561fc47d6d449060a62e0` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 12: `\large A Finite Stability Test for Twin and Background Components}`
- TeX line 30: `identities and positive semidefiniteness are finite algebraic facts; the`
- TeX line 31: `numerical census is a scoped obstruction, not a growing arithmetic theorem.`
- TeX line 34: `\section{Question and finite model}`
- TeX line 67: `Because $\sum_jz_{C,j}=0$, finite expansion gives`
- TeX line 81: `The matrix $K$ is positive semidefinite, since for any $a\in\mathbb R^4$,`
- TeX line 92: `These identities isolate a useful warning: a small coherent mean does not`
- TeX line 114: `\section{Finite readout}`
- TeX line 118: `\caption{Control-orbit energy fractions over the six finite windows.}`
- TeX line 140: `smaller windows or change sign in the finite panel.  The smallest recorded`
- TeX line 148: `The strongest positive result is a reusable finite structure: source masks,`
- TeX line 151: `control averaging does not make the full response coherent.  It moves the`
- TeX line 156: `\texttt{PROVED\_EXACT\_FINITE\_DECLARED\_MODEL}; the six-row replay,`
- TeX line 158: `\texttt{NUMERICALLY\_CERTIFIED\_FINITE}.  The transfer of these signs or`
- TeX line 159: `fractions to growing intervals is \texttt{OPEN}.  There is no arithmetic`
- TeX line 164: `\texttt{FULL\_GATE\_B=OPEN}.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#eq:class` → `main.tex#L68` (existing project target or original TeX label line).
- Link relocation: `#eq:pair` → `main.tex#L77` (existing project target or original TeX label line).
