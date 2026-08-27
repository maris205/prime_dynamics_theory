# TPC-275 paper plan

## Question

TPC-274 proved that a projected Frobenius envelope is valid but loses more than
50 on every registered row.  Does retaining the signs of the four source-block
contributions produce a genuinely sharper, source-attached finite output
identity?

## Frozen object

- the literal V59 operator, masks, prime shell, deleted diagonal, and exact beta
  source from the released TPC-268 engine;
- the TPC-269 growing-cutoff registry and the same six `(N,H,Q)` rows;
- the rank-three four-block Haar projection used by TPC-273 and TPC-274;
- source-block packets `V_j=(I-P_3)A beta^(j)`, with no synthetic packet data.

## Claim-bearing contributions

1. Prove the exact four-packet Gram and DFT reassembly identities.
2. Prove the real two-probe polarization identity used to recover every signed
   packet cross term.
3. Construct and independently replay the literal 4-by-4 packet Gram on all
   12 rows.
4. Certify that the net signed cross term is negative on every row and that
   the packet-diagonal envelope is within a factor `12/5` of the exact signed
   output, while the TPC-274 Frobenius envelope is above a factor 50.
5. Record that even this diagonal envelope has conservative margin proxy below
   `1/4` on every row; no asymptotic promotion is made.

## Route decision

This is a source-attached finite signed-reassembly audit, not a replacement
for the missing source-level arithmetic theorem.  The exact identities are
`PROVED_EXACT_FINITE`; the 12-row sign/gain statements are
`NUMERICALLY_CERTIFIED_FINITE`; the growing signed cross-Gram estimate remains
`OPEN`.
