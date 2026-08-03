# RH-350 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| Physical clock | FROZEN | `k=log(1/sigma)/(2log(lambda))+O(1)` with bounded `eta_k`. |
| Growing window | PROVED / FIXED TYPE | `m_(k,j)=k-j`, `2<=j<=J_k`, `J_k->infinity`, `J_k=o(k)`. |
| Exact coefficient identity | PROVED EXACTLY | `p_(k,j)=Y_(k,j)+P_(k,j)-S_(k,j)` in the direct coefficient type. |
| Uniform orbit demand | PROVED | `C_M S/(2H_m x^m)->1` uniformly on the selected window. |
| Uniform parity law | PROVED | `C_M P/(2H_m x^m)=a_k lambda^(2-j)+o(1)` uniformly. |
| Fixed-depth relative minimax | PROVED EXACTLY | Value `(lambda^(J-2)-1)/(lambda^(J-2)+1)` at `2lambda^(J-2)/(lambda^(J-2)+1)`. |
| Physical weighted minimax | PROVED EXACTLY | Unique optimizer `a=1`; finite value `A_N` and positive limit `A_infinity`. |
| Exact weight dominance | PROVED | `x lambda=(28/17)^2>2`; the first weighted-median atom dominates all later atoms combined. |
| Actual aggregate hypothesis | UNPROVED / EXPLICIT | `x^(-(k-2)) sum_j |Y_(k,j)|/(2H_m)->0`. |
| Conditional direct-subprefix law | PROVED CONDITIONALLY | Normalized sum equals `F_(J_k-2)(a_k)/C_M+o(1)` and has positive liminf. |
| Coefficientwise sufficient hypothesis | UNPROVED / EXPLICIT | `max_j |Y_(k,j)|/H_m->0` implies the aggregate hypothesis. |
| Unconditional physical nonclosure | NOT CLAIMED | No actual `Y` theorem is available. |
| Full `E_off`, odd, upper alias | OPEN | The selected lower-even window is not the complete prefix. |
| Finite diagnostics | REPRODUCTION ONLY | `a_k=1`, `Y=0` is a scalar fixture, not an actual noisy observation. |
| RH-288 and Gates A--E | OPEN | No determinant-gluing or Gate condition is activated. |
