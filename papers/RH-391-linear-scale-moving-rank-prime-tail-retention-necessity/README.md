# RH-391: Linear-Scale Moving-Rank Prime-Tail Retention Necessity

RH-391 proves a same-rank, two-endpoint retention obstruction throughout
the full linear moving-rank regime.  Maynard's bounded-consecutive-gap
theorem first yields one fixed gap `h_*<=600` repeated on infinitely many
consecutive-prime edges.  Along those edges, the same exact rank is used
at both endpoints, with `r->infinity` and `r<=C*x` for one fixed `C>0`.

The paper and semantic publication PDF are:

- `main.tex`, `references.bib`, and `main.pdf`;
- `linear-scale-moving-rank-prime-tail-retention-necessity.pdf`,
  byte-identical to `main.pdf`.

## Main theorem

On an extracted edge

    x=p_y, q=p_(y+1)=x+h_*, h_*<=600,

define

    E^I=P_r-I_(2r), E^J=P_r-J_r,
    Delta^I=pi^2(GapP-GapI_(<r)),
    Delta^J=pi^2(GapP-GapJ_(<r)),
    a=(x^2/(q^2-1))^r, rho=(x/q)^(2r).

For every fixed `C>0` and exact same-edge ranks satisfying
`r->infinity` and `r<=C*x`,

    x^(2r)(E^I(y)-E^I(y+1))=a+o(1),
    x^(2r)(E^J(y)-E^J(y+1))=a+o(1),
    x^(2r)(Delta^I(y)-Delta^I(y+1))/gamma_r=a+o(1),
    x^(2r)(Delta^J(y)-Delta^J(y+1))/gamma_r=a+o(1).

The all-rank coefficient obeys, for exact `r>=7`,

    gamma_r>=kappa_gamma*7^r/r,
    kappa_gamma=4*u8_lower/7>0.0347017856545.

For any of the four scalar or gamma-normalized endpoint errors `Q_r`,

    liminf ((1+rho)/a)
      max{x^(2r)|Q_r(y)|,q^(2r)|Q_r(y+1)|} >= 1.

If the optional profile hypothesis `r/x->lambda<infinity` holds, put
`a_0=exp(-2*lambda*h_*)`; then the pair lower bound is
`a_0/(1+a_0)`.  Without convergence of `r/x`, the linear bound gives
`exp(-1200*C)/2`.  The sublinear case gives `1/2`.  Every raw pair error
also dominates `P_(r+1)` by an unbounded factor.

The proof uses elementary integer tails, not a linear-rank asymptotic
`P_r~K_r`.  Necessity is pairwise and only for the frozen `P/J/I`
hierarchy.

## Exact artifact

The certificate has 60 semantic rows:

     10 definition rows
     12 edge rows
     12 gamma rows
     12 vector/Taylor rows
      8 pair-profile rows
      6 theorem/firewall rows

Its epistemic role is `finite_exact_algebra_not_analytic_proof`.  The
canonical certificate is 10,062 bytes with SHA-256
`cc2874435e62205a3e969e841d80d37243d95826855bd242f0eff3478dccf367`.
All 24 genuine semantic mutations are rejected.  The independent false
verification path calls no row or certificate builder.

`results/result.json` is 61,539 bytes with SHA-256
`023aa55c4a4e3795994eed866cc9d1412aef90bc0df9b27831f3718c069c1046`.
The recursively closed official Draft 2020-12 schema is 230,301 bytes
with SHA-256
`f5fd98019eefdf600432ca59c6546a6c6d5c7c832a4f8da0603512d20ee40f54`.

## Reproduction

Install `requirements.txt`, then run:

    make result
    make schema
    make test
    make remote
    make pdf
    make archive

`PYTHON=...` may select another interpreter.  `make remote` invokes the
frozen Johnston--Yang and Maynard verifiers in default-offline mode; both
make zero network requests.  Live verification always requires an
explicit target:

    make remote-network-jy
    make remote-network-maynard
    make remote-network

Retrieved bytes are never persisted in this publication tree.

## Source closure and redistribution boundary

The proof-minimal immutable closure contains 97 Git objects from RH-390
release `a3aa5977e9b3338e4c3035c6c42b60d50bc3ac3b`, in groups of sizes
`87+8+2`.  The ordered group digests are:

    098fdd54388471145bb2ffa8647c23b2f07e995a34e247c4e9a60ae45cd2435d
    e9a95e0c52d6063b56a0fa19479efbf419ba91f486f1697a4128c238d3312c93
    335f7b279a604eaf2259f826770d066173eab66f0fbfcd3a171770ee5ec4c460

Their aggregate digest is
`1250b73311e3fef4b2e7139db887043164f3f20a527cd45c0d5f2fad7f69bd96`.
The ordered Johnston--Yang and Maynard locks bring the closure to
`97+2=99` logical inputs, with digest
`760d1e8babf789588a4238e179193f03319de04d276d7180dd4c85b6359bccbb`.

Maynard supplies bounded consecutive gaps and the fixed-`h_*`
extraction.  Johnston--Yang is inherited provenance only and is not used
for a linear-rank prime-tail asymptotic.  The four external payload hashes
are absent from every publication member and from the entire RH-391 tree.
Both remote locks retain `redistributable_in_release=false`.

## Release and claim boundary

The fixed publication manifest contains 34 members; manifest and report
bring the release-stage set to 36 files.  The archive gates exact Stage 1
and manuscript hashes, `97+2=99` source closure, offline zero-request
replay, remote rights/nonvendoring, semantic-PDF identity, and recursive
payload exclusion.

There is no arbitrary single-vertex schedule, different rank at the two
endpoints, arbitrary-surrogate obstruction, `r/x->infinity` theorem,
linear-rank `P~K` assertion, complex channel, active `c11`, ordinary
Cesaro or growing-clock statement, `K_N`, RH-389/TPC-137/Tao dependency,
operator, trace, zero identification, or RH claim.  Gates A--E are false.
