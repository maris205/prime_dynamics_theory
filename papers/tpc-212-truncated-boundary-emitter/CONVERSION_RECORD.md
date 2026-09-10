# TPC-212 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `cf7b8b6860f476a98281628ce7522fa917796652267750b8f4f56ad5650382a7`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `1457ed5902810b12ca5db68872e816a454f862494ebd979df20cbfa02ecbc264`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `07084714302416623ebde1f5ae9aadba1a6644db548a8482870f0d0133b88a2a`; 8 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `aa5a06bc4e4b0edda7d17ccd150c0db268f9d2607587ccf0a1dbb42e004bc239`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC210_214.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | 68 | 1 | `HEADING_TEXT_MATCH` |
| `The divisor band as a signed Boolean boundary` | 141 | 2 | `HEADING_TEXT_MATCH` |
| `Notation` | 143 | 2 | `HEADING_TEXT_MATCH` |
| `Complete minus missing is an operator identity` | 243 | 4 | `HEADING_TEXT_MATCH` |
| `The reciprocal occupancy operator` | 291 | 4 | `HEADING_TEXT_MATCH` |
| `Finite emitter model` | 293 | 4 | `HEADING_TEXT_MATCH` |
| `Exact finite certificates` | 389 | 6 | `HEADING_TEXT_MATCH` |
| `Protocol` | 391 | 6 | `HEADING_TEXT_MATCH` |
| `Certificate status` | 450 | 6 | `HEADING_TEXT_MATCH` |
| `What the obstruction does and does not say` | 472 | 7 | `HEADING_TEXT_MATCH` |
| `The missing physical coupling` | 474 | 7 | `HEADING_TEXT_MATCH` |
| `Why the finite fixture is not an arithmetic result` | 502 | 7 | `HEADING_TEXT_MATCH` |
| `Conclusion and next route` | 519 | 7 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 535 | 8 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `141` before writing and `141` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `31`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `47d809557a9cb6771d236cc100888d9f4d8386650dc4b3b51771850d7444947a`.
- Source theorem/proof environment starts: lemma at TeX line 181, proof at TeX line 191, theorem at TeX line 202, proof at TeX line 215, proposition at TeX line 255, proof at TeX line 273, remark at TeX line 284, lemma at TeX line 316, proof at TeX line 334, proposition at TeX line 344, proof at TeX line 373, remark at TeX line 381.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 75–80 | `649672573d4ac5b797e2951e44b4e0edb1dfb18a84af2f13992016f586c25748` |
| D02 | equation | 82–88 | `c183adf24da544bf3e610797f42bd681d5bfed4ae601c647694586122df88b37` |
| D03 | equation | 96–101 | `2be7a4b4bdf57bd556fb5d020b5fd095562102073351512bba221f2a0a434fbf` |
| D04 | \[...\] | 146–148 | `ac0c8f6672b62df2be8665790a09d225753e66df75f057baf518b3dac14ee8f6` |
| D05 | \[...\] | 151–153 | `17b39276db788b143daab222962d41af3e76524b23a34ae7596915284f7654cc` |
| D06 | \[...\] | 156–158 | `a87638f380f07803d250ea4f7bebe6d2bb2e75261897fa21e87376505080608c` |
| D07 | equation | 160–163 | `aa35aa46ee9c10023aa5d6787621c3991dc98b335e26e5e34186135299fa5d5f` |
| D08 | \[...\] | 165–167 | `f916a384597be53bdcebb4414151e7da4e7865954af2c53fda3a7068fbafd6ae` |
| D09 | equation | 170–173 | `c910d17205477d85b4e57a5f3ca573f4a508ca9a7c9c47c273ec96a32de53711` |
| D10 | equation | 175–179 | `54be1d012dad14726f2fd64704f9c760976b3626a475024fa749162772d2df2a` |
| D11 | \[...\] | 184–187 | `423af6e18866580494370136f2f7ca2f8536a7d339996ec65b5ec23a6522dbed` |
| D12 | \[...\] | 195–198 | `24aaf4c2be180c9719fb26f40932f8d7b5d92c3d8fa609ae32cdb4a6caa9ec13` |
| D13 | \[...\] | 208–211 | `b92492703feefea246aee8de384c34a4ef88646ba963f806a725359711673e9b` |
| D14 | \[...\] | 218–220 | `de95ae92956b6f745d30c806b33219da3b8f8b89d4fa8ad39705e18bdbb26e04` |
| D15 | \[...\] | 230–232 | `47d3c251dc67377761cf4bfd8b9c394d7fcb547ca646b8f45d3c1e00983e3be9` |
| D16 | \[...\] | 234–238 | `76a7193aa94cbc01b27c29ef5a9bc8bed59ef573c2033e155b3f71b76fc6bbc2` |
| D17 | \[...\] | 247–252 | `6981da996ab01912a3212710321e8daaaeb7bf5adee14b787abbe2515739c9ba` |
| D18 | \[...\] | 258–261 | `f600f39523cb05e27a57bfaa0116d2b47a7bca984b649853baba43d41052c7fc` |
| D19 | \[...\] | 265–269 | `ea869c920c1ed8d719afce1d7ba511f3e5eab5a460ee3062accb641824b3b5f7` |
| D20 | \[...\] | 276–279 | `c519e9c484382071448fac578e3ccaa6dca981786b47e1bc7949a7075f2586c8` |
| D21 | \[...\] | 297–300 | `851c9b8c9651c653901a402c1814aa99290fde2a152488c1294e1c0bba235ef2` |
| D22 | \[...\] | 302–308 | `04b3d0eed8c1e2ed90b43c7e1b096ff2c48e79f02d61e1a8fd25e6675251a13e` |
| D23 | \[...\] | 310–312 | `a9da78bb460b53d006ec7e191f83f7f08bc536e9000256f9ff02e52bafa8a1a6` |
| D24 | equation | 319–324 | `436c973d146f99063bcf68e9dadef248e71252ace6188c0aa184e2a552800033` |
| D25 | equation | 326–331 | `58ab7b72f6199986aca9543e01dee3d9c3c9eae5a9a01cc86e812f1a99fd9690` |
| D26 | \[...\] | 336–338 | `c7fcea86521552a790a783ea586df88984337e916a87d5aeb7382c759731499f` |
| D27 | \[...\] | 347–349 | `5207d67b9261d6a49f0b7c0c7902e43d0b31c54878a724d62e65a1c7bebcc8fa` |
| D28 | \[...\] | 352–357 | `c14e08dba607ecf7f1752f2d97bbebd876dfa8315c5f359b506ead4db3c9959f` |
| D29 | \[...\] | 360–363 | `9eeb3b2ba62ffb8370e5dba4cae8f96b3cec6ffa91e8595f1036e14a56fd7aa6` |
| D30 | \[...\] | 365–368 | `bca7fbaae46f3ee44898232b363579a646a86fa837dd7701a46483ff33d4a231` |
| D31 | equation | 490–496 | `d4e9073e7f66894add5460187e933736fdcea03b57c89aedb851d0196ed69c72` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 51: `packet minus the missing-subset boundary.  We then define a finite reciprocal`
- TeX line 57: `finite checks use exact rational arithmetic and a unit-weight reciprocal fixture`
- TeX line 60: `Gate B, and the twin-prime endpoint remain open.`
- TeX line 66: `No arithmetic $L^2$ credit or fixed-atom credit is claimed.`
- TeX line 71: `literal transition carrier.  Its central difficulty is not a missing formal`
- TeX line 105: `The identity in \eqref{eq:tpc211-derivative} does not apply directly to`
- TeX line 107: `lattice, not a complete packet, and $A_d$ changes with $d$.  The precise question`
- TeX line 119: `has no cross-divisor entries.  This does not disprove a future estimate on the`
- TeX line 129: `\item a sharp finite alignment construction showing that emitter geometry alone`
- TeX line 131: `\item exact finite certificates covering four cuts, 5,810 profile coordinates,`
- TeX line 136: `The proof is finite and algebraic.  We do not estimate the shifted-prime sequence,`
- TeX line 149: `be a finite set of distinct active primes.  For a nonempty subset`
- TeX line 207: `uniformly over endpoint values.  More precisely, for a scalar endpoint $w$,`
- TeX line 240: `This is an exact witness, not a numerical approximation to a logarithm.`
- TeX line 253: `The next statement does not assume the product formula for $\Delta_S$.`
- TeX line 293: `\subsection{Finite emitter model}`
- TeX line 295: `Fix a positive integer $H$, a divisor $d\geq2$, and a finite set $\mathcal Q$`
- TeX line 296: `of integers coprime to $d$.  Define the finite index set`
- TeX line 346: `Let $\mathcal B$ be a finite divisor family and set`
- TeX line 383: `It does not say that the literal residual family can choose the aligned`
- TeX line 389: `\section{Exact finite certificates}`
- TeX line 396: `\eqref{eq:boundary-decomp} a coefficientwise finite identity rather than a`
- TeX line 397: `floating-point regression.  The emitter test uses the finite unit-weight`
- TeX line 403: `it does not import the producer module.  The optimized Python run is included`
- TeX line 448: `finite alignment statement for the emitter interface.`
- TeX line 461: `TPC212_RECIPROCAL_COLLISION = PROVED_EXACT_FINITE`
- TeX line 464: `TPC212_LITERAL_PHYSICAL_BOUNDARY_BOUND = OPEN`
- TeX line 465: `TPC212_PHYSICAL_CROSS_DIVISOR_GRAM_BOUND = OPEN`
- TeX line 472: `\section{What the obstruction does and does not say}`
- TeX line 502: `\subsection{Why the finite fixture is not an arithmetic result}`
- TeX line 504: `The finite emitter certificate sets $\psi=1$ on a finite set of $(q,m)$ pairs.`
- TeX line 507: `smooth emitter, does not include the prime shell, and does not control the`

## Conversion limitations

- 3 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:tpc211-derivative` → `main.tex#L100` (existing project target or original TeX label line).
- Link relocation: `#eq:physical-residual` → `main.tex#L79` (existing project target or original TeX label line).
- Link relocation: `#eq:log-leakage` → `main.tex#L178` (existing project target or original TeX label line).
- Link relocation: `#eq:log-leakage` → `main.tex#L178` (existing project target or original TeX label line).
- Link relocation: `#eq:log-leakage` → `main.tex#L178` (existing project target or original TeX label line).
- Link relocation: `#lem:full-incidence` → `main.tex#L182` (existing project target or original TeX label line).
- Link relocation: `#eq:missing-boundary` → `main.tex#L268` (existing project target or original TeX label line).
- Link relocation: `#eq:block-gram` → `main.tex#L356` (existing project target or original TeX label line).
- Link relocation: `#eq:aligned-residual` → `main.tex#L362` (existing project target or original TeX label line).
- Link relocation: `#eq:aligned-contribution` → `main.tex#L367` (existing project target or original TeX label line).
- Link relocation: `#prop:direct-sum` → `main.tex#L345` (existing project target or original TeX label line).
- Link relocation: `#eq:boundary-decomp` → `main.tex#L260` (existing project target or original TeX label line).
- Link relocation: `#eq:collision` → `main.tex#L323` (existing project target or original TeX label line).
- Link relocation: `#ex:35-band` → `main.tex#L228` (existing project target or original TeX label line).
- Link relocation: `#eq:aligned-residual` → `main.tex#L362` (existing project target or original TeX label line).
- Link relocation: `#prop:direct-sum` → `main.tex#L345` (existing project target or original TeX label line).
