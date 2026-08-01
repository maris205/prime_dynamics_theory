# Roadmap after RH-334

RH-334 supersedes the localized deterministic definition in RH-327.  Any
future use of the boundary/sibling/far slots must use

```text
P_n^abs(J)
  = sum_(f^n(x)=x, abs(x) in J) 1/abs(1-(f^n)'(x))
```

with the boundary-owned physical windows `J_minus=[...,b)` and
`J_plus=[b,...]` frozen before trace or fixed-point evaluation.  The repaired
first-alias constituent is

```text
q_FT = e = B + S + R + P - A,
coefficient_type = hardy_full_trace_constituent.
```

It must not be substituted for the modulus complement: with the noisy-head
discrepancy `d=h-s`, the latter is `tau-a=q_FT-d`.

The next positive route remains theorem-gated.  It may proceed only after one
common physical cyclic data type supplies:

1. sign and moving-order asymptotics for the frozen `B,S,R` slots;
2. a signed far estimate at `o(H_k)` if modular closure is claimed;
3. an identification from any proposed forward/adapted probability law to
   the frozen cyclic basepoint observation;
4. a physical, pre-evaluation exchange/observation map if the shell is split;
5. all-leg Duhamel observation and prefix/suffix bounds for an actual/model
   replacement; and
6. independent off-alias and noisy-head/counterloop closure before any
   determinant statement.

RH-333 blocks the raw full-line forward affine retained-path reference, but
does not block a newly defined cyclic bridge, truncated/folded reference,
Doob transform, or branch-complete nonlinear closing profile.  Those objects
remain `NOT_TESTABLE` until defined and identified in the required trace data
type.

Changing a window after seeing the trace changes individual slots by an exact
nonzero zero-sum vector.  Changing an exchange/model decomposition inside a
fixed shell is a different gauge.  Future papers must declare which operation
is frozen and must compare the aggregate observable slot when no physical
split is available.

No finite reproduction row is asymptotic evidence.  Gates A--E remain
false/open, and no Hilbert--Polya, Riemann-zero, zeta-divisor, or RH claim is
available.
