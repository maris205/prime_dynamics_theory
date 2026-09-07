# TPC-407 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `844ebc959958ca5fe75f793261371ce0a40b0a8a4b59d325a574bc5347623860`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `1554bf2874ce4a3ee37172cc12443deb5da32f693ad5ea7bf2c281491f7db4a2`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `61af3eb2b9d6f3dedc95de04aa4f941a20f4166e1cd0e9e3093e0ad0665d3fe0`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Complete-shell Q ladder` | 25 | 1 | `HEADING_TEXT_MATCH` |
| `Finite Q-scale theorem` | 54 | 2 | `HEADING_TEXT_MATCH` |
| `Exact certificate and observations` | 76 | 2 | `HEADING_TEXT_MATCH` |
| `Route boundary` | 102 | 2 | `HEADING_TEXT_MATCH` |
| `Reproduction` | 126 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `48` before writing and `48` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `6`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `e4124e0a16b6c29f5a8eac29ac670da2d239e314977f3db5419ede1a78bbc76c`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 29–32 | `7b69b0c6cc9de80b71e9b564cd0bd86003e6a20f6a25bd9814233f7de5d06387` |
| D02 | \[...\] | 37–41 | `e37520e2e9c8b8ab2f593857f1eca73bb047f1fbd1a9ea90ea74c2953d41922b` |
| D03 | \[...\] | 43–47 | `3a8939124fd97207782940f272d3f82b326d9f82f9905f3b314982f97bdd379e` |
| D04 | \[...\] | 49–51 | `117e3d90a4573521a043f829c143ed1810f871ef776a54ca2c6adb7a960bbf16` |
| D05 | \[...\] | 57–60 | `cb5598082793d77cda21ed1874300e6065f5e21c16be6d5c378d7b6ea112c33f` |
| D06 | \[...\] | 67–71 | `4cd110e7a80c987499a7bdfe9be93b1c173fd67685b527ee578863ca01c2ebbc` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 20: `near $0.0052$ and $H z$ remains near $0.344$, but these are finite`
- TeX line 21: `float64 observations, not an asymptotic assertion.  The result concerns one`
- TeX line 22: `synthetic proxy entry and makes no arithmetic or twin-prime claim.`
- TeX line 26: `Fix $H=66$ and $N=264$.  Let $Q>N$ and assume that the complete shell`
- TeX line 52: `This is a finite proxy model; $H$ is not the physical $h_0$.`
- TeX line 54: `\section{Finite Q-scale theorem}`
- TeX line 98: `The table is a finite numerical observation extracted from exact rational`
- TeX line 99: `squares.  It is not a fit, a growing bound, or evidence for arithmetic`
- TeX line 103: `TPC-407 establishes a finite complete-shell Q-scale ladder for one adjacent`
- TeX line 104: `entry.  It does not bound all entries or the complete normalized matrix,`
- TeX line 105: `does not allow arbitrary origins or odd shell profiles, and does not identify`
- TeX line 106: `the physical $h_0$ or an arithmetic sign law.  Consequently it pays no`
- TeX line 113: `complete-shell Q-scale ladder & \texttt{PROVED\_EXACT\_FINITE}\\`
- TeX line 114: `four exact rational Q rows & \texttt{PROVED\_EXACT\_FINITE}\\`
- TeX line 116: `full normalized operator theorem & \texttt{OPEN}\\`
- TeX line 118: `Route-A / Route-B / twin-prime result & \texttt{OPEN} / \texttt{OPEN} / \texttt{NONE}\\`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
