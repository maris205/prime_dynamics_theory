# TPC-254 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `5d1bb10430c3f56e720e62c5d58a018a2c56d7b771eb815d4e8a1127555150a6`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `279d307eacdb0e2ca70c88b683dc85e832c8a17cc37f89d4e5986c49b58e466b`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `7fefe585dfffb185218eae4a400abd5e772467442eb75667ddf9dcb3fc9fa3d3`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `f5abb13a2e5809e1c620e64ad7f203bee60635cc8b87b897f8ce96500f27cfce`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC250_254.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Frozen objects and typed source input` | 55 | 1 | `HEADING_TEXT_MATCH` |
| `Rank children and the literal \texorpdfstring{$w$}{w} moment` | 95 | 2 | `HEADING_TEXT_MATCH` |
| `Quantifier and scale firewalls` | 155 | 2 | `HEADING_TEXT_MATCH` |
| `The open adjoint lane` | 178 | 3 | `HEADING_TEXT_MATCH` |
| `Executable scope and route verdict` | 241 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 273 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `101` before writing and `101` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `16`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `c689d097b1f8e0997fe2874f137b9b5faf87fdf05208a2645ffab0c7a82c7cd5`.
- Source theorem/proof environment starts: theorem at TeX line 111, proof at TeX line 122, proposition at TeX line 214, proof at TeX line 221.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 42–44 | `401b2dc99b96f84c86a53892eb38a320f11a10d1db2d81545192ce6db1af009c` |
| D02 | equation | 58–61 | `f96ff86f7a4e1c756aaa2713337129845ea5582007afb9c50b1741172891193b` |
| D03 | equation | 63–66 | `ebf48380b0e37efadebb246b849efa602a8b5567ed206091d5353a6f507766c7` |
| D04 | equation | 69–72 | `3800fd3b12678947912689ae112c64d9abbf03fa6292c8daa68240112963b13d` |
| D05 | equation | 80–84 | `689603e61df23f7cb4edcd93c8871c3773d0b1155e385e3968f7d9c40706946d` |
| D06 | equation | 99–103 | `c3c66ca693c08127b0600c2ec6970984dfa116951f3f9100211f982e9973e4f6` |
| D07 | align | 114–119 | `315773dfecfcb8085c242247b806cca88afd4f577b77bb4f4f3a76f34910a981` |
| D08 | \[...\] | 131–133 | `225d83ce7838141728e5363694577c5ab64b313adc235c37702412d0ffd3150f` |
| D09 | equation | 136–138 | `723b44e5e7e4ea89f3c338b82b1b9037cec456a46a87340028fa7b557e63030b` |
| D10 | equation | 145–152 | `f984bc1aca123b68a631a9a7059cf727ec017ad088dd2ab514936fbfd822000e` |
| D11 | equation | 158–163 | `e2eb85f7169b90a64b8ce1d8327559aa34fab77f27e455c2e8a3f5b376e05f95` |
| D12 | equation | 172–175 | `e496529cf5963780dbd9dd814de3ca69b642c182c3dfe1fedef7f77de1fa9e32` |
| D13 | equation | 182–185 | `d67672e611086cb45ec40f3ff9eadc335612c3024cf279607914bcb07c8586cf` |
| D14 | align | 187–191 | `ff1ab1dd9bb5431ecfb5f7fb1834a0bd16c85ea20fa472fbb97262636d6ef447` |
| D15 | \[...\] | 227–231 | `bb949203b5a1cff177cb4fc0cd9a3109fe76d0bd1497c430d64fd5be583779ae` |
| D16 | \[...\] | 265–269 | `49d14f31ce96f7afbb88e6fa31a2447df88bb67e1b273a5fa8bee48789a55fd6` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 34: `$w(u)=\Lambda(u+2)-b_x^{(Z_x)}(u)$ with fixed finite cutoff`
- TeX line 46: `logarithmic saving is not a fixed power saving.  The second moment remains`
- TeX line 50: `synthetic, not literal V59 counterexamples.  A canonical exact certificate,`
- TeX line 52: `finite algebra, endpoint rules, and source-contract typing.`
- TeX line 57: `Fix a finite admissible $K$ and write`
- TeX line 74: `inspected.  It is the source-frozen TPC-253 choice, not a claim of V59`
- TeX line 89: `TPC-254 is a deterministic corollary attachment to \eqref{eq:h2}; it does not`
- TeX line 112: `Fix a finite admissible $K$.  For every fixed $M>0$ and all sufficiently`
- TeX line 165: `Bombieri--Vinogradov/fundamental-lemma savings.  Constants are not uniform as`
- TeX line 170: `Arbitrary fixed logarithmic saving is not a fixed power saving.  Indeed, for`
- TeX line 178: `\section{The open adjoint lane}`
- TeX line 212: `corpus; it is not a universal literature-absence claim.`
- TeX line 237: `Proposition~\ref{prop:sharp} is synthetic.  It does not assert that this`
- TeX line 250: `Normal and optimized Python runs agree.  None of these finite tests is`
- TeX line 268: `\text{Gate B: open}.`

## Conversion limitations

- 6 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:h2` → `main.tex#L83` (existing project target or original TeX label line).
- Link relocation: `#eq:h2` → `main.tex#L83` (existing project target or original TeX label line).
- Link relocation: `#eq:h2` → `main.tex#L83` (existing project target or original TeX label line).
- Link relocation: `#eq:endpoints` → `main.tex#L102` (existing project target or original TeX label line).
- Link relocation: `#eq:child` → `main.tex#L115` (existing project target or original TeX label line).
- Link relocation: `#eq:means` → `main.tex#L117` (existing project target or original TeX label line).
- Link relocation: `#eq:means` → `main.tex#L117` (existing project target or original TeX label line).
- Link relocation: `#eq:partial` → `main.tex#L137` (existing project target or original TeX label line).
- Link relocation: `#eq:moment` → `main.tex#L118` (existing project target or original TeX label line).
- Link relocation: `#eq:moment` → `main.tex#L118` (existing project target or original TeX label line).
- Link relocation: `#thm:main` → `main.tex#L111` (existing project target or original TeX label line).
- Link relocation: `#eq:cauchy` → `main.tex#L188` (existing project target or original TeX label line).
- Link relocation: `#prop:sharp` → `main.tex#L214` (existing project target or original TeX label line).
- Link relocation: `#eq:h2` → `main.tex#L83` (existing project target or original TeX label line).
- Link relocation: `#eq:moment` → `main.tex#L118` (existing project target or original TeX label line).
