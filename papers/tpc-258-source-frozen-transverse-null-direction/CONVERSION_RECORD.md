# TPC-258 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `d1683c8f96ae1b86f2f9fcb9ba8318c9e1aaf3f6`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `aee30ecfc8b05bd9dcc0918801374445c9e48229fc77783a24d42b51b6496281`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `ea8627dcdb1a79c023a633e90f59c809ea05c952a30577bb81aac3c3746983ac`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `8ef87cc715099b39dba45643a675f493256a1573a0cb974a6369692e1fd92527`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `4586b84fcdf5713b04821c75e99387c912e5d5147032bd61eb78b7adba5f4167`.
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
| `Question and claim boundary` | 54 | 1 | `HEADING_TEXT_MATCH` |
| `Literal clock and four-block frame` | 69 | 1 | `HEADING_TEXT_MATCH` |
| `The literal coefficient and its three curvatures` | 145 | 2 | `HEADING_TEXT_MATCH` |
| `Adjoint normal form for bounded variation` | 206 | 3 | `HEADING_TEXT_MATCH` |
| `Inherited TPC-257 floor` | 263 | 3 | `HEADING_TEXT_MATCH` |
| `TPC-258 source-frozen null cancellation` | 323 | 4 | `HEADING_TEXT_MATCH` |
| `Reproducibility and epistemic labels` | 383 | 5 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 394 | 5 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `132` before writing and `132` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `35`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `a56f67ef6f2d19c46bbd589523eee3bd1824c89c8c35604ddd849d3b996e8be8`.
- Source theorem/proof environment starts: lemma at TeX line 103, proof at TeX line 115, lemma at TeX line 247, proof at TeX line 254, theorem at TeX line 265, proof at TeX line 275, corollary at TeX line 289, proof at TeX line 304, theorem at TeX line 345, proof at TeX line 354, proposition at TeX line 367.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 44–47 | `644b8bc7a9e353ba52b44a1403388afbb18f0dffbbf97565ede0bc499531ff4c` |
| D02 | equation | 72–76 | `ec6b3018fb1f85e6a8d6fc2e2e07491ca385e45599c4ee994508c427bfc5c6ac` |
| D03 | equation | 79–83 | `f02cdd3410ad7b5ee22c6313d075300b3299b53ed55e99ee4729233b5c920534` |
| D04 | equation | 85–88 | `ca66828131a9cfd3395ddf79e0c8c9f765e88519f7478454886e8d50c7c2a25c` |
| D05 | equation | 92–95 | `6f178c155b7c2ebcfd878a4836ae4a07510b73f5f554e44f771dce615ca080fc` |
| D06 | equation | 97–100 | `f5efb7403d1d08def7bfd3c6ae5a257cbb92e10a5097e5fce04acfb11b0f7be4` |
| D07 | \[...\] | 107–110 | `88a0d8d8d3d0221e8750062b34eacf261abfa1ed14526484a82459a9f5234c39` |
| D08 | \[...\] | 117–119 | `a111aa046c9d52af92de4190806a4ee92393167191bd798237fd206b5cc68015` |
| D09 | \[...\] | 128–132 | `8e1a1e9c0b78223478e481dad7a0cf1a0a15fdaf9b63b87535cfeeed806bc6a3` |
| D10 | \[...\] | 138–141 | `d25056d393b56e9e40792eaa65026686fbe6cdd473b954047012f7dace98c381` |
| D11 | equation | 148–152 | `6dca3023e878695bfc0caee75d3c449a014cba88fa9f8c4237d34f4762ee46c4` |
| D12 | \[...\] | 154–157 | `cfa5505df07c22f976a8dcba2c89b8fdd5b740c953909315dd7ee7a000683c39` |
| D13 | equation | 160–163 | `b45f19e3dc58f67b1e0182ab74bf125c1cdcf3aef253c7f6d04001c845c18e3c` |
| D14 | equation | 169–171 | `d617c3c662828ff5bd17871031745ec97de93cf0558fafa64dc5b8dcfe95db04` |
| D15 | equation | 174–179 | `8afee10ae43282496b70aff54456755072c28a70e0d37fb32bf80bc722411491` |
| D16 | equation | 200–203 | `21401937d7ec09019568ddee0a1da0cd1c1d7fe7a83e6453c6f8026f7202eef0` |
| D17 | equation | 211–214 | `5cdbeae5113bbf09e6c74d1e80907bf071d195ac329c763f58c121b6fede21bc` |
| D18 | \[...\] | 217–219 | `f9adfd8c5e3f3a2403c6c68c10d35a3c4e15f2d8e9ea2eb928a9d40ae44d84f8` |
| D19 | equation | 224–227 | `4c7afe46c9b6ab189d7fd1e4e940276abe598da30b2d69f17a3e953e65a460a0` |
| D20 | equation | 233–237 | `0204679a48b4c2fb3e3117ba609e068c9367eec0475bedba8b309cf803af7084` |
| D21 | equation | 240–243 | `7138865e0361d999561ad8a900c7c5552dfa7b6866697473e295ea929c8841f7` |
| D22 | \[...\] | 249–251 | `919697509a3adca587d3474cfba87213b1da699ff2656fa09f19b2e7a327ca7a` |
| D23 | \[...\] | 257–259 | `0f52ed5279af575b6072639400e4f0ee41f07bca5bab1c254d02dae57a65d97d` |
| D24 | equation | 267–272 | `be6007f701aa8e20ef0ddeaffc0d3ac7c81244bfff6d33589fc831fb7f6835be` |
| D25 | \[...\] | 279–281 | `38d7ed87bc15dd67c46504de19b7e86dadd31280c731f2ffa99cb516e1ec6d62` |
| D26 | align | 292–299 | `34cf19f60bf845bd49b61e953af1822c35c5e565217fc0755bf430caf3b6e8b4` |
| D27 | \[...\] | 307–310 | `1acbdaec95cbd740dd7ce2c4e7ea73de3eadb5c4ba9d025cfcfc3489487b47c9` |
| D28 | \[...\] | 317–319 | `234cf53d9569f536d5e1bfb0de5e752681de07af4a8dac482ad6ca491c9b701d` |
| D29 | \[...\] | 326–330 | `6778bea7c9fe09498f1bdc88c5725c51b775e3ed3d02fcf57de95f0b4f0ec1e8` |
| D30 | \[...\] | 333–336 | `7486cc93c9b214cdbee2a8af2173e3a6a10425b9bcc15131cace4ca61b4ac622` |
| D31 | \[...\] | 338–343 | `7cce3663656fb2531d209917011af1539f2c58f5354b77d8939e95f3d46b3302` |
| D32 | \[...\] | 347–349 | `20606c1e61215a59d70ebe429a4b09f635a22555db6223323b241b15837a0745` |
| D33 | \[...\] | 360–363 | `5b1d84f404874c090f4381851b54f3a4baabadc11f957265b51cfd5f4e607f48` |
| D34 | \[...\] | 370–373 | `bc90dfa35764204280fb583d0d21ce65fd760fda119f2c422cb0a8e1bcf5439a` |
| D35 | \[...\] | 389–391 | `70eaa8787720eea5d1be7c19fb67a85da4f80f938364f050d87e68b7a6fb0dcc` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 51: `the strict global \(1/400\) payment, and a twin-prime conclusion remain open.`
- TeX line 58: `but a floor does not determine the direction of its leading vector.  The`
- TeX line 65: `coefficient, sign, or finite sample.  The word ''null'' refers only to the`
- TeX line 66: `leading two-coordinate diagonal.  No arithmetic \(L^2\) upper bound is hidden`
- TeX line 230: `one-jump identity; it does not discard a boundary.`
- TeX line 285: `remainder bounds after the exact combined-row cancellation; it assumes no`
- TeX line 305: `Lemma~\ref{lem:frame} gives an orthonormal family.  Therefore finite`
- TeX line 374: `This is a \textup{CONDITIONAL\_THEOREM}; it is not a fixed-power claim.`
- TeX line 379: `does not pay the strict global \(1/400\) endpoint.  It also supplies no`
- TeX line 385: `The companion certificate checks the finite rational identities, source hashes,`
- TeX line 386: `curvature logarithm vectors, and exponent ledger.  Its finite beta samples are`

## Conversion limitations

- 6 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:frame` → `main.tex#L99` (existing project target or original TeX label line).
- Link relocation: `#tab:curv` → `main.tex#L186` (existing project target or original TeX label line).
- Link relocation: `#eq:divisor` → `main.tex#L162` (existing project target or original TeX label line).
- Link relocation: `#eq:betacontrasts` → `main.tex#L202` (existing project target or original TeX label line).
- Link relocation: `#lem:bq` → `main.tex#L247` (existing project target or original TeX label line).
- Link relocation: `#eq:normalform` → `main.tex#L226` (existing project target or original TeX label line).
- Link relocation: `#eq:remainders` → `main.tex#L242` (existing project target or original TeX label line).
- Link relocation: `#lem:frame` → `main.tex#L103` (existing project target or original TeX label line).
- Link relocation: `#thm:main` → `main.tex#L265` (existing project target or original TeX label line).
- Link relocation: `#lem:frame` → `main.tex#L103` (existing project target or original TeX label line).
