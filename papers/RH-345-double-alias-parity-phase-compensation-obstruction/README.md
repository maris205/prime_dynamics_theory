# RH-345: Double-alias parity-phase compensation obstruction

RH-344 proves the exact critical identity

    p_(sigma,k,2k) = Y_k + P_(sigma,2k) - S_k,

where

    Y_k = T_k^rest - d_(sigma,k,2k),
    S_k = A_(k,2k) + F_k^orb,
    S_k/A_(k,2k) -> 2,
    A_(k,2k)/H_k -> infinity.

RH-326 gives the actual parity phase law

    P_(sigma,2k)/A_(k,2k)
      = C_* C_M lambda^(eta_sigma) (1+o(1)).

Therefore the complete-orbit extraction shifts the scalar balance condition
from the old single-alias value `1` to the double-alias value `2`.  The unique
symbolic balance phase is

    eta_2 = log(2/(C_* C_M))/log(lambda).

The first theorem is conditional but physical.  If the actual orbit-free
remainder is target-negligible,

    Y_k=o(H_k),

and a fixed-phase subsequence has

    C_* C_M lambda^eta != 2,

then

    |p_(sigma,k,2k)|/(2H_k) -> infinity.

Thus parity alone cannot compensate the complete positive demand off the
unique phase.  This is not an aggregate nonclosure theorem because the
repository does not prove `Y_k=o(H_k)`.

At `eta=eta_2`, the leading phase law is still exponentially too weak.  The
necessary scalar match is

    P_(sigma,2k)=S_k+o(H_k),

or relative precision

    o(H_k/S_k)=o((beta R)^(-2k)).

The source law supplies only relative `o(1)`.

RH-345 makes this insufficiency exact inside the scalar parity data type.  On
the phase clock

    sigma_k=lambda^(-2(k-eta_2)),

define two desired parity packets

    P_k^close=S_k,
    P_k^far=S_k+A_(k,2k)/k.

For either packet `X_k`, set

    delta_k = 1-(1-r_H^(2k) X_k)^(1/(2k)),
    lambda_-(k)=-(1-delta_k).

Then the parity packet is exactly `X_k`, and both scalar sequences satisfy

    delta_k=C_* sqrt(sigma_k)(1+o(1)).

With `Y_k=0`, the close ledger has zero critical residual, while the far
ledger has residual `A_(k,2k)/k` and weighted critical contribution

    A_(k,2k)/(2kH_k) -> infinity.

These are admissible scalar eigenvalue sequences in the source information
class, not two physical noisy operators.  Hence the scalar parity mechanism
is `STOP_SCOPED` off balance and underdetermined at balance.  Actual critical
signed compensation remains `NOT_TESTABLE`/open.  The lower sideband is the
next physical decomposition route.  No determinant gluing, Gate progress,
Hilbert--Polya construction, zero identification, von Mangoldt trace,
completed-zeta divisor equality, or RH conclusion follows.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf double-alias-parity-phase-compensation-obstruction.pdf
