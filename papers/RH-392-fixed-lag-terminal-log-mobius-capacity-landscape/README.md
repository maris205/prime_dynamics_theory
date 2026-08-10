# RH-392: Fixed-Lag Terminal-Log Möbius Diagonalization and the Square-Divisor Capacity Landscape

RH-392 proves terminal-logarithmic diagonalization for fixed finite Möbius
shifts at total degree at most two, and a separate coordinatewise-biquadratic
compiler for one fixed lag. The compiler reduces 512 truth tables to eight
actions and gives the exact safe-table capacity for every fixed `q,h>=1`.

The manuscript artifacts are `main.tex`, `references.bib`,
`outputs/main.pdf`, and `outputs/main.log`. The semantic publication PDF
`fixed-lag-terminal-log-mobius-diagonalization-and-square-divisor-capacity-landscape.pdf`
is byte-identical to `outputs/main.pdf`.

## Main formulas

For fixed distinct shifts and phase polynomials of total degree at most two,
only the constant and diagonal-square channels survive. For fixed `q,h>=1`,

```text
P_r(x,z)=sum_(0<=i,j<=2) c_ij(r) x^i z^j
```

has terminal limit

```text
sum_(r mod q) [c00(r)/q+c20(r)delta_(q,r-h)
               +c02(r)delta_(q,r)+c22(r)theta^(h)_(q,r)].
```

For `A_p={0,h mod p^2}` as a distinct set, `nu_p=|A_p|`, and
`tau_(p,r)=#{a in A_p:a=r mod p}`, the two-site density is

```text
theta^(h)_(q,r)
 = q^-1 prod_(p not|q)(1-nu_p/p^2)
        prod_(p||q)(1-tau_(p,r)/p)
        prod_(p^2|q) 1_(r mod p^2 notin A_p).
```

Only after every fixed-table limit is formed,

```text
G_log(q,h)=max_f |L_(q,h)(f)|=6/pi^2-kappa_h/2,
kappa_h=prod_(p^2|h)(1-p^-2) prod_(p^2 not|h)(1-2p^-2).
```

Squarefree `h` are exactly the maximizers. With
`kappa_*=prod_p(1-2/p^2)`,
`3/pi^2<G_log(q,h)<=6/pi^2-kappa_*/2`, and the lower endpoint is an
unattained infimum.

## Exact artifact

The 640 rows are partitioned as `512+8+64+8+9+7+12+8+6+6`. They exhaust
all `512^2` ordered table pairs, find 3375 compatible pairs, record zero
projection/reflection/involution/parity/interpolation failures, and reject
24 semantic mutations under a builder-independent verifier.

The canonical certificate is 220,832 bytes with SHA-256
`614297795d4d4dfeadfb5667d3e0d405d04fbe8e07e9d87a743faed9cb267a96`.
The stored result is 525,078 bytes with SHA-256
`83bab4eb57f1d4d2d31c646946df16203b155d49d78942f74a40df239e404bc0`.
The closed Draft 2020-12 schema is 3,324,186 bytes with SHA-256
`606d0ae74b4da9e4a97e6a951e89dfd4237108028c9b2436030e2d6861ec8f5d`.

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

`make remote` performs strict local-lock verification only. All three rows
return `NETWORK_DISABLED`, `network_opt_in=false`, and `requests_made=0`;
the verifier exposes no network implementation.

## Immutable source closure

The closure is rebound to RH-389 commit
`8b1a875b4bbefd955a419593951ce2d09987ac6f`. It contains 106 Git objects
in groups `95+8+3`, with ordered group digests:

```text
8a674e5d60237b4463e1f68ef79965633ed11a4d098957e5be44e05f471174cb
87bbdb455fa5217404d863d1054b4ae408de69da6701ff42ac439ec9bfe1605c
a03e4ba7d8b5b054acc95288c70e753bf22b82bb1957f635891b28682c67840e
```

The all-Git digest is
`3b32865a14618a605915beb8eab6432b048fca49718b69519697ef861cbe650f`.
Three ordered remote locks bring the closure to `106+3=109`, with digest
`39bf8e9030b511e85fdf26a7c71722c3e4be5bc74bc738aa253bbc29c94517f9`.

Tao Theorem 2, equation (3), is the only remote analytic input. The
Johnston--Yang and Maynard locks are inherited closure-only provenance and
are not used in this proof. No remote PDF or source archive is vendored.
All five sealed payload identities are absent from every publication member
and from the complete RH-392 tree.

## Release boundary

The fixed publication manifest contains 38 members; manifest and report
bring the release-stage set to 40 files. It hard-gates frozen Stage-1 and
manuscript hashes, result/schema regeneration, official schema validation,
106+3 source closure, rights metadata, zero-request replay, semantic-PDF
identity, payload exclusion, and tree hygiene.

All data are fixed before the terminal limit. There is no growing period or
lag, growing shift family, ordinary Cesàro theorem, effective uniform rate,
degree-three multicoordinate truth-table law, interacting multi-lag compiler,
maximum-before-limit selector, operator, trace formula, zero model, or claim
of the Riemann Hypothesis. Gates A--E remain false.
