# TPC315–319 conversion and bounded prerequisite audit

Updated 2026-09-07. Source lock:
`b9723facc6f4c261e20e0d86513230e5351dfe4d`. All five complete TeX
manuscripts, README files, proof packages, and bibliography sidecars were
read. Original manuscripts, hand-edited summaries, scientific code, and
certificates are unchanged.

## Conversion evidence

The five full-source reading layers pass the declared abstract/body
formula-sequence and normalized-text roundtrip checks: 330 math nodes and
44 raw-source display blocks. The preserved PDFs have 18 extracted pages,
with unique heading-text matches for every source section. Per-paper
records contain source/PDF hashes, section lines, page maps, formula
catalogues, conversion limits, and a link to this audit.

TPC315–317 use external BibTeX, retained in full and hash-locked with
unresolved citation keys explicit. TPC318–319 have in-source bibliography
entries; their unused sidecars remain untouched. No outside bibliographic
verification is claimed. No source producer, numerical certificate checker,
large rational anchor, eigensolver, or production cascade was run. The
limited code inspection and elementary arithmetic checks below are not
reproduction of the source's published numerical results.

Mechanical conversion does not certify visual PDF quality, PDF/TeX build
synchronization, exact floating-point enclosures, or independent correctness
of the source mathematics.

## Per-paper formula and prerequisite review

| Paper | Source location | Bounded check and limit |
|---|---|---|
| TPC315 | [weighted Gram and normalizer](../../papers/tpc-315-fresh-source-locked-weight-holdout/paper/main.tex#L98); [Gray update](../../papers/tpc-315-fresh-source-locked-weight-holdout/paper/main.tex#L122); [logarithm enclosure](../../papers/tpc-315-fresh-source-locked-weight-holdout/paper/main.tex#L135) | The weighted identity is finite real Gram algebra; a nonzero output component and positive weights make the diagonal normalizer positive. Common weight scaling cancels quadratically. Gauge reduction needs a nonempty shell, and the displayed one-bit update uses a symmetric Gram and the pre-flip sign. The atanh remainder bound needs `0<=z<1`; range reduction gives `z<1/3` for the reduced prime and `z=1/3` for log 2. Its interval must be multiplied by the integer `k`, then added to the reduced interval. Rational outward rounding and division require valid input enclosures and a denominator interval strictly above zero. The target minimizes the unweighted Gram, not necessarily each weighted objective. A locked weight menu does not remove target/Gram dependence. |
| TPC316 | [Frobenius inequality](../../papers/tpc-316-literal-arithmetic-l2-fresh-panel/paper/main.tex#L104); [residue count](../../papers/tpc-316-literal-arithmetic-l2-fresh-panel/paper/main.tex#L130); [coordinate witness](../../papers/tpc-316-literal-arithmetic-l2-fresh-panel/paper/main.tex#L173) | Rowwise Cauchy–Schwarz holds for any finite source vector; source normalization requires a nonempty interval. For the stated `m_delta=N-abs(delta)` count, restrict to `0<abs(delta)<N`, as the final sum does. If `p` divides the difference, the two excluded endpoint residue classes coincide; otherwise they are disjoint, with no double subtraction. The coordinate witness bounds the squared operator norm from below, and the Frobenius mass bounds it above. Five sampled columns are neither the maximum over all columns nor the induced norm. A large upper/lower witness ratio measures an unresolved sandwich, not a condition number or a proved ratio to the true norm. |
| TPC317 | [Schatten chain](../../papers/tpc-317-schatten-four-prime-shell-compression/paper/main.tex#L100); [entrywise trace square](../../papers/tpc-317-schatten-four-prime-shell-compression/paper/main.tex#L141) | PSD spectral calculus proves the non-strict chain, including for a zero matrix. Strict improvement over the Frobenius coefficient requires at least two positive eigenvalues; it is not automatic from PSD. The literal finite panels do have a simple rank-two witness, detailed below. The displayed entrywise squares use real symmetry; a complex extension needs conjugates/absolute squares. The trace powers are rational for the rational matrix, but their square root need not be rational. The effective trace-rank quotient requires a nonzero Gram. Decrease of an upper envelope does not by itself prove decrease of the enclosed operator norm. |
| TPC318 | [Weyl guard](../../papers/tpc-318-top-eigenvalue-prime-shell-audit/paper/main.tex#L108); [normalization and gap interpretation](../../papers/tpc-318-top-eigenvalue-prime-shell-audit/paper/main.tex#L205) | Weyl requires two symmetric matrices of the same dimension and an actual perturbation bound. For an `N`-by-`N` matrix, the stated spectral/Frobenius/maximum-entry norm comparison is valid; solver spread alone does not establish the entrywise error. A small residual can certify proximity to some eigenvalue without identifying it as the top eigenvalue. Gap ratios require positive top eigenvalue. Because the source count doubles, raw and normalized log-base-two slopes differ by one; ratios and logarithms require positivity. A small positive relative gap signals possible sensitivity, not demonstrated eigenvector instability or an arithmetic identification. |
| TPC319 | [Ky Fan variational principle](../../papers/tpc-319-kyfan-cluster-normalization-firewall/paper/main.tex#L76); [normalization flip](../../papers/tpc-319-kyfan-cluster-normalization-firewall/paper/main.tex#L95) | Use `1<=k<=N` and rank-k orthogonal projections, not arbitrary rank-k matrices or oblique idempotents. The spectral maximum is well-defined even when tied eigenvalues make a maximizing subspace nonunique. Weyl controls the k-term mass by `k` times a valid matrix perturbation bound. Comparing raw and normalized masses needs positive paired masses and the same k; the flip is exactly the raw-ratio interval `(1,2)` when the count doubles. The cluster edge-gap needs `k<N` and `lambda_k>0`; effective cluster rank requires nonzero spectral mass. Neither a Ky Fan value nor a gap census supplies a cross-scale eigenspace identification. |

## Source qualifications and discrepancies preserved

TPC315's manuscript refers to a locked rational source rule without printing
its complete coefficient formula. Read-only inspection located the
[producer call](../../papers/tpc-315-fresh-source-locked-weight-holdout/code/tpc315_fresh_source_locked_weight_holdout.py#L403)
to the [TPC268 coefficient function](../../papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/tpc268_cutoff_sensitivity_certificate.py#L190).
That function uses `1/a` at a prime power `t=p^a` (zero otherwise), minus
the sum of `mobius(d)` over divisors `d<=c`, where `c` is the greatest
nonnegative integer with `c^400<=X^133`. The inspected engine's SHA-256 is
`e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3`, matching
the [producer's declared lock](../../papers/tpc-315-fresh-source-locked-weight-holdout/code/tpc315_fresh_source_locked_weight_holdout.py#L42).
The engine was not imported or executed, and its complete dependency chain
was not audited. This source pointer is not an identification with a
growing arithmetic coefficient or the later arbitrary-source operator.

TPC315 selects `c_minus` by the counting/unweighted Gram and then evaluates
that same sign vector under three laws. Thus the manuscript's “minimum/law”
terminology denotes the selected minimum target under another weight, not
a new exhaustive minimization for every law. The source already states
that the fresh target remains selected from its own Gram matrix. No
predictive or externally independent validation follows from menu locking.

TPC316's [difference-domain wording](../../papers/tpc-316-literal-arithmetic-l2-fresh-panel/paper/main.tex#L131)
says “nonzero signed difference” before giving `|J_delta|=N-|delta|`.
Outside the realizable range this right side can be negative; an unrestricted
version needs `max(0,N-|delta|)`. The actual Hilbert–Schmidt sum already
restricts to `0<|delta|<N`, so the qualification leaves that formula intact.

TPC317's [abstract](../../papers/tpc-317-schatten-four-prime-shell-compression/paper/main.tex#L29)
and [interpretation](../../papers/tpc-317-schatten-four-prime-shell-compression/paper/main.tex#L258)
use “strictly sharper,” while the displayed general theorem is non-strict.
For a PSD matrix, `sqrt(sum lambda_i^2)<sum lambda_i` holds exactly when
at least two eigenvalues are positive. The rank-one example `diag(4,0)`
has equality. For the actual three declared source intervals, take their
first two adjacent coordinates and, for each shell, the active prime
`29,37,59,83` respectively. Neither coordinate is divisible by that prime,
and their difference is 1. The symmetric two-coordinate prime block has
zero diagonal and nonzero off-diagonal entries, hence a nonzero 2-by-2
minor. This proves `rank(A)>=2` on all 24 rows without an eigensolver or
certificate replay, and supplies the finite-panel strictness prerequisite.
The literal missing backslash in `qquad` at
[TeX line 144](../../papers/tpc-317-schatten-four-prime-shell-compression/paper/main.tex#L144)
is retained and flagged, not silently corrected.

TPC318's [abstract inference](../../papers/tpc-318-top-eigenvalue-prime-shell-audit/paper/main.tex#L36)
and [small-gap discussion](../../papers/tpc-318-top-eigenvalue-prime-shell-audit/paper/main.tex#L219)
go beyond the gap census if read as a proof of actual eigenvector
instability. For example, `diag(1,999/1000)` has relative gap `1/1000`,
but positive scalar rescaling leaves its top eigendirection exactly fixed.
Small nonzero gaps do not remove uniqueness within one symmetric matrix.
Instability across allowed perturbations or shells requires a specified
perturbation/comparison and an eigenspace analysis; comparing the different
source dimensions additionally requires an identification map. TPC319's
[canonical-surrogate wording](../../papers/tpc-319-kyfan-cluster-normalization-firewall/paper/main.tex#L176)
has the same limitation. No arithmetic eigendirection claim is endorsed.

TPC319's [proof-package maximum](../../papers/tpc-319-kyfan-cluster-normalization-firewall/PROOF_PACKAGE.md#L8)
prints only the rank constraint. Read it with the orthogonal-projection
constraints printed explicitly in TeX. Even rank-one idempotence is
insufficient: for `G=[[1,1/2],[1/2,1]]` and the oblique projector
`P=[[1,2],[0,0]]`, one has `tr(PG)=2>F_1(G)=3/2`.
Original summary notation, including missing escapes, remains unchanged.

Several original reproduction lists mix project-relative `code/` and
`experiments/` paths with repository-relative `research/` paths. In
particular, [TPC316](../../papers/tpc-316-literal-arithmetic-l2-fresh-panel/README.md#L79)
and [TPC317](../../papers/tpc-317-schatten-four-prime-shell-compression/README.md#L68)
say to run from the project directory, but their final bridge-checker
commands need the repository root or an adjusted path. The originals are
preserved; no listed writer or checker was invoked during this maintenance.

## Bounded checks and unverified scope

Standalone exact arithmetic checked 168 small signed-difference/residue
cases on `[3,9]` and `[17,32]` for primes `2,3,5,7`; a four-state Gray
traversal and its three one-bit quadratic updates; the oblique-projection
counterexample; the 12 source-interval/shell minors valid for both
exponents; and the normalization example `3/2 -> 3/4`. The 120-term
worst-case `z=1/3` tail, including `k<=7` copies for the log-2 part,
is below `10^-36` before directed-grid rounding. This does not determine
the final accumulated interval width or validate the implementation's
rounding. The large rational and binary64 numerical certificates remain
source-reported.

TPC315's finite weighted audit has `8*3*2=48` target/law cases;
TPC316 has 16 rows and 80 coordinate probes; TPC317–319 use 24 rows,
with 16 paired scale transitions and 80 transition/k combinations for
TPC319. Source intervals are disjoint across the listed scales, not
nested. Literal entry bounds `|K|<=160` follow from the declared
positive height, exponents, prime upper bound, and centered-factor bound;
they do not by themselves validate the complete floating-point error
budget, spectral ordering, or claimed numerical interval separation.

## Coverage and handoff

```bash
python -B research/tpc-big-road/check_source_markdown_batch.py --first 315 --last 319
```

The new total is 104 `full-source-md`, 0 `reliable-full-md`, 718
`partial-or-notes`, and 1 `source-inaccessible`, across 823 entries.
TPC315–418 now have mechanical full-source reading layers with 4,797 math
nodes in total. Earlier scope notes remain historical batch snapshots.

Next existing-source batch: TPC310–314. TPC418's scientific stop remains
`NONE_UNTIL_GROWING_OR_PHYSICAL_GATE_CHANGES`, with arithmetic advance
`NO`, fixed-power credit `0`, and full Gate B `OPEN`. No new paper number,
theorem, source correction, or route reopening is authorized by conversion.
