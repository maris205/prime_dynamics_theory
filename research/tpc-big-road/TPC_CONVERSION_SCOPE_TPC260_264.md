# TPC260–264 conversion and bounded prerequisite audit

Updated 2026-09-07. Source lock:
`bdc7bb8c00508788363faa2db8691f1128ab3d3e`. All five complete TeX
manuscripts, README files, proof packages, and bibliography sidecars were
read. Original scientific sources, hand-edited materials, certificates,
code, and local build products remain unchanged.

## Conversion evidence

All five mechanical reading layers pass abstract/body formula-sequence and
normalized-text roundtrips: 382 math nodes and 82 raw-source display blocks
across 24 extracted PDF pages. Every source section has a unique heading-text
page match. All five manuscripts use inline bibliography items, retained in
the reading layers; unused external BibTeX sidecars remain unchanged.
TPC262's unresolved citation command is retained explicitly as code rather
than supplied with guessed citation text. No converter change was needed.

No bibliography verification, visual PDF certification, or proof of PDF/TeX
synchronization is claimed. No original producer, physical replay, stress
suite, or publication cascade was executed. The bounded checks below use
independent small rational/Gaussian-rational examples and targeted read-only
source comparisons; they do not reproduce the published 128- or 48-clock
audits. Supplemental TPC254 and TPC257 excerpts were read only for their
stated input contracts, not independently re-proved.

## Per-paper formula and prerequisite review

| Paper | Source location | Bounded check and limit |
|---|---|---|
| TPC260 | [weighted Haar frame](../../papers/tpc-260-four-packet-residual-reassembly/paper/main.tex#L91); [polygon theorem](../../papers/tpc-260-four-packet-residual-reassembly/paper/main.tex#L139); [DFT](../../papers/tpc-260-four-packet-residual-reassembly/paper/main.tex#L193) | Positive block sizes and the weighted inner product are essential to normalization. The null vector denominator is nonzero because the two displayed logarithm ratios exceed one. Polygon completion is for the explicitly collinear complex packet family with unit w and z orthogonal to w, not an arbitrary literal coefficient-constrained family. The DFT normalization is 1/2; full reassembly energy is four times mode-zero energy. Scalar projection and full vector norm are not generally equivalent observables. |
| TPC261 | [finite-lane theorem](../../papers/tpc-261-strict-endpoint-budget-compiler/paper/main.tex#L113); [budget examples](../../papers/tpc-261-strict-endpoint-budget-compiler/paper/main.tex#L151); [scaled witness](../../papers/tpc-261-strict-endpoint-budget-compiler/paper/main.tex#L200) | The lane set is fixed, finite, and nonempty; all estimates use the same x and arbitrarily small epsilon. Finite summation permits taking a common starting threshold and summing constants. The minimum strict credit is sufficient for the sum of absolute values; it is not a necessary condition for an actual signed scalar with cancellation or stronger unstated decay. Squared norm, norm, and coupling exponents must not be exchanged. |
| TPC262 | [unit projection](../../papers/tpc-262-literal-mode-zero-cross-gram/paper/main.tex#L54); [signed operator](../../papers/tpc-262-literal-mode-zero-cross-gram/paper/main.tex#L93); [phase characters](../../papers/tpc-262-literal-mode-zero-cross-gram/paper/main.tex#L162) | Odd q makes q−1 positive and gives the stated q−2 rank. Complex extensions use adjoints and modulus squares, not real transpose identities verbatim. Residue synthesis needs H nonzero; the physical convention has H>0. A real integrable profile on a fixed finite interval/shell gives a well-defined Hermitian integrated operator. Subtracting the diagonal does not preserve positivity in general. The weighted Cq output space, signed physical J, packet-output DFT, and DFT of quadratic packet energies are distinct objects. |
| TPC263 | [frame](../../papers/tpc-263-rank-three-physical-cross-gram/paper/main.tex#L55); [hybrid moments](../../papers/tpc-263-rank-three-physical-cross-gram/paper/main.tex#L89); [channel bound](../../papers/tpc-263-rank-three-physical-cross-gram/paper/main.tex#L122) | The inherited balanced rank splits have nonempty blocks once N≥4 and sizes comparable to x at large x. Arbitrary unbalanced four-block partitions would not supply the same asymptotic scaling. The H2 m=1 row bounds every active interval before forming contrasts. Multiplication with three adjoint coefficients requires the same actual operator, beta, w, frame, and clock. M,K remain fixed; no uniformity in growing M or K is supplied. |
| TPC264 | [dimension split](../../papers/tpc-264-orthogonal-residual-schur-firewall/paper/main.tex#L138); [witnesses](../../papers/tpc-264-orthogonal-residual-schur-firewall/paper/main.tex#L198); [endpoint discussion](../../papers/tpc-264-orthogonal-residual-schur-firewall/paper/main.tex#L226) | Orthogonality of P and the complex scalar field give the disk/circle classification. Fixed data must be compatible with the complement: m=0 forces a=b=0; prescribing positive residual norms in zero dimension gives no vectors. The case ab=0 has z=0, while a full zero scalar additionally needs c=0. A phase at z=0 can be chosen arbitrarily in the disk construction. Paying the residual alone does not pay an only-logarithmic center. |

## TPC260: polygon proof wording and scalar-versus-energy control

The [proof](../../papers/tpc-260-four-packet-residual-reassembly/paper/main.tex#L166)
and [proof package](../../papers/tpc-260-four-packet-residual-reassembly/PROOF_PACKAGE.md#L31)
say that rotating one side while fixing the other three fills the entire
polygon range. For four unit lengths this is false as written. If the fixed
three sides have resultant modulus r, varying the fourth gives only
`[abs(r−1),r+1]`, of width at most two, whereas the theorem's full interval
is [0,4]. The theorem's range is consistent with allowing all four phases
to vary: the phase torus is path connected and the modulus is continuous;
once the extreme configurations are available, its image fills the interval.
This identifies the insufficient one-side sentence without changing the
source or claiming a full independent polygon theorem review. At zero
modulus, an argument is undefined; the “every argument” wording applies to
positive moduli or arbitrary phase parametrizations of zero.

Independent exact checks reproduce the plus, alternating, and fourth-root
DFT energy vectors `(4,0,0,0)`, `(0,0,4,0)`, and `(0,4,0,0)`, with
input total energy four and full output energies 16,0,0. The identity
`sum_j V_j=2 Vhat_0` follows directly from the k=0 definition, not from
inversion at input index zero as the [proof wording](../../papers/tpc-260-four-packet-residual-reassembly/paper/main.tex#L216)
suggests; inversion there instead expresses V0 in terms of all modes.

The [next-target wording](../../papers/tpc-260-four-packet-residual-reassembly/paper/main.tex#L296)
calls control of `abs(<w_perp,sum V_j>)` equivalent to control of the
mode-zero/cross-Gram vector energy. In a general Hilbert space only the
Cauchy–Schwarz implication is automatic. With w_perp=(1,0) and
G=(0,L), the scalar is zero but the output squared norm is L squared,
arbitrarily large. Equivalence holds for the constructed collinear unit-w
witness, not for an arbitrary physical output. Norm control also carries
the required norm of w_perp and the square-root exponent conversion.

Exact weighted checks on block lengths (1,2,3,4), (2,3,5,7), and (8,8,8,8)
give unit normalized Haar norms, pairwise orthogonality, and zero weighted
means. These are three small fixtures, not the original 128-case audit.

## TPC261: the baseline witness is an energy witness

Fraction checks reproduce all displayed budget values, including
`1/100−1/1200=11/1200`, its strict margin `1/150`,
`1/400−1/1200=1/600`, and the local margin
`1/48−1/400=11/600`. The abstract/README phrase “only when” must be read
relative to what the declared worst-case power bounds can guarantee.
The theorem does not say that every actual function fails little-oh when
its available upper-bound description is borderline or subcritical.

For the scaled plus family, `a=x^(5/6)` gives
`norm(G)=abs(<w,G>)=4x^(5/6)` for unit w, while
`norm(G)^2=16x^(5/3)`. At x=64 these are respectively 128 and 16384,
verified with integer arithmetic. Therefore the unsquared scalar already
has a much smaller exponent than E*=1997/1200. The construction is a
baseline-scale obstruction for squared output energy; it does not by
itself demonstrate a baseline-scale scalar coupling in the same exponent
ledger. An identification/normalization map and any source-norm factor
would be required for that transfer. The manuscript's squared formulas
are preserved and correct for their declared synthetic family.

## TPC262: three different meanings of a zero mode

An exact q=5 calculation verifies `Cq^2=Cq`, zero row sums, and
`5*norm(C5 e1)^2=15/4`. On the finite interval {1,...,6} at v=0,
the independently assembled `S* C5 S−(3/4)P5` has zero diagonal,
an off-diagonal entry −1/4 between indices 1 and 2, and an entry 3/4
between indices 1 and 6. The first pair gives a negative quadratic value
on the vector supported equally at 1 and 2. Thus the centered variance
projection being positive does not make the deleted-diagonal remainder
positive. This is one small operator fixture, not the full published shell
certificate or a growing-shell check.

For X=1,Y=i, exact fourth-root arithmetic gives
`F0=2, F1=−i, F2=0, F3=i`, agreeing with the conjugate-linear-first
slot convention. The signed quadratic polarization in the manuscript
therefore selects `<w,J beta>`, not `<beta,J w>`, under its stated
Hermitian assumptions. The constant residue-class direction of Cq,
the additive integration point v=0, and packet-index Fourier mode zero
must remain distinct.

The [endpoint corollary](../../papers/tpc-262-literal-mode-zero-cross-gram/paper/main.tex#L188)
applies the ledger to D+2R. This is a conditional statement for that
energy quantity; it does not overcome the paper's own phase-character
firewall to control the V59 coupling. Even for the identity map on one
complex coordinate, take beta=epsilon,w=1/epsilon with epsilon>0 and
`Y_j=beta+i^j w`. Then
`norm(sum_j Y_j)^2=16epsilon^2`, while `<w,beta>=1`.
Exact checks at epsilon=1/2,1/4,1/16 exhibit the distinction. Small
aggregate output energy alone cannot supply the missing character bound
without control of the second input and the proper normalization.

The finite adversary uses freely selected vectors in the weighted direct
sum of Cq images; it is not an attachment of actual beta,w to the signed
operator J. Its reported endpoint numbers are algebraically consistent:
`15+2*(45/2)=60` and `15+2*(−15/2)=0`. A genuinely global estimate
must retain the signed diagonal subtraction and the actual source packets.

## TPC263: frozen input contracts and bounded composition

The inspected [TPC254 input](../../papers/tpc-254-source-backed-rank-midpoint-hybrid-mean-closure/paper/main.tex#L77)
is a nonnegative sum over m with a maximum over active integer intervals.
Its m=1 term has weight one. The stated bound consequently controls each
of the four consecutive rank blocks under the source contract, not merely
their total. Its [quantifier order](../../papers/tpc-254-source-backed-rank-midpoint-hybrid-mean-closure/paper/main.tex#L157)
keeps K fixed, then chooses fixed log strength and auxiliary parameters,
then takes sufficiently large x. No new uniform-in-K result is inferred.

The inherited [balanced rank sizes](../../papers/tpc-257-four-block-haar-transverse-norm-floor/paper/main.tex#L89)
make all four blocks comparable to x. The [operator](../../papers/tpc-257-four-block-haar-transverse-norm-floor/paper/main.tex#L213)
retains the outer prime weight, both unit masks, deleted diagonal, and
fixed smooth normalized profile. Its [adjoint coefficient statement](../../papers/tpc-257-four-block-haar-transverse-norm-floor/paper/main.tex#L270)
is explicitly complex and does not assume an even or real kernel.
TPC263 retains the conjugation needed in the cross-Gram expansion.

Under these stated inputs, the elementary exponent multiplication
`1/2+7/6=5/3` and addition of logarithmic powers are correct.
Only three terms and fixed parameters are involved. These source excerpts
locate the assumptions; they do not independently validate H2, the PNT,
the adjoint remainder bounds, or the full source-identification chain.

## TPC264: compatible dimensions and the unpaid center

The four printed residual examples with a=3/2,b=2 give
z=3,−3,0,3i and full scalars 5+i,−1+i,2+i,2+4i. Independent
Gaussian-rational checks verify their norms and nonnegative Gram
determinants. For positive a,b the zero residual scalar is permitted in
a two-dimensional complement, but not in a one-dimensional complex
complement. In a real one-dimensional complement the nonzero feasible
set would be two points rather than a complex circle.

The inspected [dimension audit](../../papers/tpc-264-orthogonal-residual-schur-firewall/code/tpc264_schur_firewall_certificate.py#L192)
checks several positive-radius disk/circle points. Its zero-complement
and zero-residual outputs are literal zero fields; they are not executions
of a general dimension/norm feasibility validator. That distinction
limits the manuscript's claim that the small audit exercises every branch.
The geometric theorem's zero cases remain directly supported by their
stated compatible-vector assumptions.

The [proof-package corollary](../../papers/tpc-264-orthogonal-residual-schur-firewall/PROOF_PACKAGE.md#L83)
calls a paid residual-radius or residual-scalar bound sufficient for full
fixed-power endpoint payment while the center is only logarithmically
small. This is insufficient. Take
`c(x)=x^(5/3)*exp(−sqrt(log x))` and residual z=0. The center is
`O_M(x^(5/3)/(log x)^M)` for every fixed M, yet for every delta>0
its ratio to `x^(5/3−delta)` tends to infinity, since
`delta*log x−sqrt(log x)` tends to infinity. Zero residual satisfies
every proposed residual upper bound, while the full scalar is still c(x).
Such data can be realized entirely in the range of a rank-three projection.
This is a generic counterexample to the stated sufficient-input claim,
not a literal V59 family or a refutation of the Schur classification.

The manuscript [says “at least one”](../../papers/tpc-264-orthogonal-residual-schur-firewall/paper/main.tex#L246),
which does not on its own promise sufficiency. The stronger proof-package
wording needs the center lane or a new whole-scalar cancellation theorem.
The later [TPC265–269 audit](TPC_CONVERSION_SCOPE_TPC265_269.md) records
TPC265's explicit two-lane requirement. TPC264's missing backslash in
`ip{w}{g_x}` at [TeX line 54](../../papers/tpc-264-orthogonal-residual-schur-firewall/paper/main.tex#L54)
is preserved without silent correction.

## Supplemental source locks and continuation

All inspected supplemental files equal the source-commit bytes:

| Artifact | SHA-256 |
|---|---|
| TPC254 source-contract excerpts | `5d1bb10430c3f56e720e62c5d58a018a2c56d7b771eb815d4e8a1127555150a6` |
| TPC257 frame/operator/asymptotic excerpts | `4b3e26cb04976f9137cb71c00e94a5aa08fb660ddbc34e79d309c49eac6a8d90` |
| TPC264 inspected finite audit code | `09d7fad2beb289b0b43567d38352c63c5aaa61bfd7dbb8fa3ffb3c072849e8ea` |

This batch raises mechanical full-source coverage from 154 to 159 and
reduces partial/notes entries from 668 to 663. The contiguous converted
range is TPC260–418, with 8,721 mechanically preserved math nodes.
Across all 823 entries, `reliable-full-md=0` and
`source-inaccessible=1` remain unchanged.

Mechanical preservation and bounded implication checks are not independent
full-content mathematical verification. No original theorem, certificate,
claim grade, or TPC418 STOP condition is changed, and no new paper number
is created. The identified source issues are recorded, not implemented as
scientific corrections.
