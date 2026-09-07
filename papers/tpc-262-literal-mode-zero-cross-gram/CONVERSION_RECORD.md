# TPC-262 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `bdc7bb8c00508788363faa2db8691f1128ab3d3e`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `7bba63069ba675a841ece61e3fbf038826ad7900a6d53e9c2fc5460cef725db8`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `f399d62e4bd8fd1c1d91e12fc372ab3a565b1a0fb976c84ec5f18572974490ba`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `6f32b5d165eea6a8ade0961fde3c7b0a4930ae448aeac791114fe1ea9e8d98bb`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC260_264.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Scope and motivation` | 33 | 1 | `HEADING_TEXT_MATCH` |
| `The literal reduced-residue fiber` | 53 | 1 | `HEADING_TEXT_MATCH` |
| `The signed remainder operator` | 92 | 2 | `HEADING_TEXT_MATCH` |
| `Mode zero is a signed cross-Gram` | 131 | 3 | `HEADING_TEXT_MATCH` |
| `The phase-character firewall` | 162 | 3 | `HEADING_TEXT_MATCH` |
| `A finite literal operator-image adversary` | 204 | 4 | `HEADING_TEXT_MATCH` |
| `Route status and conclusion` | 253 | 4 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 290 | 5 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `83` before writing and `83` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `18`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `ba8c24830019541e1854e4ff790dcecc34be77226e90594853c6e7b20de57672`.
- Source theorem/proof environment starts: lemma at TeX line 63, proof at TeX line 68, theorem at TeX line 140, proof at TeX line 155, corollary at TeX line 188, proof at TeX line 199.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 56–59 | `28b61ff4fd65267094a01296441f0adf9a8b053987e6455b7345715fefaa73a2` |
| D02 | equation | 71–76 | `444c570965e8a2f5f1528d3113fc6d4ddd93b30d62a456fee894ecb532f5825b` |
| D03 | equation | 83–88 | `9287122197cbdaf92a149c5d0ff33034070f3b87959510f47efb8a458cc7c97f` |
| D04 | equation | 95–99 | `12ca2bc805e0f00c4ae69152441230045496ebdbfe36fd3010f08c27b6d41b6a` |
| D05 | equation | 102–106 | `37bd90380e76200aa9f7931ade3ef2a8397e462079907a73f1d960e2a940351b` |
| D06 | equation | 109–115 | `1076ec17ad473dec5656e86c76b95f5c1c7828da2633a44630f505be535fc1c7` |
| D07 | equation | 117–121 | `e9ad9033322054e074bd28ba7ae0864dd18adda99c8789253dfde5ec65e6ed49` |
| D08 | equation | 123–128 | `8c634998bec1748137db08baebbfc0ab29e4ff28caa4b448f33a2c28b5b0c943` |
| D09 | equation | 133–138 | `e9d5044fdd98f7734b33503b38c6a8bd14a42eafb0eb570861df76bca48ce65b` |
| D10 | equation | 142–145 | `2cde7db65a9a6788d404f876ae86475c7588e02d2dbd2c31e96e978774a49f5c` |
| D11 | align | 147–152 | `026c24888e4730f7da89a61e0b189560020db35610bd1f435448a903f3469331` |
| D12 | equation | 165–169 | `8d68e122b9c91550ba827dc7792eeb505fd7b2d5b6f9bc2f0a3d2f1f10a5b6f4` |
| D13 | equation | 171–177 | `97592591a567eca492420cc3bf250d5bead6e39fdc67c50a72042b73336ade2f` |
| D14 | equation | 190–194 | `dca61316c48f128c1d83c6f8be2bb2de17d35d67e11dc20e58a4d64af5df4dbf` |
| D15 | equation | 206–209 | `366ddf7aca582067a7ca42cb6eb446c6b10429bf2e3d4b76907c8d0e43b2fcb8` |
| D16 | equation | 212–217 | `350000a3dc8fe59a1944e068eb1bf89feba175975be77fd5e39e3ba839707aa2` |
| D17 | equation | 219–222 | `f1bb558df7f91b7050cc6ba5068d8f44edc3b9acf35ddb52d32b83a7652773a7` |
| D18 | equation | 225–229 | `21932ba76090cdf82103e22b9273847366a4d1f44c8ca2c82daecce063dafeac` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 28: `characters are distinct.  An exact finite operator-image certificate on`
- TeX line 30: `\(16\norm{Y}^2\) and zero.  This is a finite structural obstruction, not a`
- TeX line 43: `distinction throughout.  The finite certificate audits \(v=0\), while the`
- TeX line 44: `operator identity is phase-by-phase and the growing integral remains open.`
- TeX line 50: `\item certify a literal finite operator-image adversary with rational`
- TeX line 65: `semidefinite, has rank \(q-2\), and has kernel`
- TeX line 81: `For a finite set \(\Qp\) of odd primes, a packet source is`
- TeX line 93: `Let \(I\) be a finite interval and \(v\in\mathbb R\).  For a coefficient`
- TeX line 107: `The first term is positive semidefinite, but \(J_{q,v}\) is a signed`
- TeX line 129: `This is an exact factorization, not an estimate.`
- TeX line 153: `Thus diagonal mass alone does not determine mode zero.`
- TeX line 186: `The theorem does not replace the smooth kernel or prove a favorable sign.`
- TeX line 196: `losses, the finite-lane endpoint compiler closes when`
- TeX line 200: `This is the exact exponent substitution into TPC-261's strict finite-lane`
- TeX line 204: `\section{A finite literal operator-image adversary}`
- TeX line 205: `Take the actual finite prime shell`
- TeX line 233: `This is a finite structural adversary.  Its source probes are freely chosen`
- TeX line 236: `mode-zero saving.  It does not refute a future theorem using the arithmetic`
- TeX line 256: `written exactly on one common finite object.  It also identifies the exact`
- TeX line 265: `\(1/400\).  A finite census may instead reveal another obstruction; neither`
- TeX line 279: `Finite operator-image witness & numerically certified structural\\`
- TeX line 280: `Growing \(\beta,w\) cross-Gram estimate & open\\`
- TeX line 281: `Arithmetic \(L^2\), full Gate B, twin primes & none / open\\`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:weighted` → `main.tex#L87` (existing project target or original TeX label line).
- Link relocation: `#eq:dft` → `main.tex#L144` (existing project target or original TeX label line).
- Link relocation: `#eq:psd` → `main.tex#L75` (existing project target or original TeX label line).
