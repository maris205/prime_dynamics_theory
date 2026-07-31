# Roadmap after RH-326

RH-326 fixes the first-alias algebra and its sign convention.  In Hardy
normalization, the exact residual is

```text
raw trace packet + positive even parity packet - counterloop alias defect.
```

The parity packet and alias defect have the same weighted exponent, but their
leading ratio depends on the bounded integer clock phase.  Symbolic scalar
equality occurs only at `eta_* = -log(C_* C_M)/log(lambda)`.  If
`C_* C_M lambda < 1`, scalar-only matching fails throughout the common
`|eta| <= 1` integerization window.  Archived ordinary floating-point values
support, but do not certify, that inequality.  Thus the unconditional next
step remains the physical boundary and neighboring-shell calculation rather
than a scalar decimal comparison.

RH-327 should now construct the neighboring-shell coupling in the same data
type:

1. keep `sigma`, `k`, period `2k`, and target `k*R^(-2k)`;
2. keep `eta`, the clearance ratio `d`, and subsequential phase mode;
3. keep the retained coordinates `(V,U,W)`, orientation `(+,-,+)`, and
   output shift `kappa_aff*d`;
4. define the actual trace observation converting a local forward law into a
   signed Hardy-scaled packet;
5. include both critical siblings or an equivalent neighboring-shell
   coordinate, since RH-19 rules out treating the sibling as a small tail;
6. prove a signed decomposition of the raw trace packet with a certified
   remainder.

Once such a decomposition exists, RH-326 gives the exact join:

```text
residual = boundary packet + shell packet + remainder
           + parity packet - counterloop alias defect.
```

RH-328 may formulate a genuine joint matching equation only after the local
trace observation and shell packet are defined.  The second critical leg,
all-leg phase transport, weighted trace-observation norms, and
`o(k*R^(-2k))` remainder remain open.  Gates A--E remain false/open.
