# TPC-224 source lock

- TPC-220 supplies the literal row definition
  `B_(h,q)^(j)(a)` and the prime-AP/collision interpretation.
- TPC-222 supplies the four-packet signed/polarized interpretation and the
  warning that diagonal data alone do not identify cross-terms.
- TPC-223 supplies the target role: a common reassembly interface feeding the
  `min-minus-loss` exponent compiler.
- This paper freezes one common coefficient normalization `C_h=1/h` in its
  finite audit. That is a structural normalization choice, not a replacement
  for the V46 source coefficient.
- `source_surrogate` uses `x=Q^3`, `H=4Q^2`, `h=4Q`; `collision_stress` uses
  `x=Q^3`, `H=5Q`, `h=5`, `q=1 (mod 5)`. These clocks are separate and are
  never spliced into one asymptotic assertion.
- No external asymptotic theorem is imported.
