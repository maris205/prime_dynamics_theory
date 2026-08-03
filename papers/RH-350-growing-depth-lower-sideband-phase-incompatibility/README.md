# RH-350: Growing-depth lower-sideband phase incompatibility

RH-350 extends the fixed `j=2,3` phase law of RH-349 to a triangular lower-even window

    m_(k,j)=k-j,  2<=j<=J_k,
    J_k->infinity,  J_k=o(k).

For every selected order, RH-348 gives the exact direct coefficient

    p_(k,j)=Y_(k,j)+P_(k,j)-S_(k,j).

Put

    H_m=m R^(-2m),
    x=(beta R)^2>1,
    a_k=C_* C_M lambda^(eta_k-2).

The new unconditional deterministic/scalar theorem is the pair of uniform laws

    sup_j |C_M S_(k,j)/(2 H_(m_(k,j)) x^(m_(k,j)))-1| -> 0,

    sup_j |C_M P_(k,j)/(2 H_(m_(k,j)) x^(m_(k,j)))
           -a_k lambda^(2-j)| -> 0.

For fixed `J>=3`, the exact relative minimax is

    inf_(a>0) max_(2<=j<=J) |a lambda^(2-j)-1|
      =(lambda^(J-2)-1)/(lambda^(J-2)+1).

For the physical weighted objective

    F_N(a)=sum_(r=0)^N x^(-r)|a lambda^(-r)-1|,

the exact identity

    x lambda=(R/r_H)^2=(28/17)^2>2

forces the unique weighted median `a=1`.  Hence

    inf_(a>0) F_N(a)
      =(1-x^(-N))/(x-1)
       -(1-(x lambda)^(-N))/(x lambda-1),

and these minima increase to

    A_infinity=1/(x-1)-1/(x lambda-1)>0.

The physical conclusion is explicitly conditional.  Define

    Yagg_k=x^(-(k-2)) sum_(j=2)^(J_k) |Y_(k,j)|/(2H_(m_(k,j))).

If the actual triangular-array hypothesis `Yagg_k->0` holds, then

    x^(-(k-2)) sum_(j=2)^(J_k) W_(k,j)
      =F_(J_k-2)(a_k)/C_M+o(1),

so the liminf is at least `A_infinity/C_M>0`.  The selected lower-even direct subprefix then diverges exponentially.

The repository does not prove the actual aggregate hypothesis, or even the stronger coefficientwise sufficient condition

    max_j |Y_(k,j)|/H_(m_(k,j)) -> 0.

Finite rows use `a_k=1` and `Y_(k,j)=0` only as formula-reproduction fixtures.  They are not observations of a noisy operator.  No unconditional prefix or `E_off` nonclosure, odd-order control, upper-alias control, RH-288 activation, Gate progress, Hilbert--Polya construction, Riemann-zero identification, or Riemann-hypothesis conclusion is claimed.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf growing-depth-lower-sideband-phase-incompatibility.pdf
