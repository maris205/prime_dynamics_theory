# TPC-236 paper plan

## Title

`A Multi-Wrap Collision Envelope for Physical V59 Denominator Fibers`

## Main theorem

For `4Q<H`, `h<=Q`, and fixed residue `a mod h`, physical row multiplicity is at most

```text
2 floor(floor(2hQ/H)/gcd(a,h)) ceil(Q gcd(a,h)/h)
<=8Q^2/H.
```

Pointwise Cauchy then gives a weighted, unnormalized fixed-`h` Bessel inequality and
its exact `h`-direct-sum extension with explicit `C_h`.

## Adversarial theorem edge

The exact V59-shaped fixture `(Q,H,h)=(101,8830,80)` has three identical prime rows
`113,127,193`, so physical multiplicity two and Bessel constant two are false.

## Boundary

Cross-`h` rational-frequency reassembly, cancellation in `C_h`, arithmetic `L2`, and
full Gate B remain open.
