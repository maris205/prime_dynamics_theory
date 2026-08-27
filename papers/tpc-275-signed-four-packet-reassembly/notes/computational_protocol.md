# TPC-275 computational protocol

1. Load the frozen TPC-268 engine and verify the canonical TPC-274 parent
   payload digest.
2. Rebuild the literal operator matrix and rank-three projection independently
   with `Fraction` arithmetic.
3. Split the exact beta vector into four source blocks and compute the packet
   vectors, 4-by-4 Gram, diagonal energy, signed output energy, and DFT mode
   energies.
4. Recompute all six pairwise plus/minus polarization probes and verify their
   recovered cross terms.
5. Transfer only the parent outward intervals for `C_perp`, `W_perp`, and the
   actual output lane; evaluate the packet-diagonal margin proxy.
6. Run the independent checker, five-mutation stress audit, PDF checks, and
   normal/optimized byte-identity checks.

The matrix and packet fields are exact rational values.  The finite thresholds
`G-D<0`, `D/G<12/5`, `F/G>50`, and `m_D^2<1/16` are not extrapolated in `N`.
