# TPC-382 — c=1 origin-family magnitude audit

**Author:** Liang Wang<br>
**Affiliation:** School of Mathematics and Statistics, Huazhong University
of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-382 aggregates the sealed TPC-380 and TPC-381 `N=2048` panels under a
predeclared one-percent relative-spread rule.  Across six locked origins and
three Q values, the all-plus band magnitude is within one percent at all three
Q values; the complete four-law census has 8/12 cells within one percent, with
all four failures coming from the alternating-index or low-Q mod-4 controls.
The earlier TPC-379 `N=1024` panel is retained as a labelled scale control: its
matched all-plus high-Q mean differs from the pooled `N=2048` mean by
`2.0813995160269608%`, so the finite cross-count one-percent hypothesis is
refuted.  This is a certificate-level finite magnitude result, not an
asymptotic uniformity theorem.

## Frozen audit protocol

```text
same-count cohort = TPC380 and TPC381, each N=2048, 3 origins, 3 Q, 4 laws
same-count values = 72 (6 origins x 3 Q x 4 laws)
scale control = TPC379, N=1024, 3 origins, 3 Q, 4 laws
relative spread = (max-min)/mean over the locked origin values
stability cap = 0.01, fixed before aggregation
scale contrast = (mean_N2048 - mean_N1024)/mean_N1024
high-Q diagnostic = Q=8192
```

No response, parent metric, or row is used to select a panel.  Parent source
and certificate hashes are embedded in the result and checked before any
aggregation.  The same-count cohort is protocol-matched; the TPC-379 cohort is
explicitly a scale control because its window count is different.

The same-count all-plus relative spreads at `Q=512,2048,8192` are respectively
`1.9035250282068572e-5`, `2.380537285421679e-5`, and
`8.0645464844910632e-6`.  Its high-Q mean is
`0.66694363456350925`.  The four same-count cells outside the one-percent rule
are alternating-index at all three Q values and mod-4-character at `Q=512`.

## Claim firewall

```text
TPC382_PARENT_LOCKS = PROVED_EXACT_FINITE_HASHED
TPC382_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_CERTIFICATE_BLIND
TPC382_SAME_N_ORIGIN_MAGNITUDE_AUDIT = NUMERICALLY_CERTIFIED_FINITE_72_VALUES
TPC382_ALL_PLUS_HIGH_Q_STABILITY_1PCT = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC382_LAW_DEPENDENT_MAGNITUDE_SPREAD = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC382_CROSS_COUNT_MAGNITUDE_INVARIANCE = REFUTED_FINITE_SCOPED
TPC382_ORIGIN_UNIFORMITY = OPEN
TPC382_WINDOW_SCALE_UNIFORMITY = OPEN
TPC382_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC382_GROWING_OPERATOR_BOUND = OPEN
TPC382_SOURCE_UNIFORM_L2 = OPEN
TPC382_ARITHMETIC_ADVANCE = NO
TPC382_FIXED_POWER_CREDIT = 0
TPC382_FULL_GATE_B = OPEN
TPC382_TWIN_PRIME_RESULT = NONE
```

The positive statement is limited to the six finite, already locked origins
and the normalized c=1 diagnostic.  It does not establish origin uniformity,
scale uniformity, source validity, law selection, a growing operator bound,
arithmetic `L2`, Route-A/Route-B closure, or a twin-prime result.  The
Session-named official evaluator files are absent from this checkout; the
local Bridge-B is fail-closed repository evidence only.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-382-c1-origin-family-magnitude-audit/code/tpc382_c1_origin_family_magnitude_audit.py --write
python -B papers/tpc-382-c1-origin-family-magnitude-audit/code/tpc382_c1_origin_family_magnitude_audit.py --check
python -O -B papers/tpc-382-c1-origin-family-magnitude-audit/code/tpc382_c1_origin_family_magnitude_audit.py --check
python -B papers/tpc-382-c1-origin-family-magnitude-audit/experiments/tpc382_independent_checker.py --check
python -O -B papers/tpc-382-c1-origin-family-magnitude-audit/experiments/tpc382_independent_checker.py --check
python -B papers/tpc-382-c1-origin-family-magnitude-audit/experiments/tpc382_adversarial_certificate_stress.py --check
python -O -B papers/tpc-382-c1-origin-family-magnitude-audit/experiments/tpc382_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc382_c1_origin_family_magnitude_audit_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc382_c1_origin_family_magnitude_audit_checker.py --check
```

`ROUND2_CLUE = TEST_C1_POOLED_NORMALIZATION_CROSS_ORIGIN`.
