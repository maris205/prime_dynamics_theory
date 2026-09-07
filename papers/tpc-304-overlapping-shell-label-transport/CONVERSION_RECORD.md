# TPC-304 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `55240d2d7254cbf8bd7fc0b4755fa8f24254e424`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `ecc041fab77bed2df9f8982511f53c85769246e176f113ebb626d09741c2cb04`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `60fbe75dffda6fabe67e9397ba473410b5401ed16d79eafb6ccec1d721642165`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `54a45918d1470c8264206e428c8a5f67ba86e7e98199f7f23395cdfab04ad172`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `d215eb71b9ef847456e598354e3908754fdca2c339592e65d6c0751908c8332a`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC300_304.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and frozen data` | 30 | 1 | `HEADING_TEXT_MATCH` |
| `Gauge-invariant transport identity` | 50 | 1 | `HEADING_TEXT_MATCH` |
| `Finite crosswalk` | 85 | 2 | `HEADING_TEXT_MATCH` |
| `Obstruction and next question` | 121 | 2 | `HEADING_TEXT_MATCH` |
| `Reproducibility and scope` | 135 | 2 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 145 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `64` before writing and `64` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `2`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `101ba0efddb3dc779753e211fb5a390105b30560d7c085db724584e2856c2abb`.
- Source theorem/proof environment starts: proposition at TeX line 61, proof at TeX line 71.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 53–59 | `c0fd02f2c64dcfeb17d619e9381d862132abd524b0842f1bab944eae51bbac2c` |
| D02 | \[...\] | 63–66 | `82ca2f4167e68dcedfa27f0a9ead0c122089adb6aaa224983e5298a0de7a8852` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 6: `\title{Overlapping Prime-Shell Sign Transport Localizes a Finite\\`
- TeX line 16: `TPC-303 found a finite obstruction to cardinality-only monotonicity of a`
- TeX line 26: `is a finite localization certificate, not a causal separation or an`
- TeX line 32: `TPC-302 established a source-first finite growing-grid gap between a signed`
- TeX line 43: `as a gauge convention.  The shells are moving intervals, not a nested`
- TeX line 77: `does not change its absolute value or the minimized mismatch count.`
- TeX line 82: `$\rho\le 1/3$.  This threshold is declared for a readable finite crosswalk;`
- TeX line 85: `\section{Finite crosswalk}`
- TeX line 123: `The positive structural result is a gauge-corrected, exact finite transport`
- TeX line 128: `The obstruction is equally important.  Coincidence of minima does not imply`
- TeX line 132: `with the native target.  Uniform profile-budget growth, arithmetic $L^2$,`
- TeX line 133: `fixed-power credit, full Gate B, and a twin-prime conclusion remain open.`

## Conversion limitations

- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#tab:crosswalk` → `main.tex#L95` (existing project target or original TeX label line).
