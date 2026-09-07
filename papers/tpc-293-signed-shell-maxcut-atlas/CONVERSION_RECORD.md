# TPC-293 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `7bba57e68d04514ee33ab2192a507a1f4edfebab`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `10539ba8cf48370ffddaa5ec3398951b565351fa3b2c48dea337d0c072b02e0b`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `bd27e07a600bc9ff5941b97f6f11c60256d0ad3a5034d66cca9324b7dd4daf54`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `06e87632a59b667056b15a00786aa39d237aa2a2f846367a171d3dbae3c603ef`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `ae2cd773919ed5012db587b35b923c1204d2649d1004b7d61bfcfe9f6c1ecc23`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC290_294.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Position on the twin-prime route` | 43 | 1 | `HEADING_TEXT_MATCH` |
| `Physical Gram shell` | 61 | 1 | `HEADING_TEXT_MATCH` |
| `Signed-shell formulation` | 85 | 2 | `HEADING_TEXT_MATCH` |
| `Exact finite protocol` | 144 | 2 | `HEADING_TEXT_MATCH` |
| `Finite atlas` | 159 | 2, 3 | `UNMAPPED_OR_AMBIGUOUS` |
| `Interpretation and claim firewall` | 218 | 3 | `HEADING_TEXT_MATCH` |
| `Reproducibility and conclusion` | 236 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 255 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `56` before writing and `56` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `8`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `64ded54e6566d069027e4e5d5a3c7917ea2791afd7df336fae8a2a9f5e8e8183`.
- Source theorem/proof environment starts: theorem at TeX line 100, proof at TeX line 107, lemma at TeX line 117, proof at TeX line 124, remark at TeX line 133.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 66–70 | `a641d953a37284c10446dcf660c55e3b027e135132e489b2ff3d09a4ad996782` |
| D02 | \[...\] | 72–75 | `7bf26faa1f7a694abbe30d59293002d32056fca79e9fbac76dc1d60940e5d2ee` |
| D03 | \[...\] | 77–81 | `f253170838af3835222a73f946d4ad97e897691bfb38ecabcf4fd09b3d0a90bb` |
| D04 | \[...\] | 88–90 | `c0027215235bda8b9eb622ee15cb52ff620674e2d3a251d36067a55a0610dcdc` |
| D05 | \[...\] | 92–96 | `b72bbdfdbd015b9dd470d363f9173deff2c5eb024dc3548c2e22d3e06e8310bb` |
| D06 | \[...\] | 102–104 | `ac19e45c6a1c3aba1d0da19d98a0bde19ebccc212998c85bdb1a689d6c0e336d` |
| D07 | \[...\] | 110–112 | `57f37f87504a00910918768e6b29b94f1c2511d26816269670c6b292fa26f250` |
| D08 | \[...\] | 136–139 | `d4bea513126bd4979d1a45c311a26c9ed78f199d9a9095fbb365b405b52c6839` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 37: `exponent-crossover row has three negative edges and a finite sign-only gain of`
- TeX line 39: `selection device, not a magnitude-weighted energy estimate, an arithmetic`
- TeX line 82: `All finite calculations use exact rational arithmetic, so no floating-point`
- TeX line 118: `For any finite signed graph with $E$ edges, the minimum number of`
- TeX line 144: `\section{Exact finite protocol}`
- TeX line 159: `\section{Finite atlas}`
- TeX line 215: `pattern.  The shell-level optimization therefore does not turn the late`
- TeX line 216: `near-coherent block into a uniformly favorable cancellation direction.`
- TeX line 228: `switching invariance.  The finite atlas is certified by exact rational`
- TeX line 232: `the full Gate-B/twin-prime endpoint remain open.  The Session-named Route-A`
- TeX line 245: `The canonical finite result is`
- TeX line 252: `finite '+3' sign anomaly survives.`

## Conversion limitations

- 4 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
