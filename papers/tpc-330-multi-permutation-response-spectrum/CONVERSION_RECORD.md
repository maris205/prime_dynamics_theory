# TPC-330 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ba1fb3efe59e51e62f64f4dcb607bd390b4b4062`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `359f41cf811d138cc762f70b28e557f21ce334af544cfe26fe5ca261064154cb`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `26151898fe19ac90e4d68a83b2386cc44c50bff495e31d2580f42b1192c7c3cb`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `bf0f19d8e24a0edf9ea517e7ebed588255753ec4e5fcc6318adaa3d7a5cc4355`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `b3624ddb80e0fcda0f192a3ac222de8f9595ee4b64e2cac6af80112b72c2b022`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC330_334.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and contribution` | 45 | 1 | `HEADING_TEXT_MATCH` |
| `The finite object` | 72 | 1 | `HEADING_TEXT_MATCH` |
| `Source model and control orbit` | 107 | 2 | `HEADING_TEXT_MATCH` |
| `Exact identities and certificate protocol` | 149 | 2 | `HEADING_TEXT_MATCH` |
| `Finite response spectrum` | 182 | 3 | `HEADING_TEXT_MATCH` |
| `Inherited scale audit` | 238 | 3 | `HEADING_TEXT_MATCH` |
| `Component controls` | 257 | 4 | `HEADING_TEXT_MATCH` |
| `Exact anchor` | 269 | 4 | `HEADING_TEXT_MATCH` |
| `Interpretation and claim boundary` | 287 | 4 | `HEADING_TEXT_MATCH` |
| `Reproducibility` | 318 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 328 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `76` before writing and `76` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `23`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `8844565acdeade6ff4b48d6a89bdcc0b22a4196e979766e1a11625e4e38874e0`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 59–63 | `c88bb30403043a16998156768bee574709f772552b7e82616b6405dded0cce17` |
| D02 | \[...\] | 64–67 | `f0316737d9de27767a3d4c6793ba26fa6f9df72de32c7358430f49e743d3dc96` |
| D03 | \[...\] | 75–77 | `ef00deb1077ad608cf8719ca830a5278889cb260b18a0c1c71d2acd970398f30` |
| D04 | \[...\] | 79–82 | `eaecd3b7f187e05e23aa9bb71bef69aaff2ce8389d3b84fff34b1d8f6a19c11c` |
| D05 | equation | 84–89 | `267e0022f6ca1dfea29d495e537a9c0aed5f47ad0639b4de547ab5a7c3a672c5` |
| D06 | \[...\] | 91–93 | `6dc68a973de60528f95115754d021b8052e31e6f1633b51dc797892274cee233` |
| D07 | align | 98–103 | `7a7fc54100e09c6cfa975ba816e37abe5547c2666a915330521f3272f4af98b1` |
| D08 | \[...\] | 110–116 | `da7b892c7f308ba504441d07b3172b70fcb61cdf7d13c36a92b5cfdcb7d9ddd6` |
| D09 | equation | 118–122 | `9c6a4d967b2be9878a4fd53b095176b83b85d695900fc7f1b1e39d60396d8a45` |
| D10 | \[...\] | 131–135 | `0909ae5625996df3bc8e2f1135da1ac8ae1180d56e3b30c0d8da4e2e6e0a4c96` |
| D11 | \[...\] | 138–140 | `f0086bd031421d68495892582a08d1cdc9ef9d6f92b35b8e2d84ecdd75672027` |
| D12 | \[...\] | 142–145 | `210d455fd32ac38277fd7c0e4af44618f5e7d38961be9fe75fd838b8069dbc21` |
| D13 | \[...\] | 153–156 | `bcc8930e0ac924d0e75d9bca60f698e2953f9f9094afb09117b92b8a68abee3f` |
| D14 | \[...\] | 158–161 | `f36c38b71793f343a7f5366b37e548587d45a2b642328749e3274679bb406868` |
| D15 | \[...\] | 208–215 | `827c682cfb16c52b66c135d1fc89dc629546e9ad53ff1f727d2ae44c97d7f0cf` |
| D16 | \[...\] | 217–220 | `5826c538838491288840710a16723826bce93516a3bb82aaaf95639cd1ac29f8` |
| D17 | \[...\] | 223–230 | `68d0620c4c9f56580a0525add39bf5ad25891eeae47620ae9bebdcdf4f469f4c` |
| D18 | \[...\] | 244–247 | `16d2e60fec1cb19097f5007984f7c74f3b4eb85393cbc6d26a30f995acb1bda4` |
| D19 | \[...\] | 248–252 | `c7dc7c755b39923548d68c4d77cb5fe322e1aecebfba9513c8d5c03231a9e3f4` |
| D20 | \[...\] | 262–265 | `ef3c754b29106770ac733d762ad5f88c76405e2e082087e8248a58dce794f156` |
| D21 | \[...\] | 273–275 | `30df284b9811c7603963144d6fde298a75912cdd71b27828e8528fbc670e522c` |
| D22 | \[...\] | 277–281 | `b1cc94ff33824522e3ac3c8da7e244d58f496ab7335de7cdd03fa48ab2cf610a` |
| D23 | \[...\] | 308–313 | `7736e6284fec396d00a934e7675e9cacd86e0c103ce291e2ab35ca1498295716` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 26: `A preceding finite audit found that a single source-coordinate permutation`
- TeX line 30: `operator and the finite V59 source model fixed, we evaluate five predeclared`
- TeX line 37: `The exact finite Gram decomposition and norm invariance are proved; the`
- TeX line 39: `is a finite position-sensitivity obstruction and a rejection of both`
- TeX line 41: `does not provide a growing arithmetic estimate, fixed-power credit, a`
- TeX line 56: `The contribution is a finite response spectrum.  We keep the source, origins,`
- TeX line 69: `replicate the earlier sign reversal; reversal does not.  This is a`
- TeX line 70: `position-aware finite obstruction, not an asymptotic claim.`
- TeX line 72: `\section{The finite object}`
- TeX line 97: `For a finite vector $v=(v_t)_{t\in I_{o,N}}$, define`
- TeX line 109: `The finite source model inherited from V59 is`
- TeX line 136: `This is an exact finite statement.  It does not imply that the physical`
- TeX line 151: `\paragraph{Finite Gram identity.}`
- TeX line 152: `Since $C_ev=\sum_t v_tC_ee_t$, finite bilinearity gives`
- TeX line 162: `Consequently $E_e(v)=D_e(v)+O_e(v)$ exactly for every finite vector.  No`
- TeX line 163: `limit or arithmetic estimate is used; this is the usual finite Gram expansion`
- TeX line 168: `multiset preservation.  It does not prove`
- TeX line 182: `\section{Finite response spectrum}`
- TeX line 254: `split are $15/16$, $16/16$, and $16/16$.  These are finite observations and`
- TeX line 255: `not estimates uniform in the source or in scale.`
- TeX line 266: `This rules out a zero-energy component in this finite computation, but does`
- TeX line 284: `certificate and replayed independently.  This anchor is a finite arithmetic`
- TeX line 289: `The strongest finite positive result is a three-control affine consensus:`
- TeX line 297: `\item \texttt{PROVED\_EXACT\_FINITE}: matrix formula, Gram split, five`
- TeX line 299: `\item \texttt{NUMERICALLY\_CERTIFIED\_FINITE}: 32 rows, 640 response`
- TeX line 303: `\item \texttt{OPEN}: position-aware structural bound, growing source-native`
- TeX line 311: `\texttt{FULL\_GATE\_B=OPEN},\quad`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.

- Link relocation: `#tab:census` → `main.tex#L190` (existing project target or original TeX label line).
- Link relocation: `#eq:source` → `main.tex#L118` (existing project target or original TeX label line).
