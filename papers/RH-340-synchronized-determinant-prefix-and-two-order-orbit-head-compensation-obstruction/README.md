# RH-340: Synchronized determinant-prefix equivalence and a two-order orbit--head compensation obstruction

RH-340 puts the RH-288 determinant cut on the physical first-alias clock.  If
`L=log(1/sigma)` and `k=L/(2 log(lambda))+O(1)`, use the integer cut

    u_sigma = 4k.

The existing mass-and-cap estimate can be re-applied directly at this cut:
the noisy modulus-complement tail and the deterministic target tail both
vanish on `|z|<=R`, with `R=7/5`.  This is a short-clock corollary of RH-282,
not a claim that RH-282's displayed choice `ceil(4L)` equals `4k`.

On one common Hardy normalization and this same finite prefix, write

    p_n = tau_(sigma,n) - a_n = q_(sigma,k,n) - d_(sigma,k,n),
    P_u = sum |p_n| R^n/n,
    E_u = sum |q_n| R^n/n,
    D_u = sum |d_n| R^n/n.

The exact termwise reverse-triangle bound gives

    |P_u-E_u| <= D_u.

Thus `D_u -> 0` makes direct complement-prefix closure equivalent to the
Hardy full-trace closure.  In the one-alias window this is exactly the
same-clock conjunction `D_u -> 0`, `E_off -> 0`, and
`q_(sigma,k,2k)=o(H_k)`.

The physical orbit atoms from RH-338 and RH-339 then force two independent
signed compensation equations at orders `2k` and `2k-2`.  A route that takes
separate absolute values of orbit, diffuse complement, and head terms has a
divergent lower majorant.  This is a genuine synchronization/obstruction
theorem, not a lower bound for the fully signed prefix: aggregate `P_u`,
`E_off`, and the head budget remain `NOT_TESTABLE`.

No determinant gluing is activated, and Gates A--E remain false/open.  No
Hilbert--Polya operator, Riemann-zero identification, von Mangoldt trace,
completed-zeta divisor equality, or RH conclusion is asserted.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf synchronized-determinant-prefix-and-two-order-orbit-head-compensation-obstruction.pdf
