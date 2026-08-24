# TPC-239 Claim Firewall

## Allowed claims

- Primitive residues compile physical rows into reduced prime AP rows.
- Dropping the `q`-dependent cutoff gives the displayed AP pair census.
- Brun--Titchmarsh and the multiplier count give the explicit constant `16`.
- The V59 maximum row is
  `<<x^(1/96)loglog x/log x`.
- The finite-window common-source packet trace is
  `<<JM^2x^(1/48)(log x)^4loglog x`.
- The improvement over TPC-237 is `log x/loglog x` and is logarithmic only.
- The leading unnormalized fixed-power exponent remains `49/48+o(1)`.

## Forbidden upgrades

- Do not infer cancellation in the signed divisor weight `C_h`.
- Do not identify the unsigned trace with an actual signed four-packet scalar.
- Do not claim arithmetic `L2` or fixed-atom credit.
- Do not claim payment of strict `1/400` or passage of Gate B.
- Do not claim a twin-prime theorem.
- Do not call `1/48` or `49/48` sharp.
- Do not promote finite enumeration to evidence for the analytic theorem.
- Do not describe the logarithmic improvement as a fixed-power saving.

## Machine-readable ceiling

```text
TPC239_STATUS = PROVED_SOURCE_BACKED_PRIME_DENSITY_L1
TPC239_ROUTE_ADVANCE = YES_LOGARITHMIC_ONLY
TPC239_ARITHMETIC_INPUT = BRUN_TITCHMARSH
TPC239_ARITHMETIC_ADVANCE = NO
C_H_SIGNED_CANCELLATION = NONE
SIGNED_FOUR_PACKET_PROJECTION = NOT_PROVED
L2 = NONE
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID_GLOBAL
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
SHARPNESS = NOT_CLAIMED
```
