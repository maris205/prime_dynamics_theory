# RH-388: Rank-One P2-Scale Prime-Tail Resummation

RH-388 proves a uniform factorial resummation at the intrinsic `P_2`
scale while retaining the exact rank-one prime tail.  It also proves,
using Maynard's bounded consecutive prime gaps, that replacing this
rank-one coordinate by either frozen smooth `J` or `I` kernel cannot
meet the same `P_2` contract.

The paper and semantic publication PDF are:

- `main.tex`, `references.bib`, and `main.pdf`;
- `rank-one-p2-tail-resummation.pdf`, byte-identical to `main.pdf`.

## Main result

For `x=p_y`, `L=log x>=512`, and every integer
`1<=K<=floor(3L)`, set

    K_r = x^(1-2r)/((2r-1)L),
    a_r = 1/((2r-1)L),
    S_K(a) = sum_(j=0)^(K-1) (-1)^j j! a^j,
    I^[K]_(2r) = K_r S_K(a_r),
    Psi^[K]_c = c P_1 + sum_(r>=2) c^r I^[K]_(2r)/r.

For the exact RH-383 endpoint map `F`, define
`GapP=F(PhiP)/pi^2` and `GapK=F(Psi^[K])/pi^2`.  The theorem gives

    pi^2 |GapP-GapK|
      <= x^-3/L [7560 epsilon_x + 1638/x^2
                 + 1176 K!/(3L)^K]

and the genuinely uniform conclusion

    max_(1<=K<=floor(3 log p_y)) |GapP-GapK|/P_2(y) -> 0.

Maynard's theorem supplies infinitely many consecutive prime gaps at
most 600.  Along them the exact successor jump proves

    limsup p_y^2 |P_1-I_2| >= 1/2,
    limsup p_y^2 pi^2 |GapP-GapI| >= X_infinity,
    limsup p_y^2 pi^2 |GapP-GapJ| >= X_infinity.

This necessity statement is only for the declared `P/J/I` hierarchy;
it is not a universal impossibility theorem for every surrogate.

## Exact artifact

The certificate has 56 rows:

    12 analytic interfaces
     7 channel ledgers
    12 finite factorial regressions
     7 endpoint rows
    10 bounded-gap/Taylor rows
     8 master ledgers

Its epistemic role is `reproduction_not_analytic_proof`.  The canonical
certificate is 14,531 bytes with SHA-256
`373d870847bb0bf134aa1eba30c5e4d2c3a01dba470af9c75ebacadd81976371`.
All 24 genuine semantic mutations and every scalar-leaf mutation are
rejected by independent field-level validation.  The false/fresh mode
does not call the certificate builder, row builders, or contract builder.

`results/result.json` is 60,053 bytes with SHA-256
`b80e29174e6616bc7f4c2de999069ba9d745d80d7c46f88ae8046bf2b5b41665`.
The recursively closed official Draft 2020-12 schema is 242,806 bytes
with SHA-256
`283182d019009b282f4e653efe1dbbc4ab48510046e65ddd77ca4e9db968cbb5`.

## Reproduction

Install the test dependencies from `requirements.txt`, then run:

    make result
    make schema
    make test
    make remote
    make pdf
    make archive

`PYTHON=...` may select a different interpreter.  `make remote` is
offline and performs zero network requests.  Explicit live checks are:

    make remote-network-jy
    make remote-network-maynard
    make remote-network

The first command calls the frozen RH-387 Johnston--Yang verifier; the
second calls the local Maynard verifier.  Neither downloaded payload is
persisted in this publication tree.

## Source closure and redistribution boundary

The immutable closure has 77 Git blobs at RH-387 release commit
`dedd8e8d2c44564e66524a646f9cf5fb9a389c77`, plus two ordered remote
logical locks, for 79 logical inputs.  The ordered Git digest is
`d7f2ee43f56631c8f3442db8fcc6fb423a801b5af7607351623cd449a92c3f73`;
the logical digest is
`bffce602d6e3b568eb96662820f08aa457ff5d0de4065f3c9eeac53d8d8dfa39`.

The Johnston--Yang author PDF/source tar and the Maynard publisher PDF
are locked but not redistributed.  Their payload hashes are recursively
excluded from the publication tree and archive.  The lock records and
offline-by-default verifiers are included.

## Claim boundary

The finite `S_K` are asymptotic truncations; no convergent factorial
series is claimed.  There is no `P_3` or cubic-coefficient precision,
complex channel, growing clock, active phasewise `c11`, `K_N`, operator,
trace, zero identification, or RH assertion.  Gates A--E are false.
