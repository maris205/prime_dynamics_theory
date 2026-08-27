# Bridge B: literal source attachment and finite source-lock audit

Date: 2026-08-27

TPC-282 is the direct source-level continuation of the typed interface in
TPC-281.  It evaluates the actual comparison-weight readout of the frozen V59
operator rather than an abstract dual functional.  With

```text
S=(I-P_3)A beta,
w_perp=(I-P_3)w,
C=<w_perp,S>,
rho^2=C^2/(||w_perp||^2 ||S||^2),
```

the twelve registered `(X,H,Q,s)` rows have sign-separated `C`: eleven are
negative and one is positive.  The weakest lower attachment coefficient is at
`(256,38,6,2)` and is approximately `3.357e-5`.

```text
TPC282_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_LITERAL_SOURCE_ATTACHMENT_LOCK_PLUS_ASYMPTOTIC_NONDEGENERACY_OPEN
TPC282_ROUTE_ADVANCE = YES_SCOPED_FINITE_SOURCE_ATTACHMENT_AUDIT
TPC282_SOURCE_ATTACHMENT = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS
TPC282_SOURCE_SIGN = 11_NEGATIVE_1_POSITIVE_FINITE
TPC282_UNIFORM_ASYMPTOTIC_NONDEGENERACY = OPEN
TPC282_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC282_FIXED_POWER_CREDIT = 0
TPC282_FULL_GATE_B = OPEN
TPC282_TWIN_PRIME_RESULT = NONE
TPC282_STATUS = NUMERICALLY_CERTIFIED_FINITE_LITERAL_SOURCE_ATTACHMENT_LOCK_PLUS_ASYMPTOTIC_NONDEGENERACY_OPEN
TPC282_ROUND2_CLUE = QUANTIFY_SOURCE_ATTACHMENT_STABILITY_RADIUS_AND_SIGN_FLIPS
```

This is a finite source-lock certificate.  The sign change and weak minimum
are retained as obstructions to promoting a finite nonzero table to a uniform
power lower bound.  The Session-named `propose.md` and evaluator files are not
present in this checkout; the project proof package, independent replay,
stress audit, and this fail-closed Bridge-B checker are the available scoped
evaluation.
