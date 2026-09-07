# TPC-406 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `d56b866522f2d622a8aa9c96c6365ffcd3ece3504aa58fe04260f0f18c12c371`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `f5373712b537d23c3d4818301ba3f7534802a38b2a1ab2f2aee5dfcc613653e5`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `baca66fe95068be95b009b82562e6d3c308d3d07b248d36fdad2be29382e5393`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Scope and complete-shell model` | 26 | 1 | `HEADING_TEXT_MATCH` |
| `Complete-shell adjacent-entry theorem` | 57 | 2 | `HEADING_TEXT_MATCH` |
| `Exact complete-shell certificate` | 80 | 2 | `HEADING_TEXT_MATCH` |
| `Route boundary` | 107 | 2 | `HEADING_TEXT_MATCH` |
| `Reproduction` | 132 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `49` before writing and `49` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `6`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `fa2a562886214a4f5d9540a07d8f3ae25b3f10db9ae289fadf1cca68a2eb4d9e`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 30–33 | `659923636a395cce166a212a4251823a4025fe9c3b863da65c04f7e261696c01` |
| D02 | \[...\] | 39–43 | `e37520e2e9c8b8ab2f593857f1eca73bb047f1fbd1a9ea90ea74c2953d41922b` |
| D03 | \[...\] | 45–49 | `3a8939124fd97207782940f272d3f82b326d9f82f9905f3b314982f97bdd379e` |
| D04 | \[...\] | 51–53 | `117e3d90a4573521a043f829c143ed1810f871ef776a54ca2c6adb7a960bbf16` |
| D05 | \[...\] | 60–63 | `cb5598082793d77cda21ed1874300e6065f5e21c16be6d5c378d7b6ea112c33f` |
| D06 | \[...\] | 70–74 | `4cd110e7a80c987499a7bdfe9be93b1c173fd67685b527ee578863ca01c2ebbc` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 13: `small selected prefixes of the prime shell.  We close that finite selection`
- TeX line 21: `are finite observations, not an asymptotic theorem.  The result remains a`
- TeX line 22: `bound for one synthetic proxy entry, not a complete operator, arithmetic, or`
- TeX line 27: `Let $H,N,Q$ be integers with $H\geq1$, $N\geq H+2$, and $Q>N$.  Assume the`
- TeX line 36: `$p_i>Q>N$, the residues determine the hits in the half-open window`
- TeX line 54: `The word ''complete'' refers to the finite declared shell, not to the full`
- TeX line 76: `places these terms in both finite sums, so $S_0,S_1\geq H/4$.`
- TeX line 108: `TPC-406 advances the finite local proxy question from a selected prefix to`
- TeX line 110: `explicit alternating CRT profile.  It does not bound all entries, the`
- TeX line 112: `source primes, the physical $h_0$, or the arithmetic sign law.  Accordingly`
- TeX line 113: `it pays no arithmetic $L^2$ estimate, no fixed-power $1/400$ credit, and no`
- TeX line 119: `complete-shell local-entry boundary & \texttt{PROVED\_EXACT\_FINITE}\\`
- TeX line 120: `five-row rational certificate & \texttt{PROVED\_EXACT\_FINITE}\\`
- TeX line 122: `full normalized operator theorem & \texttt{OPEN}\\`
- TeX line 124: `Route-A / Route-B / twin-prime result & \texttt{OPEN} / \texttt{OPEN} / \texttt{NONE}\\`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
