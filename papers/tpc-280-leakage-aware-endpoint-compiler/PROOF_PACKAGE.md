# TPC-280 proof package

## Conditional two-term compiler

Assume `D >= dX^a` and
`G <= BX^(-gamma)D+ell X^(a-delta)`.  Since `D>0`, division and the source
floor imply

`G/D <= BX^(-gamma)+(ell/d)X^(-delta)`.

For `G>0`, taking positive reciprocals gives

`D/G >= [BX^(-gamma)+(ell/d)X^(-delta)]^(-1)`.

Set `kappa=min(gamma,delta)`.  Since `X>=1`, both powers are at most
`X^(-kappa)`, hence the denominator is at most
`(B+ell/d)X^(-kappa)`, proving the collapsed compiler.  The zero-coefficient
case is interpreted separately as `G=0`.

## Margin transfer

The exact four-packet identity from the parent interface is
`m^2=(D/G)m_D^2`.  Substitution of the two-term reciprocal bound proves the
two-term margin inequality.  Substitution of
`m_D>=cX^(-eta_D-epsilon)` and the collapsed gain bound proves the exponent
`-eta_D+kappa/2-epsilon`; replacing a negative effective loss by zero gives
`eta_eff=max(0,eta_D-kappa/2)`.

## Sharpness and obstruction

The equality family in `DERIVATION_PACKAGE.md` saturates the source floor and
the raw output bound, so no uniformly smaller two-term denominator follows from
these hypotheses.  With `delta<gamma` and positive leakage, the second term has
the slower decay and prevents promotion to exponent `gamma`.  The certificate
also tests the borderline endpoint equality: `sigma-eta_eff=1/400` is not a
strict payment.
