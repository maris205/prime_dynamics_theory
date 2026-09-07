# TPC-340 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `e848dbf1895cb067bad6665654a7c992406bcf65`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `2bafdc43b3952a6d7acce434d841cfb79b8a65170fec8835dd6f1ee97cff72fa`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `4892de320fa8ddac28cdec98d66c4228e05a2227a552f6faa51e21130c9654ee`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `e8f762957f1abad3695e158ed5d1d1b376558e6c705829543d17c61f68ed61f4`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC340_344.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and finite object` | 35 | 1 | `HEADING_TEXT_MATCH` |
| `Two sign-free bounds` | 60 | 1 | `HEADING_TEXT_MATCH` |
| `Audit protocol` | 104 | 2 | `HEADING_TEXT_MATCH` |
| `Finite results` | 115 | 2 | `HEADING_TEXT_MATCH` |
| `Route evaluation and scope` | 150 | 2 | `HEADING_TEXT_MATCH` |
| `Next question` | 170 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `23` before writing and `23` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `12`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `571b687f18f7b8f4648cbaa3bc9cab61278169364a330519dcca4338fbb41de0`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 24–26 | `5ffa47512573efd54b098231e553776c67bbcb9c26ea5f3f2899e2518e79f5b9` |
| D02 | \[...\] | 43–45 | `983fdf909d51e92164d08a6a592c471abfe7c7ca884de11d875bcc44e9f386c9` |
| D03 | \[...\] | 48–50 | `ac062c18460f9bdc0f2392551384f0f5dfdbdb6d9f4d2821bb6973689c66ef63` |
| D04 | \[...\] | 52–55 | `7431d73b530850917ed9d0a982722b386651cbedbed324b2405bab840fd266df` |
| D05 | equation | 64–68 | `44813c461d2468e85d249be233aaf9d2c8cf6c3b31eb8d3ac3df76e13449dadd` |
| D06 | \[...\] | 70–73 | `10ae17190ed42153fb51b1611deb675689f7ececc83db7213c4f74c3967df01f` |
| D07 | \[...\] | 76–78 | `91d7c471d693e980e08c942b8dc965952239671438534b35af5bc792ca44623a` |
| D08 | equation | 81–85 | `77315dd8ca1b2cbb636419e5bb517042388bdd1dda78b70972d6f36f931c15fb` |
| D09 | equation | 88–91 | `0d2814a7bba74326afe8dd6fc711c506dff744082458a779987e3c6d03d1b0d2` |
| D10 | \[...\] | 97–99 | `6a28f2d24d07743e6738257a0a86c5de30ff18b7b7e322a55c5a66e885636d64` |
| D11 | \[...\] | 134–137 | `a7fad55d4dce331d947279eb60b12b8a32616bdcc6bd17f23217af91bd5172b2` |
| D12 | \[...\] | 161–165 | `b1ecb493a23905cd4330ee82c941a731d747254a15a561fc47d6d449060a62e0` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 11: `\large A Sign-Free Finite Bound for Masked Twin-Prime Responses}`
- TeX line 22: `for the same finite symmetric all-plus shell operator.  If $x$ is supported on`
- TeX line 27: `The inequality is proved exactly for every finite symmetric matrix and passes`
- TeX line 31: `hybrid is a useful finite envelope and a sharper obstruction, not a growing`
- TeX line 35: `\section{Question and finite object}`
- TeX line 40: `finite envelope without importing a covariance sign.`
- TeX line 75: `For a finite symmetric matrix put`
- TeX line 115: `\section{Finite results}`
- TeX line 142: `but it does not recover alignment information for broad masks.`
- TeX line 144: `The strongest positive result is a clean finite, sign-free envelope with a`
- TeX line 147: `gap on broad masks.  The occupancy values are finite observations, not a`
- TeX line 148: `uniform-in-$x$ or growing-in-$N$ theorem.`
- TeX line 153: `\texttt{PROVED\_EXACT\_FINITE\_DECLARED\_MODEL}.  The replay and zero-violation`
- TeX line 154: `census are \texttt{NUMERICALLY\_CERTIFIED\_FINITE}; the occupancy and branch`
- TeX line 155: `ranges are finite numerical observations.  Broad-mask factor-five tightness`
- TeX line 158: `does not assert an official route pass.`
- TeX line 164: `\texttt{FULL\_GATE\_B=OPEN}.`
- TeX line 168: `norm; the unresolved gate is a uniform arithmetic operator estimate.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#eq:frob` → `main.tex#L67` (existing project target or original TeX label line).
- Link relocation: `#eq:schur` → `main.tex#L84` (existing project target or original TeX label line).
