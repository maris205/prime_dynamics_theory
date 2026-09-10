# TPC-253 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `15d2b88c709c4f65ddf941f7ecbc97d1558d41fa8ab3966e8e8bb909646c78ee`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `ebcd14ba30846dd03eed5999e45344e2f3117040414bd5aa7e05e45f02c2af3c`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `a1b46c00c91e0cdc8bbb6a307b706c950c8bf4b69e102c2ace60adf23eee3194`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `bb0c306b54dd9995976e03d85a0505eadc05ed984230bab15826e82828d4f090`.
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
| `Frozen source choice and scope` | 54 | 1 | `HEADING_TEXT_MATCH` |
| `Rank-midpoint geometry` | 84 | 1 | `HEADING_TEXT_MATCH` |
| `Partial-sum covariance compiler` | 154 | 2 | `HEADING_TEXT_MATCH` |
| `Literal kernel expansion and safe adjoint` | 208 | 3 | `HEADING_TEXT_MATCH` |
| `Sharp controls, exact audit, and limitations` | 261 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 301 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 311 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `118` before writing and `118` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `15`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `f9bd12532a8f17dfdd212a84b84d730eb9d8ffa92e79438e97583717d8bc5ac8`.
- Source theorem/proof environment starts: proposition at TeX line 92, proof at TeX line 104, proposition at TeX line 123, proof at TeX line 132, theorem at TeX line 159, proof at TeX line 189, proposition at TeX line 227, proof at TeX line 244, proposition at TeX line 263, proof at TeX line 269.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 57–59 | `1ebfa5ea3d0d0082773132962e8b94c6cc3254e907d295e1b580e424c27faae4` |
| D02 | equation | 69–72 | `aa62d7a8b49addf78ca0a507d51e136752376f3cdb0ce798e2b4c5e2af1f2ce3` |
| D03 | equation | 87–90 | `37c80d74a34ce7bd3592e894d58db62a623c47ad93fd35864fb74ef9154deb20` |
| D04 | equation | 95–99 | `09e6c6555250dc923e9d0dab472dc59749f88875d59e03cafd23185b81bd8bdd` |
| D05 | \[...\] | 106–110 | `9fe17867a26c179966aac60b82b18724f350a6787d016a2ae344c9d558312392` |
| D06 | \[...\] | 126–129 | `235de39cb6a480f0a08f26ab4639e2cb395795cca70b9a07fa0d1743bb79d4c2` |
| D07 | align | 162–176 | `c499b0497b1b6adaafc82c817d783f32c4e50b6551f1c40f4b5887679191a938` |
| D08 | equation | 178–181 | `63b326f99825d8d56a5c18175bfe549719cf911681dfb68384eb854d2922249a` |
| D09 | equation | 183–186 | `7fc329206bf70c9d576c58692ba6da5a98f4f544a432d791a3c697e6f1d1b77f` |
| D10 | \[...\] | 194–197 | `24495ad5975bcfec12b3826d82b56203f5ab2d1e23ea57fe71803686ac121c78` |
| D11 | gather | 211–218 | `b5b81346e7035e7616acb7a60a63eb0026cfc53ddc4d33410639e8c02e8ff2ea` |
| D12 | equation | 221–225 | `a3732176561d91c628512de9e733e15a51b38d418c2be7ae056eccd35d602289` |
| D13 | align | 229–236 | `cf5dda9c74f5534f300c35c6514cf464aaff1c8ed763fb6df5332afebe1a508f` |
| D14 | equation | 238–241 | `1d3e836bb8866fd3f3ca20d26c37318593d3b405d3f450caaf676ef89ad7647b` |
| D15 | \[...\] | 248–252 | `2b532e40cd6262093377abd122a1b8e1eea868c424aacd53f1748607a691ea84` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 56: `Keep the finite literal TPC-247 source object`
- TeX line 76: `sign.  It is a source-frozen modeling choice, not a unique V59-canonical`
- TeX line 219: `The inherited superscript in $b_x^{(z)}$ is source notation and does not`
- TeX line 247: `\eqref{eq:adjoint}, expand the finite sums:`
- TeX line 265: `\eqref{eq:transfer} is zero.  The synthetic choices $(w,g)=(z,z)$ and`
- TeX line 274: `These are exact finite Hilbert-space controls, not literal numerical V59`
- TeX line 286: `rejects 59 typed, semantic, digest, duplicate-key, nonfinite, and`
- TeX line 290: `identical output.  These computations reproduce finite algebra only.`
- TeX line 294: `V59 partition.  The exact-sample kernel fixture is not an actual V59`
- TeX line 297: `credit, Gate-B closure, strict $1/400$, or twin-prime result.  The open theorem`

## Conversion limitations

- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:projector` → `main.tex#L98` (existing project target or original TeX label line).
- Link relocation: `#prop:crosswalk` → `main.tex#L123` (existing project target or original TeX label line).
- Link relocation: `#eq:ranks` → `main.tex#L71` (existing project target or original TeX label line).
- Link relocation: `#eq:moment` → `main.tex#L164` (existing project target or original TeX label line).
- Link relocation: `#eq:midlong` → `main.tex#L166` (existing project target or original TeX label line).
- Link relocation: `#eq:coarselong` → `main.tex#L168` (existing project target or original TeX label line).
- Link relocation: `#prop:projector` → `main.tex#L92` (existing project target or original TeX label line).
- Link relocation: `#eq:moment` → `main.tex#L164` (existing project target or original TeX label line).
- Link relocation: `#eq:transfer` → `main.tex#L173` (existing project target or original TeX label line).
- Link relocation: `#eq:qchange` → `main.tex#L175` (existing project target or original TeX label line).
- Link relocation: `#eq:within` → `main.tex#L180` (existing project target or original TeX label line).
- Link relocation: `#eq:decomp` → `main.tex#L185` (existing project target or original TeX label line).
- Link relocation: `#eq:operator` → `main.tex#L224` (existing project target or original TeX label line).
- Link relocation: `#eq:moment` → `main.tex#L164` (existing project target or original TeX label line).
- Link relocation: `#eq:literal` → `main.tex#L235` (existing project target or original TeX label line).
- Link relocation: `#eq:adjoint` → `main.tex#L240` (existing project target or original TeX label line).
- Link relocation: `#eq:transfer` → `main.tex#L173` (existing project target or original TeX label line).
- Link relocation: `#eq:operator` → `main.tex#L224` (existing project target or original TeX label line).
- Link relocation: `#eq:adjoint` → `main.tex#L240` (existing project target or original TeX label line).
