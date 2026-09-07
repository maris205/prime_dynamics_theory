# TPC-387 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `92bb127a4ff130eff5cdadf90a1fffe5d6ad665c53083f8378f0cf6439080fb4`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `30a5916346b120a0f79c9c549d16d749419930f4832a8cd2e75e78df5bce0637`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `8257d83cb0236e9bf7e24be89aed85661b83f17ae0589510ac5e2394aa17627e`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and claim boundary` | 30 | 1 | `HEADING_TEXT_MATCH` |
| `Proxy and protocol` | 49 | 1 | `HEADING_TEXT_MATCH` |
| `Exact and computational certification` | 82 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 91 | 2 | `HEADING_TEXT_MATCH` |
| `Conclusion and next clue` | 128 | 2 | `HEADING_TEXT_MATCH` |
| `Reproduction` | 141 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `51` before writing and `51` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `5`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `df64bcbc6be2354b5827ec809fc9add2db4ab078054a1fc6660f88d698ef9362`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 40–44 | `b1ecb493a23905cd4330ee82c941a731d747254a15a561fc47d6d449060a62e0` |
| D02 | align* | 52–56 | `53f8042701001239a26c5943d04cbe21892fe5640fbb65ec0f9b96b101be0d31` |
| D03 | \[...\] | 58–60 | `251511bb23d9b66defbfc68016bc8cc8476073a99c2cf49a7f079a55d63c2f8a` |
| D04 | \[...\] | 74–77 | `754cc673ba17022273d082b6c188c6861d3c652b0dd2421c45800145453d0302` |
| D05 | \[...\] | 136–138 | `d4006db1085ed3e600e59f75286edfba5d748816e74ad73c354b6f22333d7160` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 18: `TPC-386 showed that a finite $0.64$ spectral diagnostic does not survive a`
- TeX line 25: `within a predeclared 3\% finite error envelope; the worst error is 2.6051\%.`
- TeX line 26: `This is a reproducible finite repair of the endpoint comparison, not a`
- TeX line 27: `count-uniform operator theorem and not an arithmetic result.`
- TeX line 32: `We remain in one finite $c=1$ dynamical-system family.  The preceding count`
- TeX line 43: `\texttt{FULL\_GATE\_B=OPEN}.`
- TeX line 51: `For $p\in(Q,2Q]$ define the same finite kernel as in TPC-386,`
- TeX line 79: `has been fixed.  The 3\% threshold is a finite audit convention, not an`
- TeX line 121: `The finite repair should be interpreted alongside the cap obstruction.  A`
- TeX line 125: `controls: their scales and endpoint spreads differ, so no law-uniform claim`
- TeX line 131: `calibration-only endpoint extrapolation that passes its 3\% finite census.`
- TeX line 133: `uniform in count, origin, law, or source normalization.  The reusable object`
- TeX line 139: `No arithmetic reassembly or twin-prime conclusion follows.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `papers/tpc-387-c1-count-ladder-renormalization/` → `..` (existing project target or original TeX label line).
