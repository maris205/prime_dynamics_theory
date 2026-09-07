# TPC-365 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `0930e954fd125264c343caf2a4a3d23dbda5af1a1550988b3d521bb06694f0c7`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `27c0792c7e065b65ea2c094e1c1e8aa265d8cc92e0deb49c0c086b5c98ce03d9`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `050822272817518a01c658d8d530ac67a5ecd261887907c344fb40b82705f02f`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 38 | 1 | `HEADING_TEXT_MATCH` |
| `Finite operator and selection rule` | 60 | 1 | `HEADING_TEXT_MATCH` |
| `Finite audit` | 111 | 2 | `HEADING_TEXT_MATCH` |
| `Exact and independent verification` | 167 | 2 | `HEADING_TEXT_MATCH` |
| `Claim firewall and route decision` | 185 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 212 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `40` before writing and `40` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `7`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `d7df2e11a86f43a1d6c606051de0854c48d219bce0ee1b95d2e120a36fe52180`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 44–46 | `cf7ad3806417cca18965c21b72373f276d4a07b2cdaa89514ff64b62934108dd` |
| D02 | equation | 64–69 | `decc48a06baa9404e48c796cdfa15ae1a2763ef4cd299ee702cc274f40f803ee` |
| D03 | equation | 71–77 | `7646f8cb208c13181d2f329924af6a236372a29aaf572ed2cd0298043378e350` |
| D04 | equation | 79–84 | `ac81fc3c6066b90080752abefc5fb811aa0c93263ae4cb8230bfec0674b6c81d` |
| D05 | equation | 87–92 | `bb57f66b7af183da8f7aa62bc477af1d0a56527fb55de8c048ea26e1597c11f5` |
| D06 | equation | 98–101 | `5d41b58ec10d7981265cccc7934ebf8213b7030df9f529b15c6402c82f6ec24f` |
| D07 | equation | 105–107 | `f1dcba478153e8227372578a0e4447ff55f091b830e6452ccdb18d45ff6cb513` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 9: `\title{A Response-Blind Fresh Holdout for a Finite Prime-Shell Tilt}`
- TeX line 21: `TPC-364 identified beta=2 as the only zero-failure member of a finite`
- TeX line 29: `finite spectral cap $0.64$ is exceeded in 30 of 192 beta=0 rows and in zero`
- TeX line 32: `$4.4345466941875245\times10^{-5}$.  This is finite, geometry-selected`
- TeX line 33: `transfer evidence.  It is not an asymptotic operator estimate, a`
- TeX line 47: `and found a finite beta=2 phase point on a reused panel.  The present paper`
- TeX line 53: `by an unsigned geometry functional.  Thus this is response-blind finite`
- TeX line 54: `transfer evidence, not a probabilistic independent-sample or uniform-in-`
- TeX line 60: `\section{Finite operator and selection rule}`
- TeX line 85: `The geometry is a sum of rational squares in the exact finite model.  Once`
- TeX line 86: `it is positive, the two elementary finite envelopes are`
- TeX line 111: `\section{Finite audit}`
- TeX line 117: `for every law.  The value $0.64$ is an inherited finite working threshold,`
- TeX line 118: `not a claim uniform in $Q$.`
- TeX line 122: `\caption{Beta comparison on the fresh finite panel (192 rows per beta).}`
- TeX line 157: `below the finite working Schur threshold $0.83$.  Its minimum effective shell`
- TeX line 158: `fraction is $0.66938300094026681$, a diagnostic showing that the finite`
- TeX line 165: `in the row census, but it does not identify the source-valid normalization.`
- TeX line 169: `At $Q=4$, exponent one, the half-open exact interval`
- TeX line 188: `TPC365_GEOMETRY_SELECTION = PROVED_EXACT_FINITE_RESPONSE_BLIND`
- TeX line 189: `TPC365_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE`
- TeX line 190: `TPC365_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_384_ROWS`
- TeX line 191: `TPC365_BETA2_HOLDOUT = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 192: `TPC365_BETA2_CAP_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 193: `TPC365_BETA2_ASYMPTOTIC_REPAIR = OPEN`
- TeX line 194: `TPC365_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN`
- TeX line 195: `TPC365_GROWING_OPERATOR_BOUND = OPEN`
- TeX line 196: `TPC365_SOURCE_UNIFORM_L2 = OPEN`
- TeX line 199: `TPC365_FULL_GATE_B = OPEN`
- TeX line 203: `The strongest positive result is a fixed-rule, response-blind finite transfer`
- TeX line 215: `predeclared beta=2 rule survives a fresh response-blind finite panel, while`
- TeX line 217: `maps a more promising branch of the finite route, but it does not bridge the`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#tab:q` → `main.tex#L141` (existing project target or original TeX label line).
