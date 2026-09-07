# TPC275–279 conversion and bounded prerequisite audit

Updated 2026-09-07. Source lock:
`225edf5e32a3a90ca64da6f3a05ec312dff962cb`. The five complete TeX
manuscripts, README files, proof packages, and bibliography sidecars were
read. Original scientific files, hand-edited materials, code, certificates,
and local build products remain unchanged.

## Conversion evidence

The five mechanical reading layers pass abstract/body formula-sequence and
normalized-text roundtrip checks: 343 math nodes and 52 raw-source display
blocks across 17 extracted PDF pages. Every source section has a unique
heading-text page match. Per-paper records give source/PDF hashes, source
line and page maps, formula catalogues, and this bounded audit scope.

All five manuscripts use inline bibliography items, retained in the reading
layers. Their unused external bibliography sidecars remain untouched;
bibliographic claims and citation keys are not independently verified.
No visual PDF certification or PDF/TeX synchronization is claimed.

No scientific producer, original stress suite, full physical or interval
replay, or publication cascade was run. Checks below are small standalone
arithmetic examples, a recount of printed labels, and bounded read-only
source-code inspection. They do not revalidate the saved numerical results.

## Per-paper formula and prerequisite review

| Paper | Source location | Bounded check and limit |
|---|---|---|
| TPC275 | [packet definitions](../../papers/tpc-275-signed-four-packet-reassembly/paper/main.tex#L81); [Gram identities](../../papers/tpc-275-signed-four-packet-reassembly/paper/main.tex#L95); [DFT](../../papers/tpc-275-signed-four-packet-reassembly/paper/main.tex#L111); [margin proxy](../../papers/tpc-275-signed-four-packet-reassembly/paper/main.tex#L155) | All packets use one linear projected operator and the same source split. Disjoint source blocks do not make the output packets orthogonal. The printed Gram/polarization theorem explicitly uses real packets; a complex extension needs real parts in the cross sum. The four-point DFT uses the unitary factor 1/2. Ratios require positive denominators, including D and G, and the proxy comparison is a squared-margin statement. |
| TPC276 | [margin theorem](../../papers/tpc-276-signed-gain-endpoint-budget/paper/main.tex#L76); [conditional compiler](../../papers/tpc-276-signed-gain-endpoint-budget/paper/main.tex#L104); [finite transfer](../../papers/tpc-276-signed-gain-endpoint-budget/paper/main.tex#L150) | W,D,G>0 give the exact squared identity, but strict improvement also requires C nonzero. Taking the positive square root needs nonnegative margin magnitudes. Compiler estimates must concern one common source and hold uniformly on an unbounded schedule; a finite gain table supplies no positive exponent. Positive scalar-margin lower bounds make division by m legitimate. Endpoint payment must remain strict after the two epsilon losses. |
| TPC277 | [geometric floor](../../papers/tpc-277-four-packet-gain-floor/paper/main.tex#L70); [cancellation coordinate](../../papers/tpc-277-four-packet-gain-floor/paper/main.tex#L90); [power obstruction](../../papers/tpc-277-four-packet-gain-floor/paper/main.tex#L113) | Positive G permits reciprocal order, and implies D>0. G≤4D is a geometric bound, not a lower bound on G. Under E≤0, 0≤kappa<1; without that sign hypothesis the full positive-G range is −3≤kappa<1. Constant signed gain, even with a strict negative cross term, does not force positive-power gain. Orthogonal nonzero equality examples require enough ambient dimension. |
| TPC278 | [sign equivalence](../../papers/tpc-278-cross-scale-gain-stability/paper/main.tex#L54); [finite table](../../papers/tpc-278-cross-scale-gain-stability/paper/main.tex#L79); [declared paths](../../papers/tpc-278-cross-scale-gain-stability/paper/main.tex#L104) | D,G>0 and G−D=2E imply the two strict sign/gain equivalences, with E=0 corresponding to r=1. Each comparison fixes N,z,s and the other named control, but changing Q changes the shell and its masks, hence the numerical operator; only the construction rule is frozen. The eight/four row census and four selected transitions are distinct descriptions. Neither asserts a growing schedule or a sampled zero. |
| TPC279 | [deficit equivalence](../../papers/tpc-279-coherence-to-gain-theorem/paper/main.tex#L65); [coherence definition](../../papers/tpc-279-coherence-to-gain-theorem/paper/main.tex#L120); [sharpness](../../papers/tpc-279-coherence-to-gain-theorem/paper/main.tex#L156); [interval transfer](../../papers/tpc-279-coherence-to-gain-theorem/paper/main.tex#L199) | D>0 defines q and Delta, while finite reciprocals require G>0. G=0 uses the separate infinite-gain convention, not ordinary division. A maximum over nonzero-norm pairs requires a nonempty pair set or an explicit empty-set convention. The equicorrelated Gram has the stated nonnegative eigenvalues; generic sharpness may require dimension four. Interval reciprocals reverse endpoints and intersections need two valid enclosures of the same quantity. |

## TPC275: real versus complex reassembly

The [proof package](../../papers/tpc-275-signed-four-packet-reassembly/PROOF_PACKAGE.md#L5)
states `G=trace(Gamma)+2 sum Gamma_jk` for finite vectors, then mentions
Hermitian pairing in its proof. The formula as printed is real-only; in
the complex case the sum must use `Re Gamma_jk`. For scalar packets
`(1,i,0,0)` under conjugate-linear-first convention, G=D=2 but the
unmodified right side is `2+2i`. Conjugating the convention only changes
the erroneous imaginary sign. The main TeX explicitly says real packets
and is not refuted by this example. Two real plus/minus norm probes also
recover only the real part of a complex inner product.

A separate real example uses `(1,2),(-2,1),(3,-1),(-1,-1)`. Direct rational
calculation gives `D=22,G=2,E=-10`; all six polarization identities hold.
The four DFT mode energies are `1/2,9/2,25/2,9/2`, summing to 22, with
four times the zero-mode energy equal to G. These are geometric examples,
not the twelve physical rows or their 72 stored probes.

The literal `qquad` strings at
[TeX lines 87–88](../../papers/tpc-275-signed-four-packet-reassembly/paper/main.tex#L87)
lack leading backslashes and remain preserved. The conservative-proxy
sentence must retain positive D,G as well as W; `m_D^2<1/16` alone is
not an upper bound on the actual squared margin.

## TPC276: strictness, square roots, and endpoint quantifiers

The final sentence of the [margin theorem](../../papers/tpc-276-signed-gain-endpoint-budget/paper/main.tex#L81)
says r>1 makes the proxy strictly conservative without excluding C=0.
Taking `W=1,D=2,G=1,C=0` satisfies the theorem's positive-denominator
hypotheses and r=2, but both squared margins are zero. Thus the identity
is correct, while the strictness sentence needs C nonzero.

The compiler's step `m=m_D sqrt(r)` assumes that the margins are
nonnegative magnitudes. An identity of squares alone does not select a
sign. The subsequent positive lower bound on m_D excludes C=0 on that
compiler's domain. If these are normalized correlations with m≤1,
an overcompensated exponent `gamma/2>eta_D` cannot coexist with the
stated lower bounds for all sufficiently large x and arbitrarily small
epsilon: choosing epsilon below the excess would force m to grow
unboundedly. This is a compatibility qualification for a normalized
realization, not a failure of the formal conditional upper estimate.

Direct fraction checks give `5/3−1997/1200=1/400`. For
`sigma=1/100,eta_D=1/50,gamma=3/100`, the effective loss is `1/200`;
choosing epsilon `1/1000` leaves payment `3/1000>1/400`. Equality at
the endpoint before epsilon loss would not suffice.

The [finite-power discussion](../../papers/tpc-276-signed-gain-endpoint-budget/paper/main.tex#L196)
must be read as denying an inferred positive exponent, not denying all
constant lower bounds. The four-packet structure itself supplies r≥1/4,
as TPC277 makes explicit. The proof package's “any positive function”
extension argument describes unconstrained finite data; a geometric
extension would also respect that constant floor. It can still stay at
constant gain outside the finite sample, so no positive-power conclusion
follows. No signed-margin intervals or threshold census were replayed.

## TPC277–278: cutoff metadata and fixed-control comparisons

TPC275 [lists comparison cutoffs](../../papers/tpc-275-signed-four-packet-reassembly/paper/main.tex#L79)
5 at N=256 and N=384; TPC277 [prints](../../papers/tpc-277-four-packet-gain-floor/paper/main.tex#L145)
6 and 7. This does not by itself invalidate the repeated gain values.
The inspected [source-weight function](../../papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/tpc268_cutoff_sensitivity_certificate.py#L235)
computes beta from N alone and uses z for the separate comparison weights.
The inspected [TPC277 energy routine](../../papers/tpc-277-four-packet-gain-floor/code/tpc277_four_packet_gain_floor_certificate.py#L123)
discards those comparison weights and uses only indices, beta, and N,H,Q,s
for the projected packets. Its [parent check](../../papers/tpc-277-four-packet-gain-floor/code/tpc277_four_packet_gain_floor_certificate.py#L238)
compares the gain, not equality of every metadata field or source margin.
This is a bounded dependency inspection, not a replay of those gains.

Geometric sharpness checks give D=4,G=16,r=1/4 for four equal unit
packets and D=G=4,r=1 for four orthogonal unit packets. Even strict
negative cross coupling is insufficient for a positive exponent: the
constant scalar family `(1,−1/2,0,0)` has D=5/4,G=1/4,E=−1/2,r=5
at every scale. Exact zero-sum packets instead have G=0 and are outside
the finite-ratio theorems.

TPC278's printed twelve sign labels recount as eight negative and four
positive. Its four displayed transitions agree with those labels; this
does not independently establish the rational signs. The [case labels](../../papers/tpc-278-cross-scale-gain-stability/code/tpc278_cross_scale_gain_stability_certificate.py#L90)
identify only N=192,256,384 as `NATURAL_CONTROL`; N=128,Q=5 is a
`SHELL_REFERENCE`, not a fourth transferred TPC277 natural control.
The clock comparison H=29 to H=32 is a change of three, not a unit
increment; “one-step” in the conclusion means one declared control move.
Changing Q moves both ends of `(Q,2Q]` and may change divisibility masks.
The fixed rule must not be confused with fixed matrix entries or packets.

Inspected code matches the locked source commit:

| File | SHA-256 |
|---|---|
| TPC268 source-weight engine | `e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3` |
| TPC277 gain producer | `90fe6ababc93f9465ad067049e404d34a14c7ae0476316cab6507155705bbe4e` |
| TPC278 stability producer | `d51096ff917278cabfa670e13118b8acaa8999aca1fc3cf4db859e44db04d5c4` |

## TPC279: empty coherence, opposite signs, and interval scope

D>0 permits exactly one nonzero packet, in which case there are no
nonzero-norm pairs. Merely saying to ignore zero pairs leaves the
maximum defining mu empty. A convention such as mu=0 for that case,
or a hypothesis of at least two nonzero packets, is needed. For
`(v,0,0,0)` with v nonzero, q=1 and the intended envelope is valid
with that convention. No convention is silently inserted into the original.

For 0≤mu≤1, the printed minimum `min(4,1+3mu)` is simply `1+3mu`;
the reciprocal maximum is similarly redundant, but correct. The
equicorrelated Gram attains the coherence envelope and its reciprocal
floor for every mu. The [proof package](../../papers/tpc-279-coherence-to-gain-theorem/PROOF_PACKAGE.md#L29)
says it attains “every bound”; the universal G≤4D bound is attained
only at mu=1, as the main TeX correctly specifies. Rational checks at
mu=0,1/3,1/2,1 verify the row-sum/eigenvalue formulas. The printed
near-cancellation example at epsilon=1/10 gives exactly
D=1141/100,G=1/100,r=1141, while absolute coherence remains one.

The [table caption](../../papers/tpc-279-coherence-to-gain-theorem/paper/main.tex#L227)
says the deficit sign is equivalent to the parent cross-term sign.
The exact relation is opposite signs: `Delta=−2E/D`. Thus eight
negative parent cross terms become eight positive deficits, while four
positive cross terms become four negative deficits. “Matching” censuses
must preserve this label reversal. The displayed table itself has that
orientation; this records a prose-reading hazard, not a reversed formula.

For a simple positive gain interval `[2,3]`, reciprocal order gives
q in `[1/3,1/2]` and Delta in `[1/2,2/3]`. Intersecting with another
valid Delta enclosure can tighten the interval but does not establish
that either starting enclosure was valid. Nonempty overlap alone does
not prove that two independently supplied values agree. Displayed
TPC279 numbers are explicitly midpoints, not outward endpoints.

The [“cross through zero” sentence](../../papers/tpc-279-coherence-to-gain-theorem/paper/main.tex#L235)
reports opposing sampled signs. Q is a discrete shell control, so
this does not locate a literal zero or prove a continuous interpolation.
A continuous clock interpolation would require its own domain and
continuity argument; it was not checked here. The literal `qquad` at
[TeX line 48](../../papers/tpc-279-coherence-to-gain-theorem/paper/main.tex#L48)
and [line 187](../../papers/tpc-279-coherence-to-gain-theorem/paper/main.tex#L187)
is preserved. The README's reproduction block includes a producer
`--write` command; it was not executed during this read-only audit.

## Coverage and continuation

This batch changes coverage from 139 to 144 mechanical full-source layers
and from 683 to 678 partial/notes entries. `reliable-full-md=0` and
`source-inaccessible=1` remain unchanged across 823 directories.
The contiguous converted TPC range is now TPC275–418, containing 7,659
math nodes with mechanical formula/text preservation checks.

This bounded prerequisite review is not independent full-content proof
verification, a new theorem, or an authorization to reopen TPC419.
TPC418's scientific handoff and STOP boundary remain unchanged.
