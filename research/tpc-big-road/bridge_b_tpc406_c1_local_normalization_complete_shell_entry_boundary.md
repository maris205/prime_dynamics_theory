# Bridge B: TPC-406 complete-shell local-entry boundary

TPC-406 closes the finite shell-selection gap in TPC-405.  At `Q=8192`, the
certificate selects every one of the 872 primes in `Q<p<=2Q`, uses the
explicit alternating CRT residues `0` and `-N`, and audits
`H=16,32,66,128,256` with `N=4H`.  The exact local proxy identity remains
`G_0=V_-S_0`, `G_1=V_-S_1+V_+(S_1-t_1^2)`, `M=t_1P_-`, and proves

```text
0 <= z <= t_1/(a_min sqrt(S_0 S_1)) <= 4/(a_min H) <= 4/H.
```

The producer and independent checker store and replay exact rational data,
including the complete CRT mask profile and both literal masked row energies.
All five rows pass, and the eight mutation stress cases reject altered shell,
domain, bound, case, and claim-firewall fields.

This is a finite theorem for one adjacent entry of a synthetic complete-shell
proxy.  It is not a full normalized operator estimate, a physical `h_0`
theorem, an arithmetic `L2` or sign theorem, a fixed-power saving, Route-B
closure, or a twin-prime conclusion.  The growing theorem and full operator
remain open.
