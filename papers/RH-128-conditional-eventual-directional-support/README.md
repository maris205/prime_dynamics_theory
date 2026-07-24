# RH-128: conditional eventual directional support

Let `x_n=gamma_n^2`.  RH-128 proves that if eventually

```text
x_{n+1} <= rho x_n + q,       0 <= rho < 1,
```

then `limsup x_n <= q/(1-rho)`.  If this fixed point is below one and
`liminf V_n/(L_n^4 C_n) >= A_* > 0`, then

```text
liminf B_n >= (1-sqrt(q/(1-rho)))^4 A_*.
```

Every threshold strictly below this floor is eventually supported.  The
constant-coefficient bound is sharp.  This is the exact conditional closure;
the physical all-level recurrence packet is still unproved.

