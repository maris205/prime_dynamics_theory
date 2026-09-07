# TPC335–339 conversion and bounded prerequisite audit

Updated 2026-09-07. Source lock:
`024fd8d535671c377bc5714346cb3c1b3136c9d5`. All five complete TeX
manuscripts, README files, and proof packages were read. Original sources,
hand-edited text, scientific code, and certificates are unchanged.

## Conversion evidence

The new reading layers preserve all abstract/body text and formulas under
the declared Pandoc reader/writer roundtrip checks: 156 math nodes and 44
raw-source display blocks. The preserved PDFs have 13 extracted pages;
every source section in this batch has a unique heading-text page match.
Per-paper records contain exact source/PDF hashes, source lines, page maps,
formula catalogues, and a link to this audit. No source bibliography is
present in this batch, and none is invented.

These are mechanical checks, not a proof that every source macro is
interpreted perfectly, a PDF/TeX build-synchronization certificate, or a
numerical experiment replay. No scientific generator or production cascade
was executed. The two implementation excerpts cited below were inspected
read-only to clarify a definition and an empty-input convention.

## Per-paper formula and prerequisite review

| Paper | Source location | Bounded check and limit |
|---|---|---|
| TPC335 | [source/masks](../../papers/tpc-335-twin-isolated-source-norm/paper/main.tex#L50); [masked norm split](../../papers/tpc-335-twin-isolated-source-norm/paper/main.tex#L76) | A disjoint exhaustive coordinate partition gives an exact sum of masked squared norms before applying any operator. `zero_support` concerns the source cross term, not the residual vector; it can carry nonzero residual energy. The amplification ratio requires nonzero total residual energy, total cross mass, and twin cross share. The declared finite source, cutoff, and midpoint conventions do not identify an asymptotic arithmetic source. Six-window fractions remain source-reported observations. |
| TPC336 | [output-Gram identity](../../papers/tpc-336-masked-signed-gram-response/paper/main.tex#L78) | Finite real linearity expands the full response into self energies plus twice the unordered-pair inner products. Disjoint source coordinates need not produce orthogonal outputs. The signed cross term cannot be dropped or inferred from self energies. Class gain requires a nonzero class source; the self/full-energy ratio requires positive full response energy. Complex-space generalization would require the appropriate real part/conjugation, not the printed real formula unchanged. |
| TPC337 | [finite covariance structure](../../papers/tpc-337-control-covariance-masked-response/paper/main.tex#L65) | Use the same five controls and the same `1/5` averaging in means, centered vectors, and covariance entries. Centered sums vanish, which removes the mixed terms. The class covariance is a Gram matrix, hence PSD, but individual off-diagonal entries may be negative. Energy fractions need positive denominators. The deterministic control average is not an independent-sampling or probability theorem; observed covariance signs are not universal. |
| TPC338 | [nested controls and covariance](../../papers/tpc-338-growing-control-covariance-spectrum/paper/main.tex#L31) | The odd affine multipliers are bijective for the declared power-of-two source counts because they are coprime to those counts. That does not establish bijectivity for arbitrary new moduli. Five- and nine-control ensembles must each be centered with their own mean and averaging factor. Changing the ensemble changes the centered vectors, so nesting does not imply entrywise sign monotonicity. Trace-normalized spectra require strictly positive trace. The two finite ensemble sizes do not establish a growing-control limit. |
| TPC339 | [support-restricted bound](../../papers/tpc-339-mask-aware-frobenius-envelope/paper/main.tex#L48) | For `supp(x)` contained in `S`, restriction to columns `A_S` and the induced-norm/Frobenius inequality give the stated upper bound; no covariance sign or symmetry is required. Each coordinate permutation changes the relevant support, so a support envelope must use that placement. The bound remains valid for zero vectors/operators, but its occupancy quotient needs both `x != 0` and `F(supp(x))^2 > 0`. Finite slack does not refute a sharper bound or prove cancellation. |

## Definitions and source qualifications preserved

TPC335's inspected [classifier](../../papers/tpc-335-twin-isolated-source-norm/code/tpc335_twin_isolated_source_norm.py#L82)
first assigns a coordinate to `zero_support` when the source cross product
vanishes, then classifies the remaining prime-power support. Thus the label
must not be read as `beta(t)=0`. The printed prime/prime-power class shorthand
is used on its declared finite windows; equivalence to nonzero cross support
is not silently extended to arbitrary intervals or parity cases.

TPC336 [TeX gain definition](../../papers/tpc-336-masked-signed-gram-response/paper/main.tex#L72)
defines the quotient only when its source denominator is nonzero. The
inspected [self-metric implementation](../../papers/tpc-336-masked-signed-gram-response/code/tpc336_masked_signed_gram_response.py#L139)
requires zero response for an empty source and stores `gain=0.0`. Therefore
zero minima for an empty prime-power class are an explicit storage/ordering
convention, not a defined mathematical `0/0` response gain. The numerical
six-row ordering is not independently rerun by this maintenance.

TPC339 [occupancy definition](../../papers/tpc-339-mask-aware-frobenius-envelope/paper/main.tex#L61)
mentions nonzero `x`, but that alone does not ensure a nonzero support
Frobenius denominator for an arbitrary finite matrix. For example, `A=0`
and nonzero `x` leave the inequality valid while the displayed occupancy is
undefined without a separate convention. This review therefore requires
`F(supp(x))^2 > 0` for the quotient and does not infer a failure of the
declared finite panel. The README's anchor calls 9 the “source norm” for
`x=(3,0)`; the [TeX anchor](../../papers/tpc-339-mask-aware-frobenius-envelope/paper/main.tex#L77)
correctly uses the squared norm 9 (the Euclidean norm is 3). The original
prose is preserved rather than overwritten.

The elementary anchors in the manuscripts are consistent at this bounded
algebraic level: TPC335's four squared entries sum to 50; TPC336 has
`17=5+8+2*2`; TPC337's cross decomposition is `0=1/2-1/2`;
TPC338's orbit energy split is `1=1/2+1/2`; TPC339 has `45=5*9`.
These checks do not validate the production certificates or their source locks
beyond the manuscript/bibliography/PDF provenance recorded by conversion.

## Coverage and handoff

```bash
python -B research/tpc-big-road/check_source_markdown_batch.py --first 335 --last 339
```

The new total is 84 `full-source-md`, 0 `reliable-full-md`, 738
`partial-or-notes`, and 1 `source-inaccessible`, across 823 entries.
TPC335–418 now have mechanical full-source reading layers with 3,587 math
nodes in total. Earlier scope notes remain historical batch snapshots.

Next existing-source batch: TPC330–334. TPC418's scientific stop remains
`NONE_UNTIL_GROWING_OR_PHYSICAL_GATE_CHANGES`, with arithmetic advance
`NO`, fixed-power credit `0`, and full Gate B `OPEN`. No new number,
theorem, source correction, or route reopening is authorized by conversion.
