# TPC-358 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `e29acc87ca87c17cd9a76b5d96792297b8d6d100c3e993b817c03d1c891c6530`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `e2a87eac881d8383062de35780a73c42d3abcb5bd1fa4e1bf7560fc0debb6d1b`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `8a931e6cabfe29f27d8db5f8dc47aef62fd28dd63500265ec5913b13265fcb1f`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `b18e0f85edfe4e2f20b7f6dce567b8b143444cb56c84c4731a82859e0e7d75a9`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 39 | 1 | `HEADING_TEXT_MATCH` |
| `Model and frozen holdout` | 53 | 1 | `HEADING_TEXT_MATCH` |
| `Finite inequalities and transfer criterion` | 89 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 113 | 2 | `HEADING_TEXT_MATCH` |
| `Controls and claim firewall` | 166 | 2 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 183 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 200 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `41` before writing and `41` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `8`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `d0eb9fefd6c9459b9111704239b53b0d1d3381dae96dd38a95716796d8d53c0e`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 58–63 | `df7fab9e51d7db8abd122cd56fcc12c6f02f4c560e3e20a9bbbbd9d38dac6e02` |
| D02 | equation | 67–72 | `006a762784f2300877e557e27421f14d5fd01bf4316fb656d96220d1899ef900` |
| D03 | \[...\] | 77–79 | `ab12720e31526ab8a3ac6056f4b02917434332233b50a54cdcf7bbc95e7a5ce3` |
| D04 | equation | 92–96 | `87ce7770c3ccb74c2a28b6ff8d42bbfac259b29f7cc45974c072073630d453e2` |
| D05 | equation | 98–101 | `a2a4257558c4749fa7fbbce344323bc13a2047e05dd4ecdbb662761f64518183` |
| D06 | equation | 142–147 | `dc45b4951da0e0321c229d6c211d3590e2d4c1eca516f836fdb652fbe7d042cb` |
| D07 | \[...\] | 155–157 | `9d407201d80df68ad64545bd4900f70c3208cfe499d6c2183915b2f946c5a2b0` |
| D08 | \[...\] | 160–163 | `2a730f6beec4ec571527e9f287bd619b999690053eca598aed1febcee508736b` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 9: `\title{Fresh-Origin Transfer of a Finite Operator-Norm Certificate}`
- TeX line 23: `We test whether a finite operator certificate for the position-aware`
- TeX line 33: `$0.64$.  The origin span is 168000.  This finite transfer is accompanied by`
- TeX line 35: `34 downward, and 7 flat adjacent count transitions.  No origin-uniform`
- TeX line 41: `TPC-357 established a finite Schur/spectral scale audit on three origins`
- TeX line 42: `selected by a geometry-only adversarial rule.  A finite cap can be informative`
- TeX line 47: `The experiment is intentionally operator-only.  It does not evaluate the V59`
- TeX line 89: `\section{Finite inequalities and transfer criterion}`
- TeX line 91: `For any finite real symmetric matrix $T$, the induced-norm inequality gives`
- TeX line 102: `The inequalities are exact finite statements.  They do not imply that their`
- TeX line 103: `right sides are uniform in $x$ or $N$.`
- TeX line 110: `finite comparison rule, not a statistical confidence statement or an`
- TeX line 153: `The transfer does not restore monotone scale behavior.  Of the 54 adjacent`
- TeX line 164: `The cap therefore transfers as a finite envelope while decay does not.`
- TeX line 173: `$[52031,52044]$.  The checker does not import the producer and tolerates only`
- TeX line 180: `requires byte-identical stdout.  These controls certify the finite artifact;`
- TeX line 181: `they do not supply an origin-uniform theorem.`
- TeX line 187: `caps transfer within the frozen finite thresholds.  This is a new independent`
- TeX line 188: `finite positive result.  The same experiment also preserves the key`
- TeX line 190: `finite cap transfer alone gives no growing operator estimate.`
- TeX line 192: `Accordingly, the source-uniform masked arithmetic $L^2$ problem, a growing`
- TeX line 194: `the twin-prime endpoint remain open.  The next admissible test is a hostile`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.

- Link relocation: `#tab:extrema` → `main.tex#L123` (existing project target or original TeX label line).
