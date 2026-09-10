# TPC-144 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `4031a43e39039c61f51803d48a63ee94b7ac536cc1205c164d7dc1622efc52c9`.
- Bibliography: [references.bib](references.bib), SHA-256 `c46c27698ccedf1ac7190e41824a45f09effee08090c9d0015b285ff11c20d05`.
- Preserved PDF: [tpc-144-determinant-zero-quotient-kernel-test.pdf](tpc-144-determinant-zero-quotient-kernel-test.pdf), SHA-256 `23ece6645652ba97730d1cab3f701d8c87f656487e68414494205d0907aa49f4`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `a595cb8890e9d710f1edb7c8f16a0296d64aad8e8c5ec2841ef90e35467f7f8a`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC143_146.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Two quotients, one literal domain` | 75 | 1 | `HEADING_TEXT_MATCH` |
| `The quotient-kernel criterion` | 128 | 2 | `HEADING_TEXT_MATCH` |
| `Why scalar equality is insufficient` | 210 | 3 | `HEADING_TEXT_MATCH` |
| `Exact field requirements` | 257 | 3 | `HEADING_TEXT_MATCH` |
| `Executable theorem and actual verdict` | 308 | 4 | `HEADING_TEXT_MATCH` |
| `Claim boundary` | 350 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 377 | 5 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `86` before writing and `86` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `18`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `cf9c2b1f14e56c3e5173a0290df3a8208ca1f85b4c7e293b5aeb7e10869c1894`.
- Source theorem/proof environment starts: definition at TeX line 109, theorem at TeX line 130, proof at TeX line 149, corollary at TeX line 164, proof at TeX line 171, remark at TeX line 176, proposition at TeX line 184, proof at TeX line 198, proposition at TeX line 212, proof at TeX line 222, proposition at TeX line 289, proof at TeX line 297, theorem at TeX line 352.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 87–89 | `171a421d131376cee5a6a369a27aeaebcb6f50d9da0b822bd49be11ef16e5e99` |
| D02 | equation | 91–94 | `5fe0d331747dc94a25f033c91006644ee0ad402502a79f1c0cb6e85d648adbec` |
| D03 | \[...\] | 100–102 | `20609e910b9fe1b0d4be7425568184f78458766c03a8fac67b43eaa95a864e46` |
| D04 | \[...\] | 111–113 | `812d9431652b01e901e540a3d88f869b6e7d8d484e737cd1979d00124e04e65a` |
| D05 | \[...\] | 116–118 | `f9f39bb3c809f135aa7c8cebe79a1dcae60e19ec657ad786d5a20766fdb8ea4a` |
| D06 | \[...\] | 133–135 | `019dcd18eafdd950fc485739de7865cd5f44b035436b6de08c1b37f644c9dfc2` |
| D07 | equation | 138–141 | `4e574046140769d4808ec86f8838199687737c9c93dc87882cdc542d626b68b5` |
| D08 | equation | 143–146 | `3c5325072c7bebecb46ce06432c49a0c6f93b93f0b04541a85cdba489ab054fe` |
| D09 | \[...\] | 151–153 | `3fb10c18a8302fa3221c56e511c2e499773443ade58179882d920a9997c013d1` |
| D10 | \[...\] | 155–157 | `d22dc9b9bdf92891a04937f184e785965fb2825adf1da2c2bc1acc61d160d85d` |
| D11 | \[...\] | 190–192 | `6158eb2ac62be265d2e2d2a369d234d317e15f5e60edb79e2777211e93f492e0` |
| D12 | \[...\] | 202–205 | `6055761f56f41680413adcc84809bdcd6509a9c44c6a7e6d2b7241c39002b479` |
| D13 | \[...\] | 215–218 | `3aeac0e89c9b0d72952c7322d38504bc53f04ed22408b7743f7ce0d4337e6de5` |
| D14 | \[...\] | 224–228 | `23cccd2599a3768429dca59f5a45c20ef5674cf804535998e78c9c89b596d4e6` |
| D15 | \[...\] | 231–234 | `7d529ca13b59aa78725d6b4092e64fb6cf3bdedb9ed348bf2fe46ba8a294d65f` |
| D16 | \[...\] | 246–250 | `3261993f990f3d8c4f52e96ae95aa7dedd29f0e19e792107ca79918988445c6d` |
| D17 | \[...\] | 344–347 | `909720db48f28d2e6fe7e4d3430f5d9953a449a37175be820be67b74cbb6bfab` |
| D18 | \[...\] | 354–361 | `9b52d519b01a5017fdc1b81a4b26d73e9eaf1f853a761c79ca580e3879fc3018` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 56: `simultaneous-lift criterion.  For finite surjective maps \(Q_D,Q_Z\)`
- TeX line 62: `one final scalar sum, does not imply this criterion.  Applying the`
- TeX line 78: `on all nonsoft cut paths.  This includes both eligible-tail-open and`
- TeX line 88: `x_t=m_\alpha j+h_0,\qquad y_t=m_\gamma j+h_0,`
- TeX line 124: `edge multiplier is not a quotient implementation.  A zero literal`
- TeX line 132: `Let \(H,K_D,K_Z\) be finite-dimensional vector spaces and let`
- TeX line 172: `For a finite matrix \(A\), the row space is the annihilator of`
- TeX line 195: `Kernel equality alone does not imply this condition.`
- TeX line 206: `Both kernels are zero, but the rows of \(Q_Z\) are not a permutation`
- TeX line 241: `does not determine which occurrences were identified.  If \(M\) is`
- TeX line 285: `In particular, recording \(u_t\) does not prove phase coherence, and`
- TeX line 286: `recording \(\sigma_{\theta,i}\) does not prove a signed-prefix saving`
- TeX line 300: `cut type, \(h_0\) and normalization.  They contain none of the`
- TeX line 303: `objects in an earlier paper is not a path-ID crosswalk.  Thus the`
- TeX line 312: `rational row reduction.  Synthetic matrices verify`
- TeX line 315: `\texttt{SYNTHETIC\_L0\_ONLY}.  A separate actual manifest imports the`
- TeX line 327: `& \(\PROVED_{\Lzero}\) & Exact finite-dimensional theorem.\\`
- TeX line 335: `& \(\STOP\) & Scoped stop; augmented lift remains open.\\`
- TeX line 348: `even though the current finite sample has no eligible-tail row.`
- TeX line 369: `fixed-\(h_0\) \(\Ltwo\) saving, pays the \(1/400\) endpoint, or proves`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 4 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:intertwine` → `../main.tex#L140` (existing project target or original TeX label line).
- Link relocation: `#eq:kernels` → `../main.tex#L145` (existing project target or original TeX label line).
- Link relocation: `#eq:kernels` → `../main.tex#L145` (existing project target or original TeX label line).
- Link relocation: `#thm:kernel` → `../main.tex#L131` (existing project target or original TeX label line).
- Link relocation: `#thm:kernel` → `../main.tex#L131` (existing project target or original TeX label line).
- Link relocation: `#eq:detlabel` → `../main.tex#L93` (existing project target or original TeX label line).
- Link relocation: `#thm:kernel` → `../main.tex#L131` (existing project target or original TeX label line).
- Link relocation: `#prop:literal-relabel` → `../main.tex#L185` (existing project target or original TeX label line).
- Link relocation: `#prop:scalar` → `../main.tex#L213` (existing project target or original TeX label line).
