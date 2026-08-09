# RH-390: Growing-Rank Prime-Tail Filtration and Fixed-Rank Necessity

RH-390 proves that exact retention through rank `s-1`, followed by a
factorial Laplace replacement at every rank `r>=s`, is uniformly accurate
at the next prime-tail scale throughout a genuinely growing rank window.
It also proves that deleting one more exact rank fails sharply at every
fixed threshold inside the declared `P/J/I` hierarchy.

The paper and semantic publication PDF are:

- `main.tex`, `references.bib`, and `main.pdf`;
- `growing-rank-prime-tail-filtration.pdf`, byte-identical to `main.pdf`.

## Main theorem

Let `x=p_y`, `L=log x>=512`, fix `0<delta<1`, and put

    S_y=floor((1-delta) log L/log 7).

For exact integers `2<=s<=S_y` and
`1<=K<=floor((2s-1)L)`, retain `P_r` for `r<s` and replace every
`r>=s` by the `K`-term factorial kernel

    K_r=x^(1-2r)/((2r-1)L),
    a_r=1/((2r-1)L),
    S_K(a)=sum_(j=0)^(K-1)(-1)^j j! a^j.

With `Psi_(c;s,K)` the resulting seven coordinates and
`Gap_(s,K)=F(Psi_(s,K))/pi^2`, the safe coordinate ledger is

    |PhiP_c-Psi_(c;s,K)|/K_s
      <= c^s[(4-1/s) A_(s,c) epsilon_x
             + ((2s-1)/(2s+1)) B_(s,c)/x^2
             + C_c K!/{s((2s-1)L)^K}],

where

    A_(s,c)=[(1-x^-2)^s(1-c/(x^2-1))]^-1,
    B_(s,c)=[(1-x^-2)^(s+1)(1-c/(x^2-1))]^-1,
    C_c=(1-c/x^2)^-1.

The endpoint map has `l_infinity`-to-`l_1` Lipschitz constant 126 on the
common cube, so

    max_(2<=s<=S_y, 1<=K<=floor((2s-1)L))
      |GapP-Gap_(s,K)|/P_s -> 0.

The complete factorial window is paid by the symbolic recurrence
`b_(K+1)/b_K=(K+1)/((2s-1)L)<=1`, not by finitely many fixtures.

For every fixed exact `s>=2`, put `r=s-1`.  The all-rank endpoint
coefficient `gamma_r` is positive.  Maynard's bounded consecutive gaps,
the strict successor, and a common-head Taylor estimate give

    limsup p_y^(2r)|P_r-I_(2r)| >= 1/2,
    limsup p_y^(2r) pi^2 |GapP-GapI_(<r)| >= gamma_r/2,
    limsup p_y^(2r) pi^2 |GapP-GapJ_(<r)| >= gamma_r/2.

Thus omitting rank `r=s-1` has unbounded error relative to `P_s`.  This
necessity statement is fixed-rank and applies only to the frozen `P/J/I`
surrogates.

## Exact artifact

The certificate has 72 rows:

     12 kernel/domain/master rows
      7 channel rows
     15 all-rank gamma rows
     12 factorial-window rows
     10 growing-rank rows
     10 fixed-rank necessity rows
      6 theorem/firewall rows

Its epistemic role is `finite_exact_algebra_not_analytic_proof`.  The
canonical certificate is 17,571 bytes with SHA-256
`e2116abd4aeb910c24ee470a520623f29f1f454bb9b5293840875da091682b3b`.
All 24 genuine semantic mutations are rejected by independent field-level
validation.  The `compare_fresh=false` path does not call the certificate
or any row builder.

`results/result.json` is 68,696 bytes with SHA-256
`f91eba3665de25e5572fd71de39f917da40859fb941c9b7df42e84fc02840405`.
The recursively closed official Draft 2020-12 schema is 265,230 bytes
with SHA-256
`d6d0daeb126bc90373f06fcc6314a3de1cb6cfda204629945ef77c7078406039`.

## Reproduction

Install `requirements.txt`, then run:

    make result
    make schema
    make test
    make remote
    make pdf
    make archive

`PYTHON=...` may select another interpreter.  `make remote` invokes the
two frozen upstream verifiers in default-offline mode and performs zero
network requests.  Network access is always explicit:

    make remote-network-jy
    make remote-network-maynard
    make remote-network

Retrieved bytes are never persisted in this publication tree.

## Source closure and redistribution boundary

The proof-minimal immutable closure contains 87 Git blobs from RH-388
release `8e6f89ee1e58e67c53c5f4719c05e881107113ac`.  The ordered Git digest is
`b86cb21288fe9c48304d90ae812829f5e44f4fac0a2b725a09e5c1512ca60cab`.

The ordered Johnston--Yang and Maynard locks give 89 logical inputs in
total, with logical digest
`2255b26dd68adf09f447e251eb5d38c8b1d31fbaa1c26befd8c04165097ed922`.
Johnston--Yang supplies the prime-counting envelope; Maynard supplies the
fixed-rank bounded-gap necessity.  The four external payload hashes are
absent from publication members and from the entire RH-390 tree.

## Claim boundary

The new result is the simultaneous growing-`s`, complete-`K` filtration
and the all-rank positivity bridge.  It is not a direct maximum of fixed
rank results.  There is no growing-rank necessity, arbitrary-surrogate
obstruction, convergent factorial series, complex channel, active `c11`,
growing clock, `K_N`, operator, trace, zero identification, or RH claim.
Gates A--E are false.
