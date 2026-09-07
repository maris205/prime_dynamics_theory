# TPC-379 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `93aec9c2c3b9986b2517aa53fe8e5bc72668b0c90acd203e24e6beec5b5745bd`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `8acb1351a169ff77f9a8ce10e7647398da04144a5fb121e54f6ed012d96be4c4`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `fe68755713c03fb1edc76f51da03b4d8cb3ea2bb4099e245476855722a0c0b6e`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and claim boundary` | 31 | 1 | `HEADING_TEXT_MATCH` |
| `Finite operator and four laws` | 46 | 1 | `HEADING_TEXT_MATCH` |
| `Predeclared protocol` | 85 | 1 | `HEADING_TEXT_MATCH` |
| `Results` | 105 | 2 | `HEADING_TEXT_MATCH` |
| `Audits and interpretation` | 135 | 2 | `HEADING_TEXT_MATCH` |
| `Route status and conclusion` | 152 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `61` before writing and `61` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `9`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `7ef0cfdca1dbb4c5eb21d1a51a6dcbb9f0e7c41850d3d44e0a909b2367a73c23`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 34–36 | `ca8b56506b75c095da5428941ee678cd2f7cc8938205256bab97734b0b476340` |
| D02 | \[...\] | 49–54 | `27d702ae4fdaa81db880c09013c17f07e31ce8ef4059b87dccebdc80a5151dc3` |
| D03 | \[...\] | 56–59 | `4943e1fe0324c6ca95d8dd0a9facfbde771a845a993574a4b6081d18a053cfaa` |
| D04 | \[...\] | 60–62 | `7d1f7944bfa16a6f1697f6b300b2ddd6602c867567ea2e7f6aa7ec6489821088` |
| D05 | \[...\] | 65–73 | `12d919aabed537fa88a1ff849d2d01529710ff0c7affc0fcbee514da2170e3f2` |
| D06 | \[...\] | 75–78 | `bf82736d14b3ea4d61f9314f3e30779431ea1a96f06ba73b09463f6a2243eb01` |
| D07 | \[...\] | 80–82 | `e8214712a30d05d534eb4d3382771ad684d74510636dbfcc48303eb036b639ec` |
| D08 | \[...\] | 88–90 | `845510ceee11909f6e57ab20d289eda30bdcd1654768b624569cc8f2faf8dce9` |
| D09 | \[...\] | 164–168 | `2e2ce54e2be19528b3ddddbd2a747d97dd11a9a0c6ec7ea3b8411a54418aae17` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 12: `{\Large\bf A Finite Law-Control Obstruction for the $c=1$ Prime-Shell Band}\\[5pt]`
- TeX line 20: `TPC-378 transferred a finite $c=1$ band-support profile to three fresh`
- TeX line 27: `no Schur-cap failures. This is a finite sign-law-dependence obstruction,`
- TeX line 28: `not an arithmetic or twin-prime theorem.`
- TeX line 33: `The preceding finite experiments used the all-plus shell sum`
- TeX line 41: `All conclusions concern one explicit finite panel. A signed control is a`
- TeX line 42: `diagnostic sign sequence, not a character sum known to represent the`
- TeX line 43: `twin-prime source. The terms \texttt{OPEN}, \texttt{MODELING\_CHOICE\_OPEN},`
- TeX line 46: `\section{Finite operator and four laws}`
- TeX line 83: `is an exact finite identity.`
- TeX line 112: `\caption{Finite law-control panel.}`
- TeX line 146: `The strongest positive result is a complete finite, response-blind,`
- TeX line 150: `property of the finite mask; this is not a theorem choosing a law.`
- TeX line 157: `finite protocol, coordinate separation, common geometry, sign definitions,`
- TeX line 158: `and band/tail identity are proved finite statements. The replay and census`
- TeX line 159: `are numerically certified finite statements.`
- TeX line 161: `Source-validity of the normalization, law/origin/scale uniformity,`
- TeX line 162: `cross-block causality, a growing operator bound, source-uniform $L^2$, and`
- TeX line 163: `signed prime-shell reassembly remain open. The certificate records`
- TeX line 167: `\texttt{FULL\_GATE\_B=OPEN},`
- TeX line 169: `with no twin-prime conclusion. The next minimal finite test is`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#tab:law` → `main.tex#L113` (existing project target or original TeX label line).
