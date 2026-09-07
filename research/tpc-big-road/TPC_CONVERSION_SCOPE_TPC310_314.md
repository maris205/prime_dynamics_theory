# TPC310–314 conversion and bounded prerequisite audit

Updated 2026-09-07. Source lock:
`abdb8bfb644f8d81c8d74b6ac609d88d191b913b`. All five complete TeX
manuscripts, README files, proof packages, and external bibliographies were
read. Original manuscripts, hand-edited summaries, code, and certificates
are unchanged.

## Conversion evidence

The five reading layers pass the declared abstract/body formula-sequence
and normalized-text roundtrip checks: 308 math nodes and 34 raw-source
display blocks. The preserved PDFs contain 18 extracted pages; every source
section has a unique heading-text page match. Per-paper records contain
source/PDF/BibTeX hashes, section lines, page maps, formula catalogues,
conversion limits, and a link to this audit. External BibTeX is preserved
in full with unresolved citation keys explicit; no outside bibliographic
verification is claimed.

No producer, scientific checker, optimizer, large rational physical panel,
or production cascade was run. Limited read-only code inspection and
recounting of saved TPC310 labels are described below. These checks do not
independently reproduce the parent observations, declared numerical bounds,
or physical outputs. Conversion does not certify visual PDF quality,
PDF/TeX build synchronization, or full mathematical correctness.

## Per-paper formula and prerequisite review

| Paper | Source location | Bounded check and limit |
|---|---|---|
| TPC310 | [aggregate maps](../../papers/tpc-310-cross-holdout-aggregation-order/paper/main.tex#L74); [extrema and weighting identities](../../papers/tpc-310-cross-holdout-aggregation-order/paper/main.tex#L99) | Nonempty selections and positive lower denominator bounds make pooled quotients well-defined; geometric aggregation additionally requires positive ratio endpoints. Independent finite extrema means a Cartesian product of allowed choices, not statistical independence. With coupled choices, summed extrema remain outer bounds but need not be attainable. Pooled point ratios are denominator-weighted row ratios; equal-case arithmetic ratios are different. Valid input enclosures are a prerequisite, and the source explicitly retains the padded-float/non-directed parent limitation. The pair table and the midpoint interpretation have source discrepancies detailed below. |
| TPC311 | [two-stage map](../../papers/tpc-311-stratified-tau-holdout-replication/paper/main.tex#L91); [soundness](../../papers/tpc-311-stratified-tau-holdout-replication/paper/main.tex#L134) | Positivity and nonempty finite cells make the pooling and arithmetic averaging formulas well-defined. Equal weights apply between design cells, not to the profile ratios inside a pooled cell. A permutation-symmetric sum is not an equal-weight ratio mean. The two tolerance sets partition the declared three-point grid, but do not create independent physical data, statistical confidence, or externally timestamped registration. Unresolved confirmation under wider radius selection is not a strict reversal. The proof-package equal-stratum lemma needs the already-assumed positive endpoints, not merely their ordering. |
| TPC312 | [source and normalized Gram](../../papers/tpc-312-new-source-shell-separation-atlas/paper/main.tex#L60); [enumeration](../../papers/tpc-312-new-source-shell-separation-atlas/paper/main.tex#L101); [rank certificate](../../papers/tpc-312-new-source-shell-separation-atlas/paper/main.tex#L132) | Real finite output Grams are PSD, but a positive trace/nonzero output is needed for the normalized sign energy. A nonempty shell gives two-element global-sign orbits, and an `(m-1)`-bit Gray code covers their representatives. Full rational rank can be certified by valid modular reduction with invertible denominators and a nonzero modular determinant. Neither PSD nor full rank implies a unique sign minimum or an all-plus maximum; those require the source's exhaustive comparisons. The displayed cutoff 7 differs from the engine cutoff 8 at scale 640, but the added Möbius term is zero, so this discrepancy does not change these coefficients. |
| TPC313 | [profile budget](../../papers/tpc-313-outward-budget-interval-certificate/paper/main.tex#L59); [ridge dual](../../papers/tpc-313-outward-budget-interval-certificate/paper/main.tex#L84); [interval rules](../../papers/tpc-313-outward-budget-interval-certificate/paper/main.tex#L124) | With real compatible matrices, `M>0` and `rho>0` make the ridge normal matrix positive definite. Setting the nonnegative multiplier to `1/rho` and completing the square gives the displayed weak-dual lower bound; a feasible ridge vector separately supplies the upper bound. Weak duality does not assert optimality, equality, a nonnegative dual value for every rho, or feasibility of every ridge vector. First-prefix certification needs least residuals on every preceding prefix; rank-deficient normal systems cannot simply be inverted. Source-norm ratios need nonzero physical beta. Outward rounding needs correct sign-aware endpoint rules, particularly subtraction and squares crossing zero. |
| TPC314 | [weighted ratios](../../papers/tpc-314-canonical-weight-law-audit/paper/main.tex#L75); [identities and log enclosure](../../papers/tpc-314-canonical-weight-law-audit/paper/main.tex#L103) | Weighted Gram expansion and quadratic scale cancellation are finite real identities; positive weights and a nonzero output give a positive diagonal normalizer. The minimum target is inherited from the unweighted Gram, not re-optimized for each positive law. Range-reduced atanh enclosures require `0<=z<1`, with the log-2 interval multiplied by its integer factor. Valid atomic intervals, four-endpoint product extrema, and denominator intervals avoiding zero are necessary for the propagated claim. At `z=0` the series remainder is zero, not strictly positive. The prime-support identity `Lambda(p)=log p` is not identification of a full arithmetic source. |

## TPC310: table and midpoint discrepancies

The [pairwise table](../../papers/tpc-310-cross-holdout-aggregation-order/paper/main.tex#L194)
labels its columns as ordered first/second classes and then states that all
omitted categories are zero. This is inconsistent with the printed marginal
census and the saved [certificate](../../papers/tpc-310-cross-holdout-aggregation-order/results/tpc310_certificate.json).
Recounting only the 49 saved selector labels, without recomputing any scalar
ratio, gives the following discrepancies (`R=RIGHT`, `L=LEFT`, `U=UNRESOLVED`):

- For `P|A`, the six printed entries total 47. The missing `U|L` category
  has count 2. The remaining printed entries agree with the saved labels.
- For `A|G`, the saved nonzero categories are `R|R=1`, `L|R=19`,
  `L|U=13`, `U|R=6`, and `U|U=10`. The table places 19 under `R|L`
  and 13 under `R|U`, and omits the 6 `U|R` cases. Its row totals 43,
  not 49; `R|L=19` also contradicts its own zero-LEFT marginal for G.
- The `P|G` row totals 49 and agrees with the saved label census.

These recounts also agree with the certificate's stored
`payload.finite_audit.pairwise_class_counts` object and the order convention
in the [pair counter](../../papers/tpc-310-cross-holdout-aggregation-order/code/tpc310_cross_holdout_aggregation_order.py#L318).
They do not revalidate the classifications or their parent numerical inputs.
The saved `P|A` opposite-strict count remains 29; the table issue does not
by itself contradict that narrower source-reported count.

The [midpoint discussion](../../papers/tpc-310-cross-holdout-aggregation-order/paper/main.tex#L215)
calls approximately `0.5072` a full-selector pooled midpoint ratio, outside
the paper's own pooled interval `[0.2423655855,0.3112477031]`. Using exact
fractions parsed from the saved full-selector diagnostic sums, the ratio
of right-loss midpoint sum to left-loss midpoint sum is approximately
`0.2751295075`, inside that interval. Thus `0.5072` is not the ratio of
those loss midpoints and cannot be treated as a feasible pooled ratio under
the displayed bounds. A different descriptive midpoint construction would
need an explicit definition; its intended recipe is unresolved here.
The separate largest-weight percentage claims were not reproduced.

The inspected certificate matches the source commit byte-for-byte; its
SHA-256 is `5bb814e86e742752678d36925e5f719f0b7f998eac76b6c113913aa716f97866`.
Both erroneous table placements and the midpoint prose are retained in the
mechanical full text rather than silently replaced by the recount.

## Other source qualifications and discrepancies

TPC311 states that its two-stage rule
[removes loss-scale weights from the profile dimension](../../papers/tpc-311-stratified-tau-holdout-replication/paper/main.tex#L108).
Its first-stage formula still pools profile losses, so at point values it
weights each profile ratio by its left-loss denominator. Only the second
stage assigns equal weight to the resulting design-cell ratios. For
example, profile right losses `(1,10)` and left losses `(10,1)` give a
pooled ratio 1 but an equal-profile ratio mean `101/20`. The source's
later statement that profiles are treated symmetrically can describe
permutation invariance, but cannot justify equal profile-ratio weights.

TPC312's [TeX cutoff](../../papers/tpc-312-new-source-shell-separation-atlas/paper/main.tex#L60)
and all eight saved `divisor_cutoff_U` fields are 7. The
[metadata helper](../../papers/tpc-312-new-source-shell-separation-atlas/code/tpc312_new_source_shell_separation.py#L232)
returns the largest `k` with `(k+1)^400<=X^133`, whereas the actual
[coefficient engine](../../papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/tpc268_cutoff_sensitivity_certificate.py#L190)
uses the largest cutoff `c` with `c^400<=X^133`.
The [producer calls the engine](../../papers/tpc-312-new-source-shell-separation-atlas/code/tpc312_new_source_shell_separation.py#L237)
for beta, not the metadata helper. At `X=640`, exact integer comparisons
give `c=8` and `k=7`. Since `mu(8)=0`, the cutoff-7 and cutoff-8 divisor
sums agree for every t. This is therefore an off-by-one metadata/rule
description issue, not a changed coefficient or a disproved Gram result
on this fixed panel. It must not be generalized to other cutoffs where the
extra Möbius value may be nonzero. The inspected
[TPC312 certificate](../../papers/tpc-312-new-source-shell-separation-atlas/results/tpc312_certificate.json)
matches the source commit and has SHA-256
`04528d9b7381d2f1b3e1e8ff7854114752816fca49ff8779de5a07714b95224d`.

TPC313's [interval prose](../../papers/tpc-313-outward-budget-interval-certificate/paper/main.tex#L130)
says addition and subtraction combine like endpoints. For subtraction,
the enclosing interval is `[a,b]-[c,d]=[a-d,b-c]`, not `[a-c,b-d]`.
The inspected [implementation](../../papers/tpc-313-outward-budget-interval-certificate/code/tpc313_outward_budget_interval_certificate.py#L187)
negates and swaps endpoints before adding, so it implements the correct
cross-endpoint rule. For example, `[1,2]-[3,4]=[-3,-1]`; the literal
like-endpoint reading gives only `[-2,-2]` and fails containment.
The same implementation handles a square crossing zero by using lower
bound zero. TPC314's proof-package multiplication shorthand similarly
needs both the minimum and maximum endpoint products, as its TeX states.

TPC313's profile metric requires more than a positive diagonal. For example,
`[[1,1],[1,1]]` is a singular Gram with positive diagonal. The inspected
[least-squares normal solve](../../papers/tpc-313-outward-budget-interval-certificate/code/tpc313_outward_budget_interval_certificate.py#L362)
requires nonsingular `W^T W`; when that requirement holds, `W=A^T U`
has independent columns, hence U also has independent columns and `M=U^T U`
is positive definite. This supplies the needed implication for successfully
checked prefixes; the stored prefix systems were not solved again here.
The [profile construction](../../papers/tpc-313-outward-budget-interval-certificate/code/tpc313_outward_budget_interval_certificate.py#L280)
also fixes the data types: A here collects source-dependent output vectors
as columns, and W maps profile coefficients to prime-label responses. It
is not the later arbitrary-source, stacked prime/endpoint operator merely
because both papers use the letter A.

TPC310–311 use padded parent decimal intervals and explicitly do not claim
directed rounding for the underlying physical source. TPC313–314 describe
a different rational/directed interval protocol. These evidence levels
must remain distinct. Independent endpoint choices in the finite extrema
lemmas are a Cartesian-product assumption: with only the coupled choices
`(0,1)` and `(1,0)`, the total is always 1 although the marginal minimum
sum is 0 and marginal maximum sum is 2. Outer enclosure survives this
coupling, but extremum attainability does not.

## Bounded checks and coverage

Standalone exact arithmetic checked the pooling example, endpoint
subtraction example, integer cutoff comparison, and the scalar ridge case
`W=M=b=1`, `R^2=1/4`, `rho=1/2`. The latter gives
`c=2/3`, residual square `1/9`, primal `4/9`, dual `1/6`, and true scalar
budget `1/4`, confirming the direction `dual <= budget <= primal` without
claiming equality. The sign-class count is
`2*(2^5+2^8+2^11+2^14)=37440`; shell-target count is 84. Selector and
stratum counts are 49, 147 aggregates, 54 design cells, and 162 parent
observations. No physical generator or full numerical certificate was rerun.

```bash
python -B research/tpc-big-road/check_source_markdown_batch.py --first 310 --last 314
```

The new total is 109 `full-source-md`, 0 `reliable-full-md`, 713
`partial-or-notes`, and 1 `source-inaccessible`, across 823 entries.
TPC310–418 now have mechanical full-source reading layers with 5,105 math
nodes in total. Earlier scope notes remain historical batch snapshots.

Next existing-source batch: TPC305–309. TPC418's scientific stop remains
`NONE_UNTIL_GROWING_OR_PHYSICAL_GATE_CHANGES`, with arithmetic advance
`NO`, fixed-power credit `0`, and full Gate B `OPEN`. No new number,
theorem, source correction, or route reopening is authorized by conversion.
