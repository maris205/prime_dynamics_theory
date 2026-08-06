# RH-365: Prime-return bouquet height, radius, and prime-order anchors

RH-365 is a source-locked theorem paper for the integral Hénon automorphism

    H(x,y) = (1-6x^2-y,x)

at the reversing-axis seed P0=(0,0).  It upgrades the RH-362 marked-cycle
bouquet from a formal Artin--Mazur series to a rigorously analytic germ.

Write H^n(P0)=(x_n,x_(n-1)), with x_(-1)=x_0=0, and let

    a_n = gcd(|x_n|,|x_(n-1)|).

The paper proves the exact reversibility midpoint identities

    a_(2k)   = |x_k-x_(k-1)|,
    a_(2k+1) = |x_(k+1)-x_(k-1)|.

For b_n=-x_n, n>=2, one has

    5 b_n^2 <= b_(n+1) <= 6 b_n^2,

and therefore explicit double-exponential two-sided bounds for b_n and
a_n.  In particular

    log a_n = Theta(2^(n/2)).

If r_p is the return period of P0 modulo p and

    T_n = sum_(p:r_p|n) r_p,

then the height theorem gives the all-order fixed-point envelope

    T_n <= log_2(30) n 2^(ceil(n/2)-2).

Consequently the unweighted marked-cycle product

    Z_0(z) = product_p (1-z^(r_p))^(-1)

converges normally and is holomorphic and zero-free on the strict disk

    |z| < 2^(-1/2).

This is a certified lower bound for the origin Taylor radius, not an exact
radius or natural-boundary theorem.

For every odd prime order ell,

    {p:p divides a_ell} = {p:r_p=ell}.

Thus every distinct prime divisor of a_ell is primitive,
c_ell=omega(a_ell)>=1, T_ell=ell c_ell, and

    [z^ell] log Z_0(z) = c_ell.

The anchor is the primitive Euler exponent and logarithmic coefficient.  It
is not the raw coefficient of Z_0: the finite ledger already gives
[z^7]Z_0=3 while c_7=1, and [z^11]Z_0=13 while c_11=4.

## Scoped operator negative

On the Hilbert direct sum of the marked cycle spaces, the naive operator

    B_z = direct_sum_p z U_p

is noncompact and lies in no finite Schatten class whenever z is nonzero.
The analytic Euler product is therefore not the ordinary Fredholm determinant
of this naive direct sum.  For |z|<1 the operator I-B_z is nevertheless
invertible; noncompactness must not be restated as non-Fredholmness.

## Route boundary

Route A is GO.  The exact midpoint compression, height scale, all-order trace
envelope, strict zero-free disk, prime-order primitive anchors, and scoped
operator negative form a standalone theorem package.

Route B is STOP_SCOPED.  The bouquet uses one marked cycle from each of
distinct finite-field maps.  It is not a full H_p zeta, Hasse--Weil factor,
canonical global Hénon operator, or signed von-Mangoldt trace model.

Gates A--E remain false/open.  No Hilbert--Pólya operator, self-adjoint
generator, Riemann-zero identification, completed-zeta divisor equality, or
proof of RH is claimed.

## Reproduction

Run:

    make result
    make test
    make pdf
    make archive

The finite rows reproduce exact midpoint values, height inequalities, factor
and return-rank ledgers through order twelve, and the raw-coefficient
firewall.  They are not evidence for a composite-order Zsigmondy theorem or
for an exact analytic radius.
