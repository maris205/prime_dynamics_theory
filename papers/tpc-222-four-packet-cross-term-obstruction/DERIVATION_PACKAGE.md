# TPC-222 derivation package

Use the convention `⟨x,y⟩=sum_i conjugate(x_i)y_i`. For packet vectors `V_j`, define
`G_(j,l)=⟨V_j,V_l⟩`. Then `G` is PSD and

```text
||sum_j c_j V_j||^2 = c^* G c.
```

For any two vectors, expansion of `||x+i^r y||^2` and the four roots of unity gives

```text
⟨x,y⟩ = 1/4 sum_(r=0)^3 i^(-r) ||x+i^r y||^2.
```

The trace bound follows from `G` being PSD: `lambda_max(G)<=tr(G)`, hence
`c^*Gc<=tr(G)||c||^2`.

For the exact obstruction, let `u=(1,0)`, `s^+=(1,1,1,1)`, and
`s^-=(1,-1,1,-1)`. Set `V_j^+=s_j^+u` and `V_j^-=s_j^-u`. Both Gram matrices have
diagonal `(1,1,1,1)` and trace `4`, but for `c=(1,1,1,1)` the plus energy is `16` and
the minus energy is `0`. Thus trace and individual packet norms do not identify the signed
cross-term. The polarization residuals are nevertheless exactly zero: they recover the
off-diagonal inner products only when the four phase-weighted energies are retained.
