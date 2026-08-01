# RH-341: Ten-layer actual first-alias replacement frontier review

RH-341 audits RH-332--RH-340 on one physical natural clock, one Hardy
normalization, and the common cut `u=4k`.  The batch contains rigorous local
theorems, exact typed identities, and scoped negative results, but no
aggregate physical replacement theorem.

The deterministic ancestry is now clean.  RH-241 left both a uniform
all-order target envelope and coefficient identification open.  RH-263 later
proved the all-order deterministic numerator anchor, RH-267 proved

    |a_n| < 48 q_*^n  for every n>=2,

and RH-268 proved the sharp deterministic root rate.  Those results close the
deterministic target side only.  The moving noisy all-order coefficient bridge
and Gate A remain open.

On the corrected RH-334 data type, RH-339 makes the all-order identity

    q_n = B_n + S_n + R_n + P_n - A_(k,n)

explicit.  RH-334 and RH-340 give

    p_n = tau_n-a_n = q_n-d_n,
    |P_u-E_u| <= D_u.

At `u=4k`, the noisy and deterministic tails vanish.  Therefore the existing
RH-288 route still requires the same-clock conjunction

    D_(4k) -> 0,
    E_off,(4k) -> 0,
    q_(sigma,k,2k) = o(H_k).

The physical orbit atoms of RH-338 and RH-339 impose two necessary signed
laws:

    C_k^0-d_(sigma,k,2k) = D_k^orb + o(H_k),
    C_k^--d_(sigma,k,2k-2) = D_(k-1)^orb + o(H_(k-1)).

Taking separate absolute values of the orbit, diffuse, and head pieces has a
divergent two-atom submajorant and is `STOP_SCOPED`.

The new review theorem is an information-class result.  With only the exact
identities and asymptotic atom sizes currently proved, the unspecified signed
combined complements admit an abstract cancelling completion and an abstract
noncancelling completion.  The first sets each combined complement equal to
its orbit atom; the second sets both to zero.  Thus the available signed
information determines neither aggregate prefix closure nor nonclosure.
These are algebraic ledger completions, not two physical noisy operators, and
no physical realizability is asserted.

The route coordinate is

    synchronized_actual_first_alias_signed_completion_open.

Aggregate physical prefix behavior, `E_off`, the head/counterloop budget,
determinant gluing, and every Gate A--E condition remain `NOT_TESTABLE` or
open.  No Hilbert--Polya operator, Riemann-zero identification, von Mangoldt
trace, completed-zeta divisor equality, or RH conclusion is obtained.

The individual archive audit covers ten papers.  RH-332--RH-340 contain 15
publication files each and RH-341 contains 19, for 154 batch publication
files and 176 controlled tree files after archive metadata.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf ten-layer-actual-first-alias-replacement-frontier-review.pdf
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_batch_archive.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_batch_archive.py
