# Bridge B: TPC-275 signed four-packet reassembly

TPC-275 is the source-attached continuation of TPC-274.  It keeps the same
literal V59 finite operator, exact beta source, prime shell, masks, deleted
diagonal, rank-three Haar projection, and TPC-269 growing-cutoff registry, but
retains the four source-block signs instead of applying a columnwise norm
envelope.

## New finite result

For the four actual source-block packets

```text
V_j=(I-P_3)A beta^(j),
Gamma_(j,k)=<V_j,V_k>,
D=trace(Gamma),
G=||sum_j V_j||_2^2,
```

the exact signed Gram expansion, real two-probe polarization, and normalized
four-point DFT give

```text
G = D + 2 sum_(j<k) Gamma_(j,k),
Gamma_(j,k)=(||V_j+V_k||^2-||V_j-V_k||^2)/4,
sum_k ||Vhat_k||^2=D,
G=4||Vhat_0||^2.
```

On the six registered scale triples

```text
(N,H,Q)=(64,15,4),(96,20,5),(128,24,5),
        (192,32,6),(256,38,6),(384,50,7)
```

with `s in {1,2}`, exact rational reconstruction of all 12 literal rows and
72 pairwise polarization probes certifies:

The registered audit contains 12 rows in total.

```text
G-D < 0,
1 < D/G < 12/5,
F/G > 50,
m_D^2=|C_perp|^2/(W_perp D) < 1/16.
```

Thus the signed packet diagonal is substantially sharper than the TPC-274
Frobenius envelope on this finite source, but it still cannot certify a quarter
margin through the conservative diagonal proxy.  The exact signed output is
retained; `m_D^2<1/16` is not an upper bound on the actual margin.  The result
is not an asymptotic cross-Gram estimate or a twin-prime proof.

## Claim firewall

```text
TPC275_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_SIGNED_FOUR_PACKET_REASSEMBLY_AUDIT
TPC275_ROUTE_ADVANCE = YES_SCOPED_LITERAL_SIGNED_FOUR_PACKET_REASSEMBLY
TPC275_SIGNED_GRAM_IDENTITY = PROVED_EXACT_FINITE
TPC275_DFT_LEDGER = PROVED_EXACT_FINITE
TPC275_POLARIZATION = PROVED_EXACT_FINITE
TPC275_LITERAL_PACKET_REPLAY = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS
TPC275_NET_CROSS_TERM = NUMERICALLY_CERTIFIED_FINITE_NEGATIVE_ALL_12_ROWS
TPC275_DIAGONAL_GAIN = NUMERICALLY_CERTIFIED_FINITE_BETWEEN_1_AND_12_OVER_5
TPC275_FROBENIUS_COMPARISON = NUMERICALLY_CERTIFIED_FINITE_ABOVE_50
TPC275_DIAGONAL_MARGIN = NUMERICALLY_CERTIFIED_FINITE_BELOW_QUARTER
TPC275_DIAGONAL_ROUTE = INSUFFICIENT_SCOPED
TPC275_SOURCE_LEVEL_SIGNED_CROSS_GRAM = OPEN_ASYMPTOTIC
TPC275_FIXED_POWER_CREDIT = 0
TPC275_ARITHMETIC_ADVANCE = NO
TPC275_L2 = NONE
TPC275_FULL_GATE_B = OPEN
TPC275_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC275_TWIN_PRIME_RESULT = NONE
TPC275_STATUS = NUMERICALLY_CERTIFIED_FINITE_SIGNED_FOUR_PACKET_REASSEMBLY_AUDIT
TPC275_ROUND2_CLUE = COMPILE_SIGNED_CROSS_GRAM_WITH_MARGIN_AND_ENDPOINT_BUDGET
```

TPC-260's generic DFT and synthetic null-compatible family is not being reused
as a literal counterexample here.  The packets in this release are generated
from the actual source blocks and exact beta.  The Session-named `propose.md`
and evaluator files are absent in this checkout; the project proof package,
theorem ledger, certificate, independent replay, stress audit, bridge checker,
and `AGENTS.md` are the fail-closed local fallback.
