# RH-387: All-Order Prime-Tail Integral Resummation

RH-387 replaces the entire strict prime-square Euler tail in the RH-383
endpoint map by two integral kernels, uniformly across the seven endpoint
channels. It performs the source comparison before the infinite
logarithmic resummation and then uses one endpoint Lipschitz estimate.

## Main theorem

Let x=p_y, L=log x>=512,

    V(L) = L^(3/5) (log L)^(-1/5),
    epsilon_x = 0.027 L^1.801 exp(-0.1853 V(L)),

and, for c=1,...,7,

    PhiP_c = sum_(r>=1) c^r P_r/r,
    PhiJ_c = integral_x^infinity -log(1-c/(t^2-1))/log(t) dt,
    PhiI_c = integral_x^infinity -log(1-c/t^2)/log(t) dt.

For the exact RH-383 endpoint map F, define

    GapP = B_infinity-G(q_y) = F(PhiP)/pi^2,
    GapJ = F(PhiJ)/pi^2,
    GapI = F(PhiI)/pi^2.

The certified bounds are

    max_c |PhiP_c-PhiJ_c| <= 28 epsilon_x/(xL),
    0 <= max_c(PhiJ_c-PhiI_c) <= 14/(3x^3L),
    sup_[0,1/2]^7 ||grad F||_1 <= 126,

    pi^2 |GapP-GapJ| <= 3528 epsilon_x/(xL),
    pi^2 |GapJ-GapI| <= 588/(x^3L),
    pi^2 |GapP-GapI| <= 3528 epsilon_x/(xL)+588/(x^3L).

The proof keeps the strict Stieltjes boundary and sums its absolute error
over every r by Tonelli. It is not a termwise application of the finite
partition theorem in RH-386.

## Reproduction artifact

The canonical certificate contains exactly 42 rows:

| group | rows |
|---|---:|
| analytic/source interfaces | 12 |
| channel bounds | 7 |
| endpoint coefficients | 7 |
| degree-four formal resummation fixtures | 14 |
| gradient/master ledgers | 2 |

Its canonical JSON has 10,785 bytes and SHA-256
3c89e51662bbc2f1c7712f4205ff8cde88e9eb80636e2779d06154e914459b4b.
All 24 named mathematical mutations are rejected by independently
recomputed field-level verification. Strict JSON, exact Python types,
closed official Draft 2020-12 schema validation, scalar-leaf mutations,
and optimized -OO replay are tested.

The artifact role is exactly reproduction_not_analytic_proof. The finite
rows reproduce algebraic interfaces; they do not prove the
Johnston--Yang estimate, Stieltjes integration, Tonelli's theorem, the
infinite-order exchange, or the endpoint mean-value argument.

## Source closure

The immutable Git closure has 68 rows at RH-386 release
9778e3515d45816665d672a641947b93906abf54:

| group | rows | digest |
|---|---:|---|
| RH-386 inherited closure | 59 | 62f05b53900a38353dbe3ff97629e2eedaa668707a33a0e355c7b398ee810f5b |
| RH-386 standard release files | 8 | ad8708e4d229d85d6d1f82163e9a5f0db1f8e7dd5d020f24a81cf97bca2bf9fb |
| RH-386 external-lock blob | 1 | b66c168d2dde73ec9297fc4ad8ff9905de58e6c5b42696bc72161e6ef09ec78c |

The ordered Git digest is
19def5cbed919da8e9652012cf011f3b5728efd4b24a9eef0911bb7346467d27.
One canonical remote logical lock gives 69 logical sources and digest
5016397fe59962954514b3b42d68e9de6dfeff0dae949791b01c6a516f5c61fe.

The Johnston--Yang author PDF and source tar are not vendored. The local
lock is inherited exactly from RH-386, records
redistributable_in_release=false, and has canonical-object SHA-256
d53b93212b7c5b5b6b3f7e890099c48ce8e35f2bff9bdd49f9c330a9b5039786.
The default verifier performs zero network requests; make remote-network
is an explicit opt-in replay.

## Reproduce

    make result
    make schema
    make test
    make pdf
    make archive

jsonschema>=4.18 is required for official Draft 2020-12 validation. The
build itself remains offline; network access is never implicit.

## Claim firewall

Because epsilon_x x^2 tends to infinity, the source error is larger than
the P_2 scale. RH-387 claims no second-order or cubic coefficient
precision. It also supplies no complex-c theorem, active phasewise c11
cancellation, growing clock, prefix/prime-index joint limit, adaptive
capacity, operator or trace formula, zeta-zero identification, or proof
of RH. Gates A--E are all false.
