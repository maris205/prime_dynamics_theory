# TPC-250 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `128aef3815f6a847be76108fc072c5e2c9d9dfca085f1189443f17d5984d15a6`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `1b2d6f51dce2e2bab6f1ae616da4461ac0f8cf03423fefe99177713fba896a7f`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `fb4cc845e597559e124ac092f259a2fbfacae2e8c7aafca182c8fee33c1369e5`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `ef45ef267263a8f05e5494531046118f55bc055e94d2ca09ed0299d192aba673`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC250_254.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction and source lock` | 64 | 1 | `HEADING_TEXT_MATCH` |
| `Definitions and edge cases` | 92 | 2 | `HEADING_TEXT_MATCH` |
| `The coherence envelope` | 126 | 2, 5 | `UNMAPPED_OR_AMBIGUOUS` |
| `Inheritance by the TPC-249 support radii` | 195 | 3 | `HEADING_TEXT_MATCH` |
| `Sharpness and the marginal obstruction` | 233 | 4 | `HEADING_TEXT_MATCH` |
| `Exact finite verification` | 313 | 5 | `HEADING_TEXT_MATCH` |
| `Limitations and conclusion` | 334 | 5 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 371 | 5 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `117` before writing and `117` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `22`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `c9085d5159c70a6ea59ba388c825445899d78b5b423b8218aeb85b0f5ef17aec`.
- Source theorem/proof environment starts: theorem at TeX line 128, proof at TeX line 149, remark at TeX line 187, corollary at TeX line 206, proof at TeX line 221, proposition at TeX line 239, proof at TeX line 244, proposition at TeX line 255, proof at TeX line 260, proposition at TeX line 273, proof at TeX line 278, proposition at TeX line 297, proof at TeX line 302.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 48–50 | `7c307798f0f558514d85a71fc2ed1519af2e95730b30dc748f4db2841aa9e9ab` |
| D02 | equation | 75–79 | `3c35c52874e8df3f8bf5a671e82532d28c2aca4e51b09adfbfefe4ba6bd2943c` |
| D03 | equation | 96–100 | `85394749b42016c482202d12f6c1f146803903aa423de6eee73a9a091acc4f16` |
| D04 | equation | 102–104 | `12575d421e068c459cfe9da062dc4ae3995f2b673437e2fbcabf59c0b1c8ac6f` |
| D05 | equation | 106–113 | `e484a6bd6dfcfd789d3bb8b5ba52fb56ad753b5335b7e9b861609a108f97c73a` |
| D06 | equation | 120–122 | `95527e841f4e6f8b83272eec511eb880e14dc1c5ba9fd708350c224e9e37cdd9` |
| D07 | equation | 130–132 | `2c4ede9bfcf0e524ab8f8e5e48192f5df1b8cd1c1516f4168459da992ed950c2` |
| D08 | equation | 134–138 | `0dba4f6bf5d438cbfb6c191f545c847b4cc263333edf72003ea453d9696d70cb` |
| D09 | equation | 140–145 | `8eafeba7ebac1f6d9cffcc2f6d93da1649e4fe03a1f9adff2b311392d8723d39` |
| D10 | align | 151–159 | `9ab8c1718d3d92b3c0ca4a52a9ab74b1d838b371b9441965465fd28e2178be7e` |
| D11 | \[...\] | 161–165 | `8a66e56231959ace19368e0f9d43c927f1c0d7efb9d516882779dc9272c322c4` |
| D12 | \[...\] | 167–171 | `14264fbee25b4cbe30caf7c2ab513b310bf5c343b145ec81bfca8bb010148452` |
| D13 | \[...\] | 178–180 | `c88a28634a047dd91c2d306174733c302f11bab95b439226583680e689dd87c8` |
| D14 | equation | 199–203 | `b548a9e4b3a4e9c7ace2501b5dd3cd212d4fcc7daaff9c471a068d8236a8ce07` |
| D15 | equation | 208–212 | `60e7f5047e8665dc3bda7bd0dd78ab689d18e0427278d077dc32236a9328fa0b` |
| D16 | equation | 214–218 | `9ec97b307e68925dfaf822d5697abfacd269918a0aa02196802e97563705565b` |
| D17 | \[...\] | 249–251 | `c1717c0e463d3d63cf5642793bd4312799ca1a3b51c2b8e507929fab2028eeef` |
| D18 | \[...\] | 262–264 | `e80944e07ffb927d7ac1b7c8ccbd466c327edff139979516c7e752fff3f00992` |
| D19 | \[...\] | 267–269 | `3c88578405f0ed7dc126ee48cfa36ed0d7c0bb7f3d3f89c69f01135e1bc99e28` |
| D20 | \[...\] | 286–288 | `b95ceaf07156b11784fdd53ac786d99ca204670ddc950d7218bf5580fb66ce1e` |
| D21 | \[...\] | 290–293 | `21eebfc9328477cc481b868c8e86c8948b3f8be7b82bcb38c640c9bfe4b4af00` |
| D22 | align* | 352–361 | `46d709edcdad109b2cefdee0bc659341451ec12d9c2a014a0da5f459cd0abec1` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 27: `pdfsubject={Sharp finite Hilbert-space bounds for weighted Gram quadratics},`
- TeX line 60: `positive lower bound.  These conclusions are finite structural geometry; no`
- TeX line 89: `zero floor with positive-semidefinite Gram matrices.  The last step is`
- TeX line 94: `Let $\cH$ be a complex Hilbert space, let $I$ be finite, and choose`
- TeX line 189: `available relative to diagonal energy.  Coherence alone does not determine`
- TeX line 247: `$m-1$ and $1+(m-1)\mu$ once.  Hence $G$ is positive semidefinite and is the`
- TeX line 265: `Its eigenvalues are $1-\mu$ and $1+\mu$, so it is positive semidefinite.  With`
- TeX line 281: `semidefinite, and the vectors sum to zero.  With unit weights,`
- TeX line 289: `is rank-one and positive semidefinite.  Here $\mu=1$, $D=6$, $L=4$, and`
- TeX line 309: `norm is zero.  Both Gram matrices are positive semidefinite, and the two`
- TeX line 313: `\section{Exact finite verification}`
- TeX line 319: `fixture uses a positive-semidefinite rational Gram matrix.`
- TeX line 331: `\texttt{NUMERICAL\_FINITE\_ILLUSTRATION\_ONLY}: finite examples illustrate the`
- TeX line 337: `provides favorable values of its inputs.  TPC-250 does not estimate actual V59`
- TeX line 338: `coherence, does not prove a V59 Gram asymptotic, and does not turn the`
- TeX line 343: `Within its finite scope, the result is complete.  The diagonal Gram energy`
- TeX line 347: `and positive-semidefinite examples establish the universal sharpness of both`
- TeX line 353: `\texttt{TPC250\_ACTUAL\_V59\_COHERENCE\_ASYMPTOTIC}&=\texttt{OPEN},\\`
- TeX line 357: `\texttt{TPC250\_FULL\_GATE\_B}&=\texttt{OPEN},\\`

## Conversion limitations

- The preamble-only glyphtounicode input was resolved with kpsewhich and checked against the audited SHA-256; its non-content mapping table was not expanded. The original command, source line, and dependency hash are retained in the reading layer.
- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:deviation` → `main.tex#L130` (existing project target or original TeX label line).
- Link relocation: `#eq:deviation` → `main.tex#L130` (existing project target or original TeX label line).
- Link relocation: `#eq:bounds` → `main.tex#L134` (existing project target or original TeX label line).
- Link relocation: `#eq:bounds` → `main.tex#L134` (existing project target or original TeX label line).
- Link relocation: `#eq:normalized` → `main.tex#L140` (existing project target or original TeX label line).
- Link relocation: `#thm:main` → `main.tex#L128` (existing project target or original TeX label line).
- Link relocation: `#eq:ind` → `main.tex#L208` (existing project target or original TeX label line).
- Link relocation: `#eq:glob` → `main.tex#L214` (existing project target or original TeX label line).
- Link relocation: `#prop:marginal` → `main.tex#L297` (existing project target or original TeX label line).
