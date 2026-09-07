# TPC-389 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `06fa793730e8cb345de96745ac8f0f51bfd726f1db13eae61cde4410164ddaeb`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `c3cac6b1c120279ec26715e88dd95b5864ddd0d8eae87d8f205ebf8b006b8abe`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `e175d79905fac6943b4013fb90aaf03b37892c7a0dcc84abdfb2cefe0932ea29`.
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
| `Finite proxy` | 53 | 1 | `HEADING_TEXT_MATCH` |
| `Forecast interface` | 70 | 1 | `HEADING_TEXT_MATCH` |
| `Certification and results` | 95 | 2 | `HEADING_TEXT_MATCH` |
| `Conclusion and next clue` | 133 | 2 | `HEADING_TEXT_MATCH` |
| `Reproduction` | 153 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `34` before writing and `34` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `8`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `b6285b79abc18eef4d3f6d0fc56612488a81a28a8d8643337c05aec325bd26e9`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 37–39 | `f717a2a4234607c66ea598e8b52e94d7e0d848647e61be9e5edb84d182d6f4ca` |
| D02 | \[...\] | 45–49 | `b1ecb493a23905cd4330ee82c941a731d747254a15a561fc47d6d449060a62e0` |
| D03 | align* | 56–60 | `206b9cccaefd36a7a782dc1ebfa2a22365dc68ec72d09278779a3e1f2ee8ea9f` |
| D04 | \[...\] | 76–79 | `bf257e186eda2acd0c79b06ab9c5e6cf4de29563a075f46749f9a5084b369398` |
| D05 | \[...\] | 81–86 | `40385dee186251e2363915f9abc9e20df0fd69f4f10d436bb681767d4b7eb271` |
| D06 | \[...\] | 87–90 | `22710f059191f902c504a290ac7c06b0dc04a819cbd76ca5443933dc514713e7` |
| D07 | \[...\] | 138–142 | `9c43d6a48965e549403db2b63205e3e3d2c734c839d90a5cc93eec04ff8efda3` |
| D08 | \[...\] | 147–149 | `a5c20dde4e1cba62e0062e9887cd0c15bde986109564445e4e063340cabd67d9` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 18: `TPC-388 reported a finite cross-family transfer of a logarithmic count slope.`
- TeX line 24: `predeclared 3\% finite ratio cap.  The largest errors are`
- TeX line 26: `finite stress certificate: the inherited spectral diagnostic still fails on`
- TeX line 27: `64 of 256 rows, and no arithmetic or asymptotic conclusion follows.`
- TeX line 32: `TPC-388 showed that 32 slopes learned on an earlier finite count ladder`
- TeX line 48: `\texttt{FULL\_GATE\_B=OPEN}.`
- TeX line 53: `\section{Finite proxy}`
- TeX line 61: `The row geometry is the finite square energy`
- TeX line 91: `The holdout ratio is $S_{1280}/\widehat S_{1280}-1$; the finite pass cap is`
- TeX line 93: `finite panel.`
- TeX line 107: `\caption{Finite forecast and stability census.}`
- TeX line 128: `the finite cap.  This proximity is a stress observation, not a margin for an`
- TeX line 130: `remain below their cap, so the finite forecast success does not repair the`
- TeX line 135: `TPC-389 supplies one independent finite progress point: a frozen slope remains`
- TeX line 144: `with the recursive error being near the declared boundary.  The open theorem`
- TeX line 145: `is a source-valid, origin/count-uniform growing operator and slope control.`
- TeX line 151: `open.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `papers/tpc-389-c1-long-horizon-slope-stress/` → `..` (existing project target or original TeX label line).
