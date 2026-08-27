# TPC-283 derivation package

For `S != 0`, let `L_S(u)=<u,S>` and `H_S=ker(L_S)`.  If `C=<w,S>`,
`W=||w||^2`, and `Y=||S||^2`, orthogonal projection onto the line spanned by
`S` gives

```text
w_* = w - (C/Y) S,
<w_*,S>=0,
||w-w_*||^2=C^2/Y.
```

Every `u` in `H_S` satisfies `w-u=(w-w_*)+(w_*-u)` with orthogonal summands,
so `w_*` is the unique closest point in `H_S`.  Dividing by `W` yields the
relative squared radius `C^2/(WY)`.  The TPC-282 interval for this quantity is
therefore also an interval for the zeroing radius squared.
