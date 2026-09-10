# TPC-193 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `bd8c9a9d8a0112c7fcca003bf69fe27e235f6b2c8439c7393c32c91274dbbcec`.
- Bibliography: [references.bib](references.bib), SHA-256 `703c6ba80f9e258372e7713bfa44ffe48b06a3cace06b00b0c3e3adf3da262d1`.
- Preserved PDF: [tpc-193-literal-fixed-atom-candidate-mechanism-gate.pdf](tpc-193-literal-fixed-atom-candidate-mechanism-gate.pdf), SHA-256 `5f6d7501271955fe8b497fb58b2cbb52a16eb2f8cc9ffb07a1d955e4c85726d2`; 6 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `223fb52765f2c9d56e4152e6a332183679f424e262b125ce4eb7efa41231b224`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC190_194.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Gate scope and literal coefficient` | 55 | 1 | `HEADING_TEXT_MATCH` |
| `The formula-completeness gate` | 89 | 2 | `HEADING_TEXT_MATCH` |
| `Two source-locked summation domains` | 91 | 2 | `HEADING_TEXT_MATCH` |
| `Missing physical fields` | 141 | 2 | `HEADING_TEXT_MATCH` |
| `Declared primary-source corpus` | 155 | 2 | `HEADING_TEXT_MATCH` |
| `The two direct theorem candidates` | 201 | 3 | `HEADING_TEXT_MATCH` |
| `Every fixed atom under logarithmic averaging` | 203 | 3 | `HEADING_TEXT_MATCH` |
| `A rational atom outside exceptional scales` | 237 | 3 | `HEADING_TEXT_MATCH` |
| `Scoped exhaustion theorem` | 267 | 4 | `HEADING_TEXT_MATCH` |
| `Scoped stop, endpoint ledger and claim firewall` | 300 | 4 | `HEADING_TEXT_MATCH` |
| `Reproducible audit` | 328 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 340 | 5 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `56` before writing and `56` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `17`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `7b0eced221caf756f9e656b5d8e5c30b8412c95411b8dbbf3fa51178245eb826`.
- Source theorem/proof environment starts: proposition at TeX line 123, proof at TeX line 134, theorem at TeX line 269, proof at TeX line 287.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | align | 59–64 | `eecbadc4fce79c57774e3421e07981cd56cab49d110e820de7ed9d41e8fdc320` |
| D02 | \[...\] | 66–68 | `a157c4b4e8bbf30424c1158d68c2a87e331acaa56e06cd591a4c1f22d0ff69c7` |
| D03 | equation | 73–82 | `d07e2f0e6fbcf57502672152602cdc958e6fed57ee6a79e336eb758077cf7921` |
| D04 | equation | 94–99 | `f85494cb7c0d06a6008dc4e3580bc992603bfbced6ec3ed019a13f2c582d4819` |
| D05 | equation | 106–111 | `9bc0a6beb042dcb9294b037ba379908df8ead57430ebd750f1a341d95b6676ae` |
| D06 | \[...\] | 127–129 | `ce4b5c3dd7cf8943a6cfd59c78721347bec914bc46832ced5b0762ff55db9858` |
| D07 | \[...\] | 149–151 | `175b0e1cbfef52e1eb435875b17640ca6051133d7c43facaf35dcf329e583c14` |
| D08 | equation | 208–213 | `b4247ebc32fa6a12ab04b32b595b480626d9b15c78a3f62bae6d6ea788eb677c` |
| D09 | \[...\] | 216–220 | `98d5f642c3f125a1e3df5076d4ac1a0b90b5377d7dd8c8e6cee4c15f847c6afe` |
| D10 | \[...\] | 222–224 | `6f11448c613ad75bde0fc4f3784f66d9bc7f5db01ef03d974e25d77e41c57052` |
| D11 | \[...\] | 242–245 | `869d65a297815d4a37fe7bab3185af051962aa8cfde8596192af2a10ed9127e9` |
| D12 | equation | 247–252 | `de8a19eb56c2297d05c88b6663d40f66aff4141ee81f5b257ac3e2f68e38de74` |
| D13 | \[...\] | 272–276 | `042ec82c84064192ded941d9337b65e7aadc713c150e252605edef9611d2aa97` |
| D14 | \[...\] | 279–281 | `b4ea9609cacced9eaa655cbb863ffc73ca0e684dfefd7341db9838d477221520` |
| D15 | \[...\] | 303–305 | `f14a6064f86df3aa659ca69594102fefaa514177ff2df7a1ef070052bf1ecc47` |
| D16 | \[...\] | 310–316 | `4b381dcabe17b5c536c5246c5279a8f79846af27a06b306a35dfc97d3c16b57c` |
| D17 | \[...\] | 319–322 | `777357ee8f7b8d9207a608aad9b7f241fb37e9b547ad310c36a654c7caec7361` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 18: `\newcommand{\OPEN}{\textnormal{\textsc{open}}}`
- TeX line 47: `direct contract does not specify a cumulative replacement, so the claimed`
- TeX line 49: `schedule, uniform constant, exponent, ranges and physical loss ledger are`
- TeX line 50: `also absent.  The result is a fail-closed L1 scoped exhaustion, not an L2`
- TeX line 69: `so \eqref{eq:core} is the literal fixed-\(h_0=2\) two-M\"obius`
- TeX line 70: `coefficient, not a majorant or synthetic surrogate.`
- TeX line 75: `(\mathsf{ACTUAL\_FIXED\_H0\_PACKET},`
- TeX line 112: `uniformly over prescribed prefix endpoints`
- TeX line 119: `\eqref{eq:block}, setting \(N=T\) leaves \(T<t(z)\le2T\) and does not`
- TeX line 125: `The source-locked record does not uniquely instantiate the direct target's`
- TeX line 136: `domains.  The substitution \(N=T\) does not identify them.  No locked`
- TeX line 146: `TPC-189 also does not freeze the admissible \(X,N,q\) ranges, a positive`
- TeX line 147: `pointwise exponent \(\sigma\), the uniform constant \(C\), or a complete`
- TeX line 152: `cannot yet be parsed into a unique literal theorem call.  Fixed \(h_0=2\)`
- TeX line 157: `The corpus is finite and explicit.  It contains the five primary sources`
- TeX line 159: `found by an exact twisted-correlation/Fourier-uniformity scan:`
- TeX line 191: `& single-factor Fourier uniformity averaged over interval origins`
- TeX line 234: `\eqref{eq:tw} supplies neither natural \(q/N\) control nor a uniform`
- TeX line 290: `than natural endpoint normalization; fixed data, all-prefix uniformity,`
- TeX line 291: `all-scale uniformity, a fixed-\(X\) rate and actual support also fail.  For`
- TeX line 307: `does not stop either O161 pointwise theorem, the global architecture, or`
- TeX line 335: `duplicate JSON keys and nonfinite numbers are rejected, and`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 17 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:core` → `../main.tex#L63` (existing project target or original TeX label line).
- Link relocation: `#eq:core` → `../main.tex#L63` (existing project target or original TeX label line).
- Link relocation: `#eq:block` → `../main.tex#L98` (existing project target or original TeX label line).
- Link relocation: `#eq:cumulative` → `../main.tex#L110` (existing project target or original TeX label line).
- Link relocation: `#eq:block` → `../main.tex#L98` (existing project target or original TeX label line).
- Link relocation: `#eq:cumulative` → `../main.tex#L110` (existing project target or original TeX label line).
- Link relocation: `#eq:tw` → `../main.tex#L212` (existing project target or original TeX label line).
- Link relocation: `#eq:core` → `../main.tex#L63` (existing project target or original TeX label line).
- Link relocation: `#eq:tw` → `../main.tex#L212` (existing project target or original TeX label line).
- Link relocation: `#eq:tt` → `../main.tex#L251` (existing project target or original TeX label line).
- Link relocation: `#prop:formula` → `../main.tex#L124` (existing project target or original TeX label line).
- Link relocation: `#eq:tw` → `../main.tex#L212` (existing project target or original TeX label line).
- Link relocation: `#eq:tt` → `../main.tex#L251` (existing project target or original TeX label line).
