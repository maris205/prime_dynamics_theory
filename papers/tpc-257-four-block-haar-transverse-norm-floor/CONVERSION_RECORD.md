# TPC-257 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `d1683c8f96ae1b86f2f9fcb9ba8318c9e1aaf3f6`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `4b3e26cb04976f9137cb71c00e94a5aa08fb660ddbc34e79d309c49eac6a8d90`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `28b3af777b84dea45a31dacde4546e10d2f2ae412158e7b712b3471508514686`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `b5f401cc652b4275a08c6b52e5283649078f8cedd04b1345e8c48cc4b1d47459`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `2e911be61e361a27b166cdcef4202cf165a9c8dccc6de255a0600a9ab4839341`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC255_259.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and claim boundary` | 60 | 1 | `HEADING_TEXT_MATCH` |
| `Literal clock and four-block frame` | 74 | 1 | `HEADING_TEXT_MATCH` |
| `The literal coefficient and its three curvatures` | 150 | 2 | `HEADING_TEXT_MATCH` |
| `Adjoint normal form for bounded variation` | 211 | 3 | `HEADING_TEXT_MATCH` |
| `Main theorem and norm floors` | 268 | 3 | `HEADING_TEXT_MATCH` |
| `Interpretation, obstruction, and next route` | 328 | 4 | `HEADING_TEXT_MATCH` |
| `Reproducibility and epistemic labels` | 348 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 359 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `113` before writing and `113` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `30`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `861321f223037c868ab648a5c88a91efd6b72d0092a51a9e844517d0f81cf0c0`.
- Source theorem/proof environment starts: lemma at TeX line 108, proof at TeX line 120, lemma at TeX line 252, proof at TeX line 259, theorem at TeX line 270, proof at TeX line 280, corollary at TeX line 294, proof at TeX line 309.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 46–50 | `341d06b1faca5a68f114834ab268fa8510e1f01265d5200dbb7234af9b7e9674` |
| D02 | equation | 77–81 | `ec6b3018fb1f85e6a8d6fc2e2e07491ca385e45599c4ee994508c427bfc5c6ac` |
| D03 | equation | 84–88 | `f02cdd3410ad7b5ee22c6313d075300b3299b53ed55e99ee4729233b5c920534` |
| D04 | equation | 90–93 | `ca66828131a9cfd3395ddf79e0c8c9f765e88519f7478454886e8d50c7c2a25c` |
| D05 | equation | 97–100 | `6f178c155b7c2ebcfd878a4836ae4a07510b73f5f554e44f771dce615ca080fc` |
| D06 | equation | 102–105 | `f5efb7403d1d08def7bfd3c6ae5a257cbb92e10a5097e5fce04acfb11b0f7be4` |
| D07 | \[...\] | 112–115 | `88a0d8d8d3d0221e8750062b34eacf261abfa1ed14526484a82459a9f5234c39` |
| D08 | \[...\] | 122–124 | `a111aa046c9d52af92de4190806a4ee92393167191bd798237fd206b5cc68015` |
| D09 | \[...\] | 133–137 | `8e1a1e9c0b78223478e481dad7a0cf1a0a15fdaf9b63b87535cfeeed806bc6a3` |
| D10 | \[...\] | 143–146 | `d25056d393b56e9e40792eaa65026686fbe6cdd473b954047012f7dace98c381` |
| D11 | equation | 153–157 | `6dca3023e878695bfc0caee75d3c449a014cba88fa9f8c4237d34f4762ee46c4` |
| D12 | \[...\] | 159–162 | `cfa5505df07c22f976a8dcba2c89b8fdd5b740c953909315dd7ee7a000683c39` |
| D13 | equation | 165–168 | `b45f19e3dc58f67b1e0182ab74bf125c1cdcf3aef253c7f6d04001c845c18e3c` |
| D14 | equation | 174–176 | `d617c3c662828ff5bd17871031745ec97de93cf0558fafa64dc5b8dcfe95db04` |
| D15 | equation | 179–184 | `8afee10ae43282496b70aff54456755072c28a70e0d37fb32bf80bc722411491` |
| D16 | equation | 205–208 | `21401937d7ec09019568ddee0a1da0cd1c1d7fe7a83e6453c6f8026f7202eef0` |
| D17 | equation | 216–219 | `5cdbeae5113bbf09e6c74d1e80907bf071d195ac329c763f58c121b6fede21bc` |
| D18 | \[...\] | 222–224 | `f9adfd8c5e3f3a2403c6c68c10d35a3c4e15f2d8e9ea2eb928a9d40ae44d84f8` |
| D19 | equation | 229–232 | `4c7afe46c9b6ab189d7fd1e4e940276abe598da30b2d69f17a3e953e65a460a0` |
| D20 | equation | 238–242 | `0204679a48b4c2fb3e3117ba609e068c9367eec0475bedba8b309cf803af7084` |
| D21 | equation | 245–248 | `7138865e0361d999561ad8a900c7c5552dfa7b6866697473e295ea929c8841f7` |
| D22 | \[...\] | 254–256 | `919697509a3adca587d3474cfba87213b1da699ff2656fa09f19b2e7a327ca7a` |
| D23 | \[...\] | 262–264 | `0f52ed5279af575b6072639400e4f0ee41f07bca5bab1c254d02dae57a65d97d` |
| D24 | equation | 272–277 | `be6007f701aa8e20ef0ddeaffc0d3ac7c81244bfff6d33589fc831fb7f6835be` |
| D25 | \[...\] | 284–286 | `38d7ed87bc15dd67c46504de19b7e86dadd31280c731f2ffa99cb516e1ec6d62` |
| D26 | align | 297–304 | `34cf19f60bf845bd49b61e953af1822c35c5e565217fc0755bf430caf3b6e8b4` |
| D27 | \[...\] | 312–315 | `1acbdaec95cbd740dd7ce2c4e7ea73de3eadb5c4ba9d025cfcfc3489487b47c9` |
| D28 | \[...\] | 322–324 | `234cf53d9569f536d5e1bfb0de5e752681de07af4a8dac482ad6ca491c9b701d` |
| D29 | \[...\] | 332–336 | `99a5f984f89d53f62814c496f4fd73d2653e9b558caabe52eb975c94c2e1cfee` |
| D30 | \[...\] | 354–356 | `1ba637be62e894ec98f5676f480d82450ba7bec714a16dfdf15a0ce6d3237041` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 43: `orthonormal at every admissible finite clock.  Second-order prime-density`
- TeX line 55: `the old midpoint.  This is a transverse obstruction, not an upper \(L^2\)`
- TeX line 57: `payment, and a twin-prime conclusion remain open.`
- TeX line 64: `but one scalar does not determine a vector.  The precise question here is`
- TeX line 69: `The word ''floor'' is intentional.  We prove that a finite projection is at`
- TeX line 71: `most that size.  In particular, no arithmetic \(L^2\) upper bound is hidden`
- TeX line 235: `one-jump identity; it does not discard a boundary.`
- TeX line 290: `remainder bounds after the exact combined-row cancellation; it assumes no`
- TeX line 310: `Lemma~\ref{lem:frame} gives an orthonormal family.  Therefore finite`
- TeX line 341: `\(\|\Ax\beta\|_2\), no uniform estimate over a growing Haar basis, no signed`
- TeX line 350: `The companion certificate checks the finite rational identities, source hashes,`
- TeX line 351: `curvature logarithm vectors, and exponent ledger.  Its finite beta samples are`

## Conversion limitations

- 6 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:frame` → `main.tex#L104` (existing project target or original TeX label line).
- Link relocation: `#tab:curv` → `main.tex#L191` (existing project target or original TeX label line).
- Link relocation: `#eq:divisor` → `main.tex#L167` (existing project target or original TeX label line).
- Link relocation: `#eq:betacontrasts` → `main.tex#L207` (existing project target or original TeX label line).
- Link relocation: `#lem:bq` → `main.tex#L252` (existing project target or original TeX label line).
- Link relocation: `#eq:normalform` → `main.tex#L231` (existing project target or original TeX label line).
- Link relocation: `#eq:remainders` → `main.tex#L247` (existing project target or original TeX label line).
- Link relocation: `#lem:frame` → `main.tex#L108` (existing project target or original TeX label line).
- Link relocation: `#thm:main` → `main.tex#L270` (existing project target or original TeX label line).
- Link relocation: `#lem:frame` → `main.tex#L108` (existing project target or original TeX label line).
