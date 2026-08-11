# RH-396: Euler Run Spectrum for Fixed-Lag Centered Mobius Capacity

RH-396 fixes an integer lag `h>=1`, a finite phase clock `q`, and a centered
three-value table before the terminal limit.  At phase `r` the rule reads

```text
(mu_0(n-h), mu(n), mu(n+h)) in {-1,0,+1}^3
```

and universal safety forbids two positive outputs at separation `d=2h` for
every ternary word.  The fixed-table terminal-log limit is taken first, the
finite safe maximum defining `C_h(q)` second, and only then the supremum over
finite clocks.

RH-394's complete fixed three-shift table law is the sole analytic input.
Positive projection and relation saturation give an exact eight-state
tropical trace on the cycles `r -> r+2h`.  Four-state compression is proved
when `q` does not divide `2h`; self-loop clocks with `q | 2h` retain all eight
states.  The obstruction is genuine: at `h=2,q=4`, the full and restricted
coefficient vectors are `(0,0,1/2,-1/2)` and `(0,0,1,-2)`.

The frozen manuscript quartet is `main.tex`, `references.bib`, `main.pdf`, and
`main.log`.  The semantic publication PDF
`euler-run-spectrum-for-fixed-lag-centered-mobius-capacity.pdf` is required to
be byte-identical to `main.pdf`.

## Principal endpoint

Let

```text
p0(h) = min { prime p : p does not divide 2h },
D_h(J) = product_p (1 - |{2hj mod p^2 : j in J}|/p^2),
R_(ell,h) = D_h([0,ell-1]) - D_h({-1} union [0,ell-1])
            - D_h([0,ell]) + D_h([-1,ell]).
```

Then `R_(ell,h)` is the nonnegative density of an exact bracketed squarefree
run of length `ell` in step-`2h` coordinates, and

```text
B_infinity(h) = 3/pi^2
                + (1/2) sum_(1<=ell<p0(h)^2, ell odd) R_(ell,h).
```

For every fixed positive integer `h`,

```text
sup_(q finite) C_h(q) = B_infinity(h),
C_h(q) < B_infinity(h) for every finite q.
```

Across fixed lags,

```text
B_infinity(h) > 3/pi^2 for every h,
inf_(h>=1) B_infinity(h) = 3/pi^2,
```

and the infimum is not attained.  No supremum, maximum, or monotonicity claim
in `h` is made.

## Square-support normalization and strictness

On a square-supported clock `Q`, `N_h(Q)` is the number of positive singleton
phases and `alpha_h(Q)` is the raw, unweighted step-`2h` MWIS cardinality.
The weighted quantity is

```text
M_h(Q) = K1 alpha_h(Q)/N_h(Q),  K1=6/pi^2.
```

If the square support contains `p0(h)`, the manuscript proves
`C_h(Q)=M_h(Q)`.  If `q_P | Q` and the radical is unchanged, then
`N_h(Q)=R N_h(q_P)`, `alpha_h(Q)=R alpha_h(q_P)`, and
`C_h(Q)=M_h(Q)=M_h(q_P)`, with no condition on `gcd(R,2h)`.

The qualification is necessary.  For `h=6`, the pre-`p0` cover `36 -> 72`
changes `(alpha,N)` from `(9,24)` to `(24,48)`, while the qualified cover
`900 -> 1800` scales `(291,576)` to `(582,1152)`.  Fresh-prime lifting obeys

```text
N' = (P^2-1)N,
alpha' = (P^2-1)alpha + E,
M'-M = K1 E/((P^2-1)N),
```

where `E` is the total half-length of the old even runs.  A step is strict
exactly when an even run exists; individual prime steps may plateau.  The
fixture `M_9(36)=M_9(900)=2K1/3` prevents a blanket stepwise-strict claim.
CRT nevertheless creates an even run after a finite extension, proving the
eventual strictness needed for finite-clock nonattainment.

## Exact finite artifact

The certificate has 96 rows partitioned as

```text
12 domain/source/firewall
+ 16 theta/Pi/lambda
+ 16 projection/safety/saturation/full-eight/reflection
+ 12 self-loop/compression/small-clock
+ 12 marginal/square-saturation/lifts
+ 12 finite/infinite D-R endpoint
+ 8 fresh-prime/CRT strictness
+ 8 lag-infimum/claim-ceiling.
```

It scans all `262144` ordered relation pairs and finds exactly `3375` safe
pairs.  Its canonical encoding is 83,309 bytes with SHA-256
`7cc0da78ee7e47a22b357d7e8d907bc9d9879caeb82ede30709e8cb1023032ba`.
All 32 core, 65 result, and 28 schema mutations are rejected.  The artifact
reproduces finite identities; it is not the analytic terminal-limit proof.

The stored result is 290,629 pretty bytes with SHA-256
`a7ea39793a255a9b51f2e1b8523293bf4f4a9fdd0934263f9950417ca28371d4`;
its canonical object is 159,548 bytes with SHA-256
`acda92bfc13344aced86dcae698c75a41ca0fe5097aaaf6141bc2ca88563db12`.
The recursively closed Draft 2020-12 schema is 1,629,267 pretty bytes with
SHA-256
`b78f958c60b1651446a3e0ac2af7a2e696cba2642a6414237877d997ff51691a`;
its canonical object is 482,712 bytes with SHA-256
`adc10d848052eb09412d893292b27b2cd6cbf8227a169476e78691efde5d446c`.

## Reproduction

Install `requirements.txt`, then run:

```text
make result
make schema
make test
make test-optimized
make remote
make pdf
make archive
```

`make remote` is strictly offline.  All four invocations return
`NETWORK_DISABLED`, `network_opt_in=false`, and `requests_made=0`.

## Source and release boundary

The release-bound Git closure contains 160 objects in groups `148+8+4`.
Its all-Git digest is
`472bf5ce5e352dce0d3a44ad10b22345b98e0e8b9a0cd745be9ecd93dedf0a86`.
Four ordered remote locks bring the logical closure to `160+4=164`, with
digest
`72040ab3d7a5d98ce308b91d0748d52a8d4886cf245f5079f14c69ee659cc287`.
The ordered redistribution flags are `false,false,true,false`; no external
PDF is vendored and all six sealed payload identities are excluded.

The publication manifest contains 41 members; manifest plus verification
report make 43 release-stage files.  The executable gates bind every frozen
Stage-1 and manuscript hash, exact result/schema/manifest/report replay,
official Draft 2020-12 validation, the source closure, offline rights,
semantic-PDF equality, payload exclusion, and whole-tree hygiene.

The theorem does not cover growing `h`, `q`, or tables, rates, ordinary
Cesaro averages, maximum-before-limit capacities, causal rules, even
four-shift or larger windows, generic graph capacity, analytic trace or
operator models, zeta zeros, the Riemann hypothesis, or Gates A--E.
