# RH-150: Temporal-Anchor Packet-Transport Obstruction

This paper audits the first proposed interval composition from RH-142 packet
balls into the RH-96 thresholded recursive update.

The inherited composition is not type-correct: eight channels use clock rank
5--7 rather than rank four, while the two rank-four channels start at time
zero but RH-142 certifies a postblock packet at time `H(sigma)`.  Their
triangle-transferred projector radii are already one.  Thus none of the ten
RH-142 balls is an informative RH-96 seed.

After repairing both types, direct Arb memory-Gram balls certify all ten
time-zero clock-rank packets, with maximum source projector radius
`2.88e-13`.  The outward cross/direction/Ritz recursion then certifies only
17 updates in total: every channel stops at update two or three, seven first
at a threshold branch wall and three first at a Ritz-gap wall.  The closest
decisive ratio is still `1.51`, so the wall is not a displayed-roundoff
contact.

The result is an information obstruction, not a disproof of the exact
recursive chain.  The next route should bound the joint output packet without
separately resolving weak enrichment directions, or redesign the temporal
start and packet gauge.
