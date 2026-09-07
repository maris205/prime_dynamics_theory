# TPC-256 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `d1683c8f96ae1b86f2f9fcb9ba8318c9e1aaf3f6`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `fbc08044fddd1a9b692ab5c45f32b9846a6d484a5642aa672df53cd9b4dd6961`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `0189a39a77e3326d1dca1b3c2330751c11697410ecbd8b0f9b46b4d720b70ec6`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `6b771b0cdcfbed343b91ca28476fbc68fa6b565d613220213e3c82db6f7896f6`; 6 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `35e3c2eb2edabbc9bd081e5176bee54abe57aadfe694c483b4f7d7952f467794`.
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
| `Literal clock and ordered-rank geometry` | 54 | 1 | `HEADING_TEXT_MATCH` |
| `The literal beta Haar asymptotic` | 111 | 2 | `HEADING_TEXT_MATCH` |
| `Exact adjoint lanes and their estimates` | 208 | 3 | `HEADING_TEXT_MATCH` |
| `Validation, status, and remaining gate` | 381 | 5 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 447 | 6 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `143` before writing and `143` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `38`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `ef51411b78450e603c8e81ce1afd318ffc4f350ef835c1bfbc84f8b0d79b8a3b`.
- Source theorem/proof environment starts: lemma at TeX line 78, proof at TeX line 92, lemma at TeX line 117, proof at TeX line 126, lemma at TeX line 162, proof at TeX line 170, theorem at TeX line 190, proof at TeX line 200, lemma at TeX line 246, proof at TeX line 252, lemma at TeX line 262, proof at TeX line 274, proposition at TeX line 292, proof at TeX line 300, theorem at TeX line 341, proof at TeX line 357, remark at TeX line 372.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 38–42 | `f6e6ba076117e0a58a050eca6c90001e32cb9ffb465d843f76a8471ea43677d5` |
| D02 | equation | 57–60 | `d17cee89dd94d532887a894bcb7388defa09d5bc6066d201b6fcb4bbe69d511f` |
| D03 | equation | 62–65 | `3056fcb872fbe8f9b05163a293d772deaca2858a1a34d5548c7539c79294e99e` |
| D04 | equation | 66–69 | `19bd68f017b8fd0b17e19709f3694c26d3108a4c0b3234fa27640404df95de25` |
| D05 | equation | 72–75 | `c98f8aae5c0f3f14570714878f279746aafb26044d5310ef442bd04978e12e21` |
| D06 | \[...\] | 80–84 | `54ff50f6559366eaf758b1393b91195b2e741c41ef662bf90ca656a4e7c4d508` |
| D07 | equation | 86–89 | `8a4796b4a307f50aabf88ba948c9e0d30a117766eae7a4d7051b9c1a10c9b975` |
| D08 | equation | 101–104 | `6b7d60887c4ce995abf92340144a48b9c0312a6578b396a49daede40e0e35f5b` |
| D09 | equation | 105–109 | `d1f5c3539f93182acc805bc48b519b0a2a7f0e15fd4d3ef1b5d4681310d8a701` |
| D10 | equation | 119–123 | `80690b0f5a89edde2af12e1f2063ff7bb0a561601dffe053b483e0dc4222ee19` |
| D11 | \[...\] | 132–137 | `ad4a01426117582abdd1b8f8cd1d9166b85afa3730717434e850951ce3137be4` |
| D12 | \[...\] | 142–144 | `0db50026a3012bdcd03ab145a07c5970d812f0d1ccff61810f0d00c4fd01c443` |
| D13 | equation | 148–150 | `22e9ac873e60dbce73a1d14e820dcca5ec4e4866d57b501ed0943a4e63059642` |
| D14 | \[...\] | 152–155 | `78dd4c097fe09f1031ba7ba702238a737187f507c5f96ba8f3d9b235acc2e651` |
| D15 | equation | 158–160 | `8fab69641b02df22331cc76891e3b71bfc7dcdc4272dde09f81b21d43d1936d2` |
| D16 | equation | 164–167 | `c111f40732a1f45e111aa917191114033d57c5734f0f5476d69c2969b1b8a969` |
| D17 | \[...\] | 175–178 | `2c199234873a7ef5360b6d5e40d48378a2bd44860d177b1319ec7ade1e5f68df` |
| D18 | align* | 181–185 | `af8f94d9e56546ef9ead759c606cd1af4bdc04fa000aff091c3d7af949fa3992` |
| D19 | equation | 192–197 | `a2851cca8b43eaf4d767fd07451d8f55a04f36969c2d9fa50752ba851e912b64` |
| D20 | equation | 213–216 | `4bb1359d931ffec276b4a8a81fc53a013e965f554382e77c3801b8243cf6dcbe` |
| D21 | equation | 218–221 | `d766a4a7c02c8179b66fb4588be5b0827218fb09ba6d4774c20b1c11d738c286` |
| D22 | equation | 225–228 | `65b62ca66e088f482b9c8d3c3215b32bde2ef791b8bb7ad3277519d47d8ff053` |
| D23 | align | 230–240 | `2fc981d4e473d03f9f7637d4e1aa7eaa2b4f1897587a705e68175d801283e270` |
| D24 | equation | 247–249 | `e009f1676450229d33cd421c12bff2e48d4b28e1b15da8e777d617fe38decfef` |
| D25 | \[...\] | 254–257 | `fd0319e089409dd898c258de2cadb71d28c5b2b509a66f1c374ded88496bc622` |
| D26 | equation | 264–266 | `463b7b811f2d15666c27eebebca1ea3fda8eddbb37281081fb0bfabeeb6409d8` |
| D27 | equation | 268–271 | `f6f2a3b2db3a8edb43d5f34eb1dc6132f785652515d71dad5fd371bf3b04d192` |
| D28 | \[...\] | 282–285 | `7129b4d0cc5f3adcb9e05cdfea09ac950b4b3ee51326f468ab237fba50810498` |
| D29 | align | 294–297 | `1569cf24ed64dd5eb3b4fdbbc773d3162118c9917a244363ed3b25c63435675f` |
| D30 | \[...\] | 303–307 | `4fa4d607348082f956734afaa2fabfffe5f6a577825c017ec79f065d17f5ae82` |
| D31 | \[...\] | 313–317 | `876e6d5389ae37613c17c848d9effed500b01d7bff99db469959a2ae2cab6336` |
| D32 | \[...\] | 323–326 | `fbf33154557e13a05de4e04014f0ee25d20bf7d3a47abb5fbd32636f6828bcbd` |
| D33 | \[...\] | 332–335 | `1eca6f055c38b0d512ec0f10588a0642418d5ea5fa3a511d182d63760d7804c2` |
| D34 | equation | 343–348 | `1397a1fd84521a5e288c60c2ca226ee63494674e43fa7263475a285984e6957e` |
| D35 | equation | 350–354 | `3b8bd46ac793bf8cf09796b88e5ddf2c1138e08fda30bce2a4bffeebdef110f6` |
| D36 | \[...\] | 363–365 | `47384edf3f8765dff6ba7678fbe64e03b762436ccf7e2379f8f8a885a5da247a` |
| D37 | \[...\] | 389–392 | `577e45c8f98d9c304d0678bedca01edf1bd9465817724094540305ba8ffd4177` |
| D38 | align* | 434–440 | `73e97d09f4f3866d251af5dd8228b69187db698c1078e2203829258b8d3d33c7` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 79: `Uniformly for real $x$,`
- TeX line 174: `$O(1/(x\log x))$.  Uniformly for $y\in[1/2,1]$,`
- TeX line 212: `evenness is assumed.  The literal operator is \cite{v59,tpc255}`
- TeX line 267: `Moreover, uniformly for $q\leq2Q<H$,`
- TeX line 374: `be real or even.  The theorem does not say that the scalar itself is real.`
- TeX line 375: `It also does not force the unqualified principal argument to approach`
- TeX line 388: `integer and noninteger clocks.  The finite values`
- TeX line 415: `\path{TPC256_FULL_GATE_B} & \path{OPEN}\\`
- TeX line 426: `obstruction is structural: the Poisson zero does not make this lane small;`
- TeX line 430: `\paragraph{Open theorem and reusable structure.}`
- TeX line 431: `One ordered-rank Haar projection does not control the transverse/full-output`

## Conversion limitations

- 8 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:clock` → `main.tex#L59` (existing project target or original TeX label line).
- Link relocation: `#eq:rank` → `main.tex#L64` (existing project target or original TeX label line).
- Link relocation: `#eq:contrast` → `main.tex#L74` (existing project target or original TeX label line).
- Link relocation: `#lem:endpoints` → `main.tex#L78` (existing project target or original TeX label line).
- Link relocation: `#eq:pnt` → `main.tex#L149` (existing project target or original TeX label line).
- Link relocation: `#eq:F` → `main.tex#L159` (existing project target or original TeX label line).
- Link relocation: `#eq:curvature` → `main.tex#L166` (existing project target or original TeX label line).
- Link relocation: `#lem:divisor` → `main.tex#L117` (existing project target or original TeX label line).
- Link relocation: `#eq:betamain` → `main.tex#L196` (existing project target or original TeX label line).
- Link relocation: `#eq:decomp` → `main.tex#L227` (existing project target or original TeX label line).
- Link relocation: `#eq:Rhard` → `main.tex#L236` (existing project target or original TeX label line).
- Link relocation: `#eq:Rjump` → `main.tex#L239` (existing project target or original TeX label line).
- Link relocation: `#eq:BQasymp` → `main.tex#L248` (existing project target or original TeX label line).
- Link relocation: `#eq:maskbound` → `main.tex#L265` (existing project target or original TeX label line).
- Link relocation: `#eq:firstmoment` → `main.tex#L270` (existing project target or original TeX label line).
- Link relocation: `#eq:maskbound` → `main.tex#L265` (existing project target or original TeX label line).
- Link relocation: `#eq:firstmoment` → `main.tex#L270` (existing project target or original TeX label line).
- Link relocation: `#eq:rhoidentities` → `main.tex#L88` (existing project target or original TeX label line).
- Link relocation: `#eq:boundarybound` → `main.tex#L296` (existing project target or original TeX label line).
- Link relocation: `#eq:unitrow` → `main.tex#L220` (existing project target or original TeX label line).
- Link relocation: `#prop:remainders` → `main.tex#L292` (existing project target or original TeX label line).
- Link relocation: `#thm:beta` → `main.tex#L190` (existing project target or original TeX label line).
- Link relocation: `#lem:BQ` → `main.tex#L246` (existing project target or original TeX label line).
- Link relocation: `#eq:decomp` → `main.tex#L227` (existing project target or original TeX label line).
- Link relocation: `#prop:remainders` → `main.tex#L292` (existing project target or original TeX label line).
- Link relocation: `#eq:adjointmain` → `main.tex#L347` (existing project target or original TeX label line).
- Link relocation: `#eq:phase` → `main.tex#L353` (existing project target or original TeX label line).
- Link relocation: `#eq:adjointmain` → `main.tex#L347` (existing project target or original TeX label line).
- Link relocation: `#eq:phase` → `main.tex#L353` (existing project target or original TeX label line).
