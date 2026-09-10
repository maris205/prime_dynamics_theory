# TPC-158 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `dccc04bfe231aeb071de8d9d024fdbe9558543b5ad71e79a48dd8343e1d31dfa`.
- Bibliography: [references.bib](references.bib), SHA-256 `c28bbee2cbba17126cfdfacbe3cb0b380549de939ec3658d5fee80416f61fa1c`.
- Preserved PDF: [tpc-158-additive-phase-major-minor-gate.pdf](tpc-158-additive-phase-major-minor-gate.pdf), SHA-256 `93552a3ae5a5197193d7f504e42b4f68db193c2250dd3a8dd1c62db6fae7c946`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `fd100c0422f811d79744bd13eab94de2294b463b69735533891bdaac5f1c652e`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC157_159.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Setup` | 63 | 1 | `HEADING_TEXT_MATCH` |
| `The major-arc gate` | 85 | 1 | `HEADING_TEXT_MATCH` |
| `Exact projection on a residue rectangle` | 144 | 2 | `HEADING_TEXT_MATCH` |
| `Route semantics` | 252 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 269 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 279 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `64` before writing and `64` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `17`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `c125036d621e1b2d66b4a51f1441327e4aa04418054539f96a4e730873f69468`.
- Source theorem/proof environment starts: lemma at TeX line 90, proof at TeX line 104, theorem at TeX line 111, proof at TeX line 133, theorem at TeX line 154, proof at TeX line 186, corollary at TeX line 201, proof at TeX line 229.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 66–70 | `758e68539ab324b570d9c5a1d933c13a1a1ce5de7a22666d140bed765d6cc056` |
| D02 | equation | 75–79 | `e7afd71effc4cd69413c50b2145e515a7cce7639c23afa37bb9a3f3570bc4bb1` |
| D03 | \[...\] | 92–95 | `31143f72411a55111013c4b7a63792379ffb6bd6f1c41e60e298c39b633dd3aa` |
| D04 | equation | 97–101 | `9b3d8470fc3e53349f44b4434d75d8ee3bf9ba25eb3b14a3859a513925034f29` |
| D05 | \[...\] | 113–117 | `82c160340c34c3a8373cfc356357ec74d63d9e253709d48cd2f4da74d1c317b7` |
| D06 | \[...\] | 119–121 | `c240a388c92ca48ec4f8e569326d5b5b7fba636dea889a4c535661bb63c121af` |
| D07 | equation | 123–130 | `b740257fb01bfed933c7b3f979bff4072d97e61156430e7786019639ed042b80` |
| D08 | \[...\] | 147–150 | `dd3e28a7629243b762e1431e579c874683295ca9f8235e27c7ed959f271249a7` |
| D09 | equation | 156–164 | `2c8217ebb9b37a627354df890ad76c462bcfd81f426e7263cd14b4838adaa9b0` |
| D10 | \[...\] | 167–172 | `4a50e06e33ce103ca9c0b5a62e682025cb83744e85d0f6995e92b89932e9b7bd` |
| D11 | equation | 174–183 | `dfebd19972d8455c27b4932294805076cc69779a5ac4d4570392bc6cef7da8f6` |
| D12 | \[...\] | 189–192 | `1b516e64783220fa8ca3cef2a53bcab9074db9e8fe1c36bf193cf469015130ca` |
| D13 | \[...\] | 205–208 | `8eba0bd40161236acd0e2f8ba2fc0a5ee4cb4aa09944ba345458efe9361c1b9d` |
| D14 | equation | 210–217 | `f71df3e7594a491987c69302e3da1aa51d74ba0cb7a4746774ce552056be0fc3` |
| D15 | \[...\] | 219–224 | `6a965589405754c7484fefe678a46524ec9678887096bf4922cdb445169ff9ed` |
| D16 | \[...\] | 233–242 | `71b6ecaf9b5b722cfb1a370b5aca9dc6ceb26a33c6c90976b8d54c7272a6c72e` |
| D17 | \[...\] | 257–261 | `8cb88c13bd31bad4d90984330621e838af76f78e61411c22069645b9401f51bb` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 57: `small-period approximation is expensive; it does not say that the`
- TeX line 201: `\begin{corollary}[Uniform minor-arc route stop]\label{cor:stop}`
- TeX line 216: `\label{eq:uniform-minor}`
- TeX line 218: `then, uniformly over all allowed periods,`
- TeX line 243: `The first infimum in \eqref{eq:uniform-minor} makes`
- TeX line 244: `\(K_{n,R}R/L_n=1+o(1)\) uniformly, and the second makes the squared`
- TeX line 245: `term \(o(1)\) uniformly.`
- TeX line 248: `The uniform infima in \eqref{eq:uniform-minor} are essential.  A`
- TeX line 249: `pointwise assertion for every fixed \(R\) does not stop a sequence of`
- TeX line 263: `a different physical crosswalk remains logically open.  The`
- TeX line 266: `phase-aligned fixture.  These finite checks support implementation;`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:aligned` → `../main.tex#L100` (existing project target or original TeX label line).
- Link relocation: `#eq:projection` → `../main.tex#L163` (existing project target or original TeX label line).
- Link relocation: `#eq:l1lower` → `../main.tex#L182` (existing project target or original TeX label line).
- Link relocation: `#eq:l1lower` → `../main.tex#L182` (existing project target or original TeX label line).
- Link relocation: `#eq:uniform-minor` → `../main.tex#L216` (existing project target or original TeX label line).
- Link relocation: `#eq:uniform-minor` → `../main.tex#L216` (existing project target or original TeX label line).
