# Bridge-B proof package: TPC-364 prime-shell tilt phase diagram

## Scope

TPC-364 tests a finite family of explicitly weighted versions of the literal
TPC-363 prime-shell operator.  It freezes origins `(313030,311166,321651)`;
counts `256,512`; shell anchors `Q=80,128,256,512`; exponents `1,2`; and the
four fixed sign laws.  The integer tilt menu is
`beta={-2,-1,0,1,2}` with `w_(p,beta)=(p/Q)^beta`.  The diagonal normalizer
uses the square energy of the same weighted blocks.  The certificate has 960
law rows and true spectra for every row.

## Finite result

```text
TPC364_WEIGHTED_BLOCK_DEFINITION = PROVED_EXACT_FINITE
TPC364_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE
TPC364_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_960_ROWS
TPC364_PHASE_DIAGRAM = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC364_BETA2_PANEL_CAP_REPAIR = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC364_BETA2_ASYMPTOTIC_REPAIR = OPEN
TPC364_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC364_GROWING_OPERATOR_BOUND = OPEN
TPC364_SOURCE_UNIFORM_L2 = OPEN
TPC364_ARITHMETIC_ADVANCE = NO
TPC364_FIXED_POWER_CREDIT = 0
TPC364_FULL_GATE_B = OPEN
TPC364_TWIN_PRIME_RESULT = NONE
```

The spectral-cap violation counts for beta `-2,-1,0,1,2` are
`63,36,30,30,0` over 192 rows per beta.  Beta=2 has maximum normalized
spectrum `0.61628753962786131`, maximum normalized Schur value
`0.64531400360759594`, and minimum effective shell fraction
`0.66938300094026681`.

## Exact and independent controls

The finite weighted geometry is a sum of rational squares and is positive on
the declared rows.  The producer builds the shell in forward order; the
independent checker reconstructs the sieve, masks, weights, four laws,
envelopes, and all spectra in reverse shell order.  It also recomputes five
exact rational `Q=4` anchors.  The stress checker applies 18 protocol,
certificate, phase-count, and claim-firewall mutations.  The local Bridge-B
checker locks the claim-bearing files, checks PDF identity and diagnostics,
and runs producer, independent checker, and stress in normal and optimized
modes with empty stderr and byte-identical stdout.

## Route boundary

This is a finite phase diagram and a modeling-choice candidate.  The beta=2
point is not an independent holdout, does not establish source validity, and
does not advance arithmetic reassembly or any twin-prime conclusion.  The
official Session-named Route-A and Route-B evaluator files are absent, so no
official evaluator pass is claimed.  The next test is a response-blind fresh
holdout for beta=2.
