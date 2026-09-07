# TPC290–294 conversion and bounded prerequisite audit

Updated 2026-09-07. Source lock:
`7bba57e68d04514ee33ab2192a507a1f4edfebab`. All five complete TeX
manuscripts, README files, proof packages, and external bibliographies were
read. Original scientific files, hand-edited materials, code, certificates,
and local build products remain unchanged.

## Conversion evidence

The five mechanical reading layers pass abstract/body formula-sequence and
normalized-text roundtrip checks: 311 math nodes, 46 raw-source display
blocks, and 20 extracted PDF pages. Every record locks the TeX, versioned
original PDF, and full external BibTeX, with source-line maps and a formula
catalogue. Citation keys and bibliographic claims are not independently
resolved or verified.

TPC292's `Finite atlas` heading has automatic candidates on pages 1, 2,
and 3; TPC293's same heading has candidates on pages 2 and 3. Both remain
`UNMAPPED_OR_AMBIGUOUS` in the automatic records. Direct inspection of
the extracted lines finds the numbered headings `6 Finite atlas` and
`5 Finite atlas`, respectively, on page 2. This is a bounded manual
supplement, not a silent rewrite of the automatic map or visual PDF QA.
All other section maps in the batch have unique heading-text matches.

TPC294 initially fails the LaTeX reader because its source has two literal
lines after the document terminator. The converter now separates only an
unambiguous standalone terminator and preserves any nonempty suffix in a
clearly labeled literal-code block, with source-line and suffix-hash scope
in the record. It neither deletes nor guesses the meaning of that text.
All 124 earlier conversion pairs remain byte-identical after this change,
with their 6,187 math nodes unchanged. All 20 converter regression tests
pass, including suffix retention, empty-tail identity, and fail-closed
multiple-terminator handling.

No physical producer, full scientific checker, Gram reconstruction, large
sign search, or publication cascade was run. The small standalone examples
below check only the stated finite algebra or source-prose qualification.
No original certificate, PDF/TeX synchronization, or complete mathematical
verification is claimed.

## Per-paper formula and prerequisite review

| Paper | Source location | Bounded check and limit |
|---|---|---|
| TPC290 | [weighted identity](../../papers/tpc-290-adaptive-shell-weighting-obstruction/paper/main.tex#L89); [effective support](../../papers/tpc-290-adaptive-shell-weighting-obstruction/paper/main.tex#L113); [policy scope](../../papers/tpc-290-adaptive-shell-weighting-obstruction/paper/main.tex#L150) | Real Gram symmetry, nonzero weights, and positive weighted diagonal denominator give the expansion. Positive component energies are a sufficient common premise. The coherence bound additionally needs nonnegative weights, a nonnegative coherence floor, and positive maximum diagonal for the ratio. For nonnegative nonzero weights, effective support lies between one and shell size. All-positive cross terms obstruct every nonnegative rule, but three tested policies do not exhaust full-support rules on the exceptional sign-flip row. |
| TPC291 | [Schur projection](../../papers/tpc-291-signed-schur-cancellation-atlas/paper/main.tex#L104); [Rayleigh minimum](../../papers/tpc-291-signed-schur-cancellation-atlas/paper/main.tex#L128); [sign cost](../../papers/tpc-291-signed-schur-cancellation-atlas/paper/main.tex#L149) | The unique scalar projection needs the reference energy positive; normalizing the residual also needs target energy positive. The result is a normalized squared residual, distinct from the two-coefficient normalized Rayleigh minimum. Lower eigenvectors `(1,±1)` are in diagonal-normalized coordinates; original coefficients scale by inverse square roots of component energies. At zero cross term, both optimizations give one and no preferred coefficient-sign pairing is selected. |
| TPC292 | [parity theorem](../../papers/tpc-292-three-prime-sign-frustration-atlas/paper/main.tex#L91); [Schur identity](../../papers/tpc-292-three-prime-sign-frustration-atlas/paper/main.tex#L126); [volume](../../papers/tpc-292-three-prime-sign-frustration-atlas/paper/main.tex#L146) | All three cross terms must be nonzero for the stated binary sign parity rule; zero edges are automatically nonpositive but are not edges with sign ±1. A positive-definite non-target Gram gives a unique projection coefficient, but does not ensure a nonzero target. The normalized residual and volume require their own positive target/component energies. Unnormalized Schur complement and Gram positivity survive even when a normalized quotient is undefined. |
| TPC293 | [signed graph](../../papers/tpc-293-signed-shell-maxcut-atlas/paper/main.tex#L85); [max-cut](../../papers/tpc-293-signed-shell-maxcut-atlas/paper/main.tex#L100); [switching](../../papers/tpc-293-signed-shell-maxcut-atlas/paper/main.tex#L117) | The complete signed graph uses nonzero edges with signs ±1; otherwise omit zero edges and use the actual edge count, not automatically the complete-graph count. Balanced cuts attain the all-positive bound; switching gives a bijection of labelings preserving the objective, not necessarily an unchanged label. Fixing one vertex requires a nonempty graph and removes global reversal only. Unit edge counts do not determine a magnitude-weighted norm. |
| TPC294 | [trace identity](../../papers/tpc-294-magnitude-weighted-signed-rayleigh-atlas/paper/main.tex#L89); [enumeration](../../papers/tpc-294-magnitude-weighted-signed-rayleigh-atlas/paper/main.tex#L113); [Gray update](../../papers/tpc-294-magnitude-weighted-signed-rayleigh-atlas/paper/main.tex#L136) | Symmetry and positive trace give the identity for binary signs; Gram PSD gives nonnegativity. Rational entries admit a positive common denominator. A nonempty sign cube has one representative per global reversal after fixing the first coordinate, not one per potentially larger objective symmetry class. Gray updates use the old label and exclude the diagonal from the local field. The comparison evaluates one tie-selected max-cut witness, not the best weighted value over all unit-max-cut optimizers. |

## TPC290: full support is not the same as diffuse weighting

The [abstract](../../papers/tpc-290-adaptive-shell-weighting-obstruction/paper/main.tex#L43)
says the only finite nonnegative escape is sparse concentration on a
sign-flip pair. Its [claim firewall](../../papers/tpc-290-adaptive-shell-weighting-obstruction/paper/main.tex#L218)
correctly says the three policies are not an optimization over all rules.
The sparse-only wording must therefore be read as describing the tested
witnesses, not a theorem that every full-support nonnegative rule fails.

Indeed, for any finite Gram with positive denominator at a strict sparse
subunit witness, adding sufficiently small positive weights on all omitted
components preserves the strict inequality by continuity. Full support
alone places no positive lower bound on those added weights and does not
make a rule diffuse. As a standalone rational illustration, take
`g_1=(1,0), g_2=(-1,1), g_3=(0,1)` and `w=(1,1,1/10)`.
All three weights are positive, but the quotient is `121/301<1`.
This does not test or change any published physical weighting policy.
The all-positive Gram theorem remains valid on its own stated hypothesis.

Literal `qquad` without the leading backslash at
[TeX line 117](../../papers/tpc-290-adaptive-shell-weighting-obstruction/paper/main.tex#L117)
is preserved as source notation, not silently repaired.

## TPC291–292: projection and normalization qualifications

For TPC291, the simple vectors `g_i=(3,0), g_j=(3,4)` give
`rho=9/25`, normalized squared Schur residual `16/25`, and signed
Rayleigh minimum `2/5`. Thus `1-Gamma` and `1-sqrt(Gamma)` solve
different normalization/optimization problems. The coefficient sign in
`g_i-rho*g_j` must also retain the explicit subtraction convention.
No pairwise optimum automatically composes into a shell-wide optimum or
an admissible source coefficient vector.

TPC292's [projection statement](../../papers/tpc-292-three-prime-sign-frustration-atlas/paper/main.tex#L126)
and [proof-package theorem](../../papers/tpc-292-three-prime-sign-frustration-atlas/PROOF_PACKAGE.md#L23)
omit the separate `g_i!=0` premise for division by its energy. Set the
target to zero and the two other vectors to the standard basis in R2.
The non-target Gram is the identity and has positive determinant, while
the printed normalized formula is `0/0`. The unnormalized minimum is
well-defined and zero. Likewise, the normalized-volume corollary requires
all three vectors nonzero before normalizing them to unit length.
The reported positive-volume finite census, if established independently,
would supply the missing conditions for those rows; it is not replayed here.
All eight abstract edge-sign patterns were checked against all eight vertex
labelings for the parity equivalence, not against physical Gram entries.

## TPC293: sign-only conditional check

Using only the [seven stated vertices and three negative edges](../../papers/tpc-293-signed-shell-maxcut-atlas/paper/main.tex#L183),
a standalone enumeration of 64 labelings modulo reversal gives maximum
15 and complement `21-15=6`, compared with all-positive benchmark 12.
This confirms the combinatorial consequence of the supplied sign pattern,
not the physical calculation that produced those edge signs or the entire
18-row census. The two literal `qquad` tokens at
[line 78](../../papers/tpc-293-signed-shell-maxcut-atlas/paper/main.tex#L78)
and [line 93](../../papers/tpc-293-signed-shell-maxcut-atlas/paper/main.tex#L93)
remain unchanged in the reading layer.

## TPC294: selected max-cut witness versus the optimizer set

The [README](../../papers/tpc-294-magnitude-weighted-signed-rayleigh-atlas/README.md#L24)
and [TeX comparison](../../papers/tpc-294-magnitude-weighted-signed-rayleigh-atlas/paper/main.tex#L201)
say that weighted and unit-edge optima differ on all 18 rows. The inspected
[sign optimizer](../../papers/tpc-294-magnitude-weighted-signed-rayleigh-atlas/code/tpc294_magnitude_weighted_signed_rayleigh_certificate.py#L198)
chooses the lexicographically first unit-max-cut labeling on ties. Its
[comparison](../../papers/tpc-294-magnitude-weighted-signed-rayleigh-atlas/code/tpc294_magnitude_weighted_signed_rayleigh_certificate.py#L263)
evaluates that one labeling, and the
[18-row counter](../../papers/tpc-294-magnitude-weighted-signed-rayleigh-atlas/code/tpc294_magnitude_weighted_signed_rayleigh_certificate.py#L389)
compares its weighted ratio with the unrestricted weighted minimum.
It does not minimize weighted energy across all tied unit-max-cut labels.

These are genuinely different questions. For the rational Gram of
`g_1=(1,0), g_2=(1,1), g_3=(2,0)`, all edges are positive.
With first label positive, all three nonconstant labelings attain the
unit max-cut value two. Their weighted ratios are `5/7`, `5/7`, and
`1/7`; the all-positive ratio is `17/7`. The lexicographically first
max-cut witness therefore loses to the weighted optimum, although the
weighted optimum is itself a unit-max-cut optimizer. More generally,
on the source-reported three-prime all-positive row, any nonconstant
label is a unit max-cut. A weighted optimum below one while the plus
state is above one must be one of those max-cuts. The source's selected-
witness comparison cannot establish disjoint optimizer sets on every row.
No actual physical weighted minimum was recomputed.

The inspected code matches the source lock, SHA-256
`74fadde1853e2e03aee223a61393ceb845326ce8c7baf5d2a4015be988dc62d2`.
Twenty-four single-label flips on the small three-vector Gram above
also satisfy both Gray update identities exactly; this is not a replay
of the source traversal or exhaustive physical certificate.

The original [TeX line 133](../../papers/tpc-294-magnitude-weighted-signed-rayleigh-atlas/paper/main.tex#L133)
contains a doubled backslash before `qed`, and
[line 140](../../papers/tpc-294-magnitude-weighted-signed-rayleigh-atlas/paper/main.tex#L140)
a doubled backslash before `qquad`. The two extra lines at
[line 252](../../papers/tpc-294-magnitude-weighted-signed-rayleigh-atlas/paper/main.tex#L252)
follow `end{document}`. All are retained and identified; no original
source correction or PDF rebuild is made.

## Coverage and continuation

```bash
python -B research/tpc-big-road/check_source_markdown_batch.py --first 290 --last 294
```

The new total is 129 `full-source-md`, 0 `reliable-full-md`, 693
`partial-or-notes`, and 1 `source-inaccessible`, across 823 entries.
TPC290–418 now have mechanical reading layers with 6,498 math nodes.
Earlier scope notes remain historical batch snapshots.

Next existing-source batch: TPC285–289. TPC418's scientific stop remains
`NONE_UNTIL_GROWING_OR_PHYSICAL_GATE_CHANGES`, with arithmetic advance
`NO`, fixed-power credit `0`, and full Gate B `OPEN`. Conversion creates
no new number, original-source correction, theorem, or route reopening.
