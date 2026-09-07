# TPC325–329 conversion and bounded prerequisite audit

Updated 2026-09-07. Source lock:
`b13909fddbffed372f43022d2cfaa2d7bdb1110e`. All five complete TeX
manuscripts, README files, proof packages, and external BibTeX files were
read. Original sources, hand-edited text, scientific code, and certificates
are unchanged.

## Conversion evidence

The five reading layers preserve all abstract/body text and formulas under
the declared Pandoc reader/writer roundtrip checks: 277 math nodes and 55
raw-source display blocks. The preserved PDFs have 17 extracted pages;
all source sections have unique heading-text page matches. Per-paper
records contain exact source/PDF/BibTeX hashes, section lines, page maps,
formula catalogues, conversion limits, and a link to this audit.

All five manuscripts have an external bibliography, preserved in full with
unresolved citation keys explicit. No external bibliographic verification
is claimed. Neither text extraction nor a source roundtrip certifies visual
PDF quality, PDF/TeX build synchronization, source correctness, or numerical
reproduction. No scientific producer, independent certificate checker,
spectral calculation, or production cascade was run.

## Per-paper formula and prerequisite review

| Paper | Source location | Bounded check and limit |
|---|---|---|
| TPC325 | [Grams and profiles](../../papers/tpc-325-scale-ladder-profile/paper/main.tex#L43); [amplitude/shape identity](../../papers/tpc-325-scale-ladder-profile/paper/main.tex#L66) | `A^* A` and finite sums of such matrices are PSD, but PSD alone does not give strictly positive trace. Trace normalization requires a nonzero Gram; ordered eigenvalues then give a nonnegative unit-sum vector. Positive scalar rescaling preserves that profile, not its trace. Majorization compares ordered profiles of equal dimension and equal total mass within one row; the paper's stated convention additionally demands one strict interior prefix. The four changing dimensions do not constitute a common-space unitary identity. Descending finite envelope endpoints do not prove individual-row monotonicity or a growing limit. |
| TPC326 | [cross-origin protocol](../../papers/tpc-326-cross-origin-scale-replication/paper/main.tex#L73) | Preserve the same kernel, height, shells, source counts, and sign menu when comparing the two origins. The interval endpoints prove nesting and separation of the 12001 and 16001 ladders. A translated distance kernel does not by itself preserve the absolute divisibility masks. The `0.001` and `0.005` comparisons concern the declared min-TV/max-energy summaries, not uniform rowwise error bounds, statistical confidence, or asymptotic errors. Equal category counts do not establish rowwise response equality. |
| TPC327 | [three-origin range](../../papers/tpc-327-three-origin-scale-triangulation/paper/main.tex#L69) | The maximum-minus-minimum is over the same three origins at the same scale and for the same envelope observable. A small range controls only those three envelope values; it does not bound every underlying row or a fourth origin. A positive observed range rules out identical displayed values, not all provenance failures. The new 32-row panel and the pooled three-origin diagnostic are distinct counts. Numerical spectra and exact rational digests remain source-reported. |
| TPC328 | [source-coordinate metrics](../../papers/tpc-328-source-native-l2-cancellation/paper/main.tex#L92); [Gram proof](../../papers/tpc-328-source-native-l2-cancellation/paper/main.tex#L134) | Finite real bilinearity gives the coordinate diagonal plus off-diagonal split after the shell blocks have already been combined into `C_e`. The sign readout from `E/D-1` requires `D>0`; a zero total response does not itself invalidate the identity. Negative off-diagonal mass concerns this decomposition, not a source-uniform power saving. The V59 midpoint and cutoff protocol is not an asymptotic source-identification theorem. Positive component responses do not determine the response of their difference. The claimed twin-prime anchor coordinate is incorrect, as detailed below. |
| TPC329 | [placement control](../../papers/tpc-329-heldout-growing-source-native-audit/paper/main.tex#L121); [Gram/placement identities](../../papers/tpc-329-heldout-growing-source-native-audit/paper/main.tex#L132) | `gcd(5,M)=1` for the two declared power-of-two counts makes the affine map a bijection. It preserves source norms and multisets but need not preserve `C_e^T C_e`. Equality of energy for every real vector would require the corresponding conjugated symmetric Gram matrices to agree, not merely norm invariance of the source. Scale pairing must keep origin, shell, exponent, and sign law fixed; energy ratios need a positive denominator and their logarithms need a positive ratio. Two finite slopes are not asymptotic exponents. The proof-package claim about every actual law having a positive row contradicts the printed census. |

## Source discrepancies and qualifications preserved

TPC328's [README anchor statement](../../papers/tpc-328-source-native-l2-cancellation/README.md#L101)
calls `t=20009` a local twin-prime indicator; the
[TeX anchor prose](../../papers/tpc-328-source-native-l2-cancellation/paper/main.tex#L249)
also calls it a local pair because 20011 is prime. Direct integer arithmetic
gives `20009=11*17*107`, so `(20009,20011)` is not a twin-prime pair.
Trial division through the integer square root confirms that 20011 is
prime. Moreover, the actual printed anchor vector is
`1_(t+2 prime)-1_(t odd)`, which equals `1-1=0` at this coordinate and is
not a twin-pair indicator. This invalidates the local twin-label claim,
not the finite Gram identity. The anchor's full matrix energies and digests
were not recomputed, and no source file was silently corrected.

TPC329's [proof-package obstruction](../../papers/tpc-329-heldout-growing-source-native-audit/PROOF_PACKAGE.md#L86)
states that each actual declared law has at least one positive off-diagonal
row. Its own [census](../../papers/tpc-329-heldout-growing-source-native-audit/PROOF_PACKAGE.md#L58),
also printed in the [TeX table](../../papers/tpc-329-heldout-growing-source-native-audit/paper/main.tex#L187),
has actual mod-4 and half-split counts `32 negative / 0 positive`.
Thus the assertion that every individual law fails the contraction on this
actual panel is unsupported by, and contradicts, the source's table. The
source-reported all-plus and alternating positive rows would still refute
a single joint claim quantified over all four laws and all rows; they do
not refute uniform contraction for each law separately. In particular, the
permuted half-split positive rows cannot be substituted for actual rows.
The placement-sensitivity conclusion for all-plus is a different claim and
is not invalidated merely by this prose/table contradiction.

TPC327 and TPC328 split executable paths across physical lines in their
TeX `verbatim` reproduction blocks without a shell continuation character:
[TPC327 commands](../../papers/tpc-327-three-origin-scale-triangulation/paper/main.tex#L178)
and [TPC328 commands](../../papers/tpc-328-source-native-l2-cancellation/paper/main.tex#L287).
Literal copying therefore does not form the intended commands. The original
line breaks are retained; complete path spellings are available in the
respective [TPC327 README](../../papers/tpc-327-three-origin-scale-triangulation/README.md#L103)
and [TPC328 README](../../papers/tpc-328-source-native-l2-cancellation/README.md#L138).
These are navigation pointers, not a request to run the README's writers or
the numerical reproduction suite during archive maintenance.

The word “direct” must not merge two different decompositions. TPC325–327
define `G_0=sum_p B_p^* B_p` before coherent shell reassembly. TPC328–329
define `D_e(v)=sum_t v_t^2 ||C_e e_t||^2` after reassembly, by discarding
off-diagonal **source-coordinate** Gram entries. Neither this `D_e(v)` nor
its ratio with `E_e(v)` is silently identified with the earlier direct
Gram trace, or with the quadratic response `v^T G_0 v`.

The positive-trace statements in the TPC325–326 proof packages include a
reported numerical panel check as well as exact PSD algebra. This
maintenance retains that distinction: it does not turn a reported positive
trace or spectral prefix guard into an independently reproduced certificate.
Likewise, monotonicity or proximity of lower/upper envelope endpoints alone
does not certify ordering/proximity of all unknown underlying quantities;
that would need their appropriate two-sided bounds and separation margins.

Bounded endpoint checks give largest earlier intervals `[12001,13280]`,
`[16001,17280]`, `[20001,21280]` and new TPC329 intervals
`[28001,32096]`, `[36001,40096]`, which are pairwise disjoint.
The largest shifted values are 21282 for TPC328 and 40098 for TPC329,
below the declared cutoff 50000. This check does not independently inspect
all still-earlier panels named in source provenance claims. The Cartesian
counts are 32 rows per spectral ladder, 96 TPC328 rows, 32 TPC329 rows,
64 law-level scale pairs, and 128 actual/permuted law comparisons. The
simple rescaling example `diag(3,1)` versus `diag(6,2)` has common profile
`(3/4,1/4)` but traces 4 and 8. These checks do not replay any production
certificate or any of the larger rational operator anchors.

## Coverage and handoff

```bash
python -B research/tpc-big-road/check_source_markdown_batch.py --first 325 --last 329
```

The new total is 94 `full-source-md`, 0 `reliable-full-md`, 728
`partial-or-notes`, and 1 `source-inaccessible`, across 823 entries.
TPC325–418 now have mechanical full-source reading layers with 4,151 math
nodes in total. Earlier scope notes remain historical batch snapshots.

Next existing-source batch: TPC320–324. TPC418's scientific stop remains
`NONE_UNTIL_GROWING_OR_PHYSICAL_GATE_CHANGES`, with arithmetic advance
`NO`, fixed-power credit `0`, and full Gate B `OPEN`. No new number,
theorem, source correction, or route reopening is authorized by conversion.
