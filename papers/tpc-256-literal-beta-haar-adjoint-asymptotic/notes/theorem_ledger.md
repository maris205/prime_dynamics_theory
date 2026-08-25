# TPC-256 theorem ledger

| ID | Statement | Status | Scope / payment |
|---|---|---|---|
| T256.1 | Real-clock ordered-rank endpoint and Haar normalization formulas | PROVED | All sufficiently large real `x` |
| T256.2 | Truncated divisor Haar lane is `O(U/rho)=O(x^-67/400)` by layerwise density cancellation | PROVED | No Möbius cancellation hypothesis |
| T256.3 | Prime-power child-mean difference is `2log(32/27)/log^2x+O(log^-3x)` | PROVED_SOURCE_BACKED | de la Vallée Poussin PNT |
| T256.4 | `<z_mid,beta>=[log(32/27)/sqrt(2)]sqrt(x)/log^2x+O(sqrt(x)/log^3x)>0` | PROVED_SOURCE_BACKED | Literal beta, ordered-rank Haar |
| T256.5 | `B_Q=(9/2+o(1))x^(2/3)/log x` | PROVED_SOURCE_BACKED | Weighted PNT, frozen prime shell |
| T256.6 | Full mask obeys `|v(t+h)|<=1_(q|h)+2/q` | PROVED | Output unit mask retained |
| T256.7 | Weighted mask first moment is `O_psi(H^2/q)` | PROVED | Fixed Schwartz profile, `q<H` |
| T256.8 | `R_unit=O_epsilon(x^(5/6+epsilon))` | PROVED | Literal beta divisor envelope |
| T256.9 | `R_hard,R_jump=O_(psi,epsilon)(x^(55/48+epsilon))` | PROVED | One outer/internal boundary at fixed displacement |
| T256.10 | Boundary is below diagonal by the fixed exponent `1/48` | PROVED | Choose fixed `epsilon<1/48` |
| T256.11 | Literal adjoint scalar has the stated negative-real complex asymptotic | PROVED_SOURCE_BACKED | One ordered-rank Haar projection |
| T256.12 | Real part eventually negative; scalar eventually nonzero; normalized phase tends to `-1` | PROVED | Branch-free consequences of T256.11 |
| T256.13 | Scalar is exactly real | NOT_CLAIMED | Kernel may be complex/non-even |
| T256.14 | Unqualified principal argument tends to `+pi` | NOT_CLAIMED | Principal branch endpoint ambiguity |
| T256.15 | Finite scaled beta-Haar values approach the target constant | NUMERICAL_OBSERVATION | No proof credit |
| T256.16 | Full-output/transverse estimate for `A_x beta` | OPEN | Required for stronger Gate-B route |
| T256.17 | `L2` control | NONE | Not supplied by one projection |
| T256.18 | Full Gate B and strict global `1/400` payment | OPEN / UNPAID_GLOBAL | No promotion |
| T256.19 | Twin-prime conclusion | NONE | No implication claimed |

## Refuted shortcuts

```text
REFUTED: triangle the divisor layers before cancelling their 1/d densities.
REFUTED: apply centered Poisson separately to the two output-unit pieces.
REFUTED: infer a small adjoint Haar scalar from the complete-lattice zero.
REFUTED: infer scalar reality from a negative-real leading asymptotic.
REFUTED: promote one Haar projection to full Gate B.
```
