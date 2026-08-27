# TPC-276 paper plan

## Question

TPC-275 found a finite signed gain (D/G>1) for the actual four source-block
packets.  Does that gain have an exact effect on the correlation margin, and
how does a source-level polynomial gain enter the strict `1/400` endpoint
budget?

## Frozen object

- the released TPC-275 signed four-packet certificate;
- the literal V59 operator and exact beta source already certified by TPC-268
  through TPC-275;
- the same six growing-cutoff scale triples and kernel exponents;
- no new operator, source, cutoff, or synthetic packet family.

## Claim-bearing contributions

1. Prove the exact margin-recovery identity
   (m^2=(D/G)m_D^2) whenever (G>0).
2. Prove a conditional endpoint compiler: a scalar saving (sigma), diagonal
   margin loss (eta_D), and source-level signed gain
   (D/G\ge b x^\gamma) combine as
   (sigma-eta_{m eff}>1/400), with
   (eta_{m eff}=max(0,eta_D-gamma/2)).
3. Transfer the identity exactly through the 12 TPC-275 rows and classify the
   signed margin at the quarter and eighth thresholds.
4. Prove the finite-to-asymptotic firewall: a finite gain table supplies no
   fixed-power credit without a uniform growing lower bound.

## Route decision

This is a strict-budget/compiler paper, not a claim that the finite gain is a
power saving.  The algebraic compiler is `PROVED_CONDITIONAL`; the 12-row
signed-margin recovery is `NUMERICALLY_CERTIFIED_FINITE`; the source-level gain
bound, arithmetic `L2`, full Gate B, and twin-prime conclusion remain open.
