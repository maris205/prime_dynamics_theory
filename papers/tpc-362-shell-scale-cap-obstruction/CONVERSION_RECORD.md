# TPC-362 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `32812b1cdce93035d0883208ec2e457ab4129f27a830c2f778b07fbd1d80be43`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `bad977d5412bdb53c548f896befcc99f2e697752d8b212af98d1251c775ff910`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `bd1be24bc450ac0ab02d7262c59784a16d07ae9d87098e1d97c71c990be2b98c`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [notes/route_evaluation.md](notes/route_evaluation.md), [experiments/protocol.md](experiments/protocol.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 36 | 1 | `HEADING_TEXT_MATCH` |
| `Finite operator and envelopes` | 49 | 1 | `HEADING_TEXT_MATCH` |
| `Protocol` | 78 | 1 | `HEADING_TEXT_MATCH` |
| `Results` | 96 | 2 | `HEADING_TEXT_MATCH` |
| `Audits and exact anchor` | 144 | 2 | `HEADING_TEXT_MATCH` |
| `Claim firewall and route decision` | 159 | 2 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 184 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `39` before writing and `39` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `7`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `3df5b46e29676b6290381dc95c0679f315f62a29aec84ad4886d22b046f5c816`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 52–57 | `f8797497f668f47bc3a56fad52b71277bfbd033a737b84872466f06e994d1b4a` |
| D02 | equation | 61–66 | `afc9f5c04fa4c97982b085d1ab87390cda09207a62da83f651339a9e1e581cb4` |
| D03 | equation | 69–74 | `afdcc5a2512cee54c234276027490ee1ea82f35ced13c420f03126f0d3d46553` |
| D04 | \[...\] | 81–83 | `3db3c46edfa0292615344b3f820acf6f93ea92f4b77cf5bf95b9efd6c95d87ec` |
| D05 | \[...\] | 85–88 | `402fc55cefa08139994ef620eb817d04708fdb4f42dc43b99139d98cc1014f50` |
| D06 | \[...\] | 123–125 | `141fed7316eebe8a7604a99ade99bfd9137b6984e5229fea5d35a1c43b76505f` |
| D07 | \[...\] | 127–129 | `bda43cac935ed04227878659c55b03fd8d35bf5d7518f8b5e4701d2e3cc9d1ab` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 9: `\title{A Shell-Scale Obstruction to a Finite\`
- TeX line 22: `We test the missing shell-scale quantifier in a finite normalized`
- TeX line 32: `a finite, scoped shell-scale obstruction, not an asymptotic theorem or an`
- TeX line 38: `TPC-361 independently reproduced a finite normalized cap on a new high-origin`
- TeX line 40: `different quantifier untested: uniformity as the prime shell itself grows.`
- TeX line 43: `finite cap stops transferring; it is not evidence for a twin-prime theorem.`
- TeX line 49: `\section{Finite operator and envelopes}`
- TeX line 68: `character, and a half-shell split.  For each finite real matrix $T$,`
- TeX line 75: `These inequalities are exact finite facts.  The numerical caps below are`
- TeX line 76: `working finite benchmarks inherited from the previous anchor range.`
- TeX line 139: `but not universally, the largest finite law.  Across the 336 adjacent $Q$`
- TeX line 142: `does not reduce to a choice of one exceptional count ladder.`
- TeX line 157: `an exact finite sanity check and does not affect the high-$Q$ conclusion.`
- TeX line 161: `The envelope inequalities in \eqref{eq:envelope} are proved for finite`
- TeX line 162: `matrices.  The following statuses deliberately separate the finite positive`
- TeX line 166: `TPC362_SHELL_SCALE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_384_ROWS`
- TeX line 167: `TPC362_FINITE_SCHUR_ENVELOPE = PROVED_EXACT_FINITE`
- TeX line 168: `TPC362_FINITE_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE`
- TeX line 169: `TPC362_LOW_Q_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 171: `TPC362_LAW_WINNER_CENSUS = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 172: `TPC362_GROWING_OPERATOR_BOUND = OPEN`
- TeX line 173: `TPC362_SOURCE_UNIFORM_L2 = OPEN`
- TeX line 176: `TPC362_FULL_GATE_B = OPEN`
- TeX line 180: `The high-$Q$ observation is scoped to the declared finite operator and does`
- TeX line 186: `The shell ladder locates a sharp finite route obstruction: the normalized cap`
- TeX line 187: `that survives the independent high-origin replication is not shell-uniform.`
- TeX line 189: `row geometry, then test any proposed repair under an equally explicit finite`
- TeX line 190: `holdout.  A growing masked-operator bound, source-uniform arithmetic $L^2$,`
- TeX line 192: `open.`
- TeX line 197: `\texttt{TPC362\_FULL\_GATE\_B=OPEN}.`

## Conversion limitations

- No PROOF_PACKAGE.md is present; no proof-package review is claimed.

- Link relocation: `#tab:q` → `main.tex#L104` (existing project target or original TeX label line).
- Link relocation: `#eq:envelope` → `main.tex#L73` (existing project target or original TeX label line).
