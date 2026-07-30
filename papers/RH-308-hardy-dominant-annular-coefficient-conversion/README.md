# RH-308: Hardy-dominant coefficient conversion

Contractive embedding `H-infinity -> H2` improves the annular coefficient
constant from order `eta^-1` to order `eta^-1/2`.  The `H2` constant is exact,
and dyadic Rudin--Shapiro blocks prove the same order is necessary on the
`H-infinity` unit ball.

At `R=1.4`, `rho=1.41`, the old and improved constants are
`139.00709219858135` and `8.292467894275969`.  The computation uses certified
dyadic lengths `8,64,512`.  Actual mismatch norm decay remains open.

Gates A--E remain false/open.  No Hilbert--Polya operator, Riemann-zero
identification, zeta-divisor equality, or RH conclusion is asserted.
