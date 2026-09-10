# TPC-225 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `406e13e9abdb0413d96d618507c1ebc8232dd5eb91747f507063aa274e2150d4`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `a1c9399827ce00021b599ce63ba0d73a30da14443f2e3f15662789ed3e2aa53d`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `de353837a71601fa7da5f8b3ab97d0fa17ee3b302cb6e3a96b0b73211fbaa64f`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `7f6160a26c942a970aaa84c6b31861a74224b1c8a1785e2f339c81806f09d3b0`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC225_229.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and claim ceiling` | 38 | 1 | `HEADING_TEXT_MATCH` |
| `The literal cutoff-one object` | 60 | 1 | `HEADING_TEXT_MATCH` |
| `Exact marginal identities` | 113 | 2 | `HEADING_TEXT_MATCH` |
| `Affine profiles and exact closed forms` | 149 | 2 | `HEADING_TEXT_MATCH` |
| `Adversarial profile controls` | 197 | 3 | `HEADING_TEXT_MATCH` |
| `Block decomposition and certification protocol` | 213 | 3 | `HEADING_TEXT_MATCH` |
| `Route consequence` | 276 | 4 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 301 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 313 | 5 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `82` before writing and `82` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `13`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `024c1c74198715c0fa4a81e94576ceed10ecbc4eb6482e6490f28cb29783c0b7`.
- Source theorem/proof environment starts: lemma at TeX line 97, proof at TeX line 101, theorem at TeX line 115, proof at TeX line 125.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 42–48 | `3a68487ce6009ab6d9af4221b62497ba898743daa77a0dc002bbbaa71b01efe9` |
| D02 | equation | 64–68 | `656bee32e9a141d3809dd384e6c712d52df40500d8817762e93de3d6ccddd1fe` |
| D03 | equation | 70–75 | `850dd89fc9a8fe80135e91135102c14ba4fb54a99e79ac36cb32b21007bb42fd` |
| D04 | equation | 83–87 | `43c8980b83f36f0e452b0726e3035975dc242a6344b3c512ebe33222618cba24` |
| D05 | equation | 91–95 | `8de571c2604db8501b7ec8089e76260521949e17d993240fe740c950e3a977fb` |
| D06 | equation | 118–121 | `06b1cdcf837dd87223abd7e891b6b0d9f3f90fb3b2e1b29e6cd7ebab9eeaea11` |
| D07 | \[...\] | 128–131 | `1a643933b9946a110f224126c7bb48bf8d86950e06ba901a5343bdfd5bd01cd8` |
| D08 | \[...\] | 135–137 | `e43aeefc034240c6ce9fc0e84f56db38dc6346a64c53f1191b0613fb9e340dca` |
| D09 | align | 155–162 | `b7a821e6e2b1d5f5dad03bec1e7d07c28367c80c051206d93e0a5285a99af25b` |
| D10 | equation | 165–169 | `47a56d1b21f367dd2a6ab45cd46954a6041cf7b089dda1dc2b05b5d7122afcb7` |
| D11 | equation | 204–207 | `a1405fb91beb1c68c49ed7b86b456375f9517585fb64faf1e6656fec4589366e` |
| D12 | \[...\] | 216–220 | `ef6c73d7e887e43dbc17e6d0e42c6b254241c2098a9c54f8788fc218c8e95687` |
| D13 | equation | 223–226 | `2587993dc7349ea5342284278e38d5b382518af9f95dd037be20ef96eae34fb5` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 25: `common literal Hilbert family, but left open whether both marginals can save`
- TeX line 26: `energy on one source clock.  This paper audits the named finite clock`
- TeX line 35: `scoped obstruction, not an asymptotic arithmetic \(L^2\) theorem.`
- TeX line 50: `research question is narrower: does the source clock used for the finite`
- TeX line 55: `that every possible V46 clock has the same geometry.  The clock is a finite`
- TeX line 116: `For every finite collection of real packet profiles on the clock`
- TeX line 123: `\(E_{\rm AP}\leq(1-\delta)E_{\rm diag}\) uniformly on this clock.`
- TeX line 142: `The theorem is stronger than a numerical observation: no choice of finite`
- TeX line 171: `is packet alignment, not an AP saving.`
- TeX line 199: `The exact obstruction does not depend on the affine choice.  For an aligned`
- TeX line 235: `The finite replay was designed to distinguish an identity from a floating`
- TeX line 239: `enumerator and row constructor; it does not import the producer.  It checks`
- TeX line 268: `literal finite object and its exact theorem; it does not estimate how often`
- TeX line 269: `primes occur in a longer interval, and it does not replace a source-lock`
- TeX line 282: `and the exact V46 transfer is still open.  A productive AP route must either`
- TeX line 298: `TPC225_FULL_GATE_B = OPEN`
- TeX line 309: `there is no arithmetic \(L^2\) advance, fixed-atom credit, strict`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:energies` → `main.tex#L47` (existing project target or original TeX label line).
- Link relocation: `#eq:cutoff` → `main.tex#L86` (existing project target or original TeX label line).
- Link relocation: `#eq:clock` → `main.tex#L67` (existing project target or original TeX label line).
- Link relocation: `#eq:twopoint` → `main.tex#L94` (existing project target or original TeX label line).
- Link relocation: `#eq:main` → `main.tex#L120` (existing project target or original TeX label line).
- Link relocation: `#eq:affined` → `main.tex#L158` (existing project target or original TeX label line).
- Link relocation: `#eq:affinep` → `main.tex#L161` (existing project target or original TeX label line).
- Link relocation: `#eq:block` → `main.tex#L225` (existing project target or original TeX label line).
