# TPC-170 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `e7da3acfc734c6281ec49879107260dd7475a64ae68bacdd0418aa016de1610c`.
- Bibliography: [references.bib](references.bib), SHA-256 `e471150cbeefab3ccffcb9199057ab6523b83811ebd29caef1dc6d2729f90b00`.
- Preserved PDF: [tpc-170-metric-packet-corridor-return.pdf](tpc-170-metric-packet-corridor-return.pdf), SHA-256 `6590c193ac4e40a9bcf0203f598aa334f4e8179e2b907f9756b64c7ea794a640`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `182d2d05c670daf35ccfc4c8069d78ceed357ef0760313488a9bb23941a66fe6`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC170_174.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Canonical determinant-two representatives` | 67 | 1 | `HEADING_TEXT_MATCH` |
| `Prescribed packet energies` | 117 | 2 | `HEADING_TEXT_MATCH` |
| `Metric packet-corridor theorem` | 156 | 2 | `HEADING_TEXT_MATCH` |
| `A positive-power dyadic corridor` | 201 | 3 | `HEADING_TEXT_MATCH` |
| `Exact Abel return` | 246 | 3 | `HEADING_TEXT_MATCH` |
| `The fixed-atom stop` | 291 | 4 | `HEADING_TEXT_MATCH` |
| `Route decision` | 330 | 4 | `HEADING_TEXT_MATCH` |
| `Reproducible audit and conclusion` | 361 | 5 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 381 | 5 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `82` before writing and `82` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `26`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `09a36dad9282fb0a845c299016f723d2de69ee392590e02a94400fac368d99fd`.
- Source theorem/proof environment starts: lemma at TeX line 76, proof at TeX line 98, theorem at TeX line 158, proof at TeX line 177, corollary at TeX line 203, proof at TeX line 221, proposition at TeX line 258, proof at TeX line 271, proposition at TeX line 293, proof at TeX line 300.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 70–72 | `6853bd1f68fe20c2106395c22bf909e4eb44aaecd5185fa2d7df3307ed87202e` |
| D02 | equation | 78–81 | `b59b208e422f996450690821b6c57da5e8bea1eb3e41ae00e9bedee5d1ca2221` |
| D03 | \[...\] | 83–86 | `6201d2c2aca46571e0c61cc6281d9386c08686e1d441922c27fbed60aef14876` |
| D04 | equation | 88–92 | `c4b335eae1a2e7e7d84f31feeeefed76614e7a65c80f1aac7902703d79fa5c49` |
| D05 | \[...\] | 104–108 | `e8d60f4da4eb707ac33073b7f56a193c8b246af1228d33eba302496c05bb38d1` |
| D06 | \[...\] | 125–127 | `bbc0c4668ced13efdda22cd07a1dc2fe930dce70d4e482bfeb079ee09c5dac18` |
| D07 | \[...\] | 129–134 | `fb9bd5b875762616954cfaef2cd749996895b032cf26d2a185ecd92c8daf1770` |
| D08 | \[...\] | 135–139 | `65a7bd6381a45f8c55348aed72ad019cc7e087ae73af16f6f1f3d68631c95183` |
| D09 | equation | 141–152 | `9ff129806599855990d1ef9bdddb38aeda123393e3d80cd47bcf1b627be66bca` |
| D10 | equation | 160–165 | `7d5d403f55fe5f95027352ed76c6034259b5416acf6bd84b130fbe1d90983275` |
| D11 | equation | 169–174 | `1f98200f0fe55ba5bd6b5fd30d7030c4d3efed5049b2beff330e6b84d5e794eb` |
| D12 | \[...\] | 179–181 | `a8b6a581ca45434a8c5566ffbf122fc01568c3841035ce36d885c667b3d89fe9` |
| D13 | \[...\] | 183–186 | `a5a3b7cc6e3cc2934496970ff0a771a3917eb6dd33e61ac0b748f83ed56256e4` |
| D14 | \[...\] | 205–208 | `6f52c8bd484d035a7bbacb2539a703b0ed792bc36ad85f1e498ebef9592ba459` |
| D15 | \[...\] | 209–213 | `a93488e4eca1206598fe19f2f2fe82bb55102f52ba342c345dbfbc2ad1b9ce48` |
| D16 | \[...\] | 216–218 | `d660fbbe706538ce20aa30956f6b7206781150d563c68c14cc22dc7233992116` |
| D17 | \[...\] | 223–228 | `69437bf1a2c73452f9e88709d51160326f8eeeec63ede0d4986ba39f71d8b46c` |
| D18 | \[...\] | 237–240 | `886b7cf76d48937159db279fc960b4a8aca4bd2bc6fbb97701969a4fed01173b` |
| D19 | \[...\] | 249–252 | `b272327ff60130112c0210a4c1c3f8666a870edb1fb4ba2ad29f0c269e91a7a3` |
| D20 | \[...\] | 254–256 | `0c392d2cb27ac1e9c3fd99b11dd99ad2bcc9868f8aec723f1a1fc46625cecc1d` |
| D21 | equation | 260–266 | `965e11664a26bb9fe2567ee26e83844c7f81d2371e3c8464fc029484edcd1a58` |
| D22 | \[...\] | 273–278 | `25a77b3a6becb792f7e735a9fc7a0213869b286635f521d769014d5bebd3c817` |
| D23 | \[...\] | 306–308 | `de437dba0a7b962408ff3b69c9f25f62a9152f493b9c5e3fd07ebeb71b5bc57c` |
| D24 | \[...\] | 333–336 | `572d32e026b5f7798e083a6d37cac9f9ec35ec46f92eab64045e04494d55d501` |
| D25 | \[...\] | 338–345 | `9bfaade1e5d7baa1b92877b40df8d89b101273615d6c64ce754653d723636e67` |
| D26 | align* | 348–355 | `35ddcedfcc2215a5d4f402c5b3ce10189e38b83cf3adc832c6a7f9ec68b1e09b` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 39: `only uniformity cost is the explicit sum of packet energies.`
- TeX line 60: `phase} on a prescribed packet schedule.  It is not a theorem at a`
- TeX line 61: `named fixed atom, not a theorem for a phase selected separately at`
- TeX line 62: `each scale, and not uniform over undeclared coefficient packets.`
- TeX line 73: `The apparent infinity of integer solutions does not create`
- TeX line 113: `would manufacture a false infinite union.  The covariance condition`
- TeX line 120: `\(n\), let \(\mathcal P_n\) be a finite, explicit packet list.  A`
- TeX line 153: `No two packets are assumed to share a coefficient sequence.`
- TeX line 154: `Uniformity is paid by the literal sum of \eqref{eq:packetenergy}.`
- TeX line 189: `implies that almost every \(\alpha\) belongs to only finitely many`
- TeX line 214: `uniformly in declared packets.  Then for every fixed`
- TeX line 222: `Uniformly, \(D_{n,p}=O(\log X_n)\), so`
- TeX line 288: `not a claim that the missing physical weight registry supplies the`
- TeX line 293: `\begin{proposition}[Metric information does not select an atom]`
- TeX line 316: `bounded-coefficient maximal framework, not a counterexample inside`
- TeX line 319: `TPC-168's finite-registry selector firewall forbids density-one`
- TeX line 356: `The original fixed-phase nodes remain open.  Closing either requires`
- TeX line 368: `uniformity, missing packet-energy unions, duplicate B\'ezout`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 4 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:representative` → `../main.tex#L80` (existing project target or original TeX label line).
- Link relocation: `#eq:translation` → `../main.tex#L91` (existing project target or original TeX label line).
- Link relocation: `#eq:packetenergy` → `../main.tex#L151` (existing project target or original TeX label line).
- Link relocation: `#eq:packetenergy` → `../main.tex#L151` (existing project target or original TeX label line).
- Link relocation: `#eq:eventual` → `../main.tex#L173` (existing project target or original TeX label line).
- Link relocation: `#thm:bc` → `../main.tex#L158` (existing project target or original TeX label line).
- Link relocation: `#eq:summability` → `../main.tex#L164` (existing project target or original TeX label line).
- Link relocation: `#thm:bc` → `../main.tex#L158` (existing project target or original TeX label line).
- Link relocation: `#thm:bc` → `../main.tex#L158` (existing project target or original TeX label line).
- Link relocation: `#lem:translate` → `../main.tex#L76` (existing project target or original TeX label line).
- Link relocation: `#cor:power` → `../main.tex#L203` (existing project target or original TeX label line).
