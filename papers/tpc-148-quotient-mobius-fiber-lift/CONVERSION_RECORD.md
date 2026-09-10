# TPC-148 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `b9d4902268dc8a9636669b28930e8cb6f9cb3c68cff3aaef764283a0852fb040`.
- Bibliography: [references.bib](references.bib), SHA-256 `e4ff550fa14966525c29cfe323dc9ee3469e2f1969809da917447a7f70358f13`.
- Preserved PDF: [tpc-148-quotient-mobius-fiber-lift.pdf](tpc-148-quotient-mobius-fiber-lift.pdf), SHA-256 `a13e99415af8aef9a9805cee32767bda0104f057c7e5494c08554b9a1bd8832d`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `9b99648d670a64062c4b4331eb0b4a34538f49bca25349d0b73291e618de57a3`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC147_149.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `The quotient lift` | 80 | 1 | `HEADING_TEXT_MATCH` |
| `The determinant-two fiber` | 127 | 2 | `HEADING_TEXT_MATCH` |
| `Pretentious distance under the lift` | 181 | 2 | `HEADING_TEXT_MATCH` |
| `Scope and machine certificate` | 288 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 331 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `96` before writing and `96` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `16`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `a7bf09e025ae366c611dc4326c96f64bf142d16b0a965dcb9a7adf58217820a7`.
- Source theorem/proof environment starts: definition at TeX line 85, theorem at TeX line 103, proof at TeX line 112, remark at TeX line 119, theorem at TeX line 142, proof at TeX line 154, corollary at TeX line 169, lemma at TeX line 194, proof at TeX line 207, proposition at TeX line 213, proof at TeX line 225, lemma at TeX line 234, proof at TeX line 246, corollary at TeX line 263, proof at TeX line 277.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 57–59 | `bfe956e84afc0f6888748b860052456e4dd41152b07ba008f58a3fef6a8a592e` |
| D02 | \[...\] | 62–64 | `0354d4841df578b10b7153ff3c1e516f65b1ede399eb8d606d576dd25c330561` |
| D03 | equation | 89–96 | `94ada103f7cb276e58ef9b3ac9011f4f2f3c959ae4e837b88d74471294abbc3c` |
| D04 | equation | 106–109 | `cc01349c97de1b3d3739968ae5887507b8cf9f34b2eda527904bc72777dcfeae` |
| D05 | equation | 130–133 | `5c64edd832c86c2946b5ac636858348ea901a664dcf99b6c17c43148b6d194d2` |
| D06 | equation | 137–140 | `f615c016c483f5de7887317522b32b6655825852e9f3ca573475bd971b3cbbf3` |
| D07 | align | 145–151 | `39521a2ab6ccef8e0c6cc83fe93dd87b7fe06785636264e0b4828639ee32fdb3` |
| D08 | \[...\] | 156–158 | `87f5121f0d6e3e00700e38d6f7834f46c1ce5c733c32436780e942f53f8dc868` |
| D09 | \[...\] | 162–166 | `467e2d8e4bd96038fb2a2922383644cb348b40afb39a836c1fb138f8c9e228b9` |
| D10 | \[...\] | 184–190 | `755733a5da55e9b7864cd67e13a3563bbc8b932a2137a0e78f2e8c5940937c95` |
| D11 | \[...\] | 197–203 | `05874ea9c1af2b8f6195a92dee6ad14ee862300e966d32c8594cae35a4177eed` |
| D12 | equation | 216–222 | `cdc7aa27354046398ca13551bbddfde0939dbbefd67a165ebbf15304be23d53c` |
| D13 | \[...\] | 237–241 | `2577a389aa44710c7681b7f8bac5fbda34c4aaed694263cbb1adc0019d50cc5f` |
| D14 | equation | 256–260 | `d5ad10eec5f2ad7380fe4b434b078056d5895dd66dae0f2f2fccd889eb17b1ad` |
| D15 | \[...\] | 268–271 | `9526c0e55f635efb88752762f8a6302c22b4697899c7041286fe0bc8c80ec982` |
| D16 | \[...\] | 280–283 | `e7c8af77939ef1b47524cb6ba607ed353b647989570ce922e52e966c8805f2c3` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 36: `\newcommand{\OPEN}{\textnormal{\textsc{open}}}`
- TeX line 74: `construction supplies an exact \(\Lzero\) lift and a uniform`
- TeX line 75: `\(\Lone\) nonpretentious input.  It does not supply physical weights,`
- TeX line 177: `This is a new representation of the same literal core; it does not`
- TeX line 213: `\begin{proposition}[Uniform nonpretentious stability]`
- TeX line 254: `\Citet[equation~(1.12)]{MatomakiRadziwillTao2015} prove, uniformly`
- TeX line 267: `uniformly for \(c\le(\log X)^A\),`
- TeX line 294: `the prime modification set \(\{p:p\parallel c\}\).  These finite`
- TeX line 314: `\(\OPEN\); not supplied.\\`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 4 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:local` → `../main.tex#L95` (existing project target or original TeX label line).
- Link relocation: `#eq:quotient` → `../main.tex#L108` (existing project target or original TeX label line).
- Link relocation: `#eq:shift` → `../main.tex#L146` (existing project target or original TeX label line).
- Link relocation: `#eq:progression` → `../main.tex#L147` (existing project target or original TeX label line).
- Link relocation: `#eq:t` → `../main.tex#L139` (existing project target or original TeX label line).
- Link relocation: `#eq:fiber-lift` → `../main.tex#L150` (existing project target or original TeX label line).
- Link relocation: `#eq:local` → `../main.tex#L95` (existing project target or original TeX label line).
- Link relocation: `#lem:prime` → `../main.tex#L195` (existing project target or original TeX label line).
- Link relocation: `#eq:distance` → `../main.tex#L221` (existing project target or original TeX label line).
- Link relocation: `#eq:distance` → `../main.tex#L221` (existing project target or original TeX label line).
- Link relocation: `#eq:lambda-distance` → `../main.tex#L259` (existing project target or original TeX label line).
- Link relocation: `#lem:reciprocal` → `../main.tex#L235` (existing project target or original TeX label line).
- Link relocation: `#eq:local` → `../main.tex#L95` (existing project target or original TeX label line).
- Link relocation: `#eq:quotient` → `../main.tex#L108` (existing project target or original TeX label line).
- Link relocation: `#eq:fiber-lift` → `../main.tex#L150` (existing project target or original TeX label line).
- Link relocation: `#eq:lambda-distance` → `../main.tex#L259` (existing project target or original TeX label line).
- Link relocation: `#eq:fiber-lift` → `../main.tex#L150` (existing project target or original TeX label line).
- Link relocation: `#eq:distance` → `../main.tex#L221` (existing project target or original TeX label line).
