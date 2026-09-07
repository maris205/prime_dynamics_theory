# TPC-398 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `1f4be3198072fbfa24af5d82a80a004081764b7cec42ad7d6988f9a5374e5f4f`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `378324dd37cbe0e702d0887a026f23adc17e552f532b9680a365235826acbc93`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `1b9bafb71bb8d99bc314e50705c79a489b56ef99ebe8ee4627480fee56f81fbd`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 34 | 1 | `HEADING_TEXT_MATCH` |
| `Finite construction` | 53 | 1 | `HEADING_TEXT_MATCH` |
| `Diagnostics and frozen parent interface` | 86 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 117 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and route ledger` | 162 | 2 | `HEADING_TEXT_MATCH` |
| `Reproduction` | 193 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `41` before writing and `41` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `10`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `ed49fd38c546f4e8f0ec32ec8357c7b200d032ae41b4074d6e2d93f441dccd98`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 45–49 | `b1ecb493a23905cd4330ee82c941a731d747254a15a561fc47d6d449060a62e0` |
| D02 | align* | 57–61 | `e45a400781bc5be90d8bc6bb698ce42c5d39943f089bd457ef70e2d2bb288927` |
| D03 | \[...\] | 64–67 | `d324089f65fe5b1959f88bf9575e446dfcf57bdcecaa794d248e283e6295e421` |
| D04 | \[...\] | 69–72 | `feefe37e2efecac3b57620c416c70a3fca127c091bb71f8ca4b5f8dcb2b1c9c4` |
| D05 | \[...\] | 77–79 | `fdd1a51db8998069e644c9415be75fbd77c75b0b72cfab0f52bd7c3c145feddc` |
| D06 | \[...\] | 91–94 | `82d4f641f53c127bee5e0f72b8e965bb5996291b74c13403f5d054da942ec6c0` |
| D07 | \[...\] | 101–104 | `36dc33c8ad7ea98b60155f07e8562de865c0d11bb99a717fffb117c7178efd50` |
| D08 | \[...\] | 141–146 | `4fdc631e6f7fd71ba9b542431278e1f77b4bd3a3853481c76843373ca89d1857` |
| D09 | \[...\] | 177–179 | `8e9cf65920e22d5756a65d3e9bce80cc99d387df276be595515fe2861089401c` |
| D10 | \[...\] | 182–189 | `957d8f6f83eff92e2c21c89858e8a62bfaa10a229e236a6eab6909bbb5600bd5` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 9: `\title{TPC-398: Endpoint Microgrid on a Fresh Finite \(c=1\) Family}`
- TeX line 19: `TPC-397 left a finite transition panel unresolved between the interpolation`
- TeX line 29: `within-family transfer passes, and no finite spectral or Schur row fails.`
- TeX line 30: `These are certified finite proxy observations, not an arithmetic, asymptotic,`
- TeX line 36: `The preceding TPC-397 audit replicated a finite endpoint transition: several`
- TeX line 42: `All objects in this paper are finite proxy objects.  A fractional coefficient`
- TeX line 48: `\texttt{FULL\_GATE\_B=OPEN}.`
- TeX line 51: `local proof and Bridge-B artifacts provide finite consistency evidence only.`
- TeX line 53: `\section{Finite construction}`
- TeX line 68: `TPC-398 forms the exact finite probes`
- TeX line 73: `The identity is a linear-algebra construction.  It does not identify a source`
- TeX line 96: `diagnostic, with finite caps 0.64 and 0.83 for spectral and Schur values.`
- TeX line 106: `by one; the cap is 0.03.  This is a frozen modeling baseline, not a theorem`
- TeX line 121: `\caption{TPC-398 finite panel.  Counts use the four laws; parent and transfer`
- TeX line 160: `finite check does not turn the float64 panel into an asymptotic statement.`
- TeX line 164: `The strongest positive result is a finer finite localization of the origin`
- TeX line 173: `finite matrix interpolation, a predeclared calibration/holdout family,`
- TeX line 184: `\mathrm{PROVED\_EXACT\_FINITE:}&\text{selection, disjointness, hashes, anchor identity;}\\`
- TeX line 185: `\mathrm{NUMERICALLY\_CERTIFIED:}&\text{96 finite rows and stated aggregate flags;}\\`
- TeX line 186: `\mathrm{OPEN:}&\text{source-valid uniformity, growing bounds, arithmetic }L^2;\\`
- TeX line 191: `Route-B remains open.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
