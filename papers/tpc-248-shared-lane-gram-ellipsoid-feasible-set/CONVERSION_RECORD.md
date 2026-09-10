# TPC-248 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `8715071252050013628ef4770d857d2e49d23aacf49bb2d9f2b4298c7887ce82`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `b56bf0db6b0bc56de993db6cf8e2fcf41a22c6f874113114f2665f1ba8b15649`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `883bbd66fdb7887aa772ca07f60962281fb7615c6c5fd241616aee853e5f3aec`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `c9da0830fd9ce03859d85f9d14675dd82e330f0abb16e817e11306b115d14e67`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC245_249.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `The source-native joint object` | 65 | 1 | `HEADING_TEXT_MATCH` |
| `Exact analysis-map ellipsoid` | 88 | 1 | `HEADING_TEXT_MATCH` |
| `Exact spheres and physical orientation` | 142 | 2 | `HEADING_TEXT_MATCH` |
| `Grouped budgets are not interchangeable` | 186 | 3 | `HEADING_TEXT_MATCH` |
| `Sharp adversarial fixtures` | 214 | 3 | `HEADING_TEXT_MATCH` |
| `Certificate and route boundary` | 238 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 261 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 273 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `80` before writing and `80` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `19`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `21d4361eb464f4a61834aae1ea38fa741f2d02bd3eaac67a2322a8a8c4618a61`.
- Source theorem/proof environment starts: theorem at TeX line 99, proof at TeX line 115, theorem at TeX line 144, proof at TeX line 156, corollary at TeX line 170, proof at TeX line 180, theorem at TeX line 190, proof at TeX line 204.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 53–55 | `d8edea9a77d8d9536cd60e6d3eb8ffe0987ca9f8f6bba429bc4baf3cb2ef3f42` |
| D02 | \[...\] | 69–73 | `e93afe6626d08c4299f5acf0d2d943f1aa4f72284eda19a70b049404009b90fd` |
| D03 | \[...\] | 75–77 | `abd60cbee1396a384148382116b0a7c92a225b3a0b288a5d15263204a9673cb8` |
| D04 | \[...\] | 92–95 | `76c666326d29aba77a8b8ba744aab946abf337586cc8b2abc76319849fb786a0` |
| D05 | \[...\] | 101–104 | `70fa408e44bcef1c86cf1b06e44df960fd01f1971efd62aa593b9a340408713d` |
| D06 | \[...\] | 106–108 | `c231f6505d12faf887c9ac98815aff33c04ec93b185892837dd1cb5ebce8e001` |
| D07 | \[...\] | 110–112 | `85214adb7b5b8947c25aae8e263bc3e82846904956c5f1a64b0d53ac4e4f8b2f` |
| D08 | \[...\] | 118–120 | `b731fd7495b297eb6e7e529a7f16a406151f6b9edb2cec0a763674b278aae295` |
| D09 | align* | 122–127 | `2ecf10d327c7c240b0f89679f43f9ec8c9e211834b28aecb1d1a8481ca3db998` |
| D10 | \[...\] | 131–133 | `ac3b5b465ba530d76cc260f0c7c1424e65e3d356f707aae869d8f7025409de16` |
| D11 | \[...\] | 146–148 | `70318d098dad581c19b61b73683398ae26ad8a0b4b8e46091569b7a87b6d10d4` |
| D12 | \[...\] | 150–152 | `d84a9aff6c1382e7237e9efa51401b7c3aaefd21bcc43ac799ff6cbbed91fff3` |
| D13 | \[...\] | 165–168 | `d6ec9526e5c5cc991cfed5b29ceda3daf579f0761c5ca1803dc773703b6605b8` |
| D14 | \[...\] | 172–175 | `a437e0aeba5c090d80efc4289b151db92aff79793474e99ad78b8a2325dc25c7` |
| D15 | \[...\] | 193–195 | `5ba9c0cfe5d0fba8e70c2212a692361a2575057dc5f137bd9ea0bfb8b6a29158` |
| D16 | \[...\] | 198–201 | `1ade401e1269b5053bd0fab775ec9a161a39192fff0de0ba3b1fb9cbe167c4e8` |
| D17 | \[...\] | 217–220 | `a05a9c6d975d782602d77bd8ae8d7781d82d6530d566a006f63079ec51c68dfb` |
| D18 | \[...\] | 222–224 | `351ac98b065953391c4178f04ce344cb24ad0578f4bc9af3a62b3263d2490a1d` |
| D19 | \[...\] | 251–255 | `21f7ab8964cb71fc1feea44e6364453a595e7864965561c6e4e409fdf42d40ef` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 47: `A source-index decomposition of the finite V59 twin-prime Gate-B scalar exposes,`
- TeX line 67: `TPC-247 writes the physical scalar as a finite source covariance and, for a`
- TeX line 84: `We therefore solve the following finite-dimensional problem before applying`
- TeX line 90: `Let $v_1,\ldots,v_m$ be ordered vectors in a finite-dimensional complex Hilbert`
- TeX line 116: `In finite dimension, $\Ran V^*=\Ran(V^*V)=\Ran G$.  If $y\in\Ran G$, the`
- TeX line 211: `Thus ''local ellipsoid'' does not by itself determine a cross-group feasible`
- TeX line 248: `$(\langle v_{cb},W_c\rangle)_b$ for each fixed $c$.  It does not estimate the`
- TeX line 253: `\texttt{FULL\_GATE\_B=OPEN},\qquad`
- TeX line 263: `The joint shared-lane geometry is an ellipsoid, not a product of marginal`

## Conversion limitations

- The preamble-only glyphtounicode input was resolved with kpsewhich and checked against the audited SHA-256; its non-content mapping table was not expanded. The original command, source line, and dependency hash are retained in the reading layer.
- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#thm:sphere` → `main.tex#L144` (existing project target or original TeX label line).
- Link relocation: `#thm:ball` → `main.tex#L99` (existing project target or original TeX label line).
- Link relocation: `#thm:ball` → `main.tex#L99` (existing project target or original TeX label line).
