# TPC-356 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `9b2bd6205eb483cf1b971a8d61edeaeed9e63fc9c21ba4b4483fabf52c947a60`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `cfffe9399a51bb223b388ec6279de69ff5d3d8c540fb1446a2c40d55dd9eb278`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `bbbc18b2abc402f664d08fb6b90fda7e760d49179a512ea63cfa1be0ef39c5d0`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `39217528b5276251bbb41f5d076847285e1032bf693f71b8c8e780db5adb6ba8`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 40 | 1 | `HEADING_TEXT_MATCH` |
| `Finite model` | 58 | 1 | `HEADING_TEXT_MATCH` |
| `Geometry-only adversarial selection` | 99 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 128 | 2 | `HEADING_TEXT_MATCH` |
| `Exact and independent checks` | 168 | 3 | `HEADING_TEXT_MATCH` |
| `Claim firewall and conclusion` | 185 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 203 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `43` before writing and `43` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `9`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `deef32419e35095eda6cceb66334204ab90d78e983292a3ac86b3dc00e83b941`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 62–67 | `b72d52cf49da1c2d61a8b8846d3ffb014d04ce4db427dc16e16bad115f8e8280` |
| D02 | equation | 69–73 | `ee6511a9fc69426263547658b2c1b9d13a78f947d88780d05346d859aafa06f1` |
| D03 | equation | 75–79 | `a1149b784c202db760f0b3773e64e6ec01ffa39934069092d5f0d56a0610463d` |
| D04 | equation | 87–91 | `31eb87630f449532e798b3e1e1a2e7a73e55a559f2e000617b7f0c57015aa1fb` |
| D05 | equation | 93–97 | `0b377e02a320003895e981b3a9e9a95e0350db3477e6977dbeba76cad3bff01c` |
| D06 | \[...\] | 102–104 | `dd5035bd01b9976da01b240c5f2345d49dc9ef8e9dec2377a894abd84a71fbd3` |
| D07 | \[...\] | 107–110 | `6a34a368e5333c7ebe916409b2b0ef573e7c63defc21b3c557c2d6c957a8a28e` |
| D08 | \[...\] | 114–116 | `2d76806cbc845e60739e600cf9e9f2a45c3c1b45132b209a37bc0ab68c15c621` |
| D09 | \[...\] | 156–159 | `38988a8a78fd688ceeb8df9e209755c2002253cdcc4a45b32e497ab7de752bda` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 10: `Position Normalization: A Finite Holdout}`
- TeX line 26: `preceding finite masked-operator audit.  The new test chooses origins by a`
- TeX line 35: `0.8687258535297816 to 0.87560762679420479.  These are finite, scoped`
- TeX line 36: `observations: no growing-origin bound, arithmetic advance, source-uniform`
- TeX line 43: `the literal divisibility-masked shell operator.  Its finite panels suggested`
- TeX line 45: `exception and no uniform theorem.  The present paper asks a narrower`
- TeX line 47: `finite signal when the origin is selected using only a deliberately uneven`
- TeX line 58: `\section{Finite model}`
- TeX line 74: `TPC-355 uses the finite diagonal congruence`
- TeX line 82: `The source is the inherited finite V59 model`
- TeX line 84: `and zero otherwise, and with the declared finite comparison midpoint for`
- TeX line 85: `$b$.  For either $T=A_{\varepsilon}$ or $T=A_{\varepsilon}^{\#}$, the finite`
- TeX line 113: `retained origins.  This finite rule selects`
- TeX line 136: `\caption{Finite polarization summaries on the geometry-adversarial holdout.}`
- TeX line 162: `216 positive, zero negative, and zero unresolved rows.  This does not mean`
- TeX line 164: `declared finite holdout only.  In particular, the normalized all-plus`
- TeX line 166: `0.66473411648923819, so the experiment does not support a universal floor.`
- TeX line 187: `The finite selection rule and its response-blindness are exact properties of`
- TeX line 189: `numerically certified finite observations.  The experiment therefore gives a`
- TeX line 196: `source-uniform masked $L^2$ bound, arithmetic reassembly, full Gate B, and any`
- TeX line 197: `twin-prime conclusion open.  The next rational experiment is an origin-scale`

## Conversion limitations

- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.

- Link relocation: `#tab:summary` → `main.tex#L137` (existing project target or original TeX label line).
