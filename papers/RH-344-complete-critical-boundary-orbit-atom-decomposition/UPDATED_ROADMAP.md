# Roadmap after RH-344

RH-344 replaces the partially extracted RH-338 far atom by the complete
physical `2k`-point boundary-orbit atom across the frozen RH-334 partition.
The remaining critical point has phase-dependent `J^-`/`F` allocation, but
the aggregate orbit atom is independent of that allocation.

The exact critical-order identity is now

    p_(sigma,k,2k)
      = T_k^rest + P_(sigma,2k) - d_(sigma,k,2k)
        - A_(k,2k) - F_k^orb.

Thus direct critical closure requires

    T_k^rest + P_(sigma,2k) - d_(sigma,k,2k)
      = A_(k,2k) + F_k^orb + o(H_k).

Both positive terms on the right are alias-sized, and their sum is
asymptotic to twice the alias packet.  The one marked point omitted by RH-338
is relatively small but still super-target:

    (F_k^orb-D_k^orb)/H_k -> infinity.

The RH-345 checkpoint is therefore a theorem about the actual signed
orbit-free critical remainder.  The narrow positive route is a moving-order
estimate for

    T_k^rest + P_(sigma,2k) - d_(sigma,k,2k)
      - (A_(k,2k)+F_k^orb)

at `o(H_k)`.  A genuine negative route must prove a nonzero
`H_k`-normalized failure for this same physical quantity.

Read-only admissible subroutes include proving a source-backed obstruction to
any proposed scalar-only, cell-separated, or cancellation-blind mechanism,
but such a scoped obstruction must not be advertised as aggregate physical
nonclosure.  In particular, a leading parity/alias phase law alone cannot
replace a theorem for `T_k^rest-d`.

Until an actual moving-order remainder estimate is found, critical signed
compensation is `NOT_TESTABLE`/open.  The lower sideband, remaining off-alias
background, head transport, direct strict prefix, RH-288 activation, and all
Gates A--E remain open.
