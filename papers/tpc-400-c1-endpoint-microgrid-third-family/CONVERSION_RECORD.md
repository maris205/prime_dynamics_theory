# TPC-400 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `686121fd91b93caf12ea57e697db0531b572db1a720f28e2afd60d7056861874`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `753ba6785b974a859070f825526fff12970213c3e61ca0810a6dd7b5fae33338`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `bc7d68381cdd7a825cceff2e9fc527a14ce4977ae728bc44b2f26c509f319a95`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and claim boundary` | 35 | 1 | `HEADING_TEXT_MATCH` |
| `Finite construction` | 54 | 1 | `HEADING_TEXT_MATCH` |
| `Diagnostics and frozen parent interface` | 92 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 133 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and route ledger` | 172 | 3 | `HEADING_TEXT_MATCH` |
| `Reproduction` | 208 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `42` before writing and `42` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `13`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `3e034bc378209e9c2020f6c2ba88d528383b4ece32bd2b790cb16fde3e44e3cb`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 45–49 | `b1ecb493a23905cd4330ee82c941a731d747254a15a561fc47d6d449060a62e0` |
| D02 | align* | 58–62 | `e45a400781bc5be90d8bc6bb698ce42c5d39943f089bd457ef70e2d2bb288927` |
| D03 | \[...\] | 64–66 | `e252ee1596026a2cfdefe22fc296eca3a4900a96a775db916a0b4297fd01efe5` |
| D04 | \[...\] | 68–71 | `07d60c08f904d773e0707b95f6004fe3d2a0c69185da9817b16039612e111345` |
| D05 | \[...\] | 73–76 | `3ac83ccbb2461a3f082cd7a13f82fe4e33626e0420c79b67bc42e4dde3a4be5f` |
| D06 | \[...\] | 81–83 | `6fdd2b8cc4ff71368cc9f90913ca7255407a4307d62432dcc998332340fab80e` |
| D07 | \[...\] | 85–87 | `b1d28e80afd75541220406fd6c6917e1fc64dc937a7ec90fe903df6d87d0c116` |
| D08 | \[...\] | 97–100 | `f451cf20bee824d7f42b795bce028f597304ca93d7c989312de775c58b5b3ca8` |
| D09 | \[...\] | 107–112 | `cec21f2e96bb547b45eb1d686be9371dc798162e797bd4811b448b405240f3a9` |
| D10 | \[...\] | 114–117 | `7fce15348ec0df3cc27c5dc47954f88e1dfb7c6be3033ccc6dd2625348baf643` |
| D11 | \[...\] | 156–159 | `7c6a675f5fc021951116ec7f52bc893a311510d20daca725c2fb7066b6e93538` |
| D12 | \[...\] | 161–164 | `e4e44b048fd139bd953dc66f0ffaf6f86c9ec01e35abdb59263289f72cf36e91` |
| D13 | \[...\] | 186–188 | `8c68356f1868e066b2e2eb0c338b48364db6ff60823b0743ba31f371169f820a` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 10: `\title{TPC-400: Third-Family Replication of a Finite C1 Endpoint Microgrid}`
- TeX line 20: `TPC-399 found a finite separation between same-law mean transfer and origin`
- TeX line 21: `uniformity: the probes through $\lambda=31/32$ were origin-stable, while the`
- TeX line 30: `cross-family boundary but remains below it.  This is finite replication and`
- TeX line 31: `obstruction evidence, not an arithmetic, asymptotic, Route-A/Route-B, or`
- TeX line 42: `Every object below is finite.  In particular, a fractional coefficient in a`
- TeX line 48: `\texttt{FULL\_GATE\_B=OPEN}.`
- TeX line 51: `local proof, independent checker, and Bridge-B artifacts provide finite`
- TeX line 54: `\section{Finite construction}`
- TeX line 72: `The four probes are the exact finite combinations`
- TeX line 77: `This is a finite linear-algebra identity, not an arithmetic interpolation`
- TeX line 101: `The origin cap is $R_\lambda\leq0.01$.  Finite spectral and Schur caps are`
- TeX line 137: `\caption{TPC-400 finite panel.  Counts are across the four laws.}`
- TeX line 179: `cross-family cap, so the finite panel does not justify a stronger uniformity`
- TeX line 182: `The reusable structure is a direct hash-locked same-law interface, exact finite`
- TeX line 194: `status & finite scope\\`
- TeX line 196: `PROVED\_EXACT\_FINITE & selection, disjointness, hashes, anchor identities\\`
- TeX line 198: `OPEN & source-valid uniformity, growing bounds, arithmetic $L^2$\\`
- TeX line 204: `Route-B remains open.  The certificate makes no claim about a source-uniform`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
