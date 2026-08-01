# Roadmap after RH-335

RH-335 supplies one exact finite-order gauge for distributing the global
parity correction across the frozen RH-334 basepoint cells:

```text
C_sigma,n(J)
  = r_H^(-n) [L_sigma,n(J)-P_n^abs(J)
               + ((-1)^n-lambda_minus^n) pi_sigma(J)].
```

For every frozen finite partition, these cells sum to
`c^H_sigma,n-c^H_n`; at `n=2k`, `k>=2`, the first-alias constituent is

```text
q_FT = sum_J C_sigma,2k(J) - A_k,2k.
```

This is an exact ledger, not a physical local parity theorem.  The allocation
`(-1)^n*pi_sigma(J)` uses the noisy Riesz-projector density as a frozen gauge.
Cellwise values are noncanonical because any zero-total signed measure gives
another extension with the same global scalar.  Future work must either keep
this gauge frozen or prove a separate physical identification/transport
theorem before interpreting local parity mass.

The original RH-335 adapted-norm positive route does not activate RH-336.
An actual Duhamel upper estimate still requires, on one physical cyclic data
type and clock:

1. uniform all-leg operator errors `delta_j=O(sigma)`;
2. physical trace-observation and prefix/suffix product norm upper bounds;
3. `max_j W_j=O(sigma^(-gamma))` with
   `gamma<0.3503698834605293...`; and
4. a signed, rather than separately absolute, enclosure at the target scale.

RH-18's quarter-power result is only a lower conditioning bound.  It neither
provides the missing upper exponent nor identifies its packet balance with
the RH-325 physical trace-observation weight.

Accordingly the next admissible route is a theorem-backed signed obstruction
or nonuniqueness result for the two-channel Duhamel allocation.  A positive
physical cancellation theorem may proceed only after all four inputs above
are proved.  Failure of the sufficient majorant alone is not a divergence
theorem.

No finite exact fixture is an actual noisy operator, and no local projector
gauge supplies moving-order, `o(H_k)`, off-alias, head/counterloop, or
determinant closure.  Gates A--E remain false/open.
