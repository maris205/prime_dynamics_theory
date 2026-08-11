# RH-395: All-Clock Rigidity for Centered Three-Window Möbius Capacity

RH-395 studies a centered, deliberately noncausal three-window sign rule.  At
phase `r`, a fixed table reads

```text
(mu_0(n-1), mu(n), mu(n+1)) in {-1,0,+1}^3
```

and universal safety forbids two `+1` outputs at distance two for every
ternary word.  The terminal-logarithmic limit is formed for each fixed clock
and fixed table before the finite safe maximum is taken.

The complete fixed three-shift terminal-log table law from RH-394 makes the
limit analytic.  Positive projection and saturation then turn the problem
into an exact finite relation optimization.  Fixed-clock memory can help, but
the all-clock endpoint is rigid: the supremum equals the RH-375 one-site
endpoint and is not attained by any finite clock.

The frozen manuscript quartet is `main.tex`, `references.bib`, `main.pdf`, and
`main.log`.  The semantic publication PDF
`all-clock-rigidity-for-centered-three-window-mobius-capacity.pdf` is
byte-identical to `main.pdf`.

## Principal theorem

Let `T={-1,0,+1}` and fix `q>=1` and tables `F_r:T^3->{-1,+1}`.  For every
terminal clock `1<=omega(X)<=X` with `omega(X)->infinity`, RH-395 studies

```text
epsilon_n = F_(n mod q)(mu_0(n-1),mu(n),mu(n+1))
```

under the safety condition that no pair of phase tables can output `+1` at
distance two on a shared ternary coordinate.  If `L_q(F)` is the fixed-table
terminal-log limit, then

```text
C(q)=max_(F fixed and safe) |L_q(F)|.
```

After positive projection, put

```text
A_r={(x,y):F_r(x,+1,y)=+1},
Y_r=Target(A_r),
A_r=(T\Y_(r-2)) x Y_r.
```

With

```text
lambda_r(x,y)=2^(-1_(x!=0)-1_(y!=0))
              Pi_(q,r)({C} union supp(x,y)),
K_r(U,V)=sum_(x notin U,y in V) lambda_r(x,y),
```

the exact optimizer is the tropical trace on all eight subsets of `T` along
the `r -> r+2` phase cycles.  For `q>=3`, multi-affinity permits a four-state
antipodal optimizer.  The self-loops `q=1,2` remain eight-state problems; in
particular, `q=2` genuinely needs a singleton-sign state.

Writing `K_j=prod_p(1-j/p^2)`, the first exact capacities are

```text
C(1)=K2-K3
C(2)=(3K2-K3)/4
C(3)=3K1/8=9/(4*pi^2)
C(4)=2K1/3=4/pi^2
C(6)=K1/8+K2/2.
```

At `q=6`, the centered value exceeds the corresponding one-site value
`3K1/8` because `2K2-K1>0`.  Nevertheless, for the RH-375 square clocks
`q_y` and endpoints `B_y`, the centered marginal charge proves

```text
C(Q)=B_y
```

whenever `q_y|Q` and `Q` has the same prime support.  Lifting any finite `q`
to a suitable such `Q` gives

```text
sup_(q finite) C(q)=B_infinity,
C(q)<B_infinity for every finite q.
```

## Exact finite artifact

The certificate has 72 rows with partition

```text
8 subset-state
+ 10 transfer/compression
+ 16 q=2 self-loop
+ 12 small-clock
+ 12 marginal-charge
+ 8 square-saturation
+ 6 theorem-firewall.
```

It scans all `262144` ordered relation pairs and finds exactly `3375` safe
pairs.  The canonical certificate is 32,983 bytes with SHA-256
`31afb062208af97fddb5192bc4d6f1f4f030ad69b5a3f9b6ed1d1d9b2b1128a9`.
All 57 named core mutations and all 45 named result mutations are rejected.
The certificate is a finite reproduction and regression artifact, not the
analytic proof.

The stored result is 148,331 pretty bytes with SHA-256
`7557bcc78811b29d7ac9f155fd8553c75d70b659748a37cf2fef427af4958f27`;
its canonical object is 101,772 bytes with SHA-256
`9377280e97c1c92f92f492abb10edb72ae2b4b08b90b2ded1c30cf57e2904c9b`.
The recursively closed Draft 2020-12 schema is 678,979 pretty bytes with
SHA-256
`2eb368a88cc7e3363a3c4f216ea7d3efd423b4faf9bcdec003d36316b2bfe643`;
its canonical object is 265,717 bytes with SHA-256
`1958e593b29b5095efc15eb3a447db12236504d81f447bc6626fde75978d2849`.

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

`make remote` is strictly offline.  Each of the four local lock invocations
returns `NETWORK_DISABLED`, `network_opt_in=false`, and `requests_made=0`.

## Immutable source closure

RH-394 commit `6b3d616851cd2d7cba66371d0aa9f25b8e8bf2f7` is the sole
terminal-log analytic predecessor.  RH-375 commit
`071fed1b2a5d8488b9d2e35a99a753953b233584` supplies only squarefree
phase densities, one-site MWIS data, square-clock endpoints, lift, and
same-prime-support finite combinatorics.

The release-bound Git closure has 148 objects in groups `128+8+4+8`.  Their
ordered group digests are

```text
0a44007f1e5888ed9b1cc6eae380b25fec38e17fe7e4329594625538d36c579b
cab0bfbc807eb5ed2e8c85435a3348fb48d823327a77c740dc281c195fed9e47
e9d259e020d0bef964630388a58487efcdc0a48ee895a6c335f35d0269f6d7e2
14ef15bf6df11e32a05925e5a103c8e2d16ed26abb62620153f9387d84c840ce
```

The all-Git digest is
`9b5e0c04bb3189ddcb802ccb65d5f6b3cc8aa081000acd9fa781fd9f81e50ec9`.
Four ordered remote lock objects bring the logical closure to `148+4=152`,
with digest
`5c4b81ea2f7bdd661fe4374d1174ef3a1909a8327d5982aa01510e4201340bd3`.
The ordered redistribution flags are `false,false,true,false`; all external
PDFs are nonvendored and all six sealed payload identities are excluded.

## Release boundary

The publication manifest contains 41 members; the manifest and verification
report bring the release-stage set to 43.  Executable gates cover all frozen
Stage-1 and manuscript hashes, exact result/schema/manifest/report replay,
official Draft 2020-12 validation, the 148+4 source closure, remote rights and
zero-request replay, semantic-PDF equality, payload exclusion, and whole-tree
hygiene.

No claim is made for a causal or online centered rule, the RH-378 window-end
model, growing clocks or tables, effective rates, ordinary Cesàro averages,
prelimit maxima, adaptive capacities, generic graph capacity, even
odd-support correlations of order at least four, operators, traces, zeros, or
the Riemann hypothesis.  Gates A--E remain false.
