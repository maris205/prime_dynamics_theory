# RH-356: Sharp post-first-alias mesoscopic crossover

RH-356 compares the first graded-counterloop alias with the first `L` even
coordinates immediately above it.  Let

    x   = (beta R)^2 > 1,
    y_k = (beta_k R)^2
        = x exp[-log(C_M)/k + o(1/k)].

The exact budgets are

    A_k = |s_(k,2k)|R^(2k)/(2k)
        = (1-1/k)y_k^k,

    B_k(L) = sum_(j=1)^L |s_(k,2k+2j)|R^(2k+2j)/(2k+2j)
           = sum_(j=1)^L y_k^(k+j)/(k+j),

for `1 <= L <= k-1`.  Hence

    B_k(L)/A_k = [k/(k-1)] sum_(j=1)^L y_k^j/(k+j).

## Uniform mesoscopic theorem

For every integer envelope `ell_k=o(k)`, uniformly over
`1<=L<=ell_k`,

    B_k(L)/A_k
      = x(x^L-1)/(k(x-1)) (1+o(1)).

The subtraction is part of the leading term at bounded depth.  For every
fixed integer `L>=1`,

    k B_k(L)/A_k -> x(x^L-1)/(x-1).

At finite radius the geometric factor is `1-y_k^(-L)`.  Only when both

    L -> infinity,   L=o(k)

may one delete `1-y_k^(-L)` (equivalently `1-x^(-L)` in the limiting
formula) and write

    B_k(L)/A_k
      = [x/(x-1)] x^(L-log_x(k)) (1+o(1)).

Thus `C_M` cancels at mesoscopic depth but no linear-depth extension is
claimed.

## Crossover and integer phase

With `delta_k=L-log_x(k)`, the ratio tends to zero, a finite nonzero limit,
or infinity according as `delta_k` tends to `-infinity`, `c`, or
`+infinity`.  At a finite offset,

    B_k(L)/A_k -> x^(c+1)/(x-1).

The continuous balance offset is

    log_x((x-1)/x).

For integer depth

    L_k(c) = floor(log_x(k)+c),
    theta_k(c) = {log_x(k)+c},

the phase must be retained:

    B_k(L_k(c))/A_k
      = x^(c+1-theta_k(c))/(x-1) (1+o(1)).

The phase limit set is `[0,1]`; consequently

    liminf = x^c/(x-1),
    limsup = x^(c+1)/(x-1),

and there is no single full-sequence limit.

On the physical noise clock, the crossover is only

    n-2k = 2L
         = [2/log(x)] log(log(1/sigma)) + O(1)

orders above the first alias.

## Conditional actual-head statement

The actual modulus-complete Hardy head inherits these budget ratios only if
the original unnormalized same-clock leaf

    D_(4k)(R) -> 0

is assumed.  Under that open hypothesis, the actual alias and post-alias
budgets are relatively asymptotic to the counterloop budgets, uniformly in
`1<=L<=k-1`, and the odd actual post-alias budget tends to zero.  RH-356 does
not prove this hypothesis or any root/rank identification.

RH-354's direct coefficient `p=tau-a=q-d` is not `q` or the head defect.
No direct/full-trace closure, RH-288 activation, Gate A--E, Hilbert--Polya
operator, Riemann-zero identification, von Mangoldt trace, completed-zeta
divisor equality, or proof of RH is claimed.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf sharp-post-first-alias-mesoscopic-crossover.pdf
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
