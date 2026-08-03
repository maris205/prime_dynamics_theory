# RH-349: Two lower-sideband phase incompatibility

RH-349 isolates the first two orders of the punctured lower-even ladder on
the same physical noise clock.  For fixed `j in {2,3}`, set

    m_j=k-j,  n_j=2m_j,
    H_(m_j)=m_j R^(-2m_j),
    x=(beta R)^2>1.

RH-348 gives the exact direct coefficient

    p_j=Y_j+P_j-S_j,

where

    Y_j=T_(k,m_j)^rest-d_(sigma,k,2m_j),
    S_j=F_(m_j)^orb+A_(k,2m_j).

The multiplier and radial laws imply, for each fixed `j`,

    S_j=(2m_j/C_M) beta^(2m_j)(1+o(1)),
    S_j/(2H_(m_j))=x^(m_j)/C_M(1+o(1)).

Along a physical subsequence with `eta_sigma -> eta`, the exact parity
packet and its square-root law give

    P_j/S_j -> gamma_j(eta)=C_* C_M lambda^(eta-j).

Thus `gamma_3=gamma_2/lambda`.  A single scalar phase cannot balance both
coordinates.

The physical theorem is explicitly conditional.  Assume simultaneously on
the actual direct coefficients that

    Y_2=o(H_(m_2)),  Y_3=o(H_(m_3)).

Writing `W_j=|p_j|/(2H_(m_j))` and
`a=gamma_2(eta)>0`, one obtains

    W_j/x^(m_j) -> |gamma_j(eta)-1|/C_M,

and therefore

    (W_2+W_3)/x^(k-3)
      -> [x|a-1|+|a/lambda-1|]/C_M > 0.

Consequently this two-order direct subprefix diverges exponentially under
both named hypotheses.

The convergence assumption on `eta_sigma` determines the exact limiting
coefficient above.  If `eta_sigma` is only bounded, the same two actual
remainder hypotheses still give the uniform conditional lower statement

    liminf (W_2+W_3)/x^(k-3)
      >= (1-1/lambda)/C_M.

Two exact scalar minimax identities quantify the incompatibility:

    inf_(a>0) max(|a-1|,|a/lambda-1|)
      =(lambda-1)/(lambda+1),

attained at `a=2lambda/(lambda+1)`, whereas the sharper physical-prefix
weighting gives

    inf_(a>0) [x|a-1|+|a/lambda-1|]
      =1-1/lambda,

attained at `a=1`.  The second optimizer differs because the `j=2`
coordinate carries the extra factor `x>1` after common normalization.

Neither actual hypothesis is proved.  The finite artifact sets
`Y_2=Y_3=0` only as a formula-reproduction fixture, chooses the weighted
optimizer `a=1`, and checks that

    C_M(W_2+W_3)/x^(k-3) -> 1-1/lambda.

Those rows are not observations of a noisy operator and do not verify the
actual remainder hypotheses.  No unconditional physical nonclosure,
`E_off` verdict, growing-depth uniformity, odd-order control, upper-alias
control, RH-288 activation, Gate progress, Hilbert--Polya construction,
Riemann-zero identification, or Riemann-hypothesis conclusion is claimed.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf two-lower-sideband-phase-incompatibility.pdf
