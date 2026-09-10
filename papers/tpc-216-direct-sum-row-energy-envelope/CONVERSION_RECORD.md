# TPC-216 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `dc55ef4eec89c01deb373bfe116005b537b3011506be7805fd7281cdfeadb1e4`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `e3115672948f2a81ea3cd5b04995cfae4069fc852ede8174edf0c7a8e3f3fb60`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `39515a4b3635ee563f5703651f388f372a2d558f3020c2a03358ed9ce4c66cc7`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `09a0979b57273df6176e91fe547b5b38db0c44dd5fbed2cc08ba198fc15e8dc2`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC215_219.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | 65 | 1 | `HEADING_TEXT_MATCH` |
| `Literal source lock` | 93 | 2 | `HEADING_TEXT_MATCH` |
| `Fixed-prime injectivity` | 134 | 2 | `HEADING_TEXT_MATCH` |
| `The direct-sum envelope` | 171 | 3 | `HEADING_TEXT_MATCH` |
| `Exact aligned-shell adversary` | 230 | 3 | `HEADING_TEXT_MATCH` |
| `Route evaluation and open gates` | 279 | 4 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 302 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 313 | 5 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `71` before writing and `71` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `18`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `7fbada3af9d429bcc37ff0edfa08400e40c64d1f56826ce74b6bb834c6da2608`.
- Source theorem/proof environment starts: theorem at TeX line 145, proof at TeX line 158, theorem at TeX line 173, proof at TeX line 197, remark at TeX line 222, proposition at TeX line 263, proof at TeX line 271.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 48–51 | `b913ce5c7efa38e1ad0195e77abd8e15906c4e5f4d5be0381f7bba76f05437d1` |
| D02 | equation | 68–71 | `15cdb9befb4ff11380dcb6ed2de4aab3a8ec4bcb1066bb1dfb47dc037465ca3a` |
| D03 | equation | 97–101 | `872952ac2f7af7b8b5a874a123b63483345e9dd20e0f89fea03031d618d98483` |
| D04 | equation | 103–106 | `9727c9d6b8dabf7e96ae313daeeac7fe8a8105f727452d977bb8a32c4ce9eecc` |
| D05 | equation | 108–111 | `015b538a0d564c955650109fca3448853057570bfe508a9b227f6d30cfc81059` |
| D06 | equation | 115–120 | `9ea5c9f589b43ab1d2c97040d987b3925627f94222577ff892a3a46e48fa0615` |
| D07 | equation | 125–129 | `1f72c378d1469e1a9f239acdad364fc07837212d08c09c5c13a4f41b861e7eb5` |
| D08 | equation | 137–143 | `25eca1874a8bbb3b0fb76ab9fa43909df0f5c61ee21b36e06b4136dbec458970` |
| D09 | equation | 149–155 | `44ef501c772a3cb79d614a733bee5bc2aa1f1d0a28fb959d18e71eb7250aa8bb` |
| D10 | \[...\] | 162–165 | `2ebf8a352042bb2da4483738c1762f957f91a40cde922e21a84ac4ce415348a4` |
| D11 | equation | 176–179 | `bae32eed4bf54265aec280af3ec5bfb5842afd1132a9641b2da0ea00f5c66292` |
| D12 | equation | 181–187 | `bfe8ce2ec831fe548557b9a39abce6d10d5d2c21b5e55f899ce55ca794258948` |
| D13 | equation | 189–192 | `3ad238ac870172b8726358c02588a0ef4b83c7f055946ebc060f9a4304c227df` |
| D14 | align | 200–206 | `a78d7c0650f134c5e490807574694b0b4e9b074004a9b8c139d1d248487dc39d` |
| D15 | \[...\] | 209–211 | `044365954c599a89bdcf856531ad0426106c925766f2621cd69de93c81c51e10` |
| D16 | \[...\] | 215–217 | `365bfe10bcc8252433360a7da68c5be6d69655ed49cd8d1b11cf497140d46563` |
| D17 | equation | 234–239 | `f72b9013e3d2acf8261cb467c4bb4586df368bf5040ce7803f2dc10d0d39f060` |
| D18 | equation | 282–286 | `ae5f127cbc2c9d5cf76b796fadd2571825d81679543c516ff74c286ce73d1dfc` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 55: `complete-period structural envelope only: the finite physical-window Gram,`
- TeX line 57: `open.`
- TeX line 62: `The exponent \(11/32\) is an unconditional source-locked envelope.  The finite`
- TeX line 63: `fixture is exact rational structural QA.  No arithmetic saving is claimed.`
- TeX line 80: `be before finite-window cross frequencies are restored?  The answer here is a`
- TeX line 81: `source-locked envelope, not a cancellation theorem.  The fixed-prime integer`
- TeX line 89: `another.  A finite exact fixture with primes congruent to one modulo five makes`
- TeX line 224: `It does not use the signs of \(\mu(d)\), any prime cancellation, or the`
- TeX line 226: `The finite physical interval has an off-frequency Gram that is not controlled`
- TeX line 233: `the finite rational fixture`
- TeX line 261: `finite structural adversary, not a model for an asymptotic prime shell.`
- TeX line 274: `orthogonal replacement fails on an admissible finite reciprocal-emitter`
- TeX line 275: `configuration.  The statement is scoped to the replacement rule; it does not`
- TeX line 279: `\section{Route evaluation and open gates}`
- TeX line 288: `it does not provide a saving relative to a required target scale.  The exact`
- TeX line 291: `\item attach the normalized complete-period envelope to the literal finite`
- TeX line 300: `is open.`
- TeX line 309: `artifact.  The next research step is a finite-window attachment that keeps this`

## Conversion limitations

- 3 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:fixed-row` → `main.tex#L142` (existing project target or original TeX label line).
- Link relocation: `#eq:source-inequalities` → `main.tex#L128` (existing project target or original TeX label line).
- Link relocation: `#eq:fixed-energy` → `main.tex#L154` (existing project target or original TeX label line).
- Link relocation: `#thm:no-collision` → `main.tex#L146` (existing project target or original TeX label line).
- Link relocation: `#eq:direct-energy` → `main.tex#L178` (existing project target or original TeX label line).
- Link relocation: `#eq:envelope` → `main.tex#L186` (existing project target or original TeX label line).
- Link relocation: `#thm:envelope` → `main.tex#L174` (existing project target or original TeX label line).
- Link relocation: `#eq:adversary` → `main.tex#L238` (existing project target or original TeX label line).
- Link relocation: `#thm:envelope` → `main.tex#L174` (existing project target or original TeX label line).
