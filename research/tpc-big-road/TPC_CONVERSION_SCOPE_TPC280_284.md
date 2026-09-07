# TPC280–284 conversion and bounded prerequisite audit

Updated 2026-09-07. Source lock:
`928077a9bd66c38f38bd0a9ee65d7b903ff25814`. All five complete TeX
manuscripts, README files, proof packages, and bibliography files were read.
Original scientific files, hand-edited materials, code, certificates, and
local build products remain unchanged.

## Conversion evidence

The five mechanical reading layers pass abstract/body formula-sequence and
normalized-text roundtrip checks: 364 math nodes and 50 raw-source display
blocks across 19 extracted PDF pages. Every source section has a unique
heading-text page match. Per-paper records give source/PDF hashes, source
line and page maps, formula catalogues, and this bounded audit scope.

TPC280, TPC282, and TPC284 use external BibTeX, retained in full and
hash-locked. TPC281 and TPC283 instead use inline bibliography items,
retained in the reading layers; their unused external bibliography sidecars
remain untouched. Bibliographic claims and citation keys are not independently
verified. No visual PDF certification or PDF/TeX synchronization is claimed.

No scientific producer, full physical or interval replay, original stress
suite, or publication cascade was run. The bounded checks comprise small
exact arithmetic/geometric examples and a read-only comparison of printed
TPC282–283 endpoints with the saved TPC282 result. That comparison does not
establish the validity of the saved interval construction or source operator.

## Per-paper formula and prerequisite review

| Paper | Source location | Bounded check and limit |
|---|---|---|
| TPC280 | [raw budget](../../papers/tpc-280-leakage-aware-endpoint-compiler/paper/main.tex#L51); [compiler](../../papers/tpc-280-leakage-aware-endpoint-compiler/paper/main.tex#L72); [margin](../../papers/tpc-280-leakage-aware-endpoint-compiler/paper/main.tex#L114) | X≥1, a positive source floor, and nonnegative coefficients permit division and replacement by the coarser decay exponent. Reciprocal gain requires G>0; C=0 forces G=0 and is not an ordinary reciprocal case. The margin transfer needs the inherited positive/absolute-margin convention or a common-sign identity, not only equality of squares. Uniform exponent language requires the coefficients and source floor constants to be uniform. A zero coefficient can make the minimum of the two named exponents a non-sharp summary. |
| TPC281 | [typed operator estimate](../../papers/tpc-281-arithmetic-l2-gate-b-interface-audit/paper/main.tex#L70); [output bound](../../papers/tpc-281-arithmetic-l2-gate-b-interface-audit/paper/main.tex#L80); [attachment obstruction](../../papers/tpc-281-arithmetic-l2-gate-b-interface-audit/paper/main.tex#L141) | The source/output Hilbert norms and one bounded operator must match the packet energies. Defined q requires D>0; q≤Q implies Q≥0. The operator bound squares to exponent −2σ in squared output energy. The scalar bound additionally needs readout dual norm at most one; it gives no lower attachment. The orthogonal-functional example is in real dimension two with S nonzero and is not an identification of the actual arithmetic readout. |
| TPC282 | [projection identity](../../papers/tpc-282-literal-source-attachment-audit/paper/main.tex#L78); [normalization](../../papers/tpc-282-literal-source-attachment-audit/paper/main.tex#L94); [finite theorem](../../papers/tpc-282-literal-source-attachment-audit/paper/main.tex#L118) | Equal positive block sizes give orthogonal expanded contrasts with squared norms 4b,2b,2b. The projection is self-adjoint and idempotent in the same inner product. The normalized squared attachment needs W,Y>0. Pointwise projection identities do not assert equality of independently evaluated intervals. Sign separation and interval containment are proof obligations of the original finite replay; a table caption or a hash does not discharge them. |
| TPC283 | [zeroing theorem](../../papers/tpc-283-source-attachment-stability-radius/paper/main.tex#L41); [finite radius transfer](../../papers/tpc-283-source-attachment-stability-radius/paper/main.tex#L74); [admissibility boundary](../../papers/tpc-283-source-attachment-stability-radius/paper/main.tex#L110) | For fixed nonzero S, its orthogonal hyperplane is closed and has a unique closest point. Relative distance also requires w nonzero. The quotient is the squared relative distance, not the distance. In a complex Hilbert space the printed coefficient C/Y uses the inner product linear in its first argument; conjugate-linear-first convention requires conjugating C. The zeroing perturbation changes w with S fixed and need not preserve a literal source family or a coupled change of A,beta,S. |
| TPC284 | [control map](../../papers/tpc-284-admissible-source-control-atlas/paper/main.tex#L62); [interval sign predicate](../../papers/tpc-284-admissible-source-control-atlas/paper/main.tex#L124); [finite boundary](../../papers/tpc-284-admissible-source-control-atlas/paper/main.tex#L209) | The interval-sign lemma requires a valid enclosure; strict endpoint signs exclude zero, but zero-containing intervals do not prove the underlying value is zero. Normalization additionally needs W,Y>0. The 72 rows are six baselines times two exponents times six individual controls, not all combinations of simultaneous parameter shifts. Q±1 changes both endpoints of the shell (Q,2Q]. Nonzero sampled values and discrete sign flips do not establish a continuous path or a literal zero between samples. |

## TPC280–281: reciprocals, sign, and exponent bookkeeping

TPC280 explicitly separates G=0 in the main compiler. The reciprocal and
margin identities must remain on their defined G>0 domain. In addition,
the [margin corollary](../../papers/tpc-280-leakage-aware-endpoint-compiler/paper/main.tex#L123)
takes a positive square root of an equality of squares. As a standalone
algebraic implication, `m^2=(D/G)m_D^2` and positive m_D establish a
lower bound on `|m|`, not the sign of m. For `D=4,G=1,m_D=1,m=-2`,
the squared identity holds but the positive m conclusion fails. A
nonnegative/absolute-margin definition or the inherited common orientation
must be retained explicitly; this example does not assert that the actual
upstream signed-margin definitions violate that orientation.

The collapsed `min(gamma,delta)` exponent is always a safe bound under
the nonnegative hypotheses, but need not be the best exponent if a
coefficient vanishes. With B=1, ell=0, gamma=2 and delta=0, the exact
denominator is X^-2 while the stated minimum-exponent summary is constant.
This does not contradict its inequality. Conversely, positive slower
leakage really prevents assigning it the faster main-term exponent.
All six printed rational budget rows were checked by direct substitution,
including `13/1536 <= 5/384` and `6262/234375 <= 22/375`.
The literal `qquad` at
[TeX line 165](../../papers/tpc-280-leakage-aware-endpoint-compiler/paper/main.tex#L165)
has no leading backslash and is preserved.

TPC281's displayed squared-output estimate correctly has exponent
`a-2sigma-kappa`; its [prose](../../papers/tpc-281-arithmetic-l2-gate-b-interface-audit/paper/main.tex#L130)
describing a sigma contribution to output energy must not be used to lose
the factor two. The unsquared norm has the sigma contribution. Its mixed
finite budget at X=16 checks as `3/16+1/256=49/256 <= 1/4`.
For a small real attachment example S=(3,4), the parallel and perpendicular
representatives (3,4) and (−4,3) both have norm five; their attachments
are 25 and zero. Squared attachments are 625 and zero, not 25 and zero.
No actual arithmetic operator, source estimate, or endpoint payment follows.

## TPC282: printed intervals do not enclose the saved intervals

The [printed table](../../papers/tpc-282-literal-source-attachment-audit/paper/main.tex#L141)
is captioned as outward intervals with shortened decimal display. A
read-only exact-rational comparison of its twelve rows with the
[saved canonical result](../../papers/tpc-282-literal-source-attachment-audit/results/tpc282_certificate.json)
finds:

| Compared printed interval field | Rows checked | Printed interval fails to contain saved interval |
|---|---:|---:|
| Scalar C | 12 | 12 |
| Squared normalized attachment | 12 | 9 |

For `(X,H,Q,s)=(256,38,6,2)`, the saved C interval is
`[5.4385073364,5.45158142571]`, while the table prints
`[5.43945,5.45064]`. The displayed interval is narrower at both ends,
not an outward rounding of the stored interval. The saved squared-
attachment interval is `[0.0000335599811966,0.000033723662537]`,
while the table prints `[0.00003357,0.00003372]`.
These differences do not prove that the exact underlying value lies outside
the display; they show that the display cannot stand in for the full saved
enclosure without additional evidence.

The [exact minimum fraction](../../papers/tpc-282-literal-source-attachment-audit/paper/main.tex#L125)
matches the saved weakest-row field, but equals `3.35599811966e-5`,
which rounds to `3.356e-5` at four significant figures, not the printed
`3.357e-5`. Both original fraction and decimal remain unchanged.
The inspected result matches the locked source commit, SHA-256
`58c457135a5d22c597556a8c38f6abc6458d52d78817c04542c3c3307a0b3bf3`.
No source weights, projections, interval arithmetic, or physical values
were recomputed in this comparison.

## TPC283: distance square, complex convention, and displayed upper bounds

The [README opening](../../papers/tpc-283-source-attachment-stability-radius/README.md#L7)
calls `C^2/(WY)` the relative distance. It is the squared relative
distance; the main TeX and subsequent threshold conversion use that square
correctly. For w=(3,4), S=(1,0), the nearest zeroing source is (0,4),
the distance is three, relative distance is 3/5, and squared relative
distance is 9/25. Also, `w_*` is the closest resulting source; the
perturbation itself is `w_*-w`.

The complex theorem needs an inner-product convention. Its formula is
correct with the inner product linear in the first argument. Under
conjugate-linear-first convention, take w=i and S=1, so C=−i.
The printed coefficient would give `w_*=2i`, which is not orthogonal;
using the conjugated coefficient gives zero. The magnitude/distance
formula is convention-independent. The manuscript is preserved, with
this convention requirement recorded rather than silently inserted.

The [upper-endpoint table](../../papers/tpc-283-source-attachment-stability-radius/paper/main.tex#L83)
has six decimals below the corresponding saved TPC282 upper endpoints:

| X,H,Q,s | Printed upper | Saved parent upper |
|---|---:|---:|
| 64,15,4,2 | 0.061464 | 0.0614643508731 |
| 96,20,5,1 | 0.089816 | 0.089816354497 |
| 128,24,5,1 | 0.015583 | 0.0155830604664 |
| 128,24,5,2 | 0.025142 | 0.0251421525581 |
| 192,32,6,1 | 0.00005284 | 0.0000528408798433 |
| 256,38,6,2 | 0.00003372 | 0.000033723662537 |

This is again a display-versus-saved-enclosure comparison, not a proof that
the true radius exceeds a printed number. Reading the saved parent endpoints
still gives all twelve upper endpoints below 9/100 and exactly six below
1/100. The stated 30%/10% threshold counts thus agree with those saved
records; the original interval replay remains unverified by this maintenance.

## TPC284: shell controls and discrete sign changes

The [abstract](../../papers/tpc-284-admissible-source-control-atlas/paper/main.tex#L26)
describes Q±1 as changing the lower shell endpoint. By the explicit shell
definition, it actually moves both endpoints: `(Q,2Q]` becomes
`(Q±1,2Q±2]`. For Q=4, the baseline shell is `(5,7)`;
Q−1 gives `(5)` and Q+1 gives `(7)`. This is not a perturbation with a
fixed upper endpoint. The named Q control and operator definition remain
authoritative; the abstract shorthand is not silently changed.

The [interpretive path sentence](../../papers/tpc-284-admissible-source-control-atlas/paper/main.tex#L219)
must also retain the distinction between samples and paths. Opposite signs
at two discrete samples do not identify a literal zeroing source between
them: Q and cutoff changes may be discrete, and varying parameters can
also change the output S, hence the zero-attachment hyperplane. A
continuous fixed-scalar path with opposite endpoint signs would require
continuity hypotheses and would pass through zero, even if that zero was
not sampled. The source's own finite-only remark correctly declines such
a continuous-control theorem.

Direct arithmetic checks the protocol size 72 and the weakest displayed
fraction `70591945087/5000000000000000 = 1.41183890174e-5`.
The [table introduction](../../papers/tpc-284-admissible-source-control-atlas/paper/main.tex#L156)
mentions displayed rho-squared intervals, but the seven-column sign-flip
table has no such interval column. It lists baseline parameters and the
control label, not already shifted H/Q values. These presentation limits
do not revalidate or refute the saved 72-row physical census.

## Coverage and continuation

```bash
python -B research/tpc-big-road/check_source_markdown_batch.py --first 280 --last 284
```

The new total is 139 `full-source-md`, 0 `reliable-full-md`, 683
`partial-or-notes`, and 1 `source-inaccessible`, across 823 entries.
TPC280–418 now have mechanical reading layers with 7,316 math nodes.
Earlier scope notes remain historical batch snapshots.

Next existing-source batch: TPC275–279. TPC418's scientific stop remains
`NONE_UNTIL_GROWING_OR_PHYSICAL_GATE_CHANGES`, with arithmetic advance
`NO`, fixed-power credit `0`, and full Gate B `OPEN`. Conversion creates
no new number, original-source correction, theorem, or route reopening.
