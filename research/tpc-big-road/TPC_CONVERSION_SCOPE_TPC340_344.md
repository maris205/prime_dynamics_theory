# TPC340–344 conversion and bounded prerequisite audit

Updated 2026-09-07. Source lock: repository commit
`e848dbf1895cb067bad6665654a7c992406bcf65`. The complete TeX, README, and
proof package of these five existing papers were read. Original scientific
files and hand-edited materials are preserved; this creates no new paper.

## Mechanical preservation

All five full abstract/body math-sequence and normalized-text roundtrips
pass, covering 214 math nodes and 41 raw-source display blocks. The preserved
PDFs contain 17 extracted pages. Every source section in this batch has a
unique automated heading-text page match. Each paper's conversion record
contains exact source/PDF hashes, section-line/page maps, formula catalogues,
and a link to this bounded audit. These sources have no bibliography, and
none has been invented.

The read-only batch check is reproducible with:

```bash
python -B research/tpc-big-road/check_source_markdown_batch.py --first 340 --last 344
```

It checks the five reading layers/records and the updated navigation surface:
16 linked documents, 4,100 local links, and no missing-path/same-document/
source-line-anchor issues. Cross-document non-line anchors are not
independently checked by this helper.

The mechanical checks do not independently validate Pandoc's interpretation
of every TeX macro, certify PDF/TeX synchronization, or reproduce numerical
certificates. No scientific experiment, generator, or production cascade was
executed. Numerical ranges and historical `PASS` statements in the preserved
manuscripts remain source claims, not new verification results.

## Formula and prerequisite scope

| Paper | Source location | Bounded review |
|---|---|---|
| TPC340 | [two sign-free bounds](../../papers/tpc-340-schur-frobenius-hybrid-envelope/paper/main.tex#L60) | Support restriction requires `supp(x)` contained in the selected columns. The Frobenius branch then bounds the restricted operator. The row-sum branch uses a finite symmetric matrix, so its induced one- and infinity-norms agree; symmetry cannot be silently dropped in favor of a row-sum-only bound for arbitrary matrices. Taking the minimum preserves both upper bounds. Zero vectors are allowed in the inequality, but occupancy/gain ratios need nonzero denominators. The rational anchor has output energy zero and source **squared** norm two; it does not prove a response lower bound. |
| TPC341 | [projection and holdout statistic](../../papers/tpc-341-fresh-holdout-nuisance-orthogonalization/paper/main.tex#L62) | The Pythagorean identity needs the Euclidean orthogonal projector onto the specified nuisance span. The normalized residual lies in `[0,1]` only for a nonzero target; rank-deficient nuisance columns do not invalidate the exact projection identity. The held-out nuisance span excludes the omitted control, but the finite deterministic control orbit is not an independent random sample. Means and individual responses are different targets; low mean residual does not imply low held-out residual. |
| TPC342 | [same fixed projection protocol](../../papers/tpc-342-independent-fresh-holdout-reproduction/paper/main.tex#L63) | The same projector/nonzero-target conditions apply. The three new intervals and the `+2` cutoff are explicit; their largest shifted argument is 41634, below 50000. The reported empty prime-power column and effective rank two are finite source observations, not global arithmetic negligibility. Independent implementation and disjoint windows do not establish probabilistic independence. The README direction error is recorded below. |
| TPC343 | [stacked identity and additivity](../../papers/tpc-343-cross-panel-meta-certificate/paper/main.tex#L82) | Orthogonal direct-sum blocks give additive projected/residual energies. Raw pooled retention is an energy-weighted average when the total target energy is positive; equal-row scaling additionally requires each target norm nonzero. Common scaling of each row's target and nuisance columns preserves its local residual fraction, but changes the global shared fit's weights. Row-block and shared matrices are distinct spans; their coefficients or normalization cannot be interchanged. |
| TPC344 | [contrast reparameterization](../../papers/tpc-344-panel-contrast-nuisance-basis/paper/main.tex#L90) | The identities `u_1=(b+d)/2`, `u_2=(b-d)/2`, with inverses `b=u_1+u_2`, `d=u_1-u_2`, prove equality of spans even if columns are dependent. Six declared columns need not have rank six. The contrast allows coefficients shared within each panel, not arbitrary per-row coefficients. Equal-row scaling requires positive target norms. Cross-fit coefficient prediction is not orthogonal projection onto the test panel; no Pythagorean or `[0,1]` guarantee is transferred to those prediction residuals. |

## Preserved source/editorial discrepancies

- TPC340 [TeX line 53](../../papers/tpc-340-schur-frobenius-hybrid-envelope/paper/main.tex#L53)
  contains literal `qquad` without the leading backslash. The reading layer
  retains it. The README's exact-anchor prose calls two the “source norm”;
  the TeX correctly writes `||x||_2^2=2` for `x=(1,1)`. The value two is the
  squared norm, not the Euclidean norm. No original sentence is overwritten.
- TPC342 [README line 21](../../papers/tpc-342-independent-fresh-holdout-reproduction/README.md#L21)
  describes new windows as below endpoint 40096, while all listed new
  intervals start at 40097 or later. The
  [TeX panel specification](../../papers/tpc-342-independent-fresh-holdout-reproduction/paper/main.tex#L50)
  supplies the explicit endpoints. This audit follows those numbers and
  flags the prose conflict; it does not infer a different panel.
- TPC344 [README protocol](../../papers/tpc-344-panel-contrast-nuisance-basis/README.md#L32)
  writes `2 x 3 x 9 = 18 contrast projections`, although that product is 54.
  The [TeX protocol](../../papers/tpc-344-panel-contrast-nuisance-basis/paper/main.tex#L136)
  instead explicitly describes 18 contrast holdouts as nine omitted controls
  under each of two weightings. These are not 54 separate row-local
  projections. The original README and all source data remain unchanged.

The elementary identities above were checked at the stated scope. This is
not a complete source-to-producer audit, a replay of all numeric claims, or
an independent proof of the source-uniform arithmetic hypotheses.

## Coverage and route handoff

This batch raises current archive coverage to 79 `full-source-md`, 0
`reliable-full-md`, 743 `partial-or-notes`, and 1 `source-inaccessible`, out
of 823 entries. TPC340–418 now have mechanical full-source reading layers;
the aggregate math-node count is 3,431. Earlier batch notes remain dated
snapshots, not contradictory current counts.

The next existing source-priority batch is TPC335–339. The scientific endpoint
remains TPC418 with
`NONE_UNTIL_GROWING_OR_PHYSICAL_GATE_CHANGES`, arithmetic advance `NO`,
fixed-power credit `0`, and full Gate B `OPEN`. No new number is created.
