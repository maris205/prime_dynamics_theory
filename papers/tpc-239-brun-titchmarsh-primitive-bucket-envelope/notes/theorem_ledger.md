# TPC-239 Theorem Ledger

## Proved statements

```text
TPC239_STATUS = PROVED_SOURCE_BACKED_PRIME_DENSITY_L1
TPC239_ROUTE_ADVANCE = YES_LOGARITHMIC_ONLY
TPC239_ARITHMETIC_INPUT = BRUN_TITCHMARSH
TPC239_ARITHMETIC_ADVANCE = NO
TPC239_PRIMITIVE_AP_COMPILER = PROVED_REDUCED
TPC239_BUCKET_ENVELOPE = PROVED_FACTOR_16
TPC239_H_ONE_ROW = PROVED_EMPTY_FROM_2Q_LESS_THAN_H
TPC239_V59_MAX_ROW = PROVED_X_1_OVER_96_LOGLOG_OVER_LOG
TPC239_PACKET_TRACE = PROVED_X_1_OVER_48_LOG4_LOGLOG
TPC239_UNNORMALIZED_EXPONENT = PROVED_49_OVER_48_PLUS_O_1
TPC239_IMPROVEMENT_OVER_TPC237 = PROVED_LOG_X_OVER_LOGLOG_X
```

## Exact theorem

Under `4Q<H` and `2<=h<=U<Q`, for `(a,h)=1`,

```text
R_h(a)
 <= sum_(m in M_h^x)
      [pi(2Q;h,a^(-1)m)-pi(Q;h,a^(-1)m)]
 <= 16 (Q^2/H) (h/phi(h))/log(2Q/h),
```

where `M_h=floor(2hQ/H)` and
`M_h^x={m:0<|m|<=M_h,(m,h)=1}`. For `h=1`, the row is empty.

At V59,

```text
max_(active h<=U,(a,h)=1) R_h(a)
 << x^(1/96) loglog x/log x,

N^(-1) sum_(n in I_x) sum_j |K_j(n)|^2
 << J M^2 x^(1/48)(log x)^4 loglog x.
```

The leading unnormalized fixed-power exponent is `49/48+o(1)`. This exponent
is not called sharp.

## Exact exponent ledger

```text
Q/U:                     1/3-133/400=1/1200
Q^2/H:                   2/3-21/32=1/96
row times direct energy: 1/96+1/96=1/48
window correction:       2*(133/400)-1=-67/200
unnormalized leading:     1+1/48=49/48
```

## Open or absent statements

```text
C_H_SIGNED_CANCELLATION = NONE
SIGNED_FOUR_PACKET_PROJECTION = NOT_PROVED
L2 = NONE
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID_GLOBAL
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
SHARPNESS = NOT_CLAIMED
```
