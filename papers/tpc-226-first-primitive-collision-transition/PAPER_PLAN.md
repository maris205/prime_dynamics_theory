# TPC-226 paper plan

## Research question

For the literal primitive TPC-220 rows, what is the smallest integer dilation of the
TPC-225 source-surrogate clock that creates a legitimate cross-prime support collision,
and does the first collision force an AP energy saving?

## Frozen clock family

For an integer dilation `L in {1,2,3,4}` and an integer `Q>=8`, use

```text
x=Q^3,
H=4Q^2,
h_L=4LQ,
Q<q<2Q prime,
M_L(q)={m: 0<|m|<=floor(Lq/Q), gcd(m,h_L)=1},
C_h=1/h_L.
```

The primitive condition is mandatory.  In particular, the tempting `L=3`, `Q=8`,
`m=4` overlap is rejected because `gcd(4,96)>1`.

## Main theorem target

1. For `L=1,2,3`, distinct prime-row supports are pairwise disjoint.
2. For `L=4`, every collision is, up to exchanging the two primes and changing all
   signs, the resonance

   ```text
   7p+3r=16Q,
   m_p=3,
   m_r=-7.
   ```

3. The first stable exact witness is `Q=25`, `(p,r)=(37,47)`.
4. On every nonempty `L=4` resonance graph, aligned and inherited affine profiles
   strictly amplify `E_AP`, while balanced sign profiles strictly reduce `E_AP` and
   annihilate `E_pol` and `E_all`.

## Planned exact certificate

- full primitive collision classification for every `Q=8,...,512` and `L=1,...,4`;
- selected multi-scale `L=4` witnesses through `Q=1000`;
- exact `Fraction` energies for aligned, affine, and balanced-sign profiles;
- a nonprimitive adversary that confirms why the apparent `L=3`, `m=4` overlap is
  invalid;
- independent normal/optimized replay with byte-identical output.

## Claim boundary

This paper may claim an exact finite structural transition and profile-dependent signed
energy law.  It may not claim that `h=16Q` is the physical V46 clock, that the balanced
odd packets are the arithmetic packets required by Gate B, or that any fixed-atom,
`L^2`, strict `1/400`, or twin-prime consequence has been proved.
