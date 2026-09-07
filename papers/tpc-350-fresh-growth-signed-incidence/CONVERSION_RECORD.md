# TPC-350 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `8f01227e0d63749f6e9df9b016708efd8e3b5c62e8d0603d0397f73d3a72f4a7`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `39b3e853901939784d0c8600c0b6ef3fff7074c3f025add6b954e16491d94be6`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `9b550619026a1682697290440d109c08ca89c86edfb1172d4ac0a4229d629918`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 46 | 1 | `HEADING_TEXT_MATCH` |
| `The literal masked matrix` | 61 | 1 | `HEADING_TEXT_MATCH` |
| `Exact incidence interface` | 82 | 2 | `HEADING_TEXT_MATCH` |
| `Frozen fresh-growth protocol` | 143 | 2 | `HEADING_TEXT_MATCH` |
| `Finite results` | 164 | 3 | `HEADING_TEXT_MATCH` |
| `Exact fresh anchor` | 214 | 3 | `HEADING_TEXT_MATCH` |
| `Adversarial validation and claim boundary` | 232 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion and next question` | 247 | 4 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 261 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `73` before writing and `73` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `9`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `ba48e3d3988d72159e394b681536e211af4dece6aafc66071aab0f4690438c72`.
- Source theorem/proof environment starts: proposition at TeX line 101, proof at TeX line 105, proposition at TeX line 110, proof at TeX line 118, theorem at TeX line 123, proof at TeX line 131, remark at TeX line 137.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | align* | 67–71 | `3f09ae4d647d23bcd499ea312342ead499d72c55d6e0fca938e56d27bae2cf20` |
| D02 | \[...\] | 75–80 | `b6215eff8a01b712eb737184b873219f80681be5375032f32a9f05e707dd7453` |
| D03 | \[...\] | 86–92 | `399132d8bb19b7aa44067fee317795df9e95c9a2bc1b6b563d40edcefae23a62` |
| D04 | \[...\] | 94–96 | `99449e844d3f97905734ca1f03525e1977266fc820f6c3c8dc2c196370781201` |
| D05 | equation | 112–116 | `22587787c591c0a00b72a244ba36a8dfbb36ebc76d668cda8dd8e14f01c88faa` |
| D06 | equation | 125–129 | `7521753468e02586c3bad580cc50b3fb520e195259f5687f42e932a13e52c9f9` |
| D07 | \[...\] | 147–151 | `92678523c0f159c433a83fcf6d40cf81543e7fbd10b92340f11e648e508b134e` |
| D08 | \[...\] | 218–221 | `7527221a8bb8c6ac828c22b2acd8af1fe5948f44eb0421b8c6c27ace025d9575` |
| D09 | \[...\] | 223–227 | `cf7f7228e33aea3366f5d23e7252ba66507f4577d2b2a60f89a9a9ea6678a4b1` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 29: `We test the finite prime-balanced incidence witness introduced in TPC-349 on`
- TeX line 41: `replication is positive finite evidence, while a universal quarter-floor and`
- TeX line 42: `monotonic growth law are refuted on the declared panel.  No arithmetic`
- TeX line 49: `zero-sum contrast of prime divisibility incidences.  Its finite panel showed`
- TeX line 53: `the finite floor.`
- TeX line 55: `We answer this question only on a locked finite panel.  The term ''growth''`
- TeX line 56: `below means the four lengths $M=256,512,1024,2048$; it does not mean a limit as`
- TeX line 57: `$M\to\infty$.  Likewise, the shell ladder $Q=36,80,128,256$ is a finite`
- TeX line 59: `claim, a source-uniform arithmetic estimate, or a theorem about twin primes.`
- TeX line 66: `and ideal finite matrices are`
- TeX line 73: `They are distinct from the test coefficients introduced next.  The finite`
- TeX line 98: `position; it is not an owner-class partition.  If $b_I\ne0$, write`
- TeX line 111: `For every finite matrix $D_I$,`
- TeX line 119: `Substitute the finite sum defining $b_I$, apply linearity, and expand the`
- TeX line 139: `cross-prime terms.  The theorem is a finite linear-algebra statement and does`
- TeX line 164: `\section{Finite results}`
- TeX line 169: `\caption{TPC-350 finite fresh-growth and shell-scale audit.}`
- TeX line 173: `Quantity & Certified finite readout\\`
- TeX line 193: `interface is not an artifact of the two parent origins.  The finite floor is`
- TeX line 210: `does not say that every larger shell fails, nor does it prove decay.  Along`
- TeX line 212: `is descriptive and is not a monotonicity theorem.`
- TeX line 230: `not an exclusive owner assignment.`
- TeX line 241: `These checks establish finite package integrity.  They do not establish a`
- TeX line 242: `source-uniform arithmetic $L^2$ estimate, a uniformly bounded physical masked`
- TeX line 250: `survives all three fresh origins and all four finite lengths with positive`
- TeX line 253: `structure is a fresh finite lower-witness interface, while the obstruction is`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:lower` → `main.tex#L128` (existing project target or original TeX label line).
- Link relocation: `#eq:gram` → `main.tex#L115` (existing project target or original TeX label line).
