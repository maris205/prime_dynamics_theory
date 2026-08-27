# TPC-278 derivation package

For each actual packet quadruple define `D`, `G`, `E`, and
`kappa=(D-G)/D` as in TPC-277.  The sign of `E` is the sign of `G-D`:

```text
E<0 <=> r=D/G>1,
E>0 <=> r<1.
```

TPC-278 fixes the source beta, scale, comparison cutoff, projection, and
exponent while varying only the finite shell endpoint `Q` or clock `H`.  The
exact source replay gives the following sign pattern:

```text
N=128: Q=4 NEG, Q=5 NEG, Q=6 POS
N=192: Q=5 NEG, Q=6 NEG, Q=7 POS; H=29 POS, H=35 NEG
N=256: Q=5 POS, Q=6 NEG, Q=7 NEG; N=384 natural control NEG
```

The same natural row can therefore have a favorable or unfavorable signed
gain under a one-step shell or three-unit clock perturbation.  Since these are
finite interface choices, the result is a stability obstruction rather than a
growing counterexample.
