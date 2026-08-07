# RH-384 Theorem Ledger

## Frozen inputs

| ID | Input | Immutable origin | Status |
|---|---|---|---|
| I1 | Fixed finite `q` before `N -> infinity`; universal distance-two safety; phasewise `c11=0` | RH-379–RH-383 | locked |
| I2 | `q_y=4*prod_{i<=y} p_i^2`, strict `P_r(y)=sum_{p>p_y}(p^2-1)^(-r)` | RH-383 | locked |
| I3 | `gap=A*T+B*T^2+C*S+O(T^3)` with the three Euler-ratio coefficients | RH-382 | locked |
| I4 | `pi(x)~x/log x` | Montgomery–Vaughan, Chapter 6; RH-2 repository provenance | locked |
| I5 | 51-file recursive source closure, aggregate SHA-256 `90434e...e0e4` | released blobs only | PASS |

## New theorem edges

| ID | Claim | Proof edge | Status |
|---|---|---|---|
| T1 | For fixed `r>=1`, `P_r(y)~1/[(2r-1)p_y^(2r-1)log p_y]` | strict Stieltjes boundary plus PNT tail-supremum error control | proved |
| T2 | For fixed `lambda=1^k1...` of degree `d` and length `ell`, `P_lambda~prod(2r-1)^(-k_r) p_y^(-(2d-ell)) log(p_y)^(-ell)` | finite multiplication of T1 | proved |
| T3 | `p log p*T->1` and `3p^3 log p*S->1` | T1 at `r=1,2` | proved |
| T4 | `S/T^2->0`, `T^3/S->0`, `S/[T^3 log^2 p]->1/3` | exact quotient algebra from T3 | proved |
| T5 | Five normalized gap limits L1–L5 | RH-382 input plus T3–T4 | proved |
| T6 | `Y_infinity-2*m_infinity>0` | Bonferroni Euler tail and precision-80 directed interval | certified |
| T7 | The twice-subtracted residual is eventually positive and divided by `T^3` tends to `+infinity` | T5, T6, `S/T^3~log^2(p)/3` | proved, ineffective |

The Abel boundary is explicitly

`-pi(p_y)/(p_y^2-1)^r`.

After reduction to `p^(-2r)`, it changes the apparent integral coefficient `2r/(2r-1)` to the correct net constant `1/(2r-1)`.

## Exact-subtraction contract

| Limit | Exact expression | Forbidden bare-PNT substitution |
|---|---|---|
| L1 | `gap` | none |
| L2 | `gap-A*T_y` | `A/(p_y log p_y)` for `A*T_y` |
| L3 | `(gap-A*T_y-B*T_y^2)/S_y` | either first- or second-order surrogate |
| L4 | `3p_y^3 log(p_y)*(gap-A*T_y-B*T_y^2)` | either first- or second-order surrogate |
| L5 | `(gap-A*T_y-B*T_y^2)/(T_y^3 log(p_y)^2)` | either first- or second-order surrogate |

Bare PNT supplies only relative `o(1)` errors. Those errors need not be `o(T_y^2)` for L2 or `o(S_y)` for L3–L5.

## Endpoint disclosure

The exact theorem interface uses `p>p_y` and first atom `p_(y+1)`. The exact successor identity locks that membership. The inclusive mutation adds one atom of order `p_y^(-2r)`, which is relative `o(1)` compared with the tail main term, and PNT gives `p_(y+1)/p_y->1`. Consequently neither endpoint mutation is claimed to contradict the leading asymptotic.

## Numeric certificate

- Integer cutoff: `N=100000`.
- Odd primes through cutoff: `9591`; last `99991`; next `100003`.
- Tail telescope: `theta_N=200001/20000200000`.
- Precision: 80; lower operations `ROUND_FLOOR`; upper operations `ROUND_CEILING`; `FloatOperation` trapped.
- Each upper tail loss `(m-1)*theta_N` is computed under ceiling rounding before its complement is rounded downward.
- Frozen enclosure: `[1.5463476716710499204, 1.5484488989771761113]` for `Y_infinity-2*m_infinity`, not for `C` itself.
- Canonical bytes/SHA-256: `48689` / `01c91e57a01de9841f282327ab2f6e1a9368e136393ddab7a2cfe6b019a519c8`.

## Nonclaims

No growing `r`, growing partition, effective PNT threshold, growing clock, active `c11` cancellation, adaptive capacity, intrinsic determinant, scattering completion, self-adjoint generator, von Mangoldt weighted prime-power trace, completed-zeta divisor equality, Riemann-zero identification, or proof/reduction of RH is claimed. Gates A–E are all false/open.
