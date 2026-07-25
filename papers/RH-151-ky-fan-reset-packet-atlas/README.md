# RH-151: Ky--Fan Reset Packet Atlas

RH-150 showed that separated recursive packet-radius transport stops by the
third update.  RH-151 replaces direction-coordinate propagation by two
gauge-free quantities.

First, a sharp Ky--Fan theorem converts captured-energy loss `L` across a
rank boundary of gap `g` into

`||P-Q|| <= sqrt(L/g)`.

A branch-free scalar recursion follows for every Ritz update whose search
space contains the previous packet.  It is rigorous but too lossy on the
frozen chains: only 11 of 130 snapshot bounds remain informative.

Second, each moving-memory Gram is independently reset to its native
clock-rank top packet.  Arb matrix balls plus a polar-corrected long-double
gap audit certify all 130 snapshots.  The minimum gap-to-twice-radius ratio is
`60.37`, and the maximum reset projector radius is `0.00836`.

This changes the primary route.  The next paper should test transition
coherence of the reset atlas before inserting it into the outward assembly.
