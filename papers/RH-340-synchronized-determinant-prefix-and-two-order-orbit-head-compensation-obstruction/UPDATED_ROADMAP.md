# Roadmap after RH-340

RH-340 closes the analytic tail leaves on the same physical first-alias cut
`u=4k` and proves the exact prefix synchronization inequality
`|P_u-E_u|<=D_u`.  Consequently a future RH-288 activation on this cut must
pay the three same-clock budgets

    D_u -> 0,
    E_off,u -> 0,
    q_(sigma,k,2k) = o(H_k).

The critical and first-lower-sideband orbit atoms add the necessary laws

    C_k^0-d_(sigma,k,2k) = D_k^orb + o(H_k),
    C_k^--d_(sigma,k,2k-2) = D_(k-1)^orb + o(H_(k-1)).

If the head budget is itself closed, the `d` terms are negligible at those
orders and the two diffuse complements must pay both orbit atoms internally.
Taking separate absolute values cannot meet the resulting divergent atom
majorant.  Signed aggregate cancellation remains open.

The next admissible route is a physical moving-order estimate for the common
signed complements and the head defect, on the same Hardy clock and with the
same `u=4k` prefix.  A finite fit, a wrong RH-329 clock, or a separate
unsigned majorant is not a reopening input.  RH-341 must review this exact
coordinate and the ten-paper archive batch before changing `RH_HANDOFF.md`.
