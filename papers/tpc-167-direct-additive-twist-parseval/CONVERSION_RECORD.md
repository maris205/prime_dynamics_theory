# TPC-167 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `12b6e806493f254941b66987a0040d7f6673b2ed95528ebf5f6ad79b465a622e`.
- Bibliography: [references.bib](references.bib), SHA-256 `8b9b47f32a06e4065f8549c3e01eb177ec4903efe3648ed62e93f3279af93ac5`.
- Preserved PDF: [tpc-167-direct-additive-twist-parseval.pdf](tpc-167-direct-additive-twist-parseval.pdf), SHA-256 `1792d715860ba6327dc43f5a50dd5e075ab6465c13c57838aa40771ef469547d`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `65e47b52efddec7c22037da2219da6d4d73cea60c1623606c8ad4156f44222a6`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC165_169.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `The literal core and its phase transform` | 62 | 1 | `HEADING_TEXT_MATCH` |
| `Exact phase mean square` | 95 | 2 | `HEADING_TEXT_MATCH` |
| `A finite exact Fourier registry` | 147 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation of the power envelope` | 177 | 3 | `HEADING_TEXT_MATCH` |
| `Why pointwise selection remains open` | 203 | 3 | `HEADING_TEXT_MATCH` |
| `Reproducible certificate` | 233 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 245 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 256 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `48` before writing and `48` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `17`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `53cda4bb7622c3b5dbd0e5f1196eddb4fc2824e6c433d86fb4cdd62df0931e95`.
- Source theorem/proof environment starts: theorem at TeX line 97, proof at TeX line 115, corollary at TeX line 125, proof at TeX line 137, proposition at TeX line 151, proof at TeX line 166.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 65–68 | `cd58949fab809bc39fb6693e235d2d6eb0dfb7cd4e8f718a09b95eb737e6061a` |
| D02 | \[...\] | 69–72 | `f129363ac950a11d6bc60ae9c1e53fa98c5e650e1115c26494da5f10e8cc196c` |
| D03 | \[...\] | 74–77 | `cc63470af72fa24f3af818bd90d41077a6cbeff1200a20bd4a4b81da092bed28` |
| D04 | equation | 79–82 | `75b4593c791e29f4e3a8140673926405206fac41a3a4992ff21b3a23533e3031` |
| D05 | equation | 84–88 | `7a97009492bd1523acc1c954172677df940e7abecaac1ef27b9e881b55c6fd07` |
| D06 | equation | 99–105 | `b25fe5bed9f25ed5377e9be049f0712ff72d16470ef37a8799752a15143f6b34` |
| D07 | equation | 107–111 | `0687b560b3bf3658836fd9fcf3ccea345f980a6cc77f5e0e403889227ad1fc67` |
| D08 | \[...\] | 117–120 | `f0204ea55555cc1ca418926112ad6ff340d5fe85843e69aa9009e16eceafdaa3` |
| D09 | equation | 127–134 | `f00cb7c5679185e0a95bc6bacebba6608557bc99b2f6b7c8688598e6cfd8e2f7` |
| D10 | equation | 153–158 | `dcd5b5a227c103cc6969fb3efb752cfb07adde8dfba91896c63bed782b8bf497` |
| D11 | \[...\] | 161–163 | `7b421be3c089b70bb74c2d10f6765ce59e5c730acab0f20d9efe961c23dcc790` |
| D12 | \[...\] | 180–182 | `5f6bbb8710364786c5552698be5ea2997e49164ae58bc98e022204366ee88f2d` |
| D13 | equation | 185–191 | `d6c2843fc43f7b0c6d00d34da7edd5e7df0de6a1ac51c838f7caddb1666d5ae4` |
| D14 | \[...\] | 193–196 | `7d5ed7dfc2a9bed673491c855213a9b5580958c86394b37114e7fc34039989f9` |
| D15 | \[...\] | 206–210 | `a51e10867f1f8b6447bd9fbcc607278661993fbc98d8aa518af4eae465bc313b` |
| D16 | \[...\] | 214–216 | `96abca154577f0ac05233f1e86feb188c4520f25bb7dae4237efab2d63133d35` |
| D17 | \[...\] | 224–228 | `66ed1bf021fdc64f0f7a92a67bf6375f1209c1dcb5a3370ccbd32b9a49cfa78a` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 36: `minor-arc obstruction.  We open a different, direct route by treating`
- TeX line 43: `in phase \(L^2\).  It is not a pointwise theorem for a specified`
- TeX line 44: `production phase, and therefore does not close the original`
- TeX line 56: `It is not a bound at a distinguished phase and is not a production`
- TeX line 91: `and proves that this approximation route is expensive on a uniform`
- TeX line 93: `\eqref{eq:transform} does not approximate the phase.`
- TeX line 147: `\section{A finite exact Fourier registry}`
- TeX line 167: `After expansion, the finite character average is one precisely when`
- TeX line 203: `\section{Why pointwise selection remains open}`
- TeX line 238: `finite implementation checks; the proof above establishes the`
- TeX line 247: `The minor-arc obstruction to small-period approximation does not stop`
- TeX line 253: `survives on a finite source-locked phase registry.`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:transform` → `../main.tex#L87` (existing project target or original TeX label line).
- Link relocation: `#eq:count` → `../main.tex#L81` (existing project target or original TeX label line).
- Link relocation: `#eq:parseval` → `../main.tex#L104` (existing project target or original TeX label line).
- Link relocation: `#eq:grid` → `../main.tex#L157` (existing project target or original TeX label line).
- Link relocation: `#eq:l2bound` → `../main.tex#L110` (existing project target or original TeX label line).
- Link relocation: `#eq:power` → `../main.tex#L190` (existing project target or original TeX label line).
