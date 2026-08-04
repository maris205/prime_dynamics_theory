# RH-359: Logarithmic terminal-window accuracy thresholds

RH-359 inverts the RH-358 terminal-tail law at polynomial target accuracy.
It is an unconditional theorem for the deterministic graded counterloop, with
a separately marked conditional inheritance statement for an actual
modulus-complete Hardy head.

Let

    E_k(q) = P_k(q)/C_k,
    0 <= q <= k-2,

be the relative strict-upper-band mass left after retaining the top `q`
terminal coordinates.  RH-358 gives, uniformly on every logarithmic window,

    sup_(0<=q<=A log k) |x^q E_k(q)-1| -> 0.

For `a>0`, `c` real, define

    t_k(a,c)     = a log(k)/log(x) + c,
    q_k(a,c)     = floor(t_k(a,c)),
    theta_k(a,c) = {t_k(a,c)}.

Then

    k^a E_k(q_k(a,c))
      = x^(theta_k(a,c)-c) (1+o(1)).

The phase sequence has complete limit set `[0,1]`.  Consequently the
normalized truncation error has complete limit set

    [x^(-c), x^(1-c)],

and has no single leading constant.

The sharp inverse statement uses the exact monotone tail:

    Q_k(a,c) = min{q : E_k(q) <= x^(-c) k^(-a)}.

It proves

    Q_k(a,c) = a log(k)/log(x) + c + O(1)

and, more precisely, the complete limit set of

    Q_k(a,c) - [a log(k)/log(x) + c]

is exactly `[0,1]`.  Away from phase endpoints, `Q_k=ceil(t_k)` eventually;
near an integer crossing, the allowed `o(1)` multiplier remainder prevents a
stronger universal integer choice.

More generally, for any `q_k=o(k)`,

    log E_k(q_k) / log k
      = -q_k log(x)/log(k) + o(1/log k).

Thus logarithmic windows give polynomial accuracy, superlogarithmic
sublinear windows give superpolynomial accuracy, and `q_k -> infinity` is
still the exact qualitative criterion for vanishing relative error.

## Conditional actual-head scope

If the original same-clock unnormalized leaf

    D_(4k)(R) -> 0

is assumed, then RH-358's uniform actual/deterministic tail ratio transfers
the phase law, polynomial exponent, and minimal-window limit set.  RH-359 does
not prove that leaf, identify actual roots or ranks, close a determinant or a
direct/full trace budget, activate RH-241 or RH-288, or establish any of
Gates A--E.  It does not construct a Hilbert--Polya operator, identify
Riemann zeros, or prove RH.

## Reproduction

From this directory:

    make result
    make test
    make pdf
    make archive

Finite rows are exact rational or high-precision formula reproductions.  They
are not asymptotic evidence replacing the proofs, interval certificates for
the physical multiplier, or observations of an actual noisy head.
