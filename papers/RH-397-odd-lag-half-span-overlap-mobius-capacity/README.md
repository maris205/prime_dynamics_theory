# RH-397: Odd-Lag Half-Span Overlap Mobius Capacity

RH-397 fixes an integer lag `h>=1`, a finite declared phase clock `q`, every
table `F_r:{-1,0,+1}^3->{-1,+1}`, and an admissible terminal clock before the
limit.  The centered rule reads

```text
F_(n mod q)(mu_0(n-h), mu(n), mu(n+h))
```

and is universally half-span safe when, for every phase and every four-symbol
word, it never fires positively both at phase `r` and at phase `r+h` on the
two-symbol overlap.  The fourth symbol belongs only to this finite safety
test; it is not a fourth analytic shift.

## Exact endpoints

Put `K1=6/pi^2`, let `kappa2(h)` and `kappa3(h)` be the collision-aware two-
and three-shift squarefree densities, and let `Theta_(h,q,r)({L,C,R})` be the
phase-resolved three-shift mass.  For every fixed `h` and finite `q`,

```text
C_h^hs(q) = K1 - kappa2(h)/2
            + (1/4) max_J sum_(r in J) Theta_(h,q,r)({L,C,R}),
```

where the maximum is over `J subset Z/qZ` with
`J intersect (J+h)=empty`.  This is a weighted independent-set formula; the
weights cannot be replaced by unweighted cardinalities.

For every fixed odd `h`,

```text
max_(finite q) C_h^hs(q)
  = C_h^hs(2)
  = K1 - kappa2(h)/2 + kappa3(h)/4.
```

Equality holds exactly when the declared clock `q` is even.  Every odd clock
is strict.  Declared-clock parity, rather than minimal period, is the
classification: literal repetition to any even clock preserves an attaining
two-phase family.

## Proof architecture and boundary

RH-394 supplies the sole analytic fixed-three-shift terminal law, inherited
through the direct finite predecessor RH-396.  Positive projection reduces
the problem to the relations
`A_r={(x,y):F_r(x,+1,y)=+1}`.  Source and target flags turn universal overlap
safety into `t_r s_(r+h)=0`.  Each flag class saturates to one of four exact
rectangles of sizes `4,6,6,9`.  Collision-aware weights `M,U,V,W`, the exact
translation `V_r=U_(r+h)`, and nonnegative edge filling leave precisely the
weighted rising-set bonus above.  The two-phase clock realizes the total
three-shift mass for odd `h`; a CRT argument proves that an odd clock must
lose positive mass.

The window is centered and noncausal.  The theorem does not address growing
`h`, growing `q`, growing or adaptive tables, effective uniform rates,
ordinary Cesaro averages, a maximum taken before the terminal limit, even-lag
all-clock classification, even four-shift laws, generic graph capacity,
operators, trace formulas, zeta zeros, the Riemann Hypothesis, or Gates A--E.

## Exact executable artifact

The finite certificate has 72 rows partitioned `10+10+12+12+12+12+4`.  It
enumerates all 512 ternary relations and all 262144 ordered relation pairs,
of which exactly 61440 are safe.  Its canonical encoding is 24297 bytes with
SHA-256
`23f714236b53c2b89caa72b53f8139cfeab74cd07132082061c3ab0dfc048697`.
All 60 core, 78 result, and 32 schema mutations are rejected.

The stored result is 151768 pretty bytes with SHA-256
`d21f3ab160c7cb5cfca1ff04ac7d2104ea8a7802b36eb3e2f07e32cbe1d27e4f`;
its canonical object is 105495 bytes with SHA-256
`d2445cc883371ccfd96eeb09f908d62d232fcb5cde5ea9170aa2029956047c2a`.
The recursively closed Draft 2020-12 schema is 670920 pretty bytes with
SHA-256
`4f16580a613e3e0c3930fd53e3a418023fac96e2cfa15f74ed447a60bea38f83`;
its canonical object is 257468 bytes with SHA-256
`c3a5b2a02b027cc18b67e63b32f0a238990a4754fe4f2f2ce3c8d1acf756b910`.
These finite checks reproduce identities and attack implementation drift;
they are not asymptotic evidence.

## Reproduction and release

Install the pinned requirements and run:

```text
make result
make schema
make test
make test-optimized
make remote
make pdf
make archive
```

`make remote` is strictly offline.  All four source-lock invocations report
`NETWORK_DISABLED`, `network_opt_in=false`, and `requests_made=0`.

The source closure contains 172 Git objects in groups `160+8+4`, plus four
ordered remote locks, for 176 logical inputs.  The publication manifest has
41 members; manifest and verification report bring the release-stage count
to 43.  The semantic PDF
`odd-lag-half-span-overlap-mobius-capacity.pdf` is required to be byte-exact
with `main.pdf`.
