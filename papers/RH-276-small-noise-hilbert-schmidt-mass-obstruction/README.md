# RH-276: Sharp small-noise Hilbert--Schmidt mass law

For the continuum folded Gaussian operator `A_sigma=K_sigma/0.85`,

```text
sigma ||A_sigma||_2^2 -> 1/(2 sqrt(pi) 0.85^2)
                       = 0.390442618372...
```

Thus the raw family has no Hilbert--Schmidt limit as noise tends to zero.
The exact one-dimensional row formula is audited down to `sigma=0.00025`,
where the scaled value is within `1.04%` of the limit.  This obstruction is
for the raw natural-L2 family; it does not exclude a rank-growing quotient or
cancellation-sensitive trace argument.
