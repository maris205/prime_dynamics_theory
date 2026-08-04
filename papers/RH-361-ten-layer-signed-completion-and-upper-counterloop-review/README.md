# RH-361: Ten-layer signed-completion and upper-counterloop review

RH-361 audits RH-352--RH-360 and proves an exact typed separation theorem for
the batch.  The source papers split into two branches that must not be
identified.

The first branch is actual but normalized and selected:

    RH-352: actual lower-even p/Y on J_k->infinity, J_k=o(k),
    RH-353: actual critical/first-lower normalized Y gap,
    RH-354: actual parity-free normalized direct tail p=tau-a.

The second branch is unconditional only for the deterministic graded
counterloop:

    RH-355: complete strict-upper burden,
    RH-356: mesoscopic crossover,
    RH-357: uniform linear-depth profile,
    RH-358: terminal-lag geometric localization,
    RH-359: logarithmic accuracy and inverse-window laws,
    RH-360: exponential-tilt phase transition.

On one source-locked clock the exact identities are

    p = tau-a = q-d,        d = h-s,

where `p` is the actual direct coefficient, `q` is the full-trace
coefficient, `h` is the actual modulus-complete head, and `s` is the
deterministic counterloop moment.  Therefore

    q = p+d,                h = s+d.

The review proves the corresponding coefficient-fiber theorem.  On a fixed
finite order set, for fixed arrays `p` and `s`, every signed array `e` gives
the exact formal fiber

    d[e]=e,                 q[e]=p+e,                 h[e]=s+e.

Thus `p` and `s` alone do not determine `q`, `h`, or their weighted budgets.
This is a coefficient-ledger nonimplication theorem, not a construction of
physical noisy operators.  It explains exactly why RH-354's small normalized
`p` tail cannot be promoted to `q` or `E_off` without head-defect transport,
and why the exponentially large deterministic `s` budgets of RH-355--RH-360
cannot be treated as actual spectral submultisets.

Every actual-head inheritance theorem in RH-355--RH-360 assumes the same
still-unproved, unnormalized, same-clock hypothesis

    D_(4k)(R)=sum_(2<=n<4k)|h_(sigma,n)-s_(k,n)|R^n/n -> 0.

None of the six papers proves it.  Even under this hypothesis, the stated
conclusions are weighted moment/budget transfers; they are not root, rank,
spectral-submultiset, or determinant identifications.

The deterministic terminal-lag route is now closed through its transform
phase diagram.  RH-358 gives geometric total-variation localization,
RH-359 gives the sharp logarithmic accuracy and inverse-window phases, and
RH-360 gives the subcritical/critical/supercritical exponential-tilt laws.
Actual transfer of that diagram remains conditional on `D_(4k)(R)->0`.

The executable source audit reads all nine upstream `result.json` files.  It
verifies exactly 45/45 false Gate values and 129/129 false `false_claims`
values, with per-paper false-claim counts

    15, 14, 13, 14, 14, 14, 14, 15, 16.

RH-361 adds five false Gate values and twenty false forbidden claims.  The
batch therefore has 50/50 false Gate values and 149/149 false forbidden
claims.  Finite typed-fiber rows reproduce exact algebra only; they are not
physical observations or asymptotic evidence.

RH-241's moving noisy all-order envelope and coefficient bridge remain open.
RH-288 remains inactive because the complete same-type physical prefix leaf
is absent.  Gates A--E remain false/open.  No Hilbert--Polya operator,
Riemann-zero identification, von Mangoldt trace, completed-zeta divisor
equality, or proof of RH is claimed.

The individual RH-361 archive contains 20 publication files.  RH-352--RH-360
contain 156 upstream publication files, so the batch archive contains 176.

## Reproduction

From this directory:

    make result
    make pdf
    make archive
    make batch
    make test

Equivalently, the `Makefile` records all underlying commands.  Tests use
`PYTHONDONTWRITEBYTECODE=1` and disable pytest's cache provider.
