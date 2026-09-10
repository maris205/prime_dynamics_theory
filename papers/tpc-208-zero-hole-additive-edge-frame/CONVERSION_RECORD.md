# TPC-208 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `13748cc5c817bdd5138776f39a337842a23810c123057361ed658e775efc66cc`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `9fe4cfce7d63718540db155e7ab8fadee75733714653da7b743c705fe6e73d48`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `7ea43717febeed23c9fd0089390830b0a2038d12a25223f15bd2784704d5819d`; 10 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `6685ee9621db02d6ded7dbf409f5b3e077e42d27b1d1a0c46e31f640bff8cce1`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC205_209.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction and claim firewall` | 65 | 1 | `HEADING_TEXT_MATCH` |
| `The frozen zero-hole row` | 113 | 2 | `HEADING_TEXT_MATCH` |
| `Zero-hole projection in additive frequency` | 147 | 3 | `HEADING_TEXT_MATCH` |
| `The complete-graph tight frame` | 197 | 3 | `HEADING_TEXT_MATCH` |
| `Exact edgewise diagonal deletion` | 241 | 4 | `HEADING_TEXT_MATCH` |
| `Polarization and the physical kernel` | 314 | 5 | `HEADING_TEXT_MATCH` |
| `Oriented difference fibers and uniqueness` | 405 | 6 | `HEADING_TEXT_MATCH` |
| `Sharp falsifiers and mutation boundaries` | 463 | 7 | `HEADING_TEXT_MATCH` |
| `Equal/off-equal estimation is unstable` | 465 | 7 | `HEADING_TEXT_MATCH` |
| `One coefficient cancels cellwise` | 483 | 7 | `HEADING_TEXT_MATCH` |
| `Mandatory factors` | 490 | 7 | `HEADING_TEXT_MATCH` |
| `Source boundary and related analytic engines` | 508 | 7 | `HEADING_TEXT_MATCH` |
| `Exact computational certificate` | 553 | 8 | `HEADING_TEXT_MATCH` |
| `Route consequence and open theorem` | 588 | 9 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 631 | 9 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 647 | 10 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `169` before writing and `169` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `36`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `e8f0e258fcd8a34c0226cfd40eb52fc98b36e9320048c01974d56c92f0ba0ef5`.
- Source theorem/proof environment starts: theorem at TeX line 155, proof at TeX line 165, theorem at TeX line 211, proof at TeX line 223, lemma at TeX line 249, proof at TeX line 258, corollary at TeX line 285, proof at TeX line 302, proposition at TeX line 329, proof at TeX line 339, proposition at TeX line 375, proof at TeX line 394, theorem at TeX line 435, proof at TeX line 449.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 116–118 | `0c7be269c832608517c7e21be02e4c3bdb8cd40c5ade3c83f95e0a73a2eecb96` |
| D02 | equation | 121–124 | `c40c82af6da41f8419775afe35b1bfe8e60b740035eb0eac1a4b9e3b0f00c4e5` |
| D03 | equation | 127–131 | `c8bd48bb2d9db08fbb3f7c6c0ca07dddaf404dc9672ee81210b30c7ef51c9614` |
| D04 | equation | 133–136 | `781f7531a85fae3a1f9a784dcb3573e8f5b75652219f572738da34fd216e0f07` |
| D05 | equation | 140–143 | `3f97c9f8c09e8d0a376f348eef15d2e4338bed38a4be24aa1b2f4d906739035c` |
| D06 | equation | 150–153 | `5f9af89e7736fd4124f42f0195d3814090b10f9984c49778fc2cf594cc49ffcd` |
| D07 | equation | 158–160 | `7cf25aabb51ffd0053fe48b258ad878e7743f738c17dafe8881c7cf8825cfb8f` |
| D08 | equation | 170–173 | `22b9c6bfa4180cb20475672c5d1923f1bc3ad0de442c5babbaa292fa6c611402` |
| D09 | equation | 179–183 | `36ffa914f785198886fa884be1ea44bc08602e0f994839bea331df18e6345e74` |
| D10 | equation | 185–188 | `5a1dadfa816f416bc51234c6a48eb58b1ef4393b4971d51418cb2d7eac5b6993` |
| D11 | equation | 201–205 | `04944c18f107c7ad03d761fbdd6ede6eaf5ae37af7219462f273fc5783dca281` |
| D12 | equation | 207–209 | `291743b7b2593e159f73fd94e5c6b6d08d96bfb873550b3a3d1b29a55b678b4b` |
| D13 | equation | 213–218 | `fbc4cf813b5af206177baf0b29671270ac49ff272cabe5e785386288744320c7` |
| D14 | equation | 225–229 | `7bbc80080f7bb7dfaad36cae296f619e23446739afb909abdd5cdb9900f2d33f` |
| D15 | equation | 244–246 | `722a75015ea66386d559a4df2fcbc3833717d161daa74d8c8776c61161ae3ec4` |
| D16 | equation | 251–255 | `458b37633d82a37ee6eb80383d2b207fffee1564a0ebf6a9fbbc4e52ffb9d096` |
| D17 | align* | 264–268 | `1ad6048a820139fa6471ecf70fbee7baa6bb13d1dd2de531d735843044d0e3b2` |
| D18 | equation | 272–276 | `01007bb6ba45fe89bfaa37d8303ee917d27d9af62316d280ae6406c7666e4fb3` |
| D19 | equation | 278–283 | `1b252eab9b5ed81b7c3029d26a19f19250c78b29db0384c09fd4bc953981c778` |
| D20 | equation | 289–292 | `826f65a9d49f4bcc63a0944dc7378b3cc8f77ea5f455f6cd71b6480bb1e2b85d` |
| D21 | equation | 294–299 | `f05dd155fedbb376a28df07973b6a0ade1c0181e0775b3d7e52ec1ff6abe9391` |
| D22 | equation | 317–321 | `bbb10013fc356bd6834bff5fbc0a877abe70634f6b1f70ca700519d9f097bf1a` |
| D23 | equation | 323–327 | `e9eab17aeb1e2db10fd15d98e7ed28da55544ce63d5cdd5a7bb7b6cd64f2c45e` |
| D24 | equation | 332–336 | `c155d2ed9969f6bf197c68c620b6fdf9bbea40389c65693eaa6c4fd9bb32483f` |
| D25 | equation | 350–356 | `94f5c27676639e130828fce6559ee0911f27b9656954aa0b43829da52214a990` |
| D26 | equation | 362–365 | `61c91abb96834b24f6ce1b8136b44805de35c2e7c7f9bfeef075183626218239` |
| D27 | equation | 370–373 | `1d791133426f3166d1b1b6e58dbf021b0a1b2fca476711fb7666d2e46fc515ea` |
| D28 | equation | 377–385 | `eef5b2868129d6564bd87731958b3b9edb6e055eb5465a6fd3233eb687e59a59` |
| D29 | equation | 387–390 | `2f185c3ca5ba65347e1551e3e76e25fc3a6a242976d4165f37a152d6f768a382` |
| D30 | equation | 410–415 | `3b365bdc4ebefb99b86d238ebb3add44541049098b4166687740a9a1e1ad4af4` |
| D31 | equation | 417–420 | `c0c29ace2b2824c4008d04062089799b312706d8f664f9cc3a85f8467d7776fb` |
| D32 | equation | 422–427 | `03d56b073f2e212cdf5ce36d3ba64b71a71ff4082e11067a1411eae6173b591d` |
| D33 | equation | 437–440 | `872f5f474a72b08a29dbac057102915a36e33f6a28d05b63c940efa261567488` |
| D34 | equation | 442–444 | `3fa78da4c821512ded28fd10393f6aa6cb494114e5028f533813154ee363849a` |
| D35 | equation | 470–473 | `f3b1797085a68c4a994fe560959ecae1c8ea2fabe32394f2c956e0ad3cc1ef66` |
| D36 | equation | 474–477 | `5a8b317958f2f413ab1c2934e1b8f01315d1e46be81599dd181d04510596a9fd` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 60: `independent exact certificate checks 431 finite identities for`
- TeX line 62: `pre-emitter, not a Kloosterman attachment or a prime-shell power saving.`
- TeX line 106: `All four items are finite-dimensional identities proved for every prime`
- TeX line 107: `$q$ and every finitely supported complex sequence.  They do not estimate the`
- TeX line 108: `edge cells.  In particular, the paper does not prove a prime-only`
- TeX line 119: `Let $a=(a_n)$ be a finitely supported complex sequence, let $H>0$, and let`
- TeX line 156: `For every prime $q$, every finitely supported complex sequence $a$, and every`
- TeX line 237: `not a power saving and does not permit a triangle inequality over the edge`
- TeX line 316: `For two finitely supported sequences $\beta,w$, define the bilinear edge cell`
- TeX line 506: `the physical signs and normalization; it does not supply arithmetic evidence.`
- TeX line 518: `leads to a zero-hole variance.  The source does not state`
- TeX line 519: `\eqref{eq:physical-scalar}, verify its hypotheses uniformly for the four`
- TeX line 539: `Here those hypotheses are precisely part of the open compiler.  The source is`
- TeX line 544: `The complete-graph Laplacian identity is standard finite-dimensional linear`
- TeX line 548: `does not prove literature-wide novelty.  The claim made here is narrower: the`
- TeX line 582: `assertions, reject duplicate JSON keys and nonfinite values at their trust`
- TeX line 585: `mutations.  The proofs in Sections 3--7, not the finite table, establish the`
- TeX line 588: `\section{Route consequence and open theorem}`
- TeX line 606: `Whole-frame Poisson/Kloosterman emission & \texttt{OPEN}\\`
- TeX line 607: `Prime-shell fixed saving greater than $1/400$ & \texttt{OPEN / UNPAID}\\`
- TeX line 616: `\textbf{Open collective compiler.}`

## Conversion limitations

- 5 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:projection-identity` → `main.tex#L158` (existing project target or original TeX label line).
- Link relocation: `#eq:leave-one-out` → `main.tex#L170` (existing project target or original TeX label line).
- Link relocation: `#eq:projection-identity` → `main.tex#L158` (existing project target or original TeX label line).
- Link relocation: `#thm:projection` → `main.tex#L155` (existing project target or original TeX label line).
- Link relocation: `#thm:projection` → `main.tex#L155` (existing project target or original TeX label line).
- Link relocation: `#eq:laplacian` → `main.tex#L207` (existing project target or original TeX label line).
- Link relocation: `#thm:projection` → `main.tex#L155` (existing project target or original TeX label line).
- Link relocation: `#eq:edge-frame` → `main.tex#L213` (existing project target or original TeX label line).
- Link relocation: `#thm:edge-frame` → `main.tex#L211` (existing project target or original TeX label line).
- Link relocation: `#sec:uniqueness` → `main.tex#L406` (existing project target or original TeX label line).
- Link relocation: `#eq:zero-residue-annihilation` → `main.tex#L244` (existing project target or original TeX label line).
- Link relocation: `#eq:diagonal-remainder` → `main.tex#L133` (existing project target or original TeX label line).
- Link relocation: `#eq:edge-diagonal` → `main.tex#L272` (existing project target or original TeX label line).
- Link relocation: `#lem:edge-mass` → `main.tex#L249` (existing project target or original TeX label line).
- Link relocation: `#thm:edge-frame` → `main.tex#L211` (existing project target or original TeX label line).
- Link relocation: `#cor:edge-compiler` → `main.tex#L286` (existing project target or original TeX label line).
- Link relocation: `#eq:edge-polarization` → `main.tex#L332` (existing project target or original TeX label line).
- Link relocation: `#cor:edge-compiler` → `main.tex#L286` (existing project target or original TeX label line).
- Link relocation: `#eq:physical-scalar` → `main.tex#L350` (existing project target or original TeX label line).
- Link relocation: `#eq:pre-emitter` → `main.tex#L362` (existing project target or original TeX label line).
- Link relocation: `#eq:physical-scalar` → `main.tex#L350` (existing project target or original TeX label line).
- Link relocation: `#eq:laplacian` → `main.tex#L207` (existing project target or original TeX label line).
- Link relocation: `#lem:edge-mass` → `main.tex#L249` (existing project target or original TeX label line).
- Link relocation: `#eq:literal-crosswalk` → `main.tex#L387` (existing project target or original TeX label line).
- Link relocation: `#eq:physical-scalar` → `main.tex#L350` (existing project target or original TeX label line).
- Link relocation: `#eq:difference-fiber` → `main.tex#L417` (existing project target or original TeX label line).
- Link relocation: `#eq:weighted-edge-decomposition` → `main.tex#L437` (existing project target or original TeX label line).
- Link relocation: `#thm:no-sparsification` → `main.tex#L435` (existing project target or original TeX label line).
- Link relocation: `#eq:projection-expanded` → `main.tex#L185` (existing project target or original TeX label line).
- Link relocation: `#thm:edge-frame` → `main.tex#L211` (existing project target or original TeX label line).
- Link relocation: `#eq:projection-expanded` → `main.tex#L185` (existing project target or original TeX label line).
- Link relocation: `#thm:no-sparsification` → `main.tex#L435` (existing project target or original TeX label line).
- Link relocation: `#eq:physical-scalar` → `main.tex#L350` (existing project target or original TeX label line).
- Link relocation: `#eq:pre-emitter` → `main.tex#L362` (existing project target or original TeX label line).
- Link relocation: `#eq:pre-emitter` → `main.tex#L362` (existing project target or original TeX label line).
- Link relocation: `#tab:status` → `main.tex#L596` (existing project target or original TeX label line).
- Link relocation: `#eq:oriented-physical-scalar` → `main.tex#L422` (existing project target or original TeX label line).
- Link relocation: `#thm:no-sparsification` → `main.tex#L435` (existing project target or original TeX label line).
