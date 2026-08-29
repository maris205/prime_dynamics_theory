# TPC-300 derivation package

Let M be positive definite, V be the finite physical image map, b be the
target, and R be the allowed Euclidean residual radius.  The primal frontier
is

    B_R(b)=min{c^T M c: ||Vc-b||_2 <= R}.

For a positive ridge parameter rho, let

    (V^T V+rho M)c_rho=V^T b.

The Lagrangian multiplier is mu=1/rho.  Completing the square in

    c^T M c + mu(||Vc-b||_2^2-R^2)

gives the dual value

    D_rho=(||b||_2^2-R^2-b^T V c_rho)/rho.

For every rho>0, weak duality gives D_rho<=B_R(b).  If the least-squares
distance is strictly below R<||b||, the residual along the ridge path is
continuous and strictly increasing in rho; the unique rho_* with
||Vc_rho-b||_2=R attains equality.

For the TPC profile map, V=A^T U and M=U^T U.  All entries are rational on
the finite fixture.  Choosing rational rho therefore makes c_rho and D_rho
rational.  The certificate stores hashes of the exact fraction and exact
coefficient vector, while decimal intervals are only presentation enclosures.
