# TPC-237 route evaluation

## Route A

`(A0,A1,A2,A3,A4)=(false,false,false,false,false)`.  Route A is not addressed.

## Route B

- `L0`: exact TPC-218 primitive common-source kernel retained.
- `L1`: collision-compressed finite-window packet-trace theorem with normalized
  exponent `1/48` and secondary exponent `1/50`.
- `L2`: `NONE`.
- full Gate B: `OPEN`.
- strict `1/400`: `UNPAID_GLOBAL`.

## Extracted state

- strongest positive result: replacing the coarse `P` scalar collapse by primitive
  physical incidence yields
  `N^(-1)sum_n sum_j|K_j(n)|^2 << JM^2[x^(1/48)+x^(1/50)](log x)^5`.
- strongest obstruction: every controlling inequality is unsigned; no simultaneous
  saturation, signed `C_h` cancellation, or signed four-packet scalar is proved.
- open theorem: decide whether the literal `|C_h|^2`-weighted collision energy is
  strictly smaller than the uniform `R_*` product, or construct a source-valid
  saturation obstruction.
- reusable structure: `primitive bucket collision compression -> reduced-frequency
  large sieve -> exact exponent ledger`.
- `ROUND2_CLUE`:
  `TEST_THE_ACTUAL_WEIGHTED_COLLISION_ENERGY_BEFORE_SEEKING_CROSS_H_SIGN_CANCELLATION`.

## Evaluator verdict

`CONTINUE_WITHIN_FAMILY`.  TPC-237 is a real structural Route-B advance because it
lowers the common-source finite-window trace exponent from `11/32` to `1/48` without
changing the object.  It is not an arithmetic advance and cannot be promoted beyond
`PROVED_STRUCTURAL_L1`.
