# Route update after RH-114

The missing directional tail can be expressed by one scalar generalized
Rayleigh constant

```text
gamma_Q^2 = lambda_max(G_Q^(-1/2) D_Q G_Q^(-1/2)).
```

The positive-tail block theorem supplies `D_Q=delta B_Q` whenever the tail
is PSD and its packet block `B_Q` is controlled.  RH-115 should compose this
bound with the frame certificate and the earlier volume/capacity factors,
using the maximum of all valid lower bounds.  The practical question is no
longer whether a directional route exists, but which directional upper is
stable under memory-depth changes.
