# TPC295–299 conversion and bounded prerequisite audit

Updated 2026-09-07. Source lock:
`aa6a797b49ed462881998abf696440d164a0f74c`. All five complete TeX
manuscripts, README files, proof packages, and external bibliographies were
read. Original scientific files, hand-edited materials, code, certificates,
and local build products remain unchanged.

## Conversion evidence

The five mechanical reading layers pass the declared abstract/body formula-
sequence and normalized-text roundtrip checks: 410 math nodes and 55
raw-source display blocks. Their versioned original PDFs contain 18
extracted pages; every section has a unique heading-text page match.
Per-paper records contain source/PDF/BibTeX hashes, source-line maps,
formula catalogues, preserved unsupported commands, and this scope note.
All external BibTeX is retained in full; bibliography and citation keys
are not independently verified or resolved.

No scientific producer, full checker, physical Gram reconstruction,
numerical optimization, or production cascade was executed. Limited
read-only code inspection and a recount of TPC299's saved prefix metadata
are described below; these do not revalidate any source budget, spectrum,
rank certificate, or physical result. No visual PDF certification,
PDF/TeX build synchronization, or full mathematical verification is claimed.

## Per-paper formula and prerequisite review

| Paper | Source location | Bounded check and limit |
|---|---|---|
| TPC295 | [physical columns and map](../../papers/tpc-295-source-correlation-image-audit/paper/main.tex#L69); [image and least-norm claims](../../papers/tpc-295-source-correlation-image-audit/paper/main.tex#L105); [modular lemma](../../papers/tpc-295-source-correlation-image-audit/paper/main.tex#L146) | For real/rational A, nonsingularity of `G=A^T A` gives full column rank, rational inverse, surjectivity of the unrestricted correlation map, and the unique least-Euclidean-norm witness `AG^-1 b`. A is assembled from outputs for an already frozen beta; `A^T h` is not automatically the map obtained by regenerating those outputs from h. Modular nonzero determinant is sufficient only with valid rational reduction and denominators invertible modulo a field prime. One valid nonzero determinant suffices; two moduli are redundant checks. The proof's denominator-clearing residue identity omits a nonzero scaling factor, detailed below. |
| TPC296 | [cost and tradeoff](../../papers/tpc-296-source-norm-budget-interface/paper/main.tex#L93); [one-dimensional projection](../../papers/tpc-296-source-norm-budget-interface/paper/main.tex#L143); [diagnostics](../../papers/tpc-296-source-norm-budget-interface/paper/main.tex#L185) | Full column rank gives a positive-definite Gram and minimum squared norm `b^T G^-1 b`, not the unsquared norm. The cost-energy product follows from Cauchy–Schwarz; for nonzero b equality requires an eigenvector direction. The “ray” with real alpha is a full line/span, not a nonnegative half-line. Its formula requires nonzero correlation vector v; beta-normalized cost also needs beta nonzero. Normalized RMS and normalized trade product are distinct from raw squared residual and raw cost-energy product. Finite one-line failure does not exclude richer source families. |
| TPC297 | [literal profiles](../../papers/tpc-297-literal-source-profile-span-audit/paper/main.tex#L63); [projection](../../papers/tpc-297-literal-source-profile-span-audit/paper/main.tex#L99); [nesting](../../papers/tpc-297-literal-source-profile-span-audit/paper/main.tex#L123) | Orthogonal projection gives the squared least-squares residual for any finite real V, including rank deficiency. The inverse formula additionally needs full column rank; rank three in a 3-by-4 image does not justify inverting its 4-by-4 normal Gram. One may instead use an independently spanning column subset or the orthogonal projector itself. Nesting fixes the physical A and target, and requires actual source-span inclusion. Four source columns alone imply only image rank at most four. A positive-dimensional target shell makes sign-target RMS normalization meaningful. |
| TPC298 | [angle theorem](../../papers/tpc-298-profile-angle-dimension-ladder/paper/main.tex#L102); [dimension statistic](../../papers/tpc-298-profile-angle-dimension-ladder/paper/main.tex#L145); [rank versus QR scope](../../papers/tpc-298-profile-angle-dimension-ladder/paper/main.tex#L155) | The projection identity includes zero targets, but normalized residual and vector-to-subspace angle require b nonzero. Use the acute angle in `[0,pi/2]`, so monotonicity of arcsin applies. A first threshold index requires a nonempty feasible set. Rank `min(k,m)` certified by a valid nonzero modular minor reaches the dimension ceiling and hence proves rational rank; agreement of lower ranks at two primes would not generally prove exact rank. Modular rank checks at all 17 prefixes differ from numerical full-column-rank solves only through k=m. Saturated target image does not bound source cost. |
| TPC299 | [budget definition](../../papers/tpc-299-native-profile-budget-frontier/paper/main.tex#L119); [ridge/KKT proof](../../papers/tpc-299-native-profile-budget-frontier/paper/main.tex#L129); [nesting](../../papers/tpc-299-native-profile-budget-frontier/paper/main.tex#L194) | Positive-definite source Gram gives a coercive strictly convex objective, so a nonempty closed convex feasible set has one minimizer. The strict interior radius gives the positive ridge path, with its parameter reciprocal to the KKT multiplier. At the least-squares boundary one needs the minimum-source-cost least-squares solution, not an arbitrary minimizer or an unjustified inverse at rho zero. Zero-padding preserves both cost and residual for genuine source prefixes. The reported “full” budgets stop at shell dimension, not all 17 source columns on most rows. |

## TPC295: omitted modular scaling factor

The [TeX denominator-clearing proof](../../papers/tpc-295-source-correlation-image-audit/paper/main.tex#L151)
and [proof-package lemma](../../papers/tpc-295-source-correlation-image-audit/PROOF_PACKAGE.md#L20)
say that the integer `D^m det(G)` reduces to `det(G_p)`. With the
entrywise reduction specified in the statement, it instead reduces to
`(D mod p)^m det(G_p)`, since `det(DG)=D^m det(G)`. This factor is
nonzero because p avoids D, so the nonsingularity implication survives.
For the scalar Gram `G=1/4`, D=4 and p=5, `det(DG)` reduces to 1,
while `det(G_p)` is 4; multiplying by D modulo p restores 1. The
original proof line is preserved, not silently rewritten. Zero modular
residuals at two primes are separately replay checks; without an exact
argument or a magnitude bound, they alone do not prove a rational residual
is zero. The source correctly bases exact surjectivity on full rank and
the explicit inverse formula, not those residual checks alone.

## TPC296: squared norms, normalization, and notation

The [abstract](../../papers/tpc-296-source-norm-budget-interface/paper/main.tex#L34)
calls `b^T G^-1 b` the minimum source norm, whereas the definition and
theorem correctly make it the minimum **squared** norm. The unsquared
minimum is its square root. The source-cost/energy inequality uses squared
norms consistently; changing that convention would change its scale.

The [reported trade-product range](../../papers/tpc-296-source-norm-budget-interface/paper/main.tex#L247)
is compared with lower bound one, whereas the earlier unnormalized
inequality has lower bound m squared for sign targets. The inspected
[metric implementation](../../papers/tpc-296-source-norm-budget-interface/code/tpc296_source_norm_budget_certificate.py#L150)
defines `trade_product=cost*energy/m^2`; the range is thus for this
normalized product. It computes ray RMS as
`sqrt(sum(residual_i^2)/m)`, not a raw squared residual or a fourth-root
normalization. For `A=diag(1,2), b=(1,1)`, exact arithmetic gives
cost `5/4`, energy 5, raw product `25/4`, and normalized product `25/16`.
This illustrates the scale distinction without checking published values.

The TeX also has literal `qquad` without the leading backslash at
[line 79](../../papers/tpc-296-source-norm-budget-interface/paper/main.tex#L79)
and [lines 187–188](../../papers/tpc-296-source-norm-budget-interface/paper/main.tex#L187).
These source tokens remain in the mechanical layer and are not interpreted
as corrected spacing commands. The inspected metric code matches the
source commit, SHA-256
`a30fe40b88eda0f9f257c18fb4d438f129ad5d01ea70d72e54bfe2418d8e0a26`.

## TPC297–298: projection is not normalized angle or source cost

TPC297's [README opening](../../papers/tpc-297-literal-source-profile-span-audit/README.md#L13)
calls `b^T(I-P_V)b` the residual; the displayed TeX/proof identify it as
the squared residual. Its rank-four summary must retain the explicit
rank-three exception on the three-prime row. Normal-equation coefficients
need not be unique under rank deficiency, even though the projected target
always is. The claimed non-increase relative to the frozen ray requires
that actual frozen direction to lie in the four-profile span, not merely
that one space has a larger dimension.

TPC298's [theorem](../../papers/tpc-298-profile-angle-dimension-ladder/paper/main.tex#L108)
starts with every real target, but division by `||b||^2` and its angle
part need b nonzero. The finite sign targets satisfy that when the shell
is nonempty. Its abstract/README shorthand “residual is the sine” means
the **relative norm residual**, not the raw residual or its square.
For projection onto the first coordinate and target `(3,4)`, residual
squared is 16, raw norm residual is 4, relative residual is `4/5`, and
captured energy fraction is `9/25`. The identity is `16/25+9/25=1`.
At b=0, the unnormalized projection formula still holds but the quotient
and vector angle are undefined.

TPC298's 306 modular prefix checks are `18*17`. Its
[numerical protocol](../../papers/tpc-298-profile-angle-dimension-ladder/paper/main.tex#L155)
separately restricts QR solves to full-column-rank prefixes through shell
size. The k=4 zero in the three-prime representative row is consistent
with the image already being all of the target space at k=3; it does not
license a 4-column Gram inverse. Finite image saturation supplies neither
an asymptotic angle bound nor an affordable source representation.

## TPC299: retained erratum, boundary solution, and “full” prefix scope

The [README erratum](../../papers/tpc-299-native-profile-budget-frontier/README.md#L32)
and [proof-package erratum](../../papers/tpc-299-native-profile-budget-frontier/PROOF_PACKAGE.md#L69)
already record TPC300's reciprocal correction: the stored “multiplier”
is a ridge parameter rho, while the positive multiplier on the squared
constraint is mu=1/rho. The TeX still uses the same lambda for both in
its stationarity-to-ridge step. The existing correction is linked and
preserved; this maintenance does not rewrite the theorem or recalculate
the frontier.

At the [least-squares boundary](../../papers/tpc-299-native-profile-budget-frontier/paper/main.tex#L143),
positive-definite M alone does not make V full column rank. The inverse
formula at rho=0 can be singular, and an arbitrary least-squares coefficient
need not minimize source cost. With `V=(1,0), M=I, b=1, R=0`, both
`(1,0)` and `(1,1)` are exact least-squares solutions, but their costs
are 1 and 2. The boundary solution is the least-M-norm least-squares
coefficient, equivalently the appropriate rho-to-zero ridge limit. The
uniqueness theorem remains supported by coercivity and strict convexity;
the boundary recipe needs this qualification. This toy example is not a
claim that a tested full-column-rank prefix failed.

The [abstract](../../papers/tpc-299-native-profile-budget-frontier/paper/main.tex#L37)
and [README](../../papers/tpc-299-native-profile-budget-frontier/README.md#L21)
refer to using the full available 17-profile prefix. The inspected
[producer](../../papers/tpc-299-native-profile-budget-frontier/code/tpc299_native_profile_budget_frontier_certificate.py#L308)
sets `prefix_count=min(len(shell),len(PROFILE_CUTOFFS))`, and its
[full-frontier call](../../papers/tpc-299-native-profile-budget-frontier/code/tpc299_native_profile_budget_frontier_certificate.py#L349)
uses only that prefix. Recounting only the saved metadata in the
[canonical result](../../papers/tpc-299-native-profile-budget-frontier/results/tpc299_certificate.json)
gives:

| Stored full prefix k | Rows |
|---:|---:|
| 3 | 1 |
| 5 | 1 |
| 7 | 2 |
| 10 | 3 |
| 13 | 1 |
| 15 | 8 |
| 17 | 2 |

All three saved full-frontier target fields on each row use that k;
the 18 rows total 219 tested prefix entries. Thus only two rows actually
use 17 profiles. The 11/18 source-reported “full” obstruction refers to
these shell-capped prefixes and does not establish the same count after
all 17 source directions on every row.

This distinction can matter even after target-image saturation. For
`A=(1,0)^T`, source columns `u_1=(1,10)^T`, `u_2=(0,1)^T`, target 1,
and tolerance zero, the one-column target image is already the full
one-dimensional target space. Its source budget is 101. Adding u_2
permits coefficient `(1,-10)` and source `(1,0)`, lowering the budget
to 1. The two-column source Gram is positive definite. Hence full image
rank does not justify discarding additional source directions in a budget
comparison. No physical 17-profile optimization was performed here.

The metadata file matches the source commit, SHA-256
`9be51f5bcb93e3a297a70e1c12985d52aee2b74e5e3fe4a64fbf7d5a054c559e`.
The inspected TPC299 code also matches, SHA-256
`94cb7f191378698de2f08157a475586864c59bba02621e447da98f5ffbbc7279`.
These hashes and the recount protect only the stated inspection scope,
not the validity of any numerical budget or threshold label.

## Bounded checks and coverage

Standalone exact arithmetic checked the modular scaling example, the
cost/energy normalization example, the `(3,4)` projection identity,
and the two least-squares/source-budget counterexamples. No supplied
scientific stress suite or physical panel was run. Source references,
the inherited 1,380-edge metadata, numerical diagnostic thresholds,
and existing publication labels remain preserved, not endorsed as
independently re-proved or reconciled with other census definitions.

```bash
python -B research/tpc-big-road/check_source_markdown_batch.py --first 295 --last 299
```

The new total is 124 `full-source-md`, 0 `reliable-full-md`, 698
`partial-or-notes`, and 1 `source-inaccessible`, across 823 entries.
TPC295–418 now have mechanical reading layers with 6,187 math nodes.
Earlier scope notes remain historical batch snapshots.

Next existing-source batch: TPC290–294. TPC418's scientific stop remains
`NONE_UNTIL_GROWING_OR_PHYSICAL_GATE_CHANGES`, with arithmetic advance
`NO`, fixed-power credit `0`, and full Gate B `OPEN`. Conversion creates
no new number, original-source correction, theorem, or route reopening.
