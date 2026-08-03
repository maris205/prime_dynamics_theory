# Roadmap after RH-348

RH-348 extracts the complete boundary-orbit demand across the punctured
lower-even ladder

    m_star<=m<=k-2,  n=2m.

With `x=(beta R)^2>1`, its exact weighted orbit mass satisfies

    L_k^orb
      =x^(k-1)/(C_M(x-1))(1+o(1)),

while the absolute radial correction is only `O(1/k)L_k^orb`.  Thus any
vanishing direct lower-even punctured subprefix requires the actual signed
remainder-plus-parity supply to carry the same exponentially growing
weighted mass.  The repository does not bound that supply, so actual closure
and nonclosure remain open.

The next RH-349 route is a theorem-backed two-coordinate slice of this
ladder.  Use the first two still-punctured sidebands

    m_2=k-2,  m_3=k-3.

Their scalar parity/demand ratios have the fixed-phase limits

    C_* C_M lambda^(eta-2),
    C_* C_M lambda^(eta-3).

Because these differ by the exact factor `lambda`, no scalar phase can make
both equal one.  For every positive scalar `a`,

    max(|a-1|,|a/lambda-1|)
      >= (lambda-1)/(lambda+1).

RH-349 may turn this minimax identity into a conditional physical two-order
obstruction under named target-negligibility hypotheses for both actual
signed remainders.  It must not replace those missing hypotheses by the
divergent demand mass proved here.

RH-350 may then extend the minimax law to a fixed or slowly growing depth
ladder.  Odd orders, upper off-alias orders, actual signed compensation,
head transport, the full direct prefix, RH-288, and Gates A--E remain open.
