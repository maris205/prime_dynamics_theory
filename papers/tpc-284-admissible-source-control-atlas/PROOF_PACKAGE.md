# TPC-284 proof package

## Finite interval-sign lemma

Let an executable interval replay return `C in [c_-,c_+]`.  If
`c_+<0`, then every real value represented by the replay is negative.  If
`c_->0`, every represented value is positive.  The same statement applies to
`rho^2` when its lower endpoint is positive.  This is the only numerical
logic used to classify a row.

## Control-atlas proposition

For the six registered baseline tuples, exponents `s=1,2`, and the six
controls in `DERIVATION_PACKAGE.md`, the certificate and independent replay
establish:

```text
total rows       = 72
negative signs   = 60
positive signs   = 12
zero crossings   = 0
baseline flips   = 8
rho^2 lower end  > 0 on every row.
```

The proposition is finite and conditional on the hash-locked TPC-268 source
engine, source schedule, interval grid, and declared controls.  Its proof is
the replay plus exact rational parsing of every stored endpoint; the source
operator and source profile are not replaced by a fitted model.

## Sign-flip obstruction

The eight flipped keys are

```text
(128,s=1,Q+1), (128,s=2,Q+1),
(192,s=1,z-1), (192,s=1,Q-1), (192,s=2,Q-1),
(256,s=1,z-1), (256,s=1,Q-1), (256,s=2,Q+1).
```

Thus the finite source remains nonzero under every tested control, but its
orientation relative to the baseline is not stable.  Any future sign theorem
must either restrict the control class further or prove a quantitative margin
on a growing schedule.

## Scope firewall

No statement is made about controls outside the six declared maps, continuous
perturbations, or asymptotic sequences.  In particular, the atlas does not
prove literal arithmetic `L2`, a source-identification theorem, a fixed-power
gain, Gate B, or the twin-prime conjecture.
