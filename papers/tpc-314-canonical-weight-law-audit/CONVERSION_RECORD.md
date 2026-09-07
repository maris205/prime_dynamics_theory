# TPC-314 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `abdb8bfb644f8d81c8d74b6ac609d88d191b913b`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `1383a90e7dc5f1dd7bd3d78d7ef62037b3f2bccd1d663ae8eb2bab3da2e3ab30`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `af0c68047d8dc0402bbcda1224529daaf15945f2610669e5c19fcb86167379cc`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `729a83310671984e08edd458e722eedd023442ce5e1a180cffb8ba9a077ff1db`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `93977a16140c54a83a57f090fbbd37f4afd54325c959cbae6ba0d0b462e1d2e7`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC310_314.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and route position` | 40 | 1 | `HEADING_TEXT_MATCH` |
| `Frozen physical object and three laws` | 58 | 1 | `HEADING_TEXT_MATCH` |
| `Exact identities and logarithmic enclosure` | 101 | 2 | `HEADING_TEXT_MATCH` |
| `Finite protocol and results` | 170 | 3 | `HEADING_TEXT_MATCH` |
| `Interpretation and claim firewall` | 216 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion and next gate` | 234 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 257 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `72` before writing and `72` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `8`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `4d4d155afa42b6917f03fa31cdf1f39ad9225cd1915186d1b726ccee06de5151`.
- Source theorem/proof environment starts: lemma at TeX line 103, proof at TeX line 111, lemma at TeX line 117, proof at TeX line 121, proposition at TeX line 127, proof at TeX line 140, proposition at TeX line 157, proof at TeX line 161.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 62–67 | `29de7a8dca445087163b86801509c516a8887e7b505f9734b72131b03a39bd11` |
| D02 | equation | 69–72 | `a676f4763403ba7193e37f23e647423fda43132e8be674128f281ab05f83b639` |
| D03 | equation | 77–83 | `eeb551efc0d3e061a0555d7ee1f76f452d12d9db2c02156fa2e8a94c9035f471` |
| D04 | equation | 85–90 | `126cc7399fffa95eaef51daf1705f412c728616797decd2db33b1657b7457304` |
| D05 | equation | 105–108 | `15117405f7cb87a9c8a6df80f99312ad97d76878cfc3160c35847abe885d5746` |
| D06 | equation | 130–136 | `d6d42822cb52124df46bb9233b5cf584801596be5c765f1b3ee82c3926393aca` |
| D07 | \[...\] | 143–145 | `7e50230fac782b28137396769b7d18f35521b2aedb56ab8542b3dccb7a59088e` |
| D08 | \[...\] | 209–212 | `3cf021ce41afd138f5bf14dfffcf32d3d6c9091c079b3c0ea797f8057a8348ae` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 12: `\title{Externally Motivated Weight Laws on a Finite Prime--Shell Diagnostic}`
- TeX line 23: `We audit the dependence of a finite prime--shell diagnostic on its weighting`
- TeX line 33: `strictly above it.  The finite class is therefore robust across the declared`
- TeX line 36: `These are finite source-first facts, not a canonical-weight theorem, an`
- TeX line 43: `source--shell panel and found exact finite sign separation.  TPC-313 then`
- TeX line 93: `not an assertion that the full von-Mangoldt source has been identified with`
- TeX line 99: `it does not remove the target-Gram leakage of the inherited minimum.`
- TeX line 104: `For every finite coefficient vector $c$,`
- TeX line 113: `\eqref{eq:weighted} and expand the finite square.  Positivity follows from`
- TeX line 157: `\begin{proposition}[Finite interval soundness]`
- TeX line 166: `operation preserves containment.  Induction over the finite expression tree`
- TeX line 170: `\section{Finite protocol and results}`
- TeX line 204: `three declared positive laws preserve the finite separation class.  The`
- TeX line 218: `The positive result is narrow but useful: within this locked finite panel, the`
- TeX line 219: `choice among three arithmetically recognizable positive laws does not decide`
- TeX line 226: `Consequently the experiment does not identify a canonical measure, and a`
- TeX line 229: `physical Gram matrix, and the panel is not an external holdout.  No statement`
- TeX line 231: `the certificate pays no arithmetic $L^2$ estimate, fixed-power credit, or`
- TeX line 236: `TPC-314 establishes a finite, independently replayed weighting-law audit:`
- TeX line 240: `finite obstruction to law-independent amplitude, consisting of one minimum`
- TeX line 246: `would still be finite and would not, by itself, pay the growing arithmetic`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:output` → `main.tex#L66` (existing project target or original TeX label line).
- Link relocation: `#eq:gram` → `main.tex#L71` (existing project target or original TeX label line).
- Link relocation: `#eq:weighted` → `main.tex#L82` (existing project target or original TeX label line).
- Link relocation: `#eq:weighted` → `main.tex#L82` (existing project target or original TeX label line).
- Link relocation: `#eq:logbound` → `main.tex#L135` (existing project target or original TeX label line).
- Link relocation: `#eq:weighted` → `main.tex#L82` (existing project target or original TeX label line).
