# RH-397 independent review audit

## Proof review

The independent adversarial review of the final frozen manuscript reported
zero blockers and zero minor findings.  It checked:

- the exact fixed-data quantifiers and limit-before-maximum order;
- the centered window, center-weighted score, and boundary extension;
- separation-`h` universal safety with a two-symbol overlap;
- RH-394 as the sole analytic three-shift input through RH-396, with no
  fourth-shift or `c1111` call;
- collision-aware `Theta`, inclusion-exclusion `Pi`, exact-support sign split,
  and zero all-minus baseline;
- positive projection, input reflection, and both-sign attainment;
- source/target flags, exact relation census, and all four rectangle classes;
- the factors and signs in `M,U,V,W`, every translation branch, and phase
  sums;
- local edge filling, nonnegative gain, saturated identity, rising-set
  independence, and surjectivity;
- the exact weighted independent-set capacity formula for every fixed `h,q`;
- two-phase attainment for odd `h`, nonminimal even lifts, and all branches
  of the odd-clock CRT strictness argument;
- the declared-clock parity statement and the even-lag negative-control
  boundary;
- every growing-data, Cesaro, causal, four-shift, operator, zero, RH, and Gate
  firewall.

The review explicitly rejected replacing separation `h` by `2h`, dropping
one shared overlap symbol, treating the fourth safety letter as analytic,
replacing the weighted optimizer by cardinality, requiring minimal period two,
or extending the parity theorem to even lags.

## Source, citation, and PDF review

An independent source/citation/PDF review of the identical quartet also
reported zero blockers and zero minor findings.  It checked RH-394's sole
analytic role, RH-396's direct finite-predecessor role, the comparison-only
roles of RH-392/RH-395/RH-375, both bibliography keys, the `172+4=176`
closure, the rights vector `false,false,true,false`, and nonvendoring.

The PDF passed Ghostscript parsing, text extraction, A4 geometry, encryption
and metadata checks.  All 25 font rows are embedded, subset, and
Unicode-mapped, and all nine rendered pages were visually inspected.

## Frozen quartet

```text
main.tex          27620 B  a0ded93cfcd46f48b602e3f276a39e01e99ba8c37d3961316540f3925064ec11
references.bib      505 B  2ef184fbd1594af83c0a16fd8f868c3572d91d86c30d40f98271781ca0044b3b
main.pdf         387054 B  be06c3bcd37acb7f2144cd390423ae207f9b412ffd833a8156a317c59dd44ea6
main.log          26381 B  3ff4d9317931ff356e76340cca833fba7fc50f38668234fe5ff4cec32c402aba
```

Verdict: accept within the theorem's exact fixed-data scope.
