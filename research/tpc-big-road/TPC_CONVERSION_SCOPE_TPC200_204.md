# TPC200–204 conversion and bounded prerequisite audit

Updated 2026-09-08. Preserved source commit:
`ab23455ba941e5a14ded27d49de0e874aee811ac`. Five existing manuscripts only;
no new paper, original-source repair, theorem, or publication release.

## Mechanical evidence and limits

The conversion preflight retains 132 math nodes and 18 raw displayed-
equation blocks over 12 preserved PDF pages. All five source locks and full
abstract/body formula and normalized-text roundtrips pass. Original TeX,
invoked bibliography and PDF hashes, display catalogues and original-line/
PDF-heading matches are retained in the per-paper conversion records.
All automatic source-section headings in this batch have unique matches;
that is location evidence, not PDF/source synchronization certification.

Root-layout manuscripts keep their main.tex, references.bib and exact
directory-basename PDF in place. Reading layers use paper/main.md and
relative links back to those originals. No source is copied or moved.

All five manuscripts lack a separate PROOF_PACKAGE.md. Available notes,
where present, are limited source context and not substitute proof receipts.
Full semantic validation and reliable-full-md status remain unearned.

## Independent source-reading scope

Read-only task `tpc-maintenance-source-scope-200-204-20260908` returned
`SCOPED_ARCHIVE_REVIEW_ONLY`, with no archive-level fatal mismatch and no
changed files. It fully read 15 original text files, 1,120 LF-delimited
lines: each of the five directories' README.md, complete root main.tex,
and invoked root references.bib. No child TeX is invoked. Separate proof
packages and the three optional source/theorem/route notes are absent.
All 20 original text/PDF files matched their baseline Git blobs. The five
exact directory-basename PDFs were fully extracted to stdout: 12 pages.

The sorted 20-original hash-ledger digest is
`28d7c2ac140d728f3911f5c8ea36749c7aafda98922770b535640aa7cb0c7fb8`.
Its serialization is repository-relative path, TAB, lowercase SHA-256 and
LF, sorted with LC_ALL=C; this differs from the hash-first serialization in
some older batch audits. Per-paper conversion records separately retain
the TeX, bibliography and PDF hashes. Initial/closing HEAD matched the
declared source commit, and the worktree handoff matched task hash
`865fac58c7f4e8a7b599102f1adf1cebc4bc2307f162dc79edcd6d2b166ecaa0`.
AGENTS.md was fully read; handoff content reading was restricted to the
declared header and current TPC418 section. The independent reviewer saw
the parent's newly added layout-test path, not an unexplained source edit.

## Per-paper premises and source qualifications

Here source-backed means present in the inspected original, not independently
proved by this archive review. Imported papers, source payloads and numerical
certificates were not opened or executed.

| Paper and original source | Required scope retained |
|---|---|
| [TPC200 determinant table](../../papers/tpc-200-four-form-determinant-resonance-refinement/main.tex#L34) | Positive integral slopes a,s; q=as; su−ad=2; determinant orientation m_i b_j−m_j b_i. Uniqueness of the zero determinant additionally needs positive integral h and positive odd q. The variable correlation shift h is not automatically the fixed physical h0. |
| [TPC201 absorption](../../papers/tpc-201-degenerate-shift-fejer-absorption/main.tex#L34) | V>0, E>0, p=V²/(NE); V=0 is handled separately. The imported inequality has 1≤H≤N; the absorption theorem needs 3≤H≤N. The signed off-diagonal sum has Fejer weights and a positive part, not a license to replace cancellation by unrelated absolute bounds. |
| [TPC202 theorem record](../../papers/tpc-202-new-primary-double-selector-gate/main.tex#L34) | The recorded phase supremum is outside the origin integral; both 1/X and 1/h remain. The shift-average record has k≥2, X≥H≥10, factor H^{−(k−1)}, and outer factor k. Averaged origin/shift bounds do not select prescribed production data. |
| [TPC203 route decision](../../papers/tpc-203-mvp10-direct-pointwise-route-decision/main.tex#L34) | Formula completion is per resolved symbolic packet only. Global H1, selected pointwise cancellation and direct production-crosswalk gaps are distinct. Direct, metric, bad-endpoint, structural and declared-corpus reopen triggers cannot be merged. |
| [TPC204 registry census](../../papers/tpc-204-source-locked-production-registry-crosswalk/main.tex#L44) | Seven production fields must belong to one record: atom, schedule, common ranges, uniform C, positive exponent, target normalization and full losses. Nine candidate identities and their three formula-crosswalk cells remain separate; the stop is limited to the declared corpus. |

### TPC200–201: inherited coefficient and degeneracy conditions

TPC200's [abstract](../../papers/tpc-200-four-form-determinant-resonance-refinement/main.tex#L19)
and [README](../../papers/tpc-200-four-form-determinant-resonance-refinement/README.md#L5)
compress away su−ad=2, which is explicit in the full determinant theorem.
Its “every other positive shift” wording remains in the positive-odd-q
branch. Literal coefficient masks, outer weights, z support/prefix ordering,
and the integer/positivity domain of d,u,z needed for Möbius evaluation are
not locally supplied. The source explicitly leaves a growing nondegenerate
four-Möbius correlation bound missing; the fixed-h0=2 data do not pay it.

TPC201 does not locally define A_z, S(alpha), or C(h), so support,
zero-extension, conjugation and ordering stay imported prerequisites.
The [proof](../../papers/tpc-201-degenerate-shift-fejer-absorption/main.tex#L71)
bounds the exceptional charge by 4/(Hp), the diagonal by 2/(Hp), and keeps
the remaining normalized positive-part term. The parent spot-checked these
literal factors. No growing uniform cancellation, common X/N/q regime or
strict 1/400 loss payment is inferred from finite absorption.

### TPC202–203: theorem records and route labels are not receipts

TPC202 records an external Menon theorem and labels its supplement “v1,”
but the [bibliography](../../papers/tpc-202-new-primary-double-selector-gate/references.bib#L21)
has no arXiv version suffix. The upstream source was not opened or verified
in this task; the archived record is not a version-locked external check.
The parent spot-checked the recorded averaging order and normalizations,
not the truth or attribution of the imported theorem. The single-entry
array in its selector discussion remains a model illustration, not a new
arithmetic obstruction or fixed-atom theorem.

TPC203's [seven missing fields](../../papers/tpc-203-mvp10-direct-pointwise-route-decision/main.tex#L60)
prevent promoting symbolic packet completion to production completion.
The [README hardening paragraph](../../papers/tpc-203-mvp10-direct-pointwise-route-decision/README.md#L39)
and generic manuscript certificate paragraph are source statements, not
execution receipts. Its historical refusal to authorize TPC204 stays
preserved; TPC204 separately records later workflow authorization, which
itself is not theorem evidence. Metric exceptional-set avoidance, the
natural q/N direct target and bad-endpoint local increments stay distinct.

### TPC204: three domains and one-record requirements

The parent spot-checked the [three literal formulas](../../papers/tpc-204-source-locked-production-registry-crosswalk/main.tex#L92):

| Branch | Domain / summand | Normalization |
|---|---|---|
| CORE_TERMINAL_BLOCK | N<t(z)≤2N; c_z e(−alpha z) | q/N |
| CORE_CUMULATIVE_PREFIX | 0<t(z)≤T; c_z rho(z) | q/T |
| PHYSICAL_PACKET_PREFIX | z in I_{xi,X}, z≤T; A_{xi,X}(z)e(−alpha_{xi,X}z) | Unnormalized inside the outer packet sum |

Setting N=T does not turn the terminal domain into the cumulative domain.
The local c_z, t(z), packet coefficients/support, xi ranges and fixed-h0
attachment remain imported or missing; TPC200's q=as cannot be borrowed to
fill them. The 9/63/27 census, mutation counts and source-lock claims remain
unreproduced source statements. The [“fixed-atom decay is false” wording](../../papers/tpc-204-source-locked-production-registry-crosswalk/main.tex#L177)
is a status label, not a nonexistence theorem. The declared-corpus stop does
not close either O161 parent or the global architecture.

## Complete manual PDF locators

Only each exact directory-basename PDF is present among its permitted root
PDF candidates. Each extraction completed without truncation; there are no
subsections in these five manuscripts. The table maps physical PDF pages,
not rendered-page QA or a proof of TeX/PDF synchronization.

| Preserved PDF | Complete physical-page locations |
|---|---|
| [TPC200](../../papers/tpc-200-four-form-determinant-resonance-refinement/tpc-200-four-form-determinant-resonance-refinement.pdf) | p1 title/abstract, §1 L25, §2 L34 with Theorem 1/proof, §3 L68; p2 §4 L76, §5 L91, references [1]–[2]. |
| [TPC201](../../papers/tpc-201-degenerate-shift-fejer-absorption/tpc-201-degenerate-shift-fejer-absorption.pdf) | p1 title/abstract, §1 L25, §2 L34 with Theorem 1/proof; p2 §3 L80, §4 L87, §5 L102, references [1]–[3]. |
| [TPC202](../../papers/tpc-202-new-primary-double-selector-gate/tpc-202-new-primary-double-selector-gate.pdf) | p1 title/abstract, §1 L25, §2 L34, §3 L60 with Lemma 1/proof; p2 §4 L78, §5 L87, §6 L95, §7 L110, references [1]–[2]. |
| [TPC203](../../papers/tpc-203-mvp10-direct-pointwise-route-decision/tpc-203-mvp10-direct-pointwise-route-decision.pdf) | p1 title/abstract, §1 L25, §2 L34 with Theorem 1/proof; p2 §3 L67 and its five triggers, §4 L102, §5 L117, references [1]–[2]. |
| [TPC204](../../papers/tpc-204-source-locked-production-registry-crosswalk/tpc-204-source-locked-production-registry-crosswalk.pdf) | p1 title/abstract, §1 L32, §2 L50 introduction; p2 §2 floating Table 1 L60–90, §3 L92, §4 L114 through first proof paragraph L139; p3 proof continuation L141–161, §5 L163, §6 L180, references [1]–[3]; p4 references [4]–[10]. |

## Verification scope and commands

The independent reviewer used bounded rg file discovery, complete nl/cat
source reads, git blob/working-byte SHA-256 comparisons, and five pdfinfo
plus five full pdftotext -layout extractions to stdout. All command batches
returned exit 0; conditional absence checks were reported as absence, not
failed prerequisites or substitute proof receipts. Initial/closing status,
tracked diff names and the empty index were checked. The archive ledger was
rechecked unchanged; no original source edit was observed.

No scientific script, certificate payload, numerical experiment, external
source, TeX build, PDF render or release cascade was run. Source correctness,
physical attachment, full semantic Markdown review and reliable-full-md
status remain unearned.

## Independent converter layout/identity QA

Task `tpc-maintenance-layout-identity-qa-20260908` returned `ACCEPT_SCOPED`
with no files changed or fatal mismatch. It independently ran 46 named
layout/coverage/inventory/link tests and 11 additional in-memory QA groups
in each of normal and optimized modes. The parent ran all 111 named
maintenance tests in both modes; the reviewer collected that total but
did not claim to rerun the other 65 tests or the parent's 209-paper replay.

Additional groups covered 23 malformed/nonmatching basenames, 14 invalid
number/type inputs, 64 source-layout combinations, 32 PDF-selection cases,
CLI and check_paper forwarding, eight rejected batch overrides, three real
TPC207 identity boundaries, and mocked 823-row inventory/output isolation.
These are bounded cases, not general filesystem or arbitrary-TeX safety.
Selecting the missing translation directory failed before content reading
or Pandoc; promoting critical never promoted its sibling.

Real TPC200 and TPC207-critical generated-pair checks passed, retaining 31
and 170 math nodes, both complete BibTeX payloads, six original identity
checks and 44 local links without issues. All 21 actual critical-source
labels map to original lines. TPC200 has zero actual labels; root-label
mapping is tested synthetically, not claimed as an actual-source finding.
Both --check commands and every QA command returned exit 0.

The source converter, batch checker and inventory generator reviewed hashes
are respectively `d3ab049e4c387df6353d66f1687e8f08f6f7fb9269ca265c98f2d390ec0c230d`,
`28f3b1fc4c837a134fb633ef22db80b4fdb43a00dda1fadd839088cef931a73c`,
and `06d9f0eb3e0fad3f763f6532a36577ca98367b3c63fa88593f024c7848ca6693`.
The input helper remains unchanged. QA accepted source-layout/identity
wiring only; final live inventory/handoff freshness is checked separately
by the parent, not inferred from mocked integration or this verdict.

## Scientific boundary

TPC418 retains arithmetic advance `NO`, fixed-power credit `0`, full Gate B
`OPEN`, and `NONE_UNTIL_GROWING_OR_PHYSICAL_GATE_CHANGES`. Conversion
tests and archive checks do not reopen the research route or create a paper.
