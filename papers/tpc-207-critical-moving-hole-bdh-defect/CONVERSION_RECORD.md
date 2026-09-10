# TPC-207 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `ad29a66dcfadbcf9b662b8d74bf3305bde8ff1f462130f939a6ba8cb9ddb6658`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `360981e61bf8b7765bb6f2d2cd7b23e92cf61029bba5f922d1887e2b31678a4a`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `cfa6fe55c3a36ff1bb12274001dd6060bf0e611b74bbcc0dae1f2eaacaaaa58e`; 9 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `2f04d89255cb54cf48f4159e7c2a27ca4355c482b971d9a2b749dc27ca07dab7`.
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
| `Introduction and claim firewall` | 66 | 1 | `HEADING_TEXT_MATCH` |
| `Reduced-residue BDH rows` | 98 | 2 | `HEADING_TEXT_MATCH` |
| `The moving-hole projector theorem` | 128 | 2 | `HEADING_TEXT_MATCH` |
| `Sharp rank-two spectrum and obstruction` | 169 | 3 | `HEADING_TEXT_MATCH` |
| `Exact diagonal-subtracted lift` | 212 | 4 | `HEADING_TEXT_MATCH` |
| `Translation and four-packet polarization` | 248 | 4 | `HEADING_TEXT_MATCH` |
| `Critical deterministic block bound` | 314 | 5 | `HEADING_TEXT_MATCH` |
| `The V59 critical scale` | 401 | 7 | `HEADING_TEXT_MATCH` |
| `Source boundary` | 429 | 7 | `HEADING_TEXT_MATCH` |
| `Executable exact certificate` | 456 | 8 | `HEADING_TEXT_MATCH` |
| `Limitations and open theorem` | 475 | 8 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 509 | 9 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `170` before writing and `170` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `42`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `f65e6d986e224161f0b98589cb9ea871ee165cd7629110179366bcd8f7366bd9`.
- Source theorem/proof environment starts: theorem at TeX line 130, proof at TeX line 142, proposition at TeX line 171, proof at TeX line 185, theorem at TeX line 214, proof at TeX line 226, theorem at TeX line 335, proof at TeX line 347, remark at TeX line 394.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 53–55 | `8b88b03a83aa54983e3d2f2bda46cc9ba496a8e69f3b76043ed009f46a2b1976` |
| D02 | align* | 84–93 | `513a41cba561485aa8fc21c3a4e3a1cf0c05edf33b7e2f04fb628951059b4896` |
| D03 | \[...\] | 101–105 | `fa07e9131ecc7d45748a497b78d1ff8ac9290183a320961cdd5eccdaff524dab` |
| D04 | \[...\] | 107–111 | `e42e1cd017551ba84e6f3601f2cb500a55402a569fc9972f76b7e6e8bbc154aa` |
| D05 | equation | 119–123 | `4428ce6ce00011931109522e5c70a00a13181ea31b247c5b0dce44dad88962a2` |
| D06 | equation | 132–134 | `7458035c9a2d9386a786f6f3fb6a335f73b12b6e85988c87d6b91e3d4fb921ea` |
| D07 | equation | 136–139 | `a136a6f8d48689a82e053d2939b1b21a1ba9a871169892d9cb227ef54a72a2bf` |
| D08 | \[...\] | 144–146 | `dae3a09a2b12db67d7c926a2f092bf8963dbb4639f29c003826dd1b362a73f5d` |
| D09 | align* | 149–155 | `5ef64bc99e3f4bdb44c9bdfe3c7b691bee866d4da77cca48aded52c8f2d91f97` |
| D10 | \[...\] | 160–162 | `af10e954ce996977e7b4a4a55d67bd78ea7849a7fc938b924d1903be4196d6e2` |
| D11 | equation | 165–167 | `4b4929eb8cd5c4a9d215fb16f313f224f4a784d9bac6be874fc568f1ca6bb06b` |
| D12 | \[...\] | 173–175 | `b968ca274eb658bcec07e0f14c74b751518e243c962b343654d8b24625492a89` |
| D13 | equation | 177–181 | `81f8d92599c4cea7238b7eaf86c493080a71b3cf043b50121acecb442d501b80` |
| D14 | \[...\] | 187–189 | `c37f65b2755f4200e9ba4f8575d48fc1ddfd88e35b7c909ede0b5d3ca96679ef` |
| D15 | \[...\] | 198–200 | `369a02eb710bc9ee29ccadff584d3b2a2857d19ad66a4d15fddb2ee29f53501a` |
| D16 | \[...\] | 206–208 | `8f00a4f116f5b7cf9d8a8b377c4e7b6cf2850f38b007aebd34160f0f874e0a99` |
| D17 | equation | 216–221 | `b160f3aadeb9b8d466b58e9395d631fdfa7135a1c8cf1054d73563ac70fe26b0` |
| D18 | \[...\] | 229–232 | `4cf7fb9ec7a27e182b5cba24cb50124773d47981c1ddcba3f88b752c4a8f8d0b` |
| D19 | \[...\] | 238–240 | `d29f072ffed88d7bc4ee2700415fc2c0985e8cbbf8682855e7b655880c82359d` |
| D20 | equation | 242–244 | `fdce16ad384130516517f2b31948708ed6459def4eacabf511b9595e52645c4e` |
| D21 | equation | 251–253 | `b243fa76dc7afb9a2145fae8b6a5ac51a1b7880cb9b4d2499025e8552c86b70a` |
| D22 | equation | 255–257 | `65ec6e69720b63bc2abaa965d7c12193f244eee1e48d2abe06ee66a371c831a6` |
| D23 | \[...\] | 259–261 | `01043fca17c4920b4c9e76bf02d1938e4a3b0bb1fa05b91b195811f830260adc` |
| D24 | equation | 266–268 | `ef4540924ce6fdad2c16c57b47b09c6d6ef7b48aa48cbc2fa779ca6ddd191420` |
| D25 | \[...\] | 273–277 | `153d7374cc48805e7daffc69e5281cec2bca5d7a99b5cf7b591cc4390a5c13be` |
| D26 | \[...\] | 280–282 | `30869465d85ef1b19ddf6fa298b5ec3b5b073c14ee18707134976fa70b878bbb` |
| D27 | align | 285–294 | `405d81893a6cf82834777ee420adee1b2eb5bba60d72d029302bb7bb466aa2c7` |
| D28 | equation | 303–306 | `cd720e1a3d1807a9f2dfe368a4a507a55ea133296524c71ce0b50fd553e65ccf` |
| D29 | \[...\] | 321–324 | `3dd7bf38975685483718953759e5d0cab632122fce1e62065ece8b878ad20c76` |
| D30 | equation | 327–329 | `42d53907142e1b16f0462df20e0fbf7d79dc6b5e29482be1b9ce64f98116f3a1` |
| D31 | equation | 338–342 | `cd4a7945ae5122e406562f28ac66b3bfa281d6505cefc27aae270ee7042427b5` |
| D32 | \[...\] | 349–351 | `bcc36cee0470ffcd8d36db472ff43d287f0f239e9fa65274b0b9571e392900e4` |
| D33 | equation | 353–355 | `1a3d1d53c7737cab4106bb129252215d39586fb598bc10278b8fe7ad9f4ccadd` |
| D34 | \[...\] | 364–368 | `0c9ab0ee011e9d6c1f279145df872a37bdd4430cae9db9dc58327bd7aef09b6f` |
| D35 | \[...\] | 371–373 | `dd844383e875351a64b035efe7ef0666457667d9c7a1a4065a926c97527e38bb` |
| D36 | align* | 375–382 | `efa7744fb89878b01aa6d2337789af31ceceada46ab2c3f827503847b8a26fea` |
| D37 | \[...\] | 387–390 | `58f805cf6c78f8dcbf29eea8528ef529a4e2c7daf873669eb3f93ca6d32089c7` |
| D38 | \[...\] | 404–407 | `bc00255c5c2b4fab5f4abe53002ff127725b0d71fb8995d201a7cf213cbf36b4` |
| D39 | align* | 409–413 | `d53fe4ebf2b9dbb364e8772b4d61a961bd1e618ef02293c5b55732012ea21829` |
| D40 | equation | 415–417 | `fa92076f6516202dc8ff5d21f9b6282ce81635fecd5a81ac732b688a5f968aa2` |
| D41 | equation | 421–423 | `940640802ce5b6bccea154d86f9bbf6531d7b5092b9f04198731729cb5e26f8d` |
| D42 | align* | 478–483 | `6057606a04deb92fb754ba960fa3f5094e1b70412016e0fbd937d1cb892e7ec9` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 76: `The answer has two parts.  First, a finite-dimensional projector identity`
- TeX line 79: `kernel localization and block geometry, rather than finite rank, yield the`
- TeX line 201: `Thus finite rank gives no asymptotic saving.  This is a sharp obstruction to`
- TeX line 312: `$F_{h_q}-F_0$ does not disappear from \eqref{eq:Mbc}.`
- TeX line 320: `a Schwartz tail.  Assume`
- TeX line 325: `The frequency integral is assumed to produce a kernel $K_H(m-n)$ satisfying,`
- TeX line 332: `term we assume the usual bounded-overlap property: $I_b\cap I_c$ is empty`
- TeX line 356: `uniformly in $r$.  Indeed, the residue class occurs $O(H/q+1)$ times and the`
- TeX line 362: `\eqref{eq:kernel} and \eqref{eq:l1-selector} therefore give, uniformly in the`
- TeX line 396: `has produced the complete ordered-pair defect $M_{bc}$.  It does not apply`
- TeX line 425: `This payment is local to the translation correction.  It does not estimate`
- TeX line 439: `The source does not, however, prove the object still required by V59:`
- TeX line 445: `\item the required input hypotheses must hold uniformly in block and`
- TeX line 453: `mismatch is no longer a fatal obstruction, but Harper is not a direct theorem`
- TeX line 471: `produce identical output.  These finite checks are quality assurance and`
- TeX line 475: `\section{Limitations and open theorem}`
- TeX line 486: `rank-two operator norm tends to one, so no saving is available from finite`
- TeX line 493: `the four literal V59 packets, uniformly over blocks and frequencies, and`
- TeX line 500: `Kloosterman-cell interface.  That arithmetic step remains open.`

## Conversion limitations

- 3 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:hole-difference` → `main.tex#L136` (existing project target or original TeX label line).
- Link relocation: `#thm:moving-hole` → `main.tex#L130` (existing project target or original TeX label line).
- Link relocation: `#eq:spectrum` → `main.tex#L177` (existing project target or original TeX label line).
- Link relocation: `#eq:remainder` → `main.tex#L119` (existing project target or original TeX label line).
- Link relocation: `#eq:diagonal-lift` → `main.tex#L216` (existing project target or original TeX label line).
- Link relocation: `#eq:hole-difference` → `main.tex#L136` (existing project target or original TeX label line).
- Link relocation: `#thm:diagonal` → `main.tex#L214` (existing project target or original TeX label line).
- Link relocation: `#eq:Mbc` → `main.tex#L293` (existing project target or original TeX label line).
- Link relocation: `#eq:Mbc` → `main.tex#L293` (existing project target or original TeX label line).
- Link relocation: `#eq:Mbc` → `main.tex#L293` (existing project target or original TeX label line).
- Link relocation: `#eq:Mbc` → `main.tex#L293` (existing project target or original TeX label line).
- Link relocation: `#eq:Mbc` → `main.tex#L293` (existing project target or original TeX label line).
- Link relocation: `#eq:kernel` → `main.tex#L327` (existing project target or original TeX label line).
- Link relocation: `#eq:l1-selector` → `main.tex#L353` (existing project target or original TeX label line).
- Link relocation: `#eq:Mbc` → `main.tex#L293` (existing project target or original TeX label line).
- Link relocation: `#eq:block-bound` → `main.tex#L338` (existing project target or original TeX label line).
- Link relocation: `#thm:block` → `main.tex#L335` (existing project target or original TeX label line).
- Link relocation: `#thm:moving-hole` → `main.tex#L130` (existing project target or original TeX label line).
- Link relocation: `#eq:q5-fixture` → `main.tex#L242` (existing project target or original TeX label line).
- Link relocation: `#eq:critical-clock` → `main.tex#L415` (existing project target or original TeX label line).
- Link relocation: `#eq:dft-selector` → `main.tex#L303` (existing project target or original TeX label line).
