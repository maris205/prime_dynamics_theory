# Route update after RH-113

The exterior certificate can be reduced to four directional actions without
loss on the archived fine chain and with less than `4.7e-6` relative loss on
the full five-scale chain.  This bypasses the global wedge-Lipschitz barrier.

The unresolved quantity is now the residual action `R Q`, not the whole tail
operator.  RH-114 should bound its Gramian relative to the recent restricted
Gramian.  A PSD-Rayleigh inequality of the form

```text
(RQ)^*(RQ) <= gamma^2 (AQ)^*(AQ)
```

would imply a multiplicative four-volume factor `(1-gamma)^4` and would make
the missing physical assumption explicitly directional.
