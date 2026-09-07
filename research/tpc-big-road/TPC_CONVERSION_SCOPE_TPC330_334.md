# TPC330–334 conversion and bounded prerequisite audit

Updated 2026-09-07. Source lock:
`ba1fb3efe59e51e62f64f4dcb607bd390b4b4062`. All five complete TeX
manuscripts, README files, and proof packages were read. Original sources,
hand-edited text, scientific code, and certificates are unchanged.

## Conversion evidence

The five new reading layers preserve all abstract/body text and formulas
under the declared Pandoc reader/writer roundtrip checks: 287 math nodes and
82 raw-source display blocks. The preserved PDFs have 17 extracted pages;
every source section in this batch has a unique heading-text page match.
Each per-paper record contains exact source/PDF hashes, section lines, page
maps, formula catalogues, conversion limits, and a link to this audit.

TPC330–333 each contain an external `references.bib`, preserved in full and
hash-locked. Their citation keys remain explicit; bibliography existence and
conversion do not constitute external bibliographic verification. TPC334 has
no source bibliography, and none is invented. These are mechanical checks,
not a PDF/TeX build-synchronization certificate, visual PDF certification,
complete semantic review, or a numerical experiment replay. No scientific
producer, independent certificate checker, or production cascade was run.

## Per-paper formula and prerequisite review

| Paper | Source location | Bounded check and limit |
|---|---|---|
| TPC330 | [finite metrics](../../papers/tpc-330-multi-permutation-response-spectrum/paper/main.tex#L97); [permutation invariance](../../papers/tpc-330-multi-permutation-response-spectrum/paper/main.tex#L128); [Gram expansion](../../papers/tpc-330-multi-permutation-response-spectrum/paper/main.tex#L151) | Finite real bilinearity gives the diagonal/off-diagonal split. Reading the sign from `E/D-1` requires `D>0`; no ratio is inferred at zero denominator. Odd multipliers `3,5,7` are units for the declared power-of-two source counts. Permutation norm/multiset preservation does not imply invariance of `C^T C`, and equal classifications under reversal do not prove equal responses. The five-control spectrum is deterministic, not a distribution over random permutations. The 640-observation census is source-reported, not rerun. |
| TPC331 | [mean/centered theorem](../../papers/tpc-331-control-average-centered-response-decomposition/paper/main.tex#L123); [general quadratic-form proof](../../papers/tpc-331-control-average-centered-response-decomposition/PROOF_PACKAGE.md#L3) | Use one common operator and the same nonempty finite ensemble and mean in all terms. The centered vectors sum to zero, removing the mixed terms. The proof-package symmetric quadratic-form statement also covers the indefinite off-diagonal form; positivity of that form does not follow. The diagonal-energy specialization uses its nonnegative diagonal matrix as a quadratic form, or its square root as a norm operator. The identity is for quadratic values, not the unweighted mean of response ratios. Ratios and energy shares need their own positive denominators. |
| TPC332 | [finite panel](../../papers/tpc-332-growing-control-average-ensemble/paper/main.tex#L49); [quadratic and source identities](../../papers/tpc-332-growing-control-average-ensemble/paper/main.tex#L94) | The same five controls act separately at each of the three finite power-of-two dimensions. Mean/centered identities hold within each common finite space and do not identify vectors across dimensions. Polarization uses the same shifted source `Lambda(t+2)` and comparison vector. Maximum `t+2=48098` stays below cutoff 50000. Three nested scales do not establish a growing-uniform estimate; source-reported ratios and slopes remain finite descriptors. Window overlap and the proof-package diagonal-matrix error are detailed below. |
| TPC333 | [polarization and quotients](../../papers/tpc-333-source-polarization-cross-term/paper/main.tex#L88) | Real finite polarization gives `rho=1-kappa` when the component-sum energy `S` is positive. The separately displayed normalized correlation requires both component norms positive; `S>0` alone is insufficient. Cauchy–Schwarz and `2ab<=a^2+b^2` give `-1<=kappa<=1`; for the declared nonnegative component vectors, `0<=kappa<=1`. The signed rational anchor is not such a nonnegative source. Finite observed coefficient ranges do not identify an arithmetic cancellation theorem. |
| TPC334 | [support and mass partition](../../papers/tpc-334-cross-term-support-ledger/paper/main.tex#L67) | The nonzero cross support has odd `t` and a prime-power shift `t+2`; prime versus higher-power cases and primality of `t` yield disjoint exhaustive classes for nonzero summands. Finite additivity gives the mass identity, while nonnegativity makes positive-total mass fractions lie in `[0,1]`. Fractions need strictly positive total cross mass. A zero cross product does not imply a zero residual. In the declared windows, nonprime predecessors of prime shifts are odd composites; that wording is not extended to the small exceptional predecessor 1 or to all composite coordinates. No unweighted prime-pair count or asymptotic conclusion follows from the weighted fractions. |

## Source discrepancies and qualifications preserved

TPC332's [proof package, Proposition 2](../../papers/tpc-332-growing-control-average-ensemble/PROOF_PACKAGE.md#L16)
says to take the diagonal matrix with entries `sum_u C(u,t)^2` in a theorem
about `||A x||^2`. That literal substitution gives `x^T Delta^2 x`, not
the desired `D(x)=x^T Delta x`. One must take `A=Delta^(1/2)`, as the
[TeX manuscript explicitly does](../../papers/tpc-332-growing-control-average-ensemble/paper/main.tex#L107),
or invoke the quadratic-form version. For the one-coordinate example
`Delta=(2)` and `x=(1)`, these values are 4 and 2 respectively. This is a
proof-package substitution error, not a detected failure of the finite
mean/centered identity or of the numerical certificate. The original files
remain unchanged.

The phrase “disjoint origins/ensemble” in TPC332–334 must not be read as
pairwise-disjoint new source windows. At scale 8192, the two intervals are
`[42001,46096]` and `[44001,48096]`, overlapping on 2096 coordinates.
They are disjoint from TPC331's earlier panel, whose largest endpoint is
40096. TPC333, however, retains TPC332's six windows: its
[“six disjoint-from-parent windows” sentence](../../papers/tpc-333-source-polarization-cross-term/paper/main.tex#L183)
is not true if “parent” means its explicitly named immediate parent TPC332.
The shared windows do not supply independent sampling; the original
geometries and wording are preserved with this qualification.

TPC331 has a literal `qquad` without its leading backslash in the
[control-map display](../../papers/tpc-331-control-average-centered-response-decomposition/paper/main.tex#L118).
TPC333 has the same issue in its
[normalization definitions](../../papers/tpc-333-source-polarization-cross-term/paper/main.tex#L96)
and [complement equation](../../papers/tpc-333-source-polarization-cross-term/paper/main.tex#L102).
They are retained in the reading layer, not silently repaired or interpreted
as additional variables. TPC333's [protocol prose](../../papers/tpc-333-source-polarization-cross-term/paper/main.tex#L112)
mentions “two nested scales” although its declared geometry has three scales
and its results list four adjacent pairs (two per origin). The explicit
geometry is retained; this does not authorize silently changing the prose.

In TPC332–334, abbreviated `Lambda` in a vector identity means the shifted
vector used in the source definition, not an unshifted replacement. TPC334's
prime-power class notation is a partition of the nonzero cross support in
context; outside the declared windows, a higher power of 2 has even
predecessor and zero comparison factor. Such a coordinate need not be a
nonzero prime-power contribution. Mass additivity remains valid with zero
summands, but this shorthand must not be promoted to a globally exhaustive
four-way nonzero/zero count convention without stating the masks.

Bounded arithmetic checks confirm `32*4*5=640` for TPC330 and
`2*3*4*2=48`, `48*4=192` for TPC332. TPC333's rational anchor gives
component squared norms 39 and 7, inner product -2, and residual squared norm
`50=39+7-2*(-2)`; its `kappa=-2/23` illustrates the signed-model case.
TPC334's four labeled products give `10+3+2+0=15`. The larger 16-coordinate
operator anchors in TPC330–332 and all certificate digests remain
source-reported and were not recomputed. An individual anchor tests that
instance; the general algebra rests on the finite expansions, not on a
single successful example.

## Coverage and handoff

```bash
python -B research/tpc-big-road/check_source_markdown_batch.py --first 330 --last 334
```

The new total is 89 `full-source-md`, 0 `reliable-full-md`, 733
`partial-or-notes`, and 1 `source-inaccessible`, across 823 entries.
TPC330–418 now have mechanical full-source reading layers with 3,874 math
nodes in total. Earlier scope notes remain historical batch snapshots.

Next existing-source batch: TPC325–329. TPC418's scientific stop remains
`NONE_UNTIL_GROWING_OR_PHYSICAL_GATE_CHANGES`, with arithmetic advance
`NO`, fixed-power credit `0`, and full Gate B `OPEN`. No new number,
theorem, source correction, or route reopening is authorized by conversion.
