# TPC-399 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `2d41bd1b7f0a365f0ee4a922d41ad05a30df9fd5ff6bd4f022edded0abc4b3e9`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `8638ec70073247a8236aa6852d86faaadb28ee13132b144c917b076ec429795d`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `200c67d7f551fc67cfa00a50921f23d164ffc1a8435657e48cfd0fc48af03822`.
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
| `Finite construction` | 55 | 1 | `HEADING_TEXT_MATCH` |
| `Diagnostics and frozen parent interface` | 95 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 140 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and route ledger` | 177 | 3 | `HEADING_TEXT_MATCH` |
| `Reproduction` | 212 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `44` before writing and `44` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `13`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `e8be7dd33564f1e534286d86365b1436d4166ebabf1c8769310c01f4070b9b9d`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 46–50 | `b1ecb493a23905cd4330ee82c941a731d747254a15a561fc47d6d449060a62e0` |
| D02 | align* | 59–63 | `e45a400781bc5be90d8bc6bb698ce42c5d39943f089bd457ef70e2d2bb288927` |
| D03 | \[...\] | 65–67 | `e252ee1596026a2cfdefe22fc296eca3a4900a96a775db916a0b4297fd01efe5` |
| D04 | \[...\] | 69–72 | `07d60c08f904d773e0707b95f6004fe3d2a0c69185da9817b16039612e111345` |
| D05 | \[...\] | 74–77 | `e91630b6dccdc5ef51a45cb0f740e44b6c973c142d97647c7aabb2023b9d46b3` |
| D06 | \[...\] | 83–85 | `31aa5250477029a2d8c2203c5f2f458bc3fec9077c19ec41dd417c3154ea8cc1` |
| D07 | \[...\] | 87–89 | `62843677340a68ecb00d986b165ce64f54205e399078c2ef82d2abe97b94632e` |
| D08 | \[...\] | 101–104 | `f451cf20bee824d7f42b795bce028f597304ca93d7c989312de775c58b5b3ca8` |
| D09 | \[...\] | 112–117 | `4936934c12dd16946aac049d33c46cf1d4f35220e568e45efc07c5e2dd09c136` |
| D10 | \[...\] | 120–123 | `7fce15348ec0df3cc27c5dc47954f88e1dfb7c6be3033ccc6dd2625348baf643` |
| D11 | \[...\] | 163–166 | `aef0f19608331f9ead36c3f1d2b4b6aeb96cf2ab6e517c0cac2a3bf2fcc201c0` |
| D12 | \[...\] | 168–171 | `54becb487ece91e51d291421a5948570e7a7854c9f787eb64513f6720584d0fb` |
| D13 | \[...\] | 190–192 | `dcde3357e463b06c7397522ba9e9b01f0d3b289d9736166520bbd005d54529ee` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 10: `\title{TPC-399: Cross-Family Replication of a Finite C1 Endpoint Microgrid}`
- TeX line 20: `TPC-398 reported a finite endpoint microgrid on one affine family: the`
- TeX line 29: `maximum spreads between $0.0622195$ and $0.0625497$.  The result is a finite`
- TeX line 30: `cross-family replication together with a finite obstruction to inferring origin`
- TeX line 31: `uniformity from mean transfer.  It is not an arithmetic, asymptotic,`
- TeX line 37: `The preceding TPC-398 audit used a response-blind grid of four finite matrix`
- TeX line 43: `All objects below are finite proxy objects.  In particular, a fractional`
- TeX line 49: `\texttt{FULL\_GATE\_B=OPEN}.`
- TeX line 52: `local proof, independent checker, and Bridge-B artifacts provide finite`
- TeX line 55: `\section{Finite construction}`
- TeX line 73: `The four probes are the exact finite combinations`
- TeX line 79: `arithmetic at a small anchor; it is not a claim about an underlying`
- TeX line 105: `The origin cap is $R_\lambda\leq0.01$.  Finite spectral and Schur caps are`
- TeX line 144: `\caption{TPC-399 finite panel.  Counts are across the four laws.}`
- TeX line 182: `is that this transfer does not remove endpoint origin instability: at`
- TeX line 184: `transfer and origin uniformity are empirically separate finite diagnostics.`
- TeX line 186: `The reusable structure is a direct hash-locked same-law interface, exact finite`
- TeX line 198: `status & finite scope\\`
- TeX line 200: `PROVED\_EXACT\_FINITE & selection, disjointness, hashes, anchor identities\\`
- TeX line 202: `OPEN & source-valid uniformity, growing bounds, arithmetic $L^2$\\`
- TeX line 208: `Route-B remains open.  The certificate makes no claim about a source-uniform`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
