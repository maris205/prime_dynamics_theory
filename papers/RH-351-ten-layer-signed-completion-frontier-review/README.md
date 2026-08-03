# RH-351: Ten-layer signed-completion frontier review

RH-351 audits RH-342--RH-350 and closes the batch with a new
growing-depth information-class theorem.  On the physical clock, let

    m_(k,j)=k-j,  2<=j<=J_k,
    J_k->infinity,  J_k=o(k),

and retain the exact RH-348/RH-350 direct coefficient identity

    p_(k,j)=Y_(k,j)+P_(k,j)-S_(k,j).

RH-350 proves uniform deterministic/scalar laws for `S` and `P`, together
with the exact weighted minimax functional

    F_N(a)=sum_(r=0)^N x^(-r)|a lambda^(-r)-1|.

The new theorem concerns only the signed coefficient-ledger information
class.  For any prescribed residual array `r_(k,j)`, the formal completion

    Y_(k,j)=S_(k,j)-P_(k,j)+r_(k,j)

gives `p_(k,j)=r_(k,j)` exactly.  In particular, the same proved `P/S`
arrays admit two opposite abstract completions:

    close: Y=S-P,  p=0,
    far:   Y=0,    p=P-S.

Writing

    L_k(Y)=x^(-(k-2)) sum_(j=2)^(J_k) |p_(k,j)|/(2H_(m_(k,j))),
    Yagg_k(Y)=x^(-(k-2)) sum_(j=2)^(J_k) |Y_(k,j)|/(2H_(m_(k,j))),

one has the exact budget exchange

    Yagg_k(close)=L_k(far),
    Yagg_k(far)=L_k(close)=0.

The RH-350 uniform laws then give algebraically

    L_k(far)=F_(J_k-2)(a_k)/C_M+o(1),

and

    liminf L_k(far)
      >= [1/(x-1)-1/(x lambda-1)]/C_M > 0.

Thus the far ledger has an exponentially divergent unnormalized selected
lower-even subprefix, while the close ledger is identically zero.  The
close ledger correspondingly has a non-small `Y` budget, so it does not
satisfy RH-350's unproved aggregate small-`Y` hypothesis.  This exact
exchange identifies that missing physical theorem as decisive.

These completions are abstract signed coefficient ledgers.  They are not
two noisy operators, Markov kernels, raw trace partitions, or determinant
realizations.  The actual

    Y_(k,j)=T_(k,m_(k,j))^rest-d_(sigma,k,2m_(k,j))

is not estimated in the repository.  The selected lower-even window is not
the full strict prefix: head transport, the critical and first-lower orders,
odd orders, upper-alias orders, and full `E_off` remain open.

RH-241's moving noisy all-order envelope and coefficient bridge also remain
open.  RH-263, RH-267, and RH-268 close only the deterministic numerator
anchor, deterministic envelope, and sharp radius.  RH-288 and Gates A--E
are not activated.  No Hilbert--Polya operator, Riemann-zero
identification, von Mangoldt trace, completed-zeta divisor equality, or RH
conclusion is asserted.

The individual archive covers ten papers.  RH-342--RH-350 contain 15
publication files each and RH-351 contains 19, for 154 batch publication
files and 176 controlled tree files after archive metadata.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf ten-layer-signed-completion-frontier-review.pdf
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_batch_archive.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_batch_archive.py
