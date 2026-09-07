# TPC-331 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ba1fb3efe59e51e62f64f4dcb607bd390b4b4062`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `2b501adffe984b8379d8da4efd52d262a28edf23ae8b9dd8ffc81ccb12c9b6c5`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `26151898fe19ac90e4d68a83b2386cc44c50bff495e31d2580f42b1192c7c3cb`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `8c187fa0f51d2ba1c5648a7a4da4987cbe9f9a679bbff2b886f9d673d7328713`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `b21f7f7f6dce9a19db14f7797d2cb1e40c250799e9859569ac85407a4b404b1e`.
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
| `Question and contribution` | 46 | 1 | `HEADING_TEXT_MATCH` |
| `Finite object and source model` | 65 | 1 | `HEADING_TEXT_MATCH` |
| `The control-orbit decomposition` | 109 | 2 | `HEADING_TEXT_MATCH` |
| `Certificate protocol` | 156 | 2 | `HEADING_TEXT_MATCH` |
| `Finite decomposition results` | 176 | 3 | `HEADING_TEXT_MATCH` |
| `Exact rational anchor` | 236 | 3 | `HEADING_TEXT_MATCH` |
| `Interpretation and claim boundary` | 260 | 4 | `HEADING_TEXT_MATCH` |
| `Reproducibility` | 293 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 302 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `62` before writing and `62` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `21`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `c79f0d2f195c7c73d4cb78c8d330092256568fc222edc1f5c41d501d6b009baa`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 32–34 | `4fcd64c080441ad01ffc9e10b64536ba5806c707178d1c14295840c8fcf5ff04` |
| D02 | \[...\] | 68–70 | `ef00deb1077ad608cf8719ca830a5278889cb260b18a0c1c71d2acd970398f30` |
| D03 | \[...\] | 72–75 | `d767eeab00f6be7eac56ee108b0663c42c76891ad59289d2cdfd0ff672a78422` |
| D04 | equation | 77–82 | `94d185a349273afe853153ff07c30d6e76987fdb31863125faac2a4230b02df6` |
| D05 | \[...\] | 84–86 | `6dc68a973de60528f95115754d021b8052e31e6f1633b51dc797892274cee233` |
| D06 | equation | 91–95 | `dc16451204d026eab6234fbd5b8d75a65a7b447458f672335befaf05fecfb247` |
| D07 | align | 102–106 | `ee08e479ef6899d2b05beba66608d424a3af2e0e7297aac57036778edcc2bbe1` |
| D08 | \[...\] | 112–115 | `fab5486d76f108f1406821487ca32581f55df5fafe60332baf00702f21c6fa40` |
| D09 | \[...\] | 116–119 | `e31aafc4d0c8f1b6bc590c5ae37e83741ba67f7db09b5709a7842ff8c79fe973` |
| D10 | \[...\] | 123–126 | `1c5d462446e187e9b4dde942d45347c21074da1213fdd6124ee9861b47f86fcd` |
| D11 | equation | 132–135 | `5be072d87a2955ba334ef840caf336e9d7e473982b725ae2069cfb4edd6c1c21` |
| D12 | align | 146–151 | `62192e7a654f9de2f0bfc92d798befe137703277b12a1f3ed1bc6e77e87b166d` |
| D13 | \[...\] | 164–166 | `8c7e606809be5ea08cb71f8528773e3ed00922592a651cef03275bd5eba1adaa` |
| D14 | \[...\] | 199–206 | `cea100b41990213b087fe67d4e9dab22f234ad480dd2e23a5d2bb32ad13e5b06` |
| D15 | \[...\] | 210–212 | `896bf38f1b3e45e25fc5de6a0397591080eb2b2c8e84da211080308101a9d594` |
| D16 | \[...\] | 218–221 | `c3d9d9a2240d0af16020ca2a94d0b4a1d1885c30a33f817dfae9e2a40e5351e2` |
| D17 | \[...\] | 227–231 | `d431e2a660b9bade36338aa73d470d5154c4bf1a76af3f11213c5cef17bcada4` |
| D18 | \[...\] | 239–242 | `5f4ad1c113431f8d078ac0ddda332bfbf03b038de4d8e73764cddb2034d5fe67` |
| D19 | \[...\] | 244–251 | `5e39bd2f39d300bebb8c20f3454df081915f20715decdfaf5bed819ea95ecc02` |
| D20 | \[...\] | 253–255 | `a304698a4d3c3cdab3d1d6400797c59efda23dfc6883ac4e2e2280881c6bf5f5` |
| D21 | \[...\] | 286–291 | `149cbffc2de2ddc69adfc9b91dce5e6d9e2c1db863debeaba5777340e9588053` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 26: `The preceding finite response-spectrum audit showed that three odd-affine`
- TeX line 31: `permutations $P_j$, we prove the exact finite identity`
- TeX line 41: `symbolically.  This is a finite structural localization of the response; it`
- TeX line 42: `does not supply a growing arithmetic $L^2$ estimate, a fixed-power credit, an`
- TeX line 48: `The signed-Gram diagnostic in this session acts on a finite source vector with`
- TeX line 61: `finite certificate for its three signed-Gram components.  It provides a new`
- TeX line 65: `\section{Finite object and source model}`
- TeX line 90: `The finite declared source is inherited from the V59 model:`
- TeX line 101: `For a finite vector $x$ define`
- TeX line 129: `\paragraph{Theorem (finite mean--centered identity).}`
- TeX line 130: `For any real matrix $A$ and finite vectors $w_j$, with`
- TeX line 138: `Expand $q_A(\bar v+z_j)$ and sum, as in the standard finite quadratic-form`
- TeX line 140: `$2\bar v^TA^TA(\sum_jz_j)/5=0$.  This is finite bilinearity and uses no`
- TeX line 154: `for quadratic values, not an average of the ratios $R_e$.`
- TeX line 176: `\section{Finite decomposition results}`
- TeX line 214: `$0.85206228015404784$.  These fractions are finite diagnostics, not`
- TeX line 223: `six observed signatures are finite mixed types; mod-$4$ and half split are`
- TeX line 262: `The strongest finite positive result is a localization: the all-plus positive`
- TeX line 268: `The strongest obstruction is equally important.  The decomposition does not`
- TeX line 270: `finite all-plus energy.  Therefore a future theorem must control this`
- TeX line 276: `\item \texttt{PROVED\_EXACT\_FINITE}: the mean--centered identities,`
- TeX line 277: `finite Gram split, and rational anchor;`
- TeX line 278: `\item \texttt{NUMERICALLY\_CERTIFIED\_FINITE}: 32 rows, four laws, three`
- TeX line 281: `\item \texttt{OPEN}: uniform position-response bounds, growing`
- TeX line 289: `\texttt{FULL\_GATE\_B=OPEN},\qquad`
- TeX line 298: `are scoped to the declared finite model; no official Route-A or Route-B pass`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.

- Link relocation: `#eq:quadratic` → `main.tex#L132` (existing project target or original TeX label line).
- Link relocation: `#eq:three` → `main.tex#L150` (existing project target or original TeX label line).
- Link relocation: `#tab:decomp` → `main.tex#L184` (existing project target or original TeX label line).
