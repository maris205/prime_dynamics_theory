# RH-368 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| PCF parameter and invariant interval | PROVED UPSTREAM / LOCKED | `u^3-2u^2+2u-2=0`, `J=[-(u-1),1]`, postcritical itinerary `0→1→-r→r→r`. |
| Three-cell Markov matrix | PROVED UPSTREAM / LOCKED | `A=[[0,0,1],[0,0,1],[1,1,0]]`. |
| Binary parity factor | PROVED UPSTREAM / LOCKED | `+1` positions lie in one parity class; this is `A_{\{2\}}`. |
| Finite capacity identity | PROVED | `K_N^(2)=max_r max(|-M_N+2P_r|,|-M_N-2N_r|)`. |
| Odd/even squarefree densities | PROVED INPUT | `S_odd/N→4/π²`, `S_even/N→2/π²`. |
| Parity Mertens cancellation | PROVED INPUT | `M_N=o(N)` and each fixed parity contribution is `o(N)`. |
| Capacity limit | PROVED | `K_N^(2)/N→4/π²`. |
| Endpoint row | DIAGNOSTIC | `N=2^20`, `K=425095`, ratio `0.4054021835...`. |
| RH-366 distance-two capacity | OPEN / DISTINCT | Only `4/π²≤liminf≤limsup≤6/π²` is known there. |
| Canonical arithmetic coupling | FALSE / NOT CLAIMED | The optimizer reads the Möbius prefix. |
| Operator/zeta/RH identification | FALSE / NOT CLAIMED | No canonical determinant, von-Mangoldt trace, zero model, or RH implication. |
| Gates A--E | FALSE / OPEN | None is closed. |

The finite executable rows validate the formula and source hashes; they do not
prove the analytic-number-theory density inputs.
