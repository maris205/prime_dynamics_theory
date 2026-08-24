# TPC-237 paper plan

## One-sentence contribution

For the exact primitive-frequency TPC-218 kernel, compress the prime-shell label
inside each physical residue bucket before applying the reduced-frequency additive
large sieve, replacing the coarse `P=#Q_x` scalar-collapse cost by the source-valid
collision factor

```text
R_* = 4Q^2/H + 4UQ/H
```

and proving the normalized packet-trace envelope

```text
N^(-1) sum_(n in I_x) sum_j |K_j(n)|^2
  << J M^2 [x^(1/48)+x^(1/50)](log x)^5.
```

## Frozen title

`Collision-Compressed Prime-Shell Reassembly on Finite Windows`

## Claims and evidence

| Claim | Evidence | Status |
|---|---|---|
| Primitive physical buckets have incidence at most `R_*` | TPC-236 gcd-fiber theorem with `g=(a,h)=1` | `PROVED` |
| The `q` sum may be collapsed before finite-window attachment | Coordinatewise Cauchy on the literal `B_(h,q)^(j)(a)` array | `PROVED` |
| Primitive fractions permit the factor `N-1+U^2` | Farey spacing plus the additive large sieve | `PROVED_STANDARD_INPUT` |
| Direct coefficient energy is `<< JM^2(Q^2/H)(log x)^5` | Fixed-`q` row injectivity and the literal `C_h` harmonic bound | `PROVED` |
| Normalized exponents are `1/48` and `1/50` | Exact rational exponent ledger | `PROVED` |
| A source-active finite fixture reproduces collision and window composition | `(Q,H,U,h)=(101,8830,99,82)` with `C_82^(rat)=1/82` | `NUMERICALLY_CERTIFIED_REPRODUCTION` |

## Claim ceiling

`PROVED_STRUCTURAL_L1_COMMON_SOURCE_COLLISION_COMPRESSED_FINITE_WINDOW_PACKET_TRACE`.

The unsigned packet trace is not the signed four-packet Gate-B scalar.  The proof
retains literal `C_h` at the coefficient interface but subsequently uses `|C_h|^2`;
it proves no signed divisor cancellation, arithmetic `L2`, fixed-atom credit, strict
`1/400` payment, full Gate B, or twin-prime conclusion.

## Natural successor

Test the literal weighted collision energy against the uniform `R_*` product.  A
strict improvement would have to use actual occupancy or signs; a saturation fixture
would instead identify the next obstruction.
