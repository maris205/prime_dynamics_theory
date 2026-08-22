# TPC-223 derivation package

Let `E0` denote the declared baseline exponent for the endpoint ledger.  Let
`delta_AP` be the saving supplied by a literal prime-AP/collision estimate and let
`kappa_pol` be the saving supplied by a phase-labelled four-packet correlation
estimate.  Let `lambda_struct` be the sum of already-paid structural losses.

The conditional interface is

```text
A_x << x^(E0-delta_AP+o(1)),
P_x << x^(E0-kappa_pol+o(1)),
S_x << x^lambda_struct (A_x+P_x).
```

Consequently

```text
E_compiled = max(E0-delta_AP, E0-kappa_pol) + lambda_struct
           = E0 - (min(delta_AP,kappa_pol)-lambda_struct).
```

The effective saving is therefore
`min(delta_AP,kappa_pol)-lambda_struct`.  The strict endpoint gate is paid exactly
when this saving is greater than `1/400`; equality is recorded as `BORDERLINE` and
does not pass.

The algebra is unconditional once the three displayed hypotheses are supplied.  The
two analytic estimates and the literal reassembly interface are not proved by
TPC-223; they remain named conditional inputs.
