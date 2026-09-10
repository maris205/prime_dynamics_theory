# TPC-209 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `a2843110ec4434ba69989d599e5b4283b44dd8b12e4c57e75bcec57cc6cfa06f`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `4ae8a89748da3ee1f17044c16f3a68a16e71fd40d7f5f81ba65c4104be139a7d`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `6f545a45e203cf1bce4a540f79a0d0171f02e2022a249da83ff0fd47480607e0`; 7 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `38fe37c69e83ca3828bbc26314bff6050efacc6915c6c553951294b066caf0eb`.
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
| `Introduction and claim ceiling` | 64 | 1 | `HEADING_TEXT_MATCH` |
| `The frozen additive frame` | 103 | 2 | `HEADING_TEXT_MATCH` |
| `Poisson reindexing at one divisor` | 141 | 2 | `HEADING_TEXT_MATCH` |
| `The whole-frame vector compiler` | 195 | 3 | `HEADING_TEXT_MATCH` |
| `Shared-character profile normal form` | 234 | 4 | `HEADING_TEXT_MATCH` |
| `Gauss crosswalk to the previous interface` | 272 | 4 | `HEADING_TEXT_MATCH` |
| `Sharp alignment obstruction` | 310 | 5 | `HEADING_TEXT_MATCH` |
| `Common-profile resonance and finite validation` | 355 | 5 | `HEADING_TEXT_MATCH` |
| `Source boundary and route decision` | 405 | 6 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 438 | 6 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 459 | 7 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `110` before writing and `110` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `28`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `b39ca24e696d9e7b24e4597272f57b444d5e7a80c52be98ec51d7cecbcb5a8ae`.
- Source theorem/proof environment starts: theorem at TeX line 156, proof at TeX line 179, proposition at TeX line 206, proof at TeX line 224, theorem at TeX line 250, proof at TeX line 262, proposition at TeX line 280, proof at TeX line 292, theorem at TeX line 314, proof at TeX line 330.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 106–110 | `4cf6c0562e0716de29cd65e9839950cc144bafdb43ac45e4afdaaaf74396633a` |
| D02 | \[...\] | 113–117 | `1da1bb4985676274a56aef227dc75b61e7a20226f7457411ffcf67edeb627acd` |
| D03 | \[...\] | 119–122 | `5b6773aa8b75f603ea77ec3263a93bb8ed898c833b024d5365e54d6dd39d599a` |
| D04 | \[...\] | 124–127 | `3e109bb7f14b19760ee7f8f4dba677965c986534ca514e07266909c044abf34c` |
| D05 | \[...\] | 129–134 | `5acb8d22f90c45c4d34f2c46493a1b3015ff290d473d3d6add3b7dd80db5aa60` |
| D06 | \[...\] | 145–149 | `d2e6224c0de96529cf6cb1ccb62f62e034b3044b01a70000cdee0c0d01bd146e` |
| D07 | \[...\] | 151–154 | `ce020140f710879e190f6a52cc2e1f0c97007ba74ac4760346ecbd03dfe4abb7` |
| D08 | \[...\] | 159–164 | `5462d6d6ff9b3a6d9d355a74faf0caea5d5d7f0006447853e27f7dea4f2f6479` |
| D09 | \[...\] | 167–171 | `eee158f569f4480a8bfbe915e8aaa8cddcb7b75aef61b77b3c925cd4f5e83240` |
| D10 | \[...\] | 173–176 | `bf9b2600ef20b6424f9fd866c1ae76fd2029f089eaeb62e49e319853dadb0a2f` |
| D11 | \[...\] | 184–187 | `bc55616af8f7d7c27f06dd24dde118da0d46a45188100d066d19cbcb6621d64f` |
| D12 | \[...\] | 199–204 | `aa69db37104e98dff37d04368f7a8a258ec6ee0a319223ea7c59fdf582c5de16` |
| D13 | \[...\] | 209–214 | `cb3bd9c590aa4e22656830c03c655d0b6fefec3e60209dc4baebd8ef73a1f97a` |
| D14 | \[...\] | 217–221 | `5c1090f88e8c2fb4c5cbed7de154a216dea0a3135bf54c2054c8a45caa360d1d` |
| D15 | \[...\] | 238–241 | `4e871744942e0f34948d0acf9769646c0d003e288be8d08f92ad43922b4b7e6b` |
| D16 | \[...\] | 243–246 | `c9d6711ed001662db865d861366e23d41a55b2c2465f8e9251497090abfede15` |
| D17 | \[...\] | 253–259 | `9c365fa67a918446071f46d19b2f75f32d67b0585c8febdb583fb223d3107601` |
| D18 | \[...\] | 275–278 | `88045f41606ffa6a090535308fcd8e92792456bc462a3c1e2caad559efa14441` |
| D19 | \[...\] | 283–289 | `23673c7e7616c3ad89257034faacb5c3bd88ba085785006f735065c0671f44f1` |
| D20 | \[...\] | 295–298 | `8b453f0d5352ac8f3328c79b791660af40b5f45163a3eb1a80e9051370116771` |
| D21 | \[...\] | 317–321 | `aa65ffb5bfd18fbf445b5418447e18d124858edf2b0a4ab74f8959c5cc367e21` |
| D22 | \[...\] | 323–326 | `f5e77b1c7b7f4dbea1eae0bc724d6c828e43fe76d48b962c904260f1fc1e53fe` |
| D23 | \[...\] | 332–334 | `abae1a9cfd94c67872e47ca0159db4d00d4670e82a480490fe0e3f73f328e951` |
| D24 | \[...\] | 336–339 | `0bb963718deca77ada646d4b99d7afec51d3f10709ea2b31c55a6601ee31e6fc` |
| D25 | \[...\] | 341–343 | `424dad10dbe4d95d916f6710deb5b7198b2c367f7866d91b908b90a92f1931b7` |
| D26 | \[...\] | 359–365 | `2f098ebe77d4b54bedc3a454fad21321e9d69586ec2e05fe945262fab1431a69` |
| D27 | \[...\] | 423–430 | `51b348f0ba38c2583c186768c9bf0423c2a5765f6b57f516626b44207035bd81` |
| D28 | \[...\] | 452–456 | `5e14467a7d46b742c080198f388143bb897564420ef6620b67d84212aae8b91d` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 61: `the strict $1/400$ gate, and the twin-prime endpoint remain open.`
- TeX line 77: `failure boundary.  The answer is not a simple yes or no.  A shared dual`
- TeX line 97: `The distinction matters.  A finite exact frame identity is not an arithmetic`
- TeX line 111: `For a finitely supported sequence $a$, a real $v$, and a scale $H>0$, define`
- TeX line 197: `Let $\mathcal D$ be a finite set of unit dilations and let $c_D,d_E\in\C$.`
- TeX line 269: `$\sum_Dc_D\chi(D)$ appears only after the extra assumption that the profiles`
- TeX line 293: `Exchange the finite character sum and the sum over $n$.  If $q\nmid n$,`
- TeX line 352: `This is an interface obstruction, not an asymptotic assertion about the`
- TeX line 355: `\section{Common-profile resonance and finite validation}`
- TeX line 376: `finite QA artifacts and do not constitute asymptotic evidence.`
- TeX line 380: `\caption{Finite certificate summary.}`
- TeX line 407: `The complete edge frame from TPC-208 is an exact finite-dimensional identity.`
- TeX line 432: `This is a scoped stop, not a global nonexistence theorem.  The smallest`
- TeX line 436: `remains open and is the natural next route question.`
- TeX line 453: `\texttt{FULL\_GATE\_B=OPEN},\qquad`

## Conversion limitations

- 5 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#thm:poisson` → `main.tex#L157` (existing project target or original TeX label line).
- Link relocation: `#prop:covariance` → `main.tex#L207` (existing project target or original TeX label line).
- Link relocation: `#thm:character` → `main.tex#L251` (existing project target or original TeX label line).
- Link relocation: `#prop:gauss` → `main.tex#L281` (existing project target or original TeX label line).
