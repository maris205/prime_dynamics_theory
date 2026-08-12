# RH-398: Exact Lag Endpoint Maximum and Maximizers

RH-398 compares, over all fixed positive lags, the fixed-lag endpoint obtained
in RH-396.  Every lag `h>=1`, finite declared phase clock `q`, phase table,
and admissible terminal clock are fixed before the terminal limit.  The
comparison over finite clocks and then over fixed scalar lags is taken only
after those limits.

## Fixed outer interface

Put `d=2h`, extend the Mobius function by `mu_0(k)=0` for `k<=0`, and let

```text
epsilon_F(n)=F_(n mod q)(mu_0(n-h),mu(n),mu(n+h)).
```

The terminal functional is

```text
L_(h,q,X)(F)=(log omega(X))^-1
                 sum_(X/omega(X)<n<=X) mu(n)epsilon_F(n)/n,
```

where `1<=omega(X)<=X` and `omega(X)->infinity`.  Universal distance-`d`
safety forbids simultaneous positive outputs of `F_r(a,b,c)` and
`F_(r+d)(c,e,f)` for every phase and every `a,b,c,e,f` in
`{-1,0,+1}`.  RH-396 proves the fixed-table limit, the finite safe maximum
`C_h(q)`, and the strict finite-clock endpoint

```text
C_h(q)<B_infinity(h),       sup_(q finite) C_h(q)=B_infinity(h).
```

RH-398 does not alter that analytic interface.

## Product, second difference, and telescope

For each prime `p`, define

```text
t_p(d)=p^2/gcd(d,p^2),
A_m(d)=product_p (1-min(m,t_p(d))/p^2),
R_(ell,h)=A_ell(d)-2A_(ell+1)(d)+A_(ell+2)(d).
```

If `p0` is the least prime not dividing `d`, then `A_m(d)=0` for
`m>=p0^2`.  The nonnegative `R_(ell,h)` are exact-run densities on the
finite-prime CRT phase spaces.  Two finite telescopes give

```text
B_infinity(h)=sum_(m=1)^(p0^2-1) (-1)^(m+1) A_m(d).
```

This is an identity for the fixed scalar endpoint already supplied by
RH-396; it is not a new growing-lag limit.

## Exact maximum and maximizers

The global fixed-lag maximum is

```text
max_(h>=1) B_infinity(h)=B_infinity(1).
```

Equality holds exactly on

```text
M={h>=1 : mu^2(h)=1 and gcd(h,210)=1}.
```

Both conditions are necessary.  At the prime `2`, the strict branch is
`2|h`, equivalently `4|d`; it is not described as an ordinary square-factor
condition on `h`.  For odd primes, a square divisor of `h` is strict, as is a
single factor from `3,5,7`.  Squarefree products of primes at least `11` are
locally invisible through the last possible base run length and hence give
equality.

## Complement, quantitative gap, and joint endpoint

The complement of `M` has the same supremum `B_infinity(1)` but does not
attain it.  For primes `p>=11`, the fixed lags `h=p^2` satisfy

```text
0 < B_infinity(1)-B_infinity(p^2) <= 1/p^2.
```

If `p0(h)>=5`, then `3|d`, local transfer reduces to the `h=3` comparison,
and positive-density exact-run cylinders give the strict chain

```text
B_infinity(1)-B_infinity(h)
  >= B_infinity(1)-B_infinity(3)
  > 1/36750
  > 2/1334025.
```

The cylinder proof retains every factor: `1/2`, `1/25`, `1/49`, a tail
larger than `3/5`, and the local loss `1/9`.  A finite pattern without its
positive-density cylinder would not prove strictness.

Combining the lag maximum with RH-396's strict finite-clock theorem gives

```text
sup_(h>=1,q finite) C_h(q)=B_infinity(1),
C_h(q)<B_infinity(h)<=B_infinity(1).
```

No finite pair attains the joint supremum.  The previously proved lower
endpoint is retained:

```text
inf_(h>=1) B_infinity(h)=3/pi^2,
```

and that infimum is not attained.

## Proof architecture

The comparison is made first on finite-prime CRT phase spaces.  Deleting one
residue class from a positive path of length `L` with period `T` has exact
loss `Lambda_T(L)`.  Its four parity branches are transferred prime by prime
to the three collision levels `v_p(d)=0,1,>=2`.  The local order is weak in
general and strict only at named even run lengths; odd run lengths are equal
at all three levels.  A common cofinal sequence of prime-initial supports and
the absolute Euler-product tail control in RH-396 then pass the finite
comparison to `B_infinity(h)`.  Exact-run CRT cylinders, not isolated finite
words, supply every strict inequality.

## Exact executable artifact

The certificate has 72 rows partitioned
`12+12+12+12+8+8+4+4` across path-deletion loss, local order, telescoping,
strictness, maximizers, complement/gap, joint endpoint, and firewalls.  Its
canonical encoding is 36,635 bytes with SHA-256
`d47de091a8fe5a134ba4bbf8ac4689f53b54786d45dc3bfc7061c99b46bea741`.
All 66 core, 44 result, and 32 schema mutations are rejected.

The stored result is 187,434 pretty bytes with SHA-256
`b22bd32fd515cbe98ee1fc946cef7e695273fdffd002cb5e29281ceba7e263f7`;
its canonical object is 116,612 bytes with SHA-256
`82698f0b7720ac3efcb589c38a9bf8b7b7c285637cab54c7389bd9343925178d`.
The recursively closed Draft 2020-12 schema is 961,955 pretty bytes with
SHA-256
`5852ea6e0718185cd063ec56fd5ace000464f95741a2299e15dcd5405d447e8e`;
its canonical object is 325,778 bytes with SHA-256
`1c7a26bf50e053a6293dfe8f6d226fcef1a3de39abbc62483f430aa729af9134`.
Its exact typed-node counts are `800+209+574+1000+2185=4768`, with no null
nodes.  These finite checks reproduce identities and attack implementation
drift; they are not analytic evidence.

## Source closure and reproduction

RH-396 is the sole load-bearing theorem and analytic endpoint input.  RH-397
is the direct release and provenance predecessor only.  The recursive source
closure contains 184 Git objects in groups `172+8+4`, plus four ordered
remote locks, for 188 logical inputs.  All remote replay is strictly offline.

With the pinned requirements installed, run:

```text
make result
make schema
make test
make test-optimized
make remote
make pdf
make archive
```

The publication manifest requires exactly 41 members; the manifest and outer
verification report bring the release-stage count to 43.  The semantic PDF
`exact-lag-endpoint-maximum-and-maximizers.pdf` must be byte-identical to
`main.pdf`.

The frozen quartet is `main.tex` 27,562 bytes, `references.bib` 468 bytes,
`main.pdf` 358,870 bytes, and `main.log` 27,083 bytes.  The final PDF has 11
A4 pages and 22 embedded, subset, Unicode-mapped font rows.  Complete normal
and `python -OO` replay each collect and pass 75 tests; archive verification
finishes with `failure_count=0`.

## Claim ceiling

RH-398 proves fixed scalar endpoint comparisons only.  It does not address
growing or adaptive `h`, `q`, or tables; `h` or `q` depending on `X`; a
uniform rate; a maximum before the terminal limit; ordinary Cesaro averages;
causal or online rules; monotonicity in `h`; operators; trace formulae; zeta
zeros; the Riemann Hypothesis; or Gates A--E.
