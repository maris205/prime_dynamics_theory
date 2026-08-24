# TPC-226 source lock

- TPC-220 supplies the literal primitive row, including
  `gcd(m,h)=1`, the cutoff `floor(hq/H)`, and the exact multiplicative collision
  congruence.
- TPC-224 supplies the common four-packet Hilbert interface and the finite normalization
  `C_h=1/h`.
- TPC-225 supplies the base source-surrogate clock `H=4Q^2`, `h=4Q` and the instruction
  to move to a nontrivial cutoff before claiming AP dispersion.
- TPC-226 varies only the finite modulus by the declared modeling parameter
  `h_L=4LQ`, `L=1,2,3,4`; it retains `H=4Q^2`, the active prime shell, primitive
  support, row formula, common normalization, and energy definitions.
- The apparent `L=3`, `Q=8`, `m=4` overlap is explicitly excluded because it violates
  the TPC-220 primitive-support condition.
- No PNT, prime-pair density theorem, Möbius cancellation, physical V46 synthesis, or
  fixed-atom transfer is imported.
- Author lock: Liang Wang / Huazhong University of Science and Technology.
