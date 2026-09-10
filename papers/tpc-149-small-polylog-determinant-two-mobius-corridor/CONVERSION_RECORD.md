# TPC-149 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `8d4768d022ccf536ac14182b5a645797816df63a0814f698dd9a373c504bc167`.
- Bibliography: [references.bib](references.bib), SHA-256 `d4108550f0f110fdccc6a2ea4b74b7a3511ff6ce90e430c7f1c4708d4b3b5d02`.
- Preserved PDF: [tpc-149-small-polylog-determinant-two-mobius-corridor.pdf](tpc-149-small-polylog-determinant-two-mobius-corridor.pdf), SHA-256 `6e8f9be0f0e5346a48a111c3adb2dae1cbb4d83c23918dcfd6b4ad251041ceb1`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `303954602163d3fa261f42a6b51eb2e1dfa46461cd117ab769a4f6dac77f2ab3`.
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
| `Inputs and notation` | 87 | 1 | `HEADING_TEXT_MATCH` |
| `An individual-pair corridor` | 128 | 2 | `HEADING_TEXT_MATCH` |
| `One set for all small pairs` | 197 | 2 | `HEADING_TEXT_MATCH` |
| `Squarefree and periodic reassembly audit` | 280 | 3 | `HEADING_TEXT_MATCH` |
| `Actual-core scope versus the actual archive` | 310 | 3 | `HEADING_TEXT_MATCH` |
| `Claim boundary` | 337 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 377 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `108` before writing and `108` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `20`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `b8b22edd7f1e3efa171f7ceb3448fd9c053d49c37bfa3859ba793d868a95ff2b`.
- Source theorem/proof environment starts: proposition at TeX line 133, proof at TeX line 166, remark at TeX line 189, lemma at TeX line 202, proof at TeX line 215, theorem at TeX line 220, proof at TeX line 253, proposition at TeX line 282, proof at TeX line 297.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 65–72 | `e09df2f8ab6edcc13cf56d9bca58e7bad0861039ac1d70cbe0892ae67d2d5c76` |
| D02 | equation | 90–93 | `5c64edd832c86c2946b5ac636858348ea901a664dcf99b6c17c43148b6d194d2` |
| D03 | equation | 97–100 | `f615c016c483f5de7887317522b32b6655825852e9f3ca573475bd971b3cbbf3` |
| D04 | equation | 105–108 | `c6fea4f803ce6734be79109aa901cd3fc34503e9232148576a428ac4844c134f` |
| D05 | equation | 110–114 | `383b9689f262d7baa08127ab1da95faada80f11878d53920b6fc624681a3505c` |
| D06 | equation | 117–120 | `ab7073a1fffc99c89dbb8b032f0de86d1cd990fff68df079f84fc513a17071eb` |
| D07 | \[...\] | 138–140 | `b4e3faafbb5bcf4c8eab351d27b69e8e7c91ce26138a759dd02c9b864ae822de` |
| D08 | equation | 143–147 | `bfc9d06d677796451d3aa0299bfafb20c61431a8f826ad3cbd9d408386b21007` |
| D09 | \[...\] | 149–152 | `a5cd53252ea25fe49d82ff1e8b153210652c93d8e49f448e12d21aed56c978c9` |
| D10 | equation | 155–163 | `522358f42c18f4ca5a050f4379de905c80cae0787ff2f9bfa1c12d451a62d303` |
| D11 | \[...\] | 178–180 | `fcd271ae69c25245b66896c63beba2b9723de0a8680540e7f55d5e39bf833a9e` |
| D12 | equation | 205–211 | `6c63bc512ea743defc25f26a28da85ad3f39475c941fd2e9e819793a3940a693` |
| D13 | equation | 225–230 | `64bb74ed6c780b87defdf54b45fd2ae62b0fa15cc2180479c3188ff6f97b1918` |
| D14 | align | 232–238 | `afd59f904852e9912a205565b360299bbe68072d7cb54e6c0b0c06b156e953b1` |
| D15 | equation | 240–250 | `9e330e2a0d1ecd4b44fb1b9d50e851c02290cfa4db7645a914c4303e89980d07` |
| D16 | \[...\] | 255–257 | `532ee1ce1fa3cf21f0cc525a5bd3629349d1902c048c512ff12d44f1426e26b3` |
| D17 | \[...\] | 262–267 | `fe462f70bf0a7efddfc51125a10240c95103db94864b7763f1f0b18d71026565` |
| D18 | \[...\] | 316–319 | `2239925f3dc8656616b89d686f17b401b011e3229918ea29164ac01d2ef912fb` |
| D19 | \[...\] | 322–324 | `dce1fe2e39f0522268d75e3b1b1eae484bcff51eaa6bf45e8db221242f071c66` |
| D20 | \[...\] | 330–332 | `cd8465bfb2ec2d98760268c7abc6ab43e1078a381cd01ae7b23d1e37e14629d3` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 18: `pdfsubject={Uniform actual-core cancellation with bounded periodic data},`
- TeX line 36: `\newcommand{\OPEN}{\textnormal{\textsc{open}}}`
- TeX line 41: `\textbf{M\"obius Corridor: Uniform Actual-Core}\\`
- TeX line 58: `is a uniform theorem on the literal determinant-two M\"obius`
- TeX line 73: `uniformly for coprime odd \(a,s\), determinant \(su-ad=2\), and`
- TeX line 77: `uniform in residues and allowed moduli.`
- TeX line 84: `does not approach a prime-pair conclusion by itself.`
- TeX line 109: `and proves, uniformly for small-polylogarithmic \(c\),`
- TeX line 153: `then, uniformly in all integral \(d,u\) obeying \eqref{eq:fiber}`
- TeX line 184: `refined progression.  The source exceptional set is uniform in`
- TeX line 191: `representative modulo \(asR\).  Theorem~3.1 is uniform in that`
- TeX line 220: `\begin{theorem}[Uniform determinant-two M\"obius-periodic corridor]`
- TeX line 231: `for which the following is true.  Uniformly over all data satisfying`
- TeX line 276: `uniform in every allowed modulus and residue, and TPC-147 uses this`
- TeX line 307: `denominator is small enough.  It does not include a generic real`
- TeX line 313: `the determinant \(2\) are literal; it does not assert that every`
- TeX line 326: `not manufacture numerical affine data from the finite cut sample.`
- TeX line 347: `Uniform small-polylog periodic core theorem`
- TeX line 357: `\(\OPEN\).\\`
- TeX line 359: `\(\OPEN\).\\`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 4 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:fiber` → `../main.tex#L92` (existing project target or original TeX label line).
- Link relocation: `#eq:nonpret` → `../main.tex#L113` (existing project target or original TeX label line).
- Link relocation: `#eq:core` → `../main.tex#L119` (existing project target or original TeX label line).
- Link relocation: `#eq:pair-bound` → `../main.tex#L162` (existing project target or original TeX label line).
- Link relocation: `#prop:pair` → `../main.tex#L134` (existing project target or original TeX label line).
- Link relocation: `#prop:pair` → `../main.tex#L134` (existing project target or original TeX label line).
- Link relocation: `#lem:pairs` → `../main.tex#L203` (existing project target or original TeX label line).
- Link relocation: `#eq:pair-exception` → `../main.tex#L146` (existing project target or original TeX label line).
- Link relocation: `#eq:pair-bound` → `../main.tex#L162` (existing project target or original TeX label line).
- Link relocation: `#thm:main` → `../main.tex#L221` (existing project target or original TeX label line).
- Link relocation: `#eq:core` → `../main.tex#L119` (existing project target or original TeX label line).
- Link relocation: `#thm:main` → `../main.tex#L221` (existing project target or original TeX label line).
- Link relocation: `#eq:envelope` → `../main.tex#L237` (existing project target or original TeX label line).
- Link relocation: `#thm:main` → `../main.tex#L221` (existing project target or original TeX label line).
- Link relocation: `#eq:main` → `../main.tex#L249` (existing project target or original TeX label line).
