# TPC-275 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `225edf5e32a3a90ca64da6f3a05ec312dff962cb`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `f7b3b9a17dfc26f16f6b6e58a13e7794f387e5e056fde633e4d7dcc212d094d7`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `7c1b24501fefaa9c958f2ea734121f7811f788f86c4276935b75e815a22d248b`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `b8af85c5d9b89c9df8445c7761cf71b3ffcd57353c104b88aea110a318ababae`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC275_279.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and claim ceiling` | 42 | 1 | `HEADING_TEXT_MATCH` |
| `Frozen literal object and packet split` | 63 | 1 | `HEADING_TEXT_MATCH` |
| `Exact signed reassembly identities` | 93 | 2 | `HEADING_TEXT_MATCH` |
| `Literal finite certificate` | 142 | 2 | `HEADING_TEXT_MATCH` |
| `Route evaluation and limits` | 209 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 231 | 4 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 242 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `56` before writing and `56` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `14`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `8ec77f179cd787aed0beb7d48a7554e382b7bd1bcc6544703e657e0169d8af1d`.
- Source theorem/proof environment starts: theorem at TeX line 95, proof at TeX line 104, theorem at TeX line 111, proof at TeX line 130, theorem at TeX line 181, proof at TeX line 191.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 47–49 | `4d7340e281ebb251846b569dc4c6a12049cd7c3e46cfd881f8c368cf44d8a4aa` |
| D02 | \[...\] | 55–58 | `aa5e4b137d363963c079f74ac61b394f032da3825983bcdcd6667e732a43a320` |
| D03 | \[...\] | 67–72 | `ee601a9d5a2af32dfb310b67c5a6f83df54fcbe474aff96cd9d4c795eacfb694` |
| D04 | \[...\] | 75–78 | `97ebc4edb4e6c087177f6eeddae45d177470d651f0a66772a3e440318668d05d` |
| D05 | \[...\] | 85–90 | `b61f9e15c136d75dfcb89e9795b866a083f4811c102e75e6ea7328e02bd4f0ba` |
| D06 | \[...\] | 97–101 | `90b68f028fc4f519056f91869e176099bf3cee00ac0f04561fc24486c5cd5f9d` |
| D07 | \[...\] | 113–115 | `6274adca2c46eedf5d9d1a2f195e15fe9062fb7d4515020fe499a9c9545be9f9` |
| D08 | \[...\] | 117–120 | `4be7f594e0d163a9d4660bb768308daecaeee886581df370f8e7fdce92a59158` |
| D09 | \[...\] | 122–124 | `e48d4adde2b2de41e3a156f3279122c8c23a368982a3702ef49b2f9ee3b9c0d9` |
| D10 | \[...\] | 125–127 | `e4e6955d8d39d65a3f9e96bad9ee3675b65bbae7d0718cff5ed08fe283b40c1e` |
| D11 | \[...\] | 152–154 | `f013c92346e0e3ad1fcac0f7b4d340ba1f01fa27b4aaf07bac9a6020e07d2543` |
| D12 | \[...\] | 156–158 | `e6795075a8980004165bfefaec0bbc39c69ba8701a5b3e66114d69cf5d20cfde` |
| D13 | \[...\] | 183–186 | `a8f4db7fa12a0d89b4636ab9ce5d49a71301da2ff181554727fcdc04b6d5e59a` |
| D14 | \[...\] | 216–222 | `08e6799d0a19edec970c0ba4970e76f1a21a48ddfcbb647b3753d870feb368d3` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 38: `source-attached finite signed-reassembly result, not an asymptotic`
- TeX line 56: `\texttt{PROVED\_EXACT\_FINITE}\quad+\quad`
- TeX line 57: `\texttt{NUMERICALLY\_CERTIFIED\_FINITE}.`
- TeX line 59: `The finite packet-diagonal route is marked`
- TeX line 60: `\texttt{INSUFFICIENT\_SCOPED}; no finite observation is promoted to a growing`
- TeX line 96: `For real finite packets,`
- TeX line 142: `\section{Literal finite certificate}`
- TeX line 202: `signs.  Thus signed reassembly materially sharpens the finite envelope from a`
- TeX line 203: `factor above 50 to a factor below \(12/5\).  It does not make the diagonal`
- TeX line 211: `TPC-260 supplied a generic DFT and a synthetic null-compatible completion`
- TeX line 214: `The result is consequently a finite source attachment, but not a source-level`
- TeX line 218: `\texttt{SOURCE\_LEVEL\_SIGNED\_CROSS\_GRAM}=\texttt{OPEN\_ASYMPTOTIC}\\`
- TeX line 223: `No finite ratio is an exponent in \(N\), and the one positive phase row is`
- TeX line 224: `retained.  The strict \(1/400\) endpoint payment and full Gate B remain open.`
- TeX line 228: `margin loss explicitly.  That is a new theorem target, not a consequence of`
- TeX line 229: `the present finite table.`
- TeX line 238: `the quarter-margin condition on these rows.  TPC-275 therefore opens the`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
