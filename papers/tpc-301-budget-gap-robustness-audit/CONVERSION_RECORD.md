# TPC-301 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `55240d2d7254cbf8bd7fc0b4755fa8f24254e424`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `0537b80d34ea0c25c0834164234b0994c08c5576836c6fb191d61c0dcace895a`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `1a1a04bce6b6183a4754ad6035411fba5bed67be78dd7d0c2d86165d645a5c3d`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `008737fc259f8c952d642bfade89b004b7e6ba08b1a8a7ded499c78e5fb8e9f7`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `2432fad7c44442a3eed6c9130638d49a0f16297b627dac4d77dcd666b2de7bcd`.
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
| `Question and finite model` | 38 | 1 | `HEADING_TEXT_MATCH` |
| `Finite theorem layer` | 76 | 2 | `HEADING_TEXT_MATCH` |
| `Hostile audit protocol` | 135 | 2 | `HEADING_TEXT_MATCH` |
| `Finite results` | 160 | 3 | `HEADING_TEXT_MATCH` |
| `Reproducibility and claim firewall` | 196 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 213 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 222 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `60` before writing and `60` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `9`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `2785e270dbe8d7acc25ba26a7ec4983867536151d06b5e8432623474d34f7777`.
- Source theorem/proof environment starts: proposition at TeX line 78, proof at TeX line 86, proposition at TeX line 92, proof at TeX line 99, proposition at TeX line 105, proof at TeX line 114, proposition at TeX line 120, proof at TeX line 129.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 25–27 | `b82569d057401ea3d794386613d5d4a9e8c0b9f8bde97f075ead4072d7e00341` |
| D02 | \[...\] | 51–53 | `c0d51fb212190b6104f51de4adabf1c10ee1a05bb6adfec6b4f5be7215fed208` |
| D03 | \[...\] | 55–59 | `2b7861b636f9f4d6cd52d1bf14821c9222b265d1e4d0b13aeb3909f541286e6b` |
| D04 | \[...\] | 65–69 | `adb703ffe7a72755939e5b9034e7f720e755aaf4aca6ade285f1336da668408a` |
| D05 | \[...\] | 80–82 | `3e5802eae5b32299db64f8021990d5803432b40a64d9f008bd94b456faefaaf4` |
| D06 | \[...\] | 94–96 | `2831f421fadc4c9f819d301c9979f910482b04f7e1b1bba09572b74b04b4e2df` |
| D07 | \[...\] | 107–109 | `3a5ee35efebafce1de0816769f168c238954c7d92acedec01d6c88fcdb571914` |
| D08 | \[...\] | 123–126 | `0ce9939b0a24e16d6f81aeb8126860b3500c01c06abf4351c445c954f7bdf36f` |
| D09 | \[...\] | 151–155 | `0b18d6194ea4be845facbf66b30432e4fc6f7f170e4f3fe8f25af81044e9ce7c` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 19: `A finite native-profile audit for the twin-prime dynamical bridge found a`
- TeX line 24: `three source-side normalizations are compared.  The finite budget`
- TeX line 34: `This is a finite restricted robustness certificate, not an asymptotic`
- TeX line 38: `\section{Question and finite model}`
- TeX line 40: `The preceding releases measured literal source profiles for a finite`
- TeX line 43: `finite dual witnesses \cite{tpc300}.  Those results used one normalized RMS`
- TeX line 45: `finite obstruction can be misleading if it is caused by a tolerance`
- TeX line 60: `The source Gram is positive definite for every tested prefix.  The targets`
- TeX line 70: `All finite matrix entries are formed from rational arithmetic before the`
- TeX line 76: `\section{Finite theorem layer}`
- TeX line 160: `\section{Finite results}`
- TeX line 191: `frozen finite atlas; in particular, the gap can vary by several orders of`
- TeX line 193: `the separation does not disappear at the stricter or looser tested`
- TeX line 199: `frozen TPC-299 source-first engine.  An independent checker, which does not`
- TeX line 205: `The finite theorem layer is proved exactly on the declared finite model.  The`
- TeX line 208: `does not prove a growing profile-budget bound, arithmetic $L^2$ estimate,`
- TeX line 215: `The TPC-300 finite native-budget obstruction survives the first natural`
- TeX line 217: `and normalization protocol to growing shells, where the finite theorem`
- TeX line 219: `controlled uniformly.`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#tab:gap` → `main.tex#L171` (existing project target or original TeX label line).
